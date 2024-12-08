# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

import tarfile
from io import BytesIO
from pathlib import Path

import pandas as pd

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

df = pd.read_parquet('./metadata.parquet')

TAGS_FOLDER = "F:/tags"

TOTAL_TAR_COUNT = int(1e3)

g_threads = 48 # Set 1 for single thread

EXT_TXT = ".txt"
EXT_TAR = ".tar"

# Directly write things to tar will be a lot more efficient then making *.txt.
# https://stackoverflow.com/questions/740820/python-write-string-directly-to-tarfile

# Since we are dealing TBs of data and Ms of records, get a proper workstation (e.g. X99), your notebook cannot handle this lol 
# Do not use row count!
df_max_id = df.index.max()
# Do not forget ID counts from 1
captions_only = [None] * (df_max_id + 1)

print(f"Max ID in the dataset: {df_max_id}")

# Multi threads needs packing parameters, so it will be a bit counter intuitive. Equivalent to "for row in df.itertuples()"
def dump_tags(row):
    #AngelBottomless: df.set_index has been applied on field "id" (so it is hidden in HF online preview)
    #This is never in ascending order! The actual df is in chronological order! You can find the hint in FFFF.json.
    danbooru_post_id = int(row.Index)

    #In 2412, khoyas-ss should handle well
    #tag = row.tag_string.replace(" ",",")
    rearranged_tags = [row.tag_string_character, row.tag_string_copyright, row.tag_string_artist, row.tag_string_general, row.tag_string_meta]
    must_exist = [tag for tag in rearranged_tags if tag]

    #A bit philosophical and controversal: I don't even add year tag here. 
    #Danbooru has defined styles and years like "2000s" and "2024", which has stated explictly "do not link with upload time". 
    #Disrupting the tag definiton will cause AI/ML problems, which AI cannot learn contradictions.
    #If the final destination is learning "some artist in some topic in some time window", please make embedding or train a LoRA.
    tag = " ".join(must_exist).replace(" ",", ")

    captions_only[danbooru_post_id] = tag

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