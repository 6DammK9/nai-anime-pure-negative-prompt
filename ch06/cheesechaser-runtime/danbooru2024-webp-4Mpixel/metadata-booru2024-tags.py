# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

from pathlib import Path
import tarfile
import os.path
import shutil
import glob

from tqdm.auto import tqdm
import pandas as pd
tqdm.pandas() # register progress_apply

# read parquet file
df = pd.read_parquet('./metadata.parquet')

#df_sample = df.head(5)

#print(df_sample)

#df_sample.to_json("metadata-sample.json")

#tag_string
#media_asset.id

#tag_string_general
#tag_string_character 
#tag_string_copyright
#tag_string_artist 
#tag_string_meta

#character > copyright > artist > general > meta

#1.webp
#1.text

#https://github.com/kohya-ss/sd-scripts/blob/main/docs/config_README-en.md#multi-line-captions

#df['tag_string'].str

TAGS_FOLDER = "F:/tags"

for row in tqdm(df.itertuples(), desc="Extracting Tags", position=0):
    #print(row)
    #media_asset.id = _37
    media_asset_id = row._37
    #I don't know why the source alignment is 1e3 instead of 1e4.
    subfolder = str(int(media_asset_id % 1e3)).zfill(4)
    tfp = "{}/{}/{}.txt".format(TAGS_FOLDER, subfolder, row._37)
    
    #In 2412, khoyas-ss should handle well
    #tag = row.tag_string.replace(" ",",")
    tag = " ".join([row.tag_string_character, row.tag_string_copyright, row.tag_string_artist, row.tag_string_general, row.tag_string_meta]).replace(" ",", ")
    
    Path("{}/{}".format(TAGS_FOLDER,subfolder)).mkdir(parents=True, exist_ok=True)
    with open(tfp, 'w', encoding="utf-8") as f:
        f.write(tag)
       
#No throw for df.head(5)
#I'll keep 1e4 here because I've made a mess
for i in tqdm(range(int(1e4)), desc="Making *.tar Files", position=0):
    subfolder = str(i).zfill(4)
    tf = "{}/{}.tar".format(TAGS_FOLDER, subfolder)
    tfd = "{}/{}".format(TAGS_FOLDER, subfolder)
    with tarfile.open(tf, "w") as tar:
        try:
            for fullpath in glob.iglob("{}/*.txt".format(tfd), recursive=False):
                tar.add(fullpath, arcname=os.path.basename(fullpath))        
        except:
            pass
    # Finally nuke the folder to reduce file entries (costly in developement)
    try:
        shutil.rmtree(tfd)
    except:
        pass