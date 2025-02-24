# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

import tarfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

LOCAL_DIR = "C:/temp/e621-captions" 

EXT_JSONL = ".jsonl"

TAGS_FOLDER = "C:/temp/tags"

TOTAL_TAR_COUNT = int(1e3)

g_threads = 9 # Set 1 for single thread

EXT_CAPTION = ".caption"
EXT_TAR = ".tar"

# Directly write things to tar will be a lot more efficient then making *.txt.
# https://stackoverflow.com/questions/740820/python-write-string-directly-to-tarfile

# Since we are dealing TBs of data and Ms of records, get a proper workstation (e.g. X99), your notebook cannot handle this lol 
# Do not use row count!
# 250225: Count manually.
df_max_id = 6000000
# Do not forget ID counts from 1
captions_only = [None] * (df_max_id + 1)

print(f"Max ID in the dataset: {df_max_id}")

def dump_year(y):
    count = 0
    for m in range(1, 12 + 1):
        sm = str(m).zfill(2)
        dl_json = "{}/{}-{}_grouped{}".format(LOCAL_DIR, y, sm, EXT_JSONL)
        
        # This file not exist.
        if y == 2007 and m == 1:
            continue

        df = pd.read_json(path_or_buf=dl_json, lines=True)
        
        for row in df.itertuples():
            danbooru_post_id = int(row.id)

            #2502224: There is not much captions. Meanwhile it is so incomplete.
            rearranged_tags = [row.regular_summary, row.brief_summary] if row.response_finish_reason == "STOP" else [row.tags]
                
            must_exist = [tag for tag in rearranged_tags if tag]

            #250224: There are many \n which will break kohyas trainer's wildcard.
            caption = " ".join(must_exist).replace("\n","").replace("\r","")

            captions_only[danbooru_post_id] = caption

            count = count + 1

    return count
        
res_dump_tags = thread_map(dump_year, range(2007, 2024 + 1), max_workers=g_threads, desc="dumping caption in year", position=0)

print(f"Tags found: {sum(res_dump_tags)}")
       
# May throw (e.g. os.Error)
def dump_tar(mod_1e3):
    subfolder = str(mod_1e3).zfill(4)
    tf = f"{TAGS_FOLDER}/{subfolder}{EXT_TAR}"
    with tarfile.open(tf, "w") as tar:
        for i in range(mod_1e3, df_max_id + 1, TOTAL_TAR_COUNT):
            tag = captions_only[i]
            if tag:            
                # This is tricky: str default in utf-8, meanwhile file size are in bytes = 8bits
                info = tarfile.TarInfo(f'{i}{EXT_CAPTION}')        
                content = bytes(tag, 'utf-8')
                b = BytesIO(content)
                info.size = len(content)
                tar.addfile(info, b)
    return tf

Path(TAGS_FOLDER).mkdir(parents=True, exist_ok=True)
res_dump_tar = thread_map(dump_tar, range(TOTAL_TAR_COUNT), max_workers=g_threads)

print(f"Files written: {len(res_dump_tar)}")