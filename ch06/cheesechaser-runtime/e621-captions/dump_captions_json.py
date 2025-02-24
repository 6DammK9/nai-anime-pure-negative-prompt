import json

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

LOCAL_DIR = "C:/temp/e621-captions" 

EXT_JSONL = ".jsonl"

# This is not directly used. I leave it as reference.
DD_TAG_JSON = "./meta_cap.json"

# This is for preparing bucket latents
SPLIT_DD_TAG_JSON = "./meta_cap_{}.json"

# Set 1 for single thread
g_threads = 9

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

tags_found = 0

for i in range(split_count):
    split_result[i] = {}

def dump_year(y):
    count = 0
    for m in range(1, 12 + 1):
        sm = str(m).zfill(2)
        dl_json = "{}/{}-{}_grouped{}".format(LOCAL_DIR, y, sm, EXT_JSONL)
        
        # This file not exist.
        if y == 2007 and m == 1:
            continue

        df = pd.read_json(path_or_buf=dl_json, lines=True)
        
        for row in df.itertuples():
            danbooru_post_id = int(row.id)

            #2502224: There is not much captions. Meanwhile it is so incomplete.
            rearranged_tags = [row.regular_summary, row.brief_summary] if row.response_finish_reason == "STOP" else [row.tags]
                
            must_exist = [tag for tag in rearranged_tags if tag]

            #250224: There are many \n which will break kohyas trainer's wildcard.
            caption = " ".join(must_exist).replace("\n","").replace("\r","")

            final_result[str(danbooru_post_id)] = { "caption": caption }
            split_result[danbooru_post_id % split_count][str(danbooru_post_id)] = { "caption": caption }

            count = count + 1

    return count
        
res_dump_tags = thread_map(dump_year, range(2007, 2024 + 1), max_workers=g_threads, desc="dumping caption in year", position=0)

print(f"Captions found: {sum(res_dump_tags)}")
       
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