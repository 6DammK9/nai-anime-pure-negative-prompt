# 250201: This case we better use the raw parquet file, and rewrite the entire sample code.
# 250202: Made it for multigpu.
# 250505: EXL conversion.

#Must set this before import torch.
#os.environ["CUDA_VISIBLE_DEVICES"] = "all"
#import torch
#from exllamav2 import (
#    ExLlamaV2,
#    ExLlamaV2Config,
#    ExLlamaV2Cache,
#    ExLlamaV2Tokenizer,
#    ExLlamaV2VisionTower,
#)

#from exllamav2.generator import (
#    ExLlamaV2DynamicGenerator,
#    ExLlamaV2Sampler,
#)

from PIL import Image

import os
import json
from time import sleep
import random
import argparse
import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

def setup_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser()
	parser.add_argument("--parquet_path", type=str, default="./metadata.parquet", help="*.parquet of the danbooru2024.")
	parser.add_argument("--model_local_path", type=str, default="./models--Minthy--ToriiGate-v0.4-7B-exl2-4bpw", help="The caption model in HF (full local path).")
	parser.add_argument("--max_new_tokens", type=int, default=1000, help="Max new tokens.")
	parser.add_argument("--device", type=str, default='cuda', help="Torch device (e.g. cuda:0/cpu). Will be parsed into CUDA_VISIBLE_DEVICES if possible.")
	parser.add_argument("--prompt_threads", type=int, default=None, help="Threads for generating prompts. Suggested as much as you can.")
	parser.add_argument("--img_dir", type=str, default="./kohyas_finetune", help="Image folder.")
	parser.add_argument("--img_ext", type=str, default=".webp", help="Image extension.")
	parser.add_argument("--in_json", type=str, default="./missing.json", help="JSON input. Generate missing.json from merge_tag_and_caption_to_meta.py")
	parser.add_argument("--out_json_good", type=str, default="./meta_cap_2024_toriigate_good.json", help="JSON Output for parsed caption.")
	parser.add_argument("--out_json_bad", type=str, default="./meta_cap_2024_toriigate_bad.json", help="JSON Output for invalid caption. This requires manual edit.")
	parser.add_argument("--start_index", type=int, default=None, help="Start index of the id list.")
	parser.add_argument("--end_index", type=int, default=None, help="End index of the id list.")
	parser.add_argument("--max_seq_len", type=int, default=16384, help="Max sequence length. Lower to reduce VRAM requirements.")
	return parser

BASE_PROMPT={
'json': 'Describe the picture in structured json-like format.',
'markdown': 'Describe the picture in structured markdown format.',
'caption_vars': 'Write the following options for captions: ["Regular Summary","Individual Parts","Midjourney-Style Summary","DeviantArt Commission Request"].',
'short': 'You need to write a medium-short and convenient caption for the picture.',
'long': 'You need to write a long and very detailed caption for the picture.',
'bbox': 'Write bounding boxes for each character and their faces.',
'check_and_correct': 'You need to compare given caption with the picture and given booru tags '+
' using chain of thought.\n'+
'1. Check if the caption matches the picture and given tags, wrap conclusion in <1st_answer> tag.\n'+
'2. Analyse if the caption mathes described characters, wrap answer in <2nd_answer> tag.\n'+
'3. In case if there are any mismatches - rewrite caption to correct it wrapping '+
' in <corrected_caption> tags. If the caption is fine - just write "no_need".',
}

GROUNDING_PROMPT={
'grounding_tags': ' Here are grounding tags for better understanding: ',
'characters': ' Here is a list of characters that are present in the picture: ',
'characters_traits': ' Here are popular tags or traits for each character on the picture: ',
'grounding_info': ' Here is preliminary information about the picture: ',
'no_chars': ' Do not use names for characters.',
}

# 250205: Limit detected character into 3. The model will break for crowds.
DETECTED_CHARACTER_LIMIT = 3

