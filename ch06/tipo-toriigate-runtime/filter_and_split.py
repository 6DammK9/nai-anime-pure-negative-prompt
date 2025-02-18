import json
from tqdm import tqdm
#from tqdm.contrib.concurrent import thread_map

META_LAT = "F:/danbooru2024-webp-4Mpixel/meta_cap_dd.json"
EMPTY_2023 = "./empty_2023.json"
EMPTY_2023_FILTERED = "./empty_2023_filtered_25021702.json"

meta_lat_keys = []
empty2023_keys = []

print("loading META_LAT")

with open(META_LAT, 'r') as file:
    meta_lat = json.load(file)
    meta_lat_keys = list(meta_lat.keys())
    print(f"count: {len(meta_lat_keys)}")

    #print(meta_lat["12468"])

print("loading EMPTY_2023")

with open(EMPTY_2023, 'r') as file:
    empty2023 = json.load(file)
    empty2023_keys = list(empty2023["caption"])
    print(f"count: {len(empty2023_keys)}")

print("filtering")

#filtered_empty2023 = [m for m in empty2023_keys if m in meta_lat_keys]

filtered_empty2023 = []

for m in tqdm(empty2023_keys, desc="Matching keys", position=0): 
    if m in meta_lat:
        filtered_empty2023.append(m)

print(f"count: {len(filtered_empty2023)}")

print("writing output")

# Align to actual metadata json.
output_missing = json.dumps({ "caption": filtered_empty2023 }, indent=2)

with open(EMPTY_2023_FILTERED, "w") as outfile:
    outfile.write(output_missing)
