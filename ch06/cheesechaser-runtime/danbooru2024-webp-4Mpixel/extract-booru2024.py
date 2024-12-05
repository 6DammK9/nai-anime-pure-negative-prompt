from pathlib import Path
import tarfile
import os.path
import shutil
import glob

from tqdm.auto import tqdm
import pandas as pd
tqdm.pandas() # register progress_apply

# File structure should be "image/FFFF.tar/FFFFFFF.png" > "image/FFFFFFF.png"
# Fine Tune in khoyas_ss is a bit strict in methodology.
# https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904

SRC_TAR_FOLDER_WEBP = "G:/raw_files/images"
SRC_TAR_FOLDER_TXT = "G:/tags"
DST_TAR_FOLDER = "H:/danbooru2024-webp-4Mpixel/khoyas_finetune"

TAR_COUNT = 1 #int(1e4)

for i in tqdm(range(TAR_COUNT), desc="Extracting *.tar Files", position=0):
    subfolder = str(i).zfill(4)
    tf_webp = "{}/{}.tar".format(SRC_TAR_FOLDER_WEBP, subfolder)
    with tarfile.open(tf_webp, "r:*") as f:
        f.extractall(DST_TAR_FOLDER, filter="data")
    tf_txt = "{}/{}.tar".format(SRC_TAR_FOLDER_TXT, subfolder)
    with tarfile.open(tf_txt, "r:*") as f:
        f.extractall(DST_TAR_FOLDER, filter="data")
