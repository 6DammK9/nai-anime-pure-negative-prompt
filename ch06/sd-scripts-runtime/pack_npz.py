import argparse
import json
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import os.path
from pathlib import Path
import tarfile

g_threads = 48

TOTAL_TAR_COUNT = int(1e3)
EXT_TAR = ".tar"
EXT_NPZ = ".npz"

tar_mappings = {}

# Modified from verify_npz. Make sure all npz files are generated!
# Warning: Validation will be minimal!

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npz_dir", type=str, default="./kohyas_finetune", help="directory storing *.npz files.")
    parser.add_argument("--meta_json", type=str, default="./meta_cap_dd.json", help="The input metadata JSON.")
    parser.add_argument("--tar_dir", type=str, default="./latents", help="directory storing *.tar files.")
    parser.add_argument("--start_from", type=int, default=0, help="Start from a non zero index.")
    return parser

def main(args):
    # Same approach: We don't use glob, we use the metadata directly.
    npz_dir = args.npz_dir
    meta_json = args.meta_json
    TAGS_FOLDER = args.tar_dir

    data = None
    allid = None

    with open(meta_json, 'r') as file:
        data = json.load(file)
        allid = list(data.keys())

    scan_range = [int(id) for id in allid[args.start_from:]]

    print(f"Found entries: {len(scan_range)}")

    df_max_id = max(scan_range)

    print(f"Max ID in the dataset: {df_max_id}")

    # May throw (e.g. os.Error)
    def dump_tar(mod_1e3):
        subfolder = str(mod_1e3).zfill(4)
        tf = f"{TAGS_FOLDER}/{subfolder}{EXT_TAR}"
        detected_npz = 0
        with tarfile.open(tf, "w") as tar:
            for i in range(mod_1e3, df_max_id + 1, TOTAL_TAR_COUNT):
                npz_file_name = f"{npz_dir}/{i}{EXT_NPZ}"
                if os.path.isfile(npz_file_name):                    
                    tar.add(npz_file_name, arcname=f"{i}{EXT_NPZ}")
                    detected_npz = detected_npz + 1
        return detected_npz

    Path(TAGS_FOLDER).mkdir(parents=True, exist_ok=True)
    res_dump_tar = thread_map(dump_tar, range(TOTAL_TAR_COUNT), max_workers=g_threads, desc="packing npz files", position=0)

    print(f"Files written: {len(res_dump_tar)}")
    # Should equal to found entries.
    print(f"Detected npz: {sum(res_dump_tar)}.")

if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)