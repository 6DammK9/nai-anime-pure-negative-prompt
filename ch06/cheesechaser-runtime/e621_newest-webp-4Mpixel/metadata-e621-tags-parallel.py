# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

import tarfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# Notes: Raw parquet has different schemas, this is the merged one
# Meanwhile it is no more hidden index field.
df = pd.read_parquet('./e621-merged.parquet')

TAGS_FOLDER = "F:/tags2"

TOTAL_TAR_COUNT = int(1e3)

g_threads = 48 # Set 1 for single thread

EXT_TXT = ".txt"
EXT_TAR = ".tar"

# Directly write things to tar will be a lot more efficient then making *.txt.
# https://stackoverflow.com/questions/740820/python-write-string-directly-to-tarfile

# Somehow the set_index doesn't work!
df_max_id = df["id"].max()
# Do not forget ID counts from 1
captions_only = [None] * (df_max_id + 1)

print(f"Max ID in the dataset: {df_max_id}")

# Multi threads needs packing parameters, so it will be a bit counter intuitive. Equivalent to "for row in df.itertuples()"
def dump_tags(row):
    # Folow what danbooru case does.
    danbooru_post_id = int(row.id)

    # There is nothing to do.
    captions_only[danbooru_post_id] = row.tag_string

    return danbooru_post_id

# The return value is arbitary. itertuples() is an iterator and thread_map will beautifully .
res_dump_tags = thread_map(dump_tags, df.itertuples(), max_workers=g_threads)

print(f"Tags found: {len(res_dump_tags)}")
       
# May throw (e.g. os.Error)
def dump_tar(mod_1e3):
    subfolder = str(mod_1e3).zfill(4)
    tf = f"{TAGS_FOLDER}/{subfolder}{EXT_TAR}"
    with tarfile.open(tf, "w") as tar:
        for i in range(mod_1e3, df_max_id + 1, TOTAL_TAR_COUNT):
            tag = captions_only[i]
            if tag:            
                # This is tricky: str default in utf-8, meanwhile file size are in bytes = 8bits
                info = tarfile.TarInfo(f'{i}{EXT_TXT}')        
                content = bytes(tag, 'utf-8')
                b = BytesIO(content)
                info.size = len(content)
                tar.addfile(info, b)
    return tf

Path(TAGS_FOLDER).mkdir(parents=True, exist_ok=True)
res_dump_tar = thread_map(dump_tar, range(TOTAL_TAR_COUNT), max_workers=g_threads)

print(f"Files written: {len(res_dump_tar)}")