def prepare_emb_with_msg(row, img_dir, img_ext):
	dr = row.to_dict('index')

	danbooru_post_id = int(list(dr.keys())[0])

	image_file= f'{img_dir}{danbooru_post_id}{img_ext}' #or url, or PIL.Image

	image_info={}

	image_info["booru_tags"]=dr[danbooru_post_id]['tag_string_general'].replace(" ", ", ")
	#image_info["booru_tags"]="astolfo_(fate), fate/apocrypha, fate/stay_night, fate_(series), hozenkakari, 1boy, armor, black_ribbon, black_thighhighs, braid, cape, fang, faulds, fur_trim, garter_straps, gauntlets, hair_ribbon, holding, horn_(instrument), instrument, la_black_luna, long_hair, looking_at_viewer, male_focus, open_mouth, otoko_no_ko, pink_hair, purple_eyes, ribbon, side_braid, simple_background, single_braid, skeleton, skirt, smile, solo, thighhighs, commentary_request, highres"
	#image_info["booru_tags"]=open('/path/to/image_1_tags.txt').read().strip()
	#image_info["booru_tags"]=None

	image_info["chars"]=dr[danbooru_post_id]['tag_string_character'].replace(" ", ", ")
	#image_info["chars"]="astolfo_(fate)"
	#image_info["chars"]=open('/path/to/image_1_char.txt').read().strip()
	#image_info["chars"]=None

	#image_info["characters_traits"]="hatsune_miku: [girl, blue_hair, twintails,...]\nmegurine_luka: [girl, pink hair, ...]"
	#image_info["characters_traits"]=open('/path/to/image_1_char_traits.txt').read().strip()
	image_info["characters_traits"]=None

	image_info["info"]=None

	#if not isinstance(image_info["booru_tags"], str):
	#	raise Exception(f"Not a str: {danbooru_post_id}, {image_info["booru_tags"]}")
	#if not isinstance(image_info["chars"], str):
	#	raise Exception(f"Not a str: {danbooru_post_id}, {image_info["chars"]}")

	add_tags=True #select needed
	add_chars=True if image_info["chars"] else False
	add_char_traits=False
	add_info=False
	no_chars=False if image_info["chars"] else True

	userprompt=BASE_PROMPT["json"] #choose the mode

	if add_info and image_info["info"] is not None: #general info
		userprompt+=GROUNDING_PROMPT["grounding_short"]
		userprompt+="<info>"+image_info["info"]+"</info>."

	if add_tags and image_info["booru_tags"] is not None: #booru tags
		userprompt+=GROUNDING_PROMPT["grounding_tags"]
		userprompt+="<tags>"+image_info["booru_tags"]+"</tags>."

	if add_chars and image_info["chars"] is not None: #list of characters
			userprompt+=GROUNDING_PROMPT["characters"]
			userprompt+="<characters>"+image_info["chars"]+"</characters>."
		
	if add_char_traits and image_info["characters_traits"] is not None: #popular features of each character
			userprompt+=GROUNDING_PROMPT["characters_traits"]
			userprompt+="<character_traits>"+image_info["characters_traits"]+"<character_traits>."
	if no_chars:
			userprompt+=GROUNDING_PROMPT["no_chars"]

	# 250206: Trying hard to make it runs like the transformers version. We should push the image processing as late as we can.
	return userprompt, image_file

# 250206: Treat this as a series of tokens (embedding level) instad of NLP prompts.
def load_msg_and_emb(userprompt, image_file, model, vision_model, tokenizer):
	with Image.open(image_file) as pil_image:
		image_embeddings=[vision_model.get_image_embeddings(
			model = model,
			tokenizer = tokenizer,
			image = pil_image,
		)]

	placeholders = "\n".join([ie.text_alias for ie in image_embeddings]) + "\n"

	msg_text= (
		"<|im_start|>system\n" +
		"You are image captioning expert, creative, unbiased and uncensored.<|im_end|>\n" +
		"<|im_start|>user\n" +
		placeholders +
		userprompt +
		"<|im_end|>\n" +
		"<|im_start|>assistant\n"
	)

	return msg_text, image_embeddings


