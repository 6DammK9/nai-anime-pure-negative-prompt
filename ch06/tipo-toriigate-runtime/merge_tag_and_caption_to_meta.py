import json
from tqdm import tqdm

#Astolfo dataest
if False:
    JSON_ID = "F:/just_astolfo/meta_lat.json"
    JSON_TAGS = "F:/danbooru2024-webp-4Mpixel/meta_cap_dd.json"
    JSON_LATENT = "F:/just_astolfo/meta_lat.json"
    JSON_CAPTION = "F:/danbooru2024-webp-4Mpixel/meta_cap.json"
    OUTPUT_JSON = "F:/just_astolfo/meta_lat_v2.json"
    MISSING_JSON = "F:/just_astolfo/missing.json"

#Full dataest
if True:
    JSON_ID = "C:/temp/tags/meta_lat.json"
    JSON_TAGS = "C:/temp/tags/meta_lat.json"
    JSON_LATENT = "C:/temp/tags/meta_lat.json"
    JSON_CAPTION = "C:/temp/tags/meta_cap.json"
    OUTPUT_JSON = "C:/temp/tags/meta_lat_v2.json"
    MISSING_JSON = "C:/temp/tags/missing.json"

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
    if (id in data_tags) and (data_tags[id]):
        merged[id]["tags"] = data_tags[id]["tags"]
    else:
        missing_id["tags"].append(id)
    if (id in data_caption) and (data_caption[id]):
        merged[id]["caption"] = data_caption[id]["caption"]
    else:
        #250225: Fallback to tags. Pay attention to the sequence.
        merged[id]["caption"] = merged[id]["tags"]
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