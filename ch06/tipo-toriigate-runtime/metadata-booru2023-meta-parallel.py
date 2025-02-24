# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

import json

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

df = pd.read_parquet('./danbooru2023-prompt-gen-data.parquet', columns=['index', 'rating', 'phi3v_horny', 'pixtral_caption', 'florence_short', 'florence_long'])

# This is not directly used. I leave it as reference.
DD_TAG_JSON = "./meta_cap.json"

# This is for preparing bucket latents
SPLIT_DD_TAG_JSON = "./meta_cap_{}.json"

# Set 1 for single thread
g_threads = 48 

# GPU count. Used for caching latents and ARB.
split_count = 16

#Dump everything to kohyas metadata file.
#{
#  "id": {
#    "caption": ""
#  }
#}

final_result = {}

split_result = {}

for i in range(split_count):
    split_result[i] = {}

# Multi threads needs packing parameters, so it will be a bit counter intuitive. Equivalent to "for row in df.itertuples()"
def dump_tags(row):
    #Use this filter for nsfw only
    #if (row.rating[0] == "s") or (row.rating[0] == "g"):
    #    return None

    #AngelBottomless: df.set_index has been applied on field "id" (so it is hidden in HF online preview)
    #This is never in ascending order! The actual df is in chronological order! You can find the hint in FFFF.json.
    danbooru_post_id = int(row.Index)

    #In 2412, kohyas-ss should handle well
    #tag = row.tag_string.replace(" ",",")
    #rearranged_tags = [row.tag_string_character, row.tag_string_copyright, row.tag_string_artist, row.tag_string_general, row.tag_string_meta]
    rearranged_tags = [row.phi3v_horny, row.pixtral_caption, row.florence_short, row.florence_long]
    must_exist = [tag for tag in rearranged_tags if tag]

    #A bit philosophical and controversal: I don't even add year tag here. 
    #Danbooru has defined styles and years like "2000s" and "2024", which has stated explictly "do not link with upload time". 
    #Disrupting the tag definiton will cause AI/ML problems, which AI cannot learn contradictions.
    #If the final destination is learning "some artist in some topic in some time window", please make embedding or train a LoRA.
    #250224: There are many \n which will break kohyas trainer's wildcard.
    caption = " ".join(must_exist).replace("\n","")

    final_result[str(danbooru_post_id)] = { "caption": caption }
    split_result[danbooru_post_id % split_count][str(danbooru_post_id)] = { "caption": caption }

    return danbooru_post_id

# The return value is arbitary. itertuples() is an iterator and thread_map will beautifully .
res_dump_tags = thread_map(dump_tags, df.itertuples(), max_workers=g_threads, desc="dumping tags", position=0)

print(f"Tags found: {len(res_dump_tags)}")
       
# Align to actual metadata json.
json_object = json.dumps(final_result, indent=2)
 
with open(DD_TAG_JSON, "w") as outfile:
    outfile.write(json_object)

#for i in range(split_count):
#    json_object = json.dumps(split_result[i], indent=2)
# 
#    with open(SPLIT_DD_TAG_JSON.format(str(i)), "w") as outfile:
#        outfile.write(json_object)

print(f"Dump complete.")