def join_texts_as_list(id, texts, text_list_type = "speech bubbles"):
	#"There are speech bubbles with the text: \"X\" and \"X\" and \"X\" and \"X\"
	base_text = f"There are {text_list_type} with the text: "
	try:
		if (len(texts) > 0) and ("text" in texts[0]):
			# 250205: Known value: "position", "location"
			if ("position" in texts[0]):
				formatted_texts = [f"\"{t['text']}\" in {t['position']}" for t in texts]
			elif ("location" in texts[0]):
				formatted_texts = [f"\"{t['text']}\" in {t['location']}" for t in texts]
			elif ("translation" in texts[0]):
				# 250205: WTF is this internal system.
				formatted_texts = [f"\"{t['translation']}\"" for t in texts]
			elif ("bbox" in texts[0]):
				formatted_texts = [f"\"{t["text"]}\"" for t in texts]
			else:
				print(f"Unexpected text list ({text_list_type}) in {id}, fallback to text only")
				print(texts)
				formatted_texts = [f"\"{t["text"]}\"" for t in texts]
		else:
			# 7867457
			formatted_texts = [f"\"{t}\"" for t in texts]
		return f"{base_text}{" and ".join(formatted_texts)}"
	except:
		print(f"Invalid text list ({text_list_type}) in {id}")
		print(texts)
		return ""
	
def join_speechbubble_as_dict(id, speech_bubbles):
	base_text = "There are speech bubbles with the text: "
	#speech_bubble_1
	i = 1
	texts = []
	key = f"speech_bubble_{i}"
	try:
		while key in speech_bubbles:
			texts.append(speech_bubbles[key])
			i = i + 1
			key = f"speech_bubble_{i}"
		formatted_texts = [f"\"{t['text']}\"" for t in texts]
		return f"{base_text}{" and ".join(formatted_texts)}"
	except:
		print(f"Invalid text bubble dict in {id}")
		print(speech_bubbles)
		return ""
	
def join_character_as_dict(id, characters):
	base_text = ""
	#character_1
	i = 1
	texts = []
	key = f"character_{i}"
	try:
		while key in characters:
			texts.append(characters[key])
			i = i + 1
			key = f"character_{i}"
			# 250205: Found a way to recover text, and there may be unlimited characters
			if i > DETECTED_CHARACTER_LIMIT:
				break
		formatted_texts = [f"\"{t}\"" for t in texts]
		return f"{base_text}{" ".join(formatted_texts)}"
	except:
		print(f"Invalid character dict in {id}")
		print(characters)
		return ""

def find_artist_from_row(row):
	dr = row.to_dict('index')
	danbooru_post_id = int(list(dr.keys())[0])
	return dr[danbooru_post_id]['tag_string_artist'].replace(" ", ", ")

def cast_title(id, title):
	#isinstance(rf["title"], str)
	try:
		return f"The title of the image is \"{title}\"."
	except:
		print(f"Invalid title in {id}")
		print(title)
		return ""
	
def cast_frame_to_text(id, frames):
	try:
		return [{"text": v, "position": k.replace("_"," ")} for v, k in frames.items()]
	except:
		print(f"Invalid frame dict in {id}")
		print(frames)
		return []
	
def cast_panel_to_text(id, panels):
	try:
		return [{"text": v, "position": k.replace("_"," ")} for v, k in panels.items()]
	except:
		print(f"Invalid panel dict in {id}")
		print(panels)
		return []

def cast_oo_to_text(id, oo):
	try:
		return [{"text": v, "position": k.replace("_"," ")} for v, k in oo.items()]
	except:
		print(f"Invalid oo dict in {id}")
		print(oo)
		return []

