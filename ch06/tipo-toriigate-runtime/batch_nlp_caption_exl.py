# 250201: This case we better use the raw parquet file, and rewrite the entire sample code.
# 250202: Made it for multigpu.
# 250205: EXL conversion.
# 250208: Modularize the core logic for more use cases.

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
import argparse
import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

#250208: Split in modules to support both exl and transformers in one go
from nlp_stuffs import parse_output_text, prepare_user_prompt_and_image_path

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

	output_text = output.split('<|im_start|>assistant\n')[-1]
	# Rare case, 1 in 30k
	output_text = output_text.split("<|endoftext|>")[0]
	# 7872263, 8044837: Not even outputing a valid KV pair.
	# print(output_text)

	caption, is_good_caption = parse_output_text(output_text, id, row)
	return caption, is_good_caption

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

	print("Preparing prompts")

	# 250202: Slightly ugly inner funtion.
	# 250206: Different from sample code, embedding has been delayed until making caption.
	# 250217: Pass 2: There are gaps between 2023 and 2024. Now we need to check if image really exists.
	#df.itertuples() is not used.
	def prepare_msg_from_tid(tid):
		row = df[df.index == tid]
		if row.empty:
			#raise Exception(f"Not found: {tid}")
			return None
		usr_prompt, img_path = prepare_user_prompt_and_image_path(row, IMG_DIR, IMG_EXT)
		if not os.path.exists(img_path):
			return None
		return {'id': tid, 'msg': usr_prompt, 'row': row, 'img': img_path}

	all_msgs = thread_map(prepare_msg_from_tid, target_ids, max_workers=g_threads, desc="Making prompt messages", position=0)
	all_msgs = [m for m in all_msgs if m]
	print(f"Filtering: {len(target_ids)} > {len(all_msgs)}")
	print("Sorting")
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
	for mo in tqdm(all_msgs, desc="Making caption", position=0):
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