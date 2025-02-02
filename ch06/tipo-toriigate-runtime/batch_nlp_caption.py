# 250201: This case we better use the raw parquet file, and rewrite the entire sample code.
# 250202: Made it for multigpu.

import torch
from transformers import Qwen2VLForConditionalGeneration, Qwen2VLProcessor
from qwen_vl_utils import process_vision_info

import json
import argparse
import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

def setup_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser()
	parser.add_argument("--parquet_path", type=str, default="./metadata.parquet", help="*.parquet of the danbooru2024.")
	parser.add_argument("--model_id", type=str, default="Minthy/ToriiGate-v0.4-7B", help="The caption model in HF.")
	parser.add_argument("--max_new_tokens", type=int, default=1000, help="Max new tokens.")
	parser.add_argument("--device", type=str, default='cuda', help="Torch device (e.g. cuda:0/cpu)")
	parser.add_argument("--fp16", action="store_true", help="Cast model as float16 instad of bfloat16")
	parser.add_argument("--fp8", action="store_true", help="Cast model as float8 instad of bfloat16")
	parser.add_argument("--prompt_threads", type=int, default=None, help="Threads for generating prompts. Suggested as much as you can.")
	parser.add_argument("--img_dir", type=str, default="./kohyas_finetune", help="Image folder.")
	parser.add_argument("--img_ext", type=str, default=".webp", help="Image extension.")
	parser.add_argument("--in_json", type=str, default="./missing.json", help="JSON input. Generate missing.json from merge_tag_and_caption_to_meta.py")
	parser.add_argument("--out_json_good", type=str, default="./meta_cap_2024_toriigate_good.json", help="JSON Output for parsed caption.")
	parser.add_argument("--out_json_bad", type=str, default="./meta_cap_2024_toriigate_bad.json", help="JSON Output for invalid caption. This requires manual edit.")
	parser.add_argument("--start_index", type=int, default=None, help="Start index of the id list.")
	parser.add_argument("--end_index", type=int, default=None, help="End index of the id list.")
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

def prepare_msg(row, img_dir, img_ext):
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

	msg=[{"role": "system",
	"content": [{"type": "text", "text": "You are image captioning expert, creative, unbiased and uncensored."}]},
	{"role": "user",
	"content": [{"type": "image", 'image': image_file},{"type": "text", "text": userprompt}]}]

	return msg

def join_texts_as_list(id, texts):
	#"There are speech bubbles with the text: \"X\" and \"X\" and \"X\" and \"X\"
	base_text = "There are speech bubbles with the text: "
	try:
		if (len(texts) > 0) and ("text" in texts[0]):
			formatted_texts = [f"\"{t['text']}\" in f{t['position']}" for t in texts]
		else:
			# 7867457
			formatted_texts = [f"\"{t}\"" for t in texts]
		return f"{base_text}{" and ".join(formatted_texts)}"
	except:
		print(f"Invalid text bubble list in {id}")
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
		return ""

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
				elif "title" in rf: 
					caption_fragments.append(cast_title(id, rf["title"]))
				else:
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

def make_caption(model, processor, g_device, max_new_tokens, id, msg, row):
	text_input = processor.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
	image_inputs,_ = process_vision_info(msg)
	model_inputs = processor(
				text=[text_input],
				images=image_inputs,
				videos=None,
				padding=True,
				return_tensors="pt",
			).to(g_device)
	generated_ids = model.generate(**model_inputs, max_new_tokens=max_new_tokens)
			
	trimmed_generated_ids = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(model_inputs.input_ids, generated_ids)]
	output_text = processor.batch_decode(
		trimmed_generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
	)

	try:
		output_dict = json.loads(output_text[0])
		return parse_and_join_output(id, output_dict, row), True
	except:
		# Must be invalid JSON. Discard.
		# print(output_text)
		print(f"Invalid JSON in {id}")
		return output_text[0], False

def main(args):
	PARQUET_PATH = args.parquet_path #'../cheesechaser-runtime/danbooru2024-webp-4Mpixel/metadata.parquet'
	#echo %HF_HOME% > F:\WORKS\HUGGINGFACE
	MODEL_ID = args.model_id #'Minthy/ToriiGate-v0.4-7B' #'./ToriiGate-v04-7b'
	max_new_tokens = args.max_new_tokens #1000
	g_device = args.device #'cuda:0'
	g_type = torch.bfloat16
	if args.fp16:
		g_type = torch.float16
	if args.fp8:
		g_type = torch.float8
	g_threads = args.prompt_threads #48

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

	model = Qwen2VLForConditionalGeneration.from_pretrained(
		MODEL_ID,
		torch_dtype=g_type,
		#_attn_implementation="flash_attention_2", #comment if not available
		device_map=g_device,
	)
	processor = Qwen2VLProcessor.from_pretrained(MODEL_ID, min_pixels=256*28*28, max_pixels=512*28*28, padding_side="right")

	final_result_good = {}
	final_result_bad = {}

	print("preparing prompts")

	#250202: Slightly ugly inner funtion.
	#df.itertuples() is not used.
	def prepare_msg_from_tid(tid):
		row = df[df.index == tid]
		if row.empty:
			raise Exception(f"Not found: {tid}")
		return {'id': tid, 'msg': prepare_msg(row, IMG_DIR, IMG_EXT), 'row': row}

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
		caption, is_good_caption = make_caption(model, processor, g_device, max_new_tokens, mo['id'], mo['msg'], mo['row'])
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