import argparse
import json
import numpy as np
from tqdm import tqdm

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--npz_dir", type=str, default="./kohyas_finetune", help="directory storing *.npz files.")
    parser.add_argument("--meta_json", type=str, default="./meta_cap_dd.json", help="The input metadata JSON.")
    return parser

def main(args):
    # Same approach: We don't use glob, we use the metadata directly.
    npz_dir = args.npz_dir
    meta_json = args.meta_json

    # Sample npz file
    if False:
        test = np.load('{}/1342091.npz'.format(npz_dir))

        # NpzFile 'H:/just_astolfo/test/1342091.npz' with keys: latents, original_size, crop_ltrb
        print(test)
        #(4, 96, 128)
        print(test["latents"].shape)
        #[1024  768]
        print(test["original_size"])
        #[   0.    0. 1024.  768.]
        print(test["crop_ltrb"])

    data = None
    allnpz = None

    with open(meta_json, 'r') as file:
        data = json.load(file)
        allnpz = data.keys()

    for i in tqdm(allnpz, desc="verifying npz files", position=0):
        try:
            test = np.load(f"{npz_dir}/{i}.npz")
            if "latents" not in test:
                raise Exception("latents misisng")
            if "original_size" not in test:
                raise Exception("original_size misisng")
            if "crop_ltrb" not in test:
                raise Exception("crop_ltrb misisng")
        except:
            raise Exception(f"Missing or invalid file: {npz_dir}/{i}.npz")

    print(f"All pass.")

if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)