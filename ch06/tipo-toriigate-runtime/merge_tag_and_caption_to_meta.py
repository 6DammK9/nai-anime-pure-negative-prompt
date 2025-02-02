import json
from tqdm import tqdm

JSON_ID = "./meta_lat.json"
JSON_TAGS = "./meta_lat.json"
JSON_LATENT = "./meta_lat.json"
JSON_CAPTION = "./meta_cap.json"
OUTPUT_JSON = "./meta_lat_merged.json"
MISSING_JSON = "./missing.json"

merged = dict()
data_id = None
data_tags = None
data_caption = None
data_lat = None
missing_id = {
    "tags": [],
    "caption": [],
    "latent": []
}

print("loading JSON_ID")

with open(JSON_ID, 'r') as file:
    data_id = json.load(file)

print("loading JSON_TAGS")

with open(JSON_TAGS, 'r') as file:
    data_tags = json.load(file)

print("loading JSON_CAPTION")

with open(JSON_CAPTION, 'r') as file:
    data_caption = json.load(file)

print("loading JSON_LATENT")

with open(JSON_LATENT, 'r') as file:
    data_lat = json.load(file)

print("start merging")

all_ids = data_id.keys()

#Dump everything to kohyas metadata file.
#{
#  "id": {
#    "tags": "",
#    "caption": "".
#    "train_resolution": []
#  }
#}

for id in tqdm(all_ids, desc="merging json files", position=0): 
    merged[id] = {}
    if id in data_tags:
        merged[id]["tags"] = data_tags[id]["tags"]
    else:
        missing_id["tags"].append(id)
    if id in data_caption:
        merged[id]["caption"] = data_caption[id]["caption"]
    else:
        missing_id["caption"].append(id)
    if id in data_lat:
        merged[id]["train_resolution"] = data_lat[id]["train_resolution"]
    else:
        missing_id["latent"].append(id)

print(f"ids: {len(all_ids)}, missing tags: {len(missing_id["tags"])}, missing caption: {len(missing_id["caption"])}, missing latent: {len(missing_id["latent"])}")

print("writing OUTPUT_JSON")

# Align to actual metadata json.
output_merged = json.dumps(merged, indent=2)
 
with open(OUTPUT_JSON, "w") as outfile:
    outfile.write(output_merged)

print("writing MISSING_JSON")

# Align to actual metadata json.
output_missing = json.dumps(missing_id, indent=2)
 
with open(MISSING_JSON, "w") as outfile:
    outfile.write(output_missing)

print(f"Merge complete.")