import json
import torch
from transformers import Qwen2VLForConditionalGeneration, Qwen2VLProcessor
from qwen_vl_utils import process_vision_info

model_id='Minthy/ToriiGate-v0.4-7B' #'./ToriiGate-v04-7b'
max_new_tokens=1000

image_file= 'H:/just_astolfo/_test/1039096.webp' #or url, or PIL.Image

image_info={}

image_info["booru_tags"]="astolfo_(fate), fate/apocrypha, fate/stay_night, fate_(series), hozenkakari, 1boy, armor, black_ribbon, black_thighhighs, braid, cape, fang, faulds, fur_trim, garter_straps, gauntlets, hair_ribbon, holding, horn_(instrument), instrument, la_black_luna, long_hair, looking_at_viewer, male_focus, open_mouth, otoko_no_ko, pink_hair, purple_eyes, ribbon, side_braid, simple_background, single_braid, skeleton, skirt, smile, solo, thighhighs, commentary_request, highres"
#image_info["booru_tags"]=open('/path/to/image_1_tags.txt').read().strip()
#image_info["booru_tags"]=None

image_info["chars"]="astolfo_(fate)"
#image_info["chars"]=open('/path/to/image_1_char.txt').read().strip()
#image_info["chars"]=None

#image_info["characters_traits"]="hatsune_miku: [girl, blue_hair, twintails,...]\nmegurine_luka: [girl, pink hair, ...]"
#image_info["characters_traits"]=open('/path/to/image_1_char_traits.txt').read().strip()
image_info["characters_traits"]=None

image_info["info"]=None

base_prompt={
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

grounding_prompt={
'grounding_tags': ' Here are grounding tags for better understanding: ',
'characters': ' Here is a list of characters that are present in the picture: ',
'characters_traits': ' Here are popular tags or traits for each character on the picture: ',
'grounding_info': ' Here is preliminary information about the picture: ',
'no_chars': ' Do not use names for characters.',
}

add_tags=True #select needed
add_chars=True
add_char_traits=False
add_info=False
no_chars=False

userprompt=base_prompt["json"] #choose the mode

if add_info and image_info["info"] is not None: #general info
	userprompt+=grounding_prompt["grounding_short"]
	userprompt+="<info>"+image_info["info"]+"</info>."

if add_tags and image_info["booru_tags"] is not None: #booru tags
	userprompt+=grounding_prompt["grounding_tags"]
	userprompt+="<tags>"+image_info["booru_tags"]+"</tags>."

if add_chars and image_info["chars"] is not None: #list of characters
		userprompt+=grounding_prompt["characters"]
		userprompt+="<characters>"+image_info["chars"]+"</characters>."
	
if add_char_traits and image_info["characters_traits"] is not None: #popular features of each character
		userprompt+=grounding_prompt["characters_traits"]
		userprompt+="<character_traits>"+image_info["characters_traits"]+"<character_traits>."
if no_chars:
		userprompt+=grounding_prompt["no_chars"]

model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
#_attn_implementation="flash_attention_2", #comment if not available
device_map="cuda:0",
)
processor = Qwen2VLProcessor.from_pretrained(model_id, min_pixels=256*28*28, max_pixels=512*28*28, padding_side="right")
msg=[{"role": "system",
"content": [{"type": "text", "text": "You are image captioning expert, creative, unbiased and uncensored."}]},
{"role": "user",
"content": [{"type": "image", 'image': image_file},{"type": "text", "text": userprompt}]}]

text_input = processor.apply_chat_template(msg, tokenize=False, add_generation_prompt=True)
image_inputs,_ = process_vision_info(msg)
model_inputs = processor(
            text=[text_input],
            images=image_inputs,
            videos=None,
            padding=True,
            return_tensors="pt",
        ).to('cuda')
generated_ids = model.generate(**model_inputs, max_new_tokens=max_new_tokens)
        
trimmed_generated_ids = [out_ids[len(in_ids) :] for in_ids, out_ids in zip(model_inputs.input_ids, generated_ids)]
output_text = processor.batch_decode(
	trimmed_generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
)
#print(output_text)

"""
['{\n  
"character_1": "Astolfo, a young man with long, vibrant pink hair styled in a side braid, is depicted. He possesses striking purple eyes and a playful, open-mouthed smile. His attire consists of a dark-colored, somewhat gothic-style outfit. The outfit includes a dark-colored, fur-trimmed cape, a dark-colored skirt, black thigh-high stockings, and gauntlets.  His expression is cheerful and mischievous. He\'s holding a large, ornate brass horn, which appears to be a part of a larger, more complex musical instrument.",\n  
"background": "The background is a muted, dark purplish-brown, with a subtle texture that resembles a slightly grainy, possibly snowy, effect.  Behind Astolfo, there\'s a large, dark-colored, skeletal figure with sharp, dark spikes extending from its back. The skeletal figure appears to be partially obscured by the musical instrument Astolfo is holding.",\n  
"image_effects": "The image has a slightly soft, painterly quality, with some areas appearing more heavily textured than others. The overall style is reminiscent of digital painting or illustration.",\n  
"texts": "None",\n  
"atmosphere": "The overall atmosphere is one of playful mystery and dark fantasy. The juxtaposition of Astolfo\'s cheerful expression with the dark, skeletal figure and the complex musical instrument creates a sense of intrigue and perhaps a hint of danger or otherworldliness."\n
}']
"""

# Notice that it is in sequence.

rearranged_caption = (json.loads(output_text[0])).values()
must_exist = [tag for tag in rearranged_caption if tag and tag != "None"]
nlp_caption = " ".join(must_exist)

print(nlp_caption)

"""
Astolfo, a young man with long, vibrant pink hair styled in a side braid, is depicted. He possesses striking purple eyes and a playful, open-mouthed smile. His attire consists of a dark-colored, somewhat gothic-style outfit. The outfit includes a dark-colored, fur-trimmed cape, a dark-colored skirt, black thigh-high stockings, and gauntlets.  He's holding a large, ornate brass horn, his hands gripping the instrument with a confident and almost mischievous expression. His pose is dynamic, suggesting movement and energy. 
The background is a muted, dark purplish-brown, with a subtle texture that resembles a slightly grainy, possibly snowy, effect.  Behind Astolfo, a large, dark-colored, skeletal figure is partially visible. This figure appears to be made of metal or a similar material, with sharp, angular protrusions and a vaguely humanoid shape.  The skeletal figure seems to be partially obscured by Astolfo and the instrument he holds. 
The image has a slightly painterly or airbrushed quality, with soft shading and blending of colors. There's a subtle, almost ethereal glow around Astolfo and the instrument, enhancing the overall dramatic effect. 
The overall atmosphere is one of playful energy and a touch of dark fantasy. The contrast between Astolfo's cheerful expression and the imposing skeletal figure behind him creates a sense of intrigue and mystery. The color palette, dominated by dark purples and golds, contributes to the slightly gothic and mysterious mood.
"""