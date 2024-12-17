# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

import pandas as pd
from pathlib import Path
from tqdm import tqdm
import shutil

FULL_DATASET = "H:/danbooru2024-webp-4Mpixel/kohyas_finetune"

JUST_ASTOLFO = "H:/just_astolfo/kohyas_finetune"

EXT_WEBP = ".webp"
EXT_TXT = ".txt"
EXT_TAR = ".tar"

df = pd.read_parquet('metadata.parquet', columns=['id', 'tag_string'])

# Do query whatever you want                     
subdf = df[df['tag_string'].str.contains('astolfo')]
ids = subdf.index.tolist()

print(f"{len(ids)} pairs to be copied.")

Path(JUST_ASTOLFO).mkdir(parents=True, exist_ok=True)

for _id in tqdm(ids, desc="Copying image-caption pairs", position=0):

    src_webp = f"{FULL_DATASET}/{_id}{EXT_WEBP}"
    src_txt = f"{FULL_DATASET}/{_id}{EXT_TXT}"
    dst_webp = f"{JUST_ASTOLFO}/{_id}{EXT_WEBP}"
    dst_txt = f"{JUST_ASTOLFO}/{_id}{EXT_TXT}"
    
    res1 = shutil.copyfile(src_webp, dst_webp)
    res2 = shutil.copyfile(src_txt, dst_txt)