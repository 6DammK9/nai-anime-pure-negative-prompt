# 250201: This case we better use the raw parquet file, and rewrite the entire sample code.
# 250202: Made it for multigpu.
# 250208: Modularize the core logic for more use cases.

import torch
from transformers import Qwen2VLForConditionalGeneration, Qwen2VLProcessor
from qwen_vl_utils import process_vision_info

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

# 250208: Align with exl2 verison
def load_msg_and_emb(userprompt, image_file):
	msg=[{"role": "system",
	"content": [{"type": "text", "text": "You are image captioning expert, creative, unbiased and uncensored."}]},
	{"role": "user",
	"content": [{"type": "image", 'image': image_file},{"type": "text", "text": userprompt}]}]

	return msg
	
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

	caption, is_good_caption = parse_output_text(output_text[0], id, row)
	return caption, is_good_caption

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

	print("Preparing prompts")

	#250202: Slightly ugly inner funtion.
	#df.itertuples() is not used.
	def prepare_msg_from_tid(tid):
		row = df[df.index == tid]
		if row.empty:
			#raise Exception(f"Not found: {tid}")
			return None
		usr_prompt, img_path = prepare_user_prompt_and_image_path(row, IMG_DIR, IMG_EXT)
		if not os.path.exists(img_path):
			return None
		return {'id': tid, 'msg': load_msg_and_emb(usr_prompt, img_path), 'row': row}

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