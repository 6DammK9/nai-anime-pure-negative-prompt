# 250208: The routine is "bad > edited > fixed". "good + fixed" will be edited again for unseen challenges.

import os
import json
import argparse
import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

#250208: Split in modules to support both exl and transformers in one go
from nlp_stuffs import parse_output_text

"""
Edited
{
  "7927424": {
    "caption": "{\n  \"character_1\": \"A muscular man with short... and fun.\"\n}"
  }
}
Fixed
{
  "7927424": {
    "caption": "This is an digital illustration from artist..."
  }
}
"""

EXT_JSON = ".json"

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet_path", type=str, default="F:/danbooru2024-webp-4Mpixel/metadata.parquet", help="*.parquet of the danbooru2024.")
    parser.add_argument("--edited_json_prefix", type=str, default="./split_files_fix/meta_cap_2024_toriigate_edited", help="Manual edited JSONs. Prefix only, before '_0.json'.")
    parser.add_argument("--edited_json_start", type=int, default=0, help="range(start, end) of the split.")
    parser.add_argument("--edited_json_end", type=int, default=64, help="range(start, end) of the split.")
    parser.add_argument("--nosplit", action="store_true", help="No split applied. No suffix will be added.")
    parser.add_argument("--fixed_json_prefix", type=str, default="./split_files_fix/meta_cap_2024_toriigate_fixed", help="Fixed JSONs. Prefix only, before '_0.json'.")
    return parser

def parse_output_again(edited_file_path, fixed_file_path, df):

    final_result_fixed = {}

    try:
        # file exists
        #print(edited_file_path)
        with open(edited_file_path, 'r') as file:
            data_edited = json.load(file)
            for tid, edited_json_pkg in data_edited.items():
                if "caption" in edited_json_pkg:
                    edited_json_str = edited_json_pkg["caption"]
                    row = df[df.index == int(tid)]
                    if row.empty:
                        raise Exception(f"Not found: {tid}")
                    caption, is_good_caption = parse_output_text(edited_json_str, tid, row)
                    if is_good_caption:
                        final_result_fixed[tid] = { "caption": caption }
                    else:
                        print("Bad JSON string:")
                        print(edited_json_str)
                        raise Exception(f"Still bad: {tid}")
                else:
                    raise Exception(f"Please add 'caption' again: {tid}")
                
        # Align to actual metadata json.
        json_object_fixed = json.dumps(final_result_fixed, indent=2)

        with open(fixed_file_path, "w") as outfile:
            outfile.write(json_object_fixed)
    except FileNotFoundError as e404:
        pass
    except Exception as e:
        # Output is new files, which should be obvious.
        print(e)
        pass

def main(args):
    PARQUET_PATH = args.parquet_path #'../cheesechaser-runtime/danbooru2024-webp-4Mpixel/metadata.parquet'

    print("Preparing the tagging database")

    df = pd.read_parquet(PARQUET_PATH, columns=['id', 'tag_string_character', 'tag_string_general', 'tag_string_artist'])

    edited_json_prefix = args.edited_json_prefix
    fixed_json_prefix = args.fixed_json_prefix
    edited_json_start = args.edited_json_start
    edited_json_end = args.edited_json_end
    nosplit = args.nosplit

    if not nosplit:
        for i in tqdm(range(edited_json_start, edited_json_end), desc="Remaking captions from edited files", position=0):
            edited_file_path = f"{edited_json_prefix}_{i}{EXT_JSON}"
            fixed_file_path = f"{fixed_json_prefix}_{i}{EXT_JSON}"
            parse_output_again(edited_file_path, fixed_file_path, df)
    else:
        edited_file_path = f"{edited_json_prefix}{EXT_JSON}"
        fixed_file_path = f"{fixed_json_prefix}{EXT_JSON}"
        parse_output_again(edited_file_path, fixed_file_path, df)

    print(f"Dump complete.")

if __name__ == "__main__":
    parser = setup_parser()

    args = parser.parse_args()
    main(args)