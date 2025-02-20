import json
from tqdm import tqdm

LAT_JSON_DIR = "H:/danbooru2024-webp-4Mpixel"

# Merge target
LAT_JSON = "{}/meta_lat.json"

# To be merged
SPLIT_LAT_JSON = "{}/meta_lat_{}.json"

# GPU count. Used for caching latents and ARB.
split_count = 16

merged = dict()

for i in tqdm(range(split_count), desc="merging (huge) json files", position=0): 
    with open(SPLIT_LAT_JSON.format(LAT_JSON_DIR, i), 'r') as file:
        data = json.load(file)
        merged.update(data)

# Align to actual metadata json.
json_object = json.dumps(merged, indent=2)
 
with open(LAT_JSON.format(LAT_JSON_DIR), "w") as outfile:
    outfile.write(json_object)

print(f"Merge complete.")