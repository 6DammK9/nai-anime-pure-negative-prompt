import argparse
import json
import numpy as np
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
import os.path
from pathlib import Path

g_threads = 48

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npz_dir", type=str, default="./kohyas_finetune", help="directory storing *.npz files.")
    parser.add_argument("--meta_json", type=str, default="./meta_cap_dd.json", help="The input metadata JSON.")
    parser.add_argument("--image_ext_static", type=str, default=".webp", help="Static image extensions. Use along with no_listdir")
    parser.add_argument("--start_from", type=int, default=0, help="Start from a non zero index.")
    return parser

def inspect_npz(test, i):
    # NpzFile 'H:/just_astolfo/test/1342091.npz' with keys: latents, original_size, crop_ltrb
    print(i)
    #print(test)
    #(4, 96, 128)
    print(test["latents"].shape)
    #[1024  768]
    print(test["original_size"])
    #[   0.    0. 1024.  768.]
    #print(test["crop_ltrb"])

def main(args):
    # Same approach: We don't use glob, we use the metadata directly.
    npz_dir = args.npz_dir
    meta_json = args.meta_json

    # Sample npz file
    if False:
        #savez will replace the file even it is corrputed.
        #np.savez('{}/1039096.npz'.format(npz_dir), np.arange(10),  np.arange(10))
        test = np.load('{}/1039096.npz'.format(npz_dir))
        inspect_npz(test, 1039096)

    data = None
    allnpz = None

    with open(meta_json, 'r') as file:
        data = json.load(file)
        allnpz = list(data.keys())

    print(f"Start from id {allnpz[args.start_from]}")
    #return
    scan_range = allnpz[args.start_from:]
    
    # Simplified version from train_util.is_disk_cached_latents_is_expected: Just scan for corrupted files without bucket validation.
    # Meanwhile I added auto remove, since there may be a lot of corrupted files due to hardware issue.
    # Hint: https://stackoverflow.com/questions/26064061/closing-a-file-after-using-np-load-using-spyder
    # start notepad++ "F:/e621_newest-webp-4Mpixel/kohyas_finetune/3179435.npz"
    def check_and_nuke_npz(i):
        img_file_name = f"{npz_dir}/{i}{args.image_ext_static}"
        npz_file_name = f"{npz_dir}/{i}.npz"

        #E621 dataset is stil have img missing. Danbooru should all exist.
        if not os.path.isfile(img_file_name):
            return None        
        if not os.path.isfile(npz_file_name):
            #Tolerate for finding corrupted npz files quickly.
            return None
            #raise Exception(f"npz misisng: {npz_file_name}")

        del_file = False
        try:
            with np.load(npz_file_name) as test:           
                if "latents" not in test:
                    raise Exception(f"latents misisng: {npz_file_name}")
                if "original_size" not in test:
                    raise Exception(f"original_size misisng: {npz_file_name}")
                if "crop_ltrb" not in test:
                    raise Exception(f"crop_ltrb misisng: {npz_file_name}")
                return i
        except Exception as e:
            #print(e)
            print(f"Corrupted file: {npz_file_name}")
            del_file = True
        
        if del_file:
            Path.unlink(npz_file_name)
        return None

    res_dump_tags = []

    # This will create O(N) thread calls. Handle with care.
    res_dump_tags = thread_map(check_and_nuke_npz, scan_range, max_workers=g_threads, desc="verifying npz files", position=0)

    #for i in tqdm(scan_range, desc="verifying npz files", position=0):
    #    res_dump_tags.append(check_and_nuke_npz(i))

    print(f"All pass ({len(res_dump_tags)}).")

if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)