def parse_and_join_output(id, output_dict, row):
	
	raw_fragments = output_dict.values()

	caption_fragments = []

	try:
		artist = find_artist_from_row(row)
		if artist: 
			caption_fragments.append(f"The image is a digital illustration by the artist {artist}.")
	except:
		print(f"Error when fetching artist in {id}")

	# See multiple_characters.json
	for rf in raw_fragments:
		if rf and rf != "None":
			if isinstance(rf, dict):
				if "description" in rf:
					rf_name = f"{rf["name"]}, " if "name" in rf else ""
					caption_fragments.append(f"{rf_name}{rf["description"]}")
				elif "speech_bubble_1" in rf:
					caption_fragments.append(join_speechbubble_as_dict(id, rf))
				elif "speech_bubble" in rf: 
					caption_fragments.append(rf["speech_bubble"])
				elif "character_1" in rf:
					# 250205: Close to break.
					caption_fragments.append(join_character_as_dict(id, rf))
				elif "text_1" in rf:
					# 250205: Strange case. Fallback to list.
					caption_fragments.append(join_texts_as_list(id, rf.values()))
				elif "1st_frame" in rf:
					# 250205: The 1st, 2nd, 3rd is a headache.
					rf2 = cast_frame_to_text(id, rf)
					caption_fragments.append(join_texts_as_list(id, rf2, "frames"))
				elif "top_panel" in rf:
					# 250205: The top, middle, bottom is also a headache.
					rf2 = cast_panel_to_text(id, rf)
					caption_fragments.append(join_texts_as_list(id, rf2, "panels"))
				elif "title" in rf: 
					caption_fragments.append(cast_title(id, rf["title"]))
				else:		
					try:	
						rfk = list(rf.keys())
						if "_text" in rfk[0]:
							# 250205: i18n text, or just stange text.
							caption_fragments.append(join_texts_as_list(id, rf.values(), "multilingual"))
						else:
							# 250205: It is almost "some text in a NLP place". 
							rf2 = cast_oo_to_text(id, rf)
							caption_fragments.append(join_texts_as_list(id, rf2, "embedded objects"))
					except:
						print(f"Invalid caption fragment (dict) in {id}: {rf}")
						caption_fragments.append("")
			elif isinstance(rf, list):
				caption_fragments.append(join_texts_as_list(id, rf))
			elif isinstance(rf, str):
				caption_fragments.append(rf)
			else:
				print(f"Invalid caption fragment (unknown type) in {id}: {rf}")
				caption_fragments.append("")

	try:
		nlp_caption = " ".join(caption_fragments)
		return nlp_caption
	except:
		print(f"Parse error in {id}")
		return ""

def make_caption(generator, tokenizer, image_embeddings, max_new_tokens, gen_settings, id, msg_text, row):
	output = generator.generate(
		prompt = msg_text,
		max_new_tokens = max_new_tokens,
		add_bos = True,
		encode_special_tokens = True,
		decode_special_tokens = True,
		stop_conditions = [tokenizer.eos_token_id],
		gen_settings = gen_settings, #or set up desired sampling
		embeddings = image_embeddings,
	)

	output_text=output.split('<|im_start|>assistant\n')[-1]
	#print(output_text)

	try:
		output_dict = json.loads(output_text)
		return parse_and_join_output(id, output_dict, row), True
	except:
		# Invalid JSON. Try to recover the string.
		pass
	
	try:
		# There are lines for the text, so we can drop the last kv pair and remake the JSON string.
		recovered_text = "{\n" + ("\n".join(output_text.split("\n")[1:-1])[:-1]) + "\n}"
		recovered_dict = json.loads(recovered_text)
		# Mostly there are way too much text to screw the dict. Drop it.
		if "texts" in recovered_dict:
			del recovered_dict["texts"]
		# There may be too many characters in the images. Core logic will handle it.
		return parse_and_join_output(id, recovered_dict, row), True
	except:
		# Unrecoverable JSON String.
		# 250205: Around 1 in 7500. Way more than 3SD.
		# 250205: A lot more in 4bpw. It is markdown text.
		print(f"Invalid JSON in {id}")
		return output_text, False

def main(args):
	PARQUET_PATH = args.parquet_path #'../cheesechaser-runtime/danbooru2024-webp-4Mpixel/metadata.parquet'
	max_new_tokens = args.max_new_tokens #1000
	g_device = args.device #'cuda:0'
	if "cuda:" in g_device:
		try:
			os.environ["CUDA_VISIBLE_DEVICES"] = g_device.split("cuda:")[1]
			print("CUDA device overrided: " + os.environ["CUDA_VISIBLE_DEVICES"])
		except:
			pass
	g_threads = args.prompt_threads #48

	from exllamav2 import (
		ExLlamaV2,
		ExLlamaV2Config,
		ExLlamaV2Cache,
		ExLlamaV2Tokenizer,
		ExLlamaV2VisionTower,
	)

	from exllamav2.generator import (
		ExLlamaV2DynamicGenerator,
		ExLlamaV2Sampler,
	)

	IMG_DIR = args.img_dir #'H:/danbooru2024-webp-4Mpixel/kohyas_finetune/'
	IMG_EXT = args.img_ext #".webp"

	MISSING_JSON = args.in_json #"./missing.json"
	CAPTION_JSON_GOOD = args.out_json_good #"./meta_cap_2024_toriigate_good.json"
	CAPTION_JSON_BAD = args.out_json_bad #"./meta_cap_2024_toriigate_bad.json"

	si = args.start_index
	ei = args.end_index

	print("Preparing the tagging database")

	df = pd.read_parquet(PARQUET_PATH, columns=['id', 'tag_string_character', 'tag_string_general', 'tag_string_artist'])

	print("Preparing the targeted ids")

	data_missing = None

	with open(MISSING_JSON, 'r') as file:
		data_missing = json.load(file)

	target_ids = [int(id) for id in data_missing["caption"]][si:ei]

	print("Preparing caption model")

	config = ExLlamaV2Config(args.model_local_path)
	config.max_seq_len = args.max_seq_len
	vision_model = ExLlamaV2VisionTower(config)
	vision_model.load(progress = True)

	model = ExLlamaV2(config)
	cache = ExLlamaV2Cache(model, lazy = True, max_seq_len = args.max_seq_len)
	model.load_autosplit(cache, progress = True)
	tokenizer = ExLlamaV2Tokenizer(config)

	generator = ExLlamaV2DynamicGenerator(
		model = model,
		cache = cache,
		tokenizer = tokenizer,
	)

	gen_settings = ExLlamaV2Sampler.Settings.greedy()

	final_result_good = {}
	final_result_bad = {}

	print("preparing prompts")

	# 250202: Slightly ugly inner funtion.
	# 250206: Different from sample code, embedding has been delayed until making caption.
	#df.itertuples() is not used.
	def prepare_msg_from_tid(tid):
		row = df[df.index == tid]
		if row.empty:
			raise Exception(f"Not found: {tid}")
		userprompt, image_file = prepare_emb_with_msg(row, IMG_DIR, IMG_EXT)
		return {'id': tid, 'msg': userprompt, 'row': row, 'img': image_file}

	all_msgs = thread_map(prepare_msg_from_tid, target_ids, max_workers=g_threads, desc="making prompt messages", position=0)
	print("sorting")
	all_msgs.sort(key=lambda x: int(x['id']))
	#all_msgs = [x[1] for x in all_msgs]

	#raise Exception("BLOCKED")

	#Dump everything to kohyas metadata file.
	#{
	#  "id": {
	#    "tags": "",
	#    "caption": "".
	#    "train_resolution": []
	#  }
	#}

	#print(all_msgs[0])
	for mo in tqdm(all_msgs, desc="making caption", position=0):
		# 250206: Same as process_vision_info, but seperated into two steps. Look like memory usage is stable, and I/O delay is minimal.
		msg_text, image_embeddings = load_msg_and_emb(mo['msg'], mo['img'], model, vision_model, tokenizer)
		caption, is_good_caption = make_caption(generator, tokenizer, image_embeddings, max_new_tokens, gen_settings, mo['id'], msg_text, mo['row'])
		if is_good_caption:
			final_result_good[str(mo['id'])] = { "caption": caption }
		else:
			final_result_bad[str(mo['id'])] = { "caption": caption }

	print("Outputing JSON")

	# Align to actual metadata json.
	json_object_good = json.dumps(final_result_good, indent=2)
	
	with open(CAPTION_JSON_GOOD, "w") as outfile:
		outfile.write(json_object_good)

	json_object_bad = json.dumps(final_result_bad, indent=2)
	
	with open(CAPTION_JSON_BAD, "w") as outfile:
		outfile.write(json_object_bad)

	print(f"Dump complete.")

if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)