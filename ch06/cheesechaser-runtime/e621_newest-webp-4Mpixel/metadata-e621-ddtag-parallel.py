# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow
import json

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# Notes: Raw parquet has different schemas, this is the merged one
# Meanwhile it is no more hidden index field.
df = pd.read_parquet('./e621-merged.parquet')

# This is not directly used. I leave it as reference.
DD_TAG_JSON = "./meta_cap_dd.json"

# This is for preparing bucket latents
SPLIT_DD_TAG_JSON = "./meta_cap_dd_{}.json"

# Set 1 for single thread
g_threads = 1 

# GPU count. Used for caching latents and ARB.
split_count = 4 

#Dump everything to kohyas metadata file.
#{
#  "id": {
#    "tags": ""
#  }
#}

final_result = {}

split_result = {}

for i in range(split_count):
    split_result[i] = {}

# Multi threads needs packing parameters, so it will be a bit counter intuitive. Equivalent to "for row in df.itertuples()"
def dump_tags(row):
    #Use this filter for nsfw only
    #if (row.rating == "s") or (row.rating == "g"):
    #    return None

    # Folow what danbooru case does.
    danbooru_post_id = int(row.id)

    # There is nothing to do.
    final_result[str(danbooru_post_id)] = { "tags": row.tag_string }
    split_result[danbooru_post_id % split_count][str(danbooru_post_id)] = { "tags": row.tag_string }

    return danbooru_post_id

# The return value is arbitary. itertuples() is an iterator and thread_map will beautifully .
res_dump_tags = thread_map(dump_tags, df.itertuples(), max_workers=g_threads)

print(f"Tags found: {len(res_dump_tags)}")
       
# Align to actual metadata json.
json_object = json.dumps(final_result, indent=2)
 
with open(DD_TAG_JSON, "w") as outfile:
    outfile.write(json_object)
    
for i in range(split_count):
    json_object = json.dumps(split_result[i], indent=2)
 
    with open(SPLIT_DD_TAG_JSON.format(str(i)), "w") as outfile:
        outfile.write(json_object)

print(f"Dump complete.")