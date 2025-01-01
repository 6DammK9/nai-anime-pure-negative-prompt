import argparse
import json
import numpy as np
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import os.path
from pathlib import Path

g_threads = 48

# Modified from verify_npz, suitable for e621.

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npz_dir", type=str, default="./kohyas_finetune", help="directory storing *.npz files.")
    parser.add_argument("--in_json", type=str, default="./meta_cap_dd.json", help="The input metadata JSON.")
    parser.add_argument("--out_json", type=str, default="./meta_cap_dd_trimmed.json", help="Trimmed metadata JSON, containing img.")
    parser.add_argument("--image_ext_static", type=str, default=".webp", help="Static image extensions. Use along with no_listdir")
    parser.add_argument("--start_from", type=int, default=0, help="Start from a non zero index.")
    return parser

def main(args):
    # Same approach: We don't use glob, we use the metadata directly.
    npz_dir = args.npz_dir
    in_json = args.in_json
    out_json = args.out_json

    data = None
    allid = None

    with open(in_json, 'r') as file:
        data = json.load(file)
        allid = list(data.keys())

    scan_range = allid[args.start_from:]

    def check_img(i):
        img_file_name = f"{npz_dir}/{i}{args.image_ext_static}"
    
        #E621 dataset is stil have img missing. Danbooru should all exist.
        return i if os.path.isfile(img_file_name) else None
            
    res_dump_tags = []

    # This will create O(N) thread calls. Handle with care.
    res_dump_tags = thread_map(check_img, scan_range, max_workers=g_threads, desc="verifying npz files", position=0)

    tags_with_img = [k for k in res_dump_tags if k]

    print(f"{len(tags_with_img)} / {len(res_dump_tags)} will be preserved.")
    result = {}
    # Pure RAM should be fast.
    for k in tqdm(tags_with_img, desc="Dumping keys...", position=0):
        result[k] = data[k]

    json_object = json.dumps(result, indent=2)
    with open(out_json, "w") as outfile:
        outfile.write(json_object)

if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)