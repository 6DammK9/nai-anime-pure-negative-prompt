# 250216: A bit personal and one time use.

import json
import os
from tqdm import tqdm

GOOD_JSON_DIR = "F:/tipo-toriigate-runtime/split_files"
FIXED_JSON_DIR = "F:/tipo-toriigate-runtime/split_files_fix"
TARGET_JSON_DIR = "F:/danbooru2024-webp-4Mpixel"

# Merge target
TARGET_JSON = "{}/meta_cap.json"

# To be merged
SPLIT_GOOD_JSON = "{}/meta_cap_2024_toriigate_good_{}.json"
SPLIT_FIXED_JSON = "{}/meta_cap_2024_toriigate_fixed_{}.json"

BASE_JSON = "{}/meta_cap_2023.json"
KEY_CAPTION = "caption"

# Depends on previous stage
# There is 4 passes (64 + 4 + 1 + 1)
split_count = 70

merged = dict()

if True:
    print("merge meta_cap.json")
    k0 = 0
    k1 = 0
    with open(BASE_JSON.format(TARGET_JSON_DIR), 'r') as file:
        data = json.load(file)
        k0 = len(list(data.keys()))
        # 250217: Found many empty captions. Need to trim.
        data_trimmed = {k:v for (k,v) in data.items() if v[KEY_CAPTION]}
        k1 = len(list(data_trimmed.keys()))
        merged.update(data_trimmed)

    print(f"Keys count: {k0} > {k1}")

# 250216: Not all files are exist.

for i in tqdm(range(split_count), desc="merging good json", position=0): 
    cur_path = SPLIT_GOOD_JSON.format(GOOD_JSON_DIR, i)
    if os.path.exists(cur_path):
        with open(cur_path, 'r') as file:
            data = json.load(file)
            merged.update(data)
    else:
        print(f"Not extst (skip): {cur_path}")

print(f"Keys count: {len(list(merged.keys()))}")

for i in tqdm(range(split_count), desc="merging fixed json", position=0): 
    cur_path = SPLIT_FIXED_JSON.format(FIXED_JSON_DIR, i)
    if os.path.exists(cur_path):
        with open(cur_path, 'r') as file:
            data = json.load(file)
            merged.update(data)
    else:
        print(f"Not extst (skip): {cur_path}")

m0 = len(list(merged.keys()))

merged_trimmed = {k:v for (k,v) in merged.items() if v[KEY_CAPTION]}

m1 = len(list(merged_trimmed.keys()))

print(f"Keys count: {m0} > {m1}")

print("Outputing merged json.")

# Align to actual metadata json.
json_object = json.dumps(merged_trimmed, indent=2)
 
with open(TARGET_JSON.format(TARGET_JSON_DIR), "w") as outfile:
    outfile.write(json_object)

print(f"Merge complete.")