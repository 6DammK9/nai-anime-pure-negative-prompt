# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow
import json

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# Notes: Raw parquet has different schemas, this is the merged one
# Meanwhile it is no more hidden index field.
df = pd.read_parquet('./e621-merged.parquet')

DD_TAG_JSON = "./meta_cap_dd.json"

g_threads = 48 # Set 1 for single thread

#Dump everything to kohyas metadata file.
#{
#  "id": {
#    "tags": ""
#  }
#}

final_result = {}

# Multi threads needs packing parameters, so it will be a bit counter intuitive. Equivalent to "for row in df.itertuples()"
def dump_tags(row):
    #I want nsfw only
    if (row.rating == "s") or (row.rating == "g"):
        return None

    # Folow what danbooru case does.
    danbooru_post_id = int(row.id)

    # There is nothing to do.
    final_result[str(danbooru_post_id)] = { "tags": row.tag_string }

    return danbooru_post_id

# The return value is arbitary. itertuples() is an iterator and thread_map will beautifully .
res_dump_tags = thread_map(dump_tags, df.itertuples(), max_workers=g_threads)

print(f"Tags found: {len(res_dump_tags)}")
       
# Align to actual metadata json.
json_object = json.dumps(final_result, indent=2)
 
with open(DD_TAG_JSON, "w") as outfile:
    outfile.write(json_object)

print(f"Dump complete.")