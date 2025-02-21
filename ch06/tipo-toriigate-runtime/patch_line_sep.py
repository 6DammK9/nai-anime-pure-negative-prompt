# 250222: 2023 Captions has "\n" which will break the kohyas trainer logic (considered as "wildcard"). They must be eliminated. IDE is not capable for a 14GB JSON.

import argparse
import json
import numpy as np
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import os.path
from pathlib import Path

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_json", type=str, default="./meta_lat.json", help="Input JSON")
    parser.add_argument("--out_json", type=str, default="./meta_lat_patched.json", help="Output JSON")
    return parser

def main(args):
    in_json = args.in_json
    out_json = args.out_json

    data = {}

    with open(in_json, 'r') as file:
        data = json.load(file)

    for k in tqdm(data.keys(), desc="patching entries", position=0): 
        data[k]["caption"] = data[k]["caption"].replace("\n","")
    
    print("writing to out_json")

    # Align to actual metadata json.
    output_patched = json.dumps(data, indent=2)
    
    with open(out_json, "w") as outfile:
        outfile.write(output_patched)
    
    print(f"Patch complete.")

# python patch_line_sep.py --in_json "/run/media/user/Intel P4510 3/danbooru2024-webp-4Mpixel/meta_lat_has_sep.json" --out_json "/run/media/user/Intel P4510 3/danbooru2024-webp-4Mpixel/meta_lat.json"
if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)
