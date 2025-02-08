import json

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

def prepare_user_prompt_and_image_path(row, img_dir, img_ext):
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
			elif ("bbox" in texts[0]) or ("bounding_box" in texts[0]) or ("coordinates" in texts[0]):
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
		formatted_texts = [f"\"{t['text'] if isinstance(t, dict) and ('text' in t) else t}\"" for t in texts]
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
		# 7893383
		return [{"text": v, "position": k.replace("_"," ")} for v, k in oo.items() if not ("bbox" in k)]
	except:
		print(f"Invalid oo dict in {id}")
		print(oo)
		return []

def parse_and_join_output(id, output_dict, row):
	
	raw_fragments = output_dict.values()

	caption_fragments = []

	try:
		#The truth value of a DataFrame is ambiguous
		if row is not None:
			artist = find_artist_from_row(row)
			if artist: 
				caption_fragments.append(f"The image is a digital illustration by the artist {artist}.")
			else:
				#print(f"Artist not found in {id}")
				pass
		else:
			#print(f"No row provided in {id}")
			pass
	except Exception as e:
		print(e)
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
					caption_fragments.append(join_texts_as_list(id, list(rf.values())))
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
							caption_fragments.append(join_texts_as_list(id, list(rf.values()), "multilingual"))
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

def parse_output_text(output_text, id, row):
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
	
if __name__ == "__main__":
	print("Please run other scripts to fully test this module.")

	# This may be useful for recovering "bad JSON strings" after human editing. This is < 0.1% of the case.
	nlp_sample = "{\n  \"character\": \"The image features a girl named Tokino Sora. She has long brown hair adorned with a star-shaped hair ornament and a red ribbon. Her blue eyes are looking directly at the viewer, and she has a slight blush on her cheeks. She is lying on her back, wearing a winter coat and a red scarf, which adds to the cozy and warm atmosphere.\",\n  \"background\": \"The background is a snowy scene with footprints visible, suggesting a cold, winter setting.\",\n  \"texts\": \"The image contains the text 'WINTER' prominently displayed in large letters. Additional text includes 'TOKINO SORA', 'HOLOCTOBER presents', 'AN ILLUSTRATION BY MOCOMILIANO', 'STARRING TOKINO SORA \\\"WINTER\\\"', 'Sketch by MOCOMILIANO / colors by MOCOMILIANO / rendering by MOCOMILIANO', 'character design by ORDAN / live2d by SCHWARZ'.\",\n  \"atmosphere\": \"The overall atmosphere is serene and peaceful, capturing the essence of a winter day with a sense of warmth and comfort.\"\n}"
	caption, is_good_caption = parse_output_text(nlp_sample, 8319750, None)
	if is_good_caption:
		print(caption)
	else:
		print("error")