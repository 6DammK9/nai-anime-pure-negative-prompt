# install necessary packages, you can choose pyarrow or fastparquet
#%pip install pandas pyarrow

from pathlib import Path
import tarfile
import os.path
import shutil
import glob

from tqdm.auto import tqdm
import pandas as pd
tqdm.pandas() 

df = pd.read_parquet('./metadata.parquet')

TAGS_FOLDER = "F:/tags"

for row in tqdm(df.itertuples(), desc="Extracting Tags", position=0):
    
    #AngelBottomless: df.set_index has been applied on field "id" (so it is hidden in HF online preview)
    media_asset_id = row.Index
    #I don't know why the source alignment is 1e3 instead of 1e4.
    subfolder = str(int(media_asset_id % 1e3)).zfill(4)
    tfp = "{}/{}/{}.txt".format(TAGS_FOLDER, subfolder, media_asset_id)
    
    #In 2412, khoyas-ss should handle well
    #tag = row.tag_string.replace(" ",",")
    rearranged_tags = [row.tag_string_character, row.tag_string_copyright, row.tag_string_artist, row.tag_string_general, row.tag_string_meta]
    must_exist = [tag for tag in rearranged_tags if tag]

    #A bit philosophical and controversal: I don't even add year tag here. 
    #Danbooru has defined styles and years like "2000s" and "2024", which has stated explictly "do not link with upload time". 
    #Disrupting the tag definiton will cause AI/ML problems, which AI cannot learn contradictions.
    #If the final destination is learning "some artist in some topic in some time window", please make embedding or train a LoRA.
    tag = " ".join(must_exist).replace(" ",", ")
    
    Path("{}/{}".format(TAGS_FOLDER,subfolder)).mkdir(parents=True, exist_ok=True)
    with open(tfp, 'w', encoding="utf-8") as f:
        f.write(tag)
       
#No throw (it takes 12 hours!)
for i in tqdm(range(int(1e3)), desc="Making *.tar Files", position=0):
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