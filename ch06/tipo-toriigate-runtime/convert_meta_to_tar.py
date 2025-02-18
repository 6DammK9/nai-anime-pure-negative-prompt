import json
import tarfile
from io import BytesIO
from pathlib import Path

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

META_JSON = "H:/danbooru2024-webp-4Mpixel/meta_cap.json"

TAGS_FOLDER = "H:/danbooru2024-webp-4Mpixel/tags"
CAPTIONS_FOLDER = "H:/danbooru2024-webp-4Mpixel/captions"

TOTAL_TAR_COUNT = int(1e3)

g_threads = 32 # Set 1 for single thread

EXT_TXT = ".txt"
EXT_CAPTION = ".caption"
EXT_TAR = ".tar"

EXTRACT_TAGS = False
EXTRACT_CAPTIONS = True

# Refer to kohyas
KEY_TAGS = "tags"
KEY_CAPTIONS = "caption"

meta_data = {}
res_dump_tar = []

print("Reading source JSON")
with open(META_JSON, 'r') as file:
    meta_data = json.load(file)

print(f"Keys count: {len(list(meta_data.keys()))}")
       
max_id = max([int(k) for k in meta_data.keys()])

print(f"max id: {max_id}")
    
# May throw (e.g. os.Error)
def dump_contents(mod_1e3, ctx_folder, k, ext):
    subfolder = str(mod_1e3).zfill(4)
    tf = f"{ctx_folder}/{subfolder}{EXT_TAR}"
    with tarfile.open(tf, "w") as tar:
        for i in range(mod_1e3, max_id + 1, TOTAL_TAR_COUNT):
            si = str(i) #booru post id, align with upstream tasks
            if si in meta_data:
                if k in meta_data[si]:
                    txt = meta_data[si][k]
                
                    # This is tricky: str default in utf-8, meanwhile file size are in bytes = 8bits
                    info = tarfile.TarInfo(f'{si}{ext}')        
                    content = bytes(txt, 'utf-8')
                    b = BytesIO(content)
                    info.size = len(content)
                    tar.addfile(info, b)
    return tf

def dump_tags(mod_1e3):
    return dump_contents(mod_1e3, TAGS_FOLDER, KEY_TAGS, EXT_TXT)
    
def dump_captions(mod_1e3):
    return dump_contents(mod_1e3, CAPTIONS_FOLDER, KEY_CAPTIONS, EXT_CAPTION)

if EXTRACT_TAGS:
    Path(TAGS_FOLDER).mkdir(parents=True, exist_ok=True)
    res_dump_tar = res_dump_tar + thread_map(dump_tags, range(TOTAL_TAR_COUNT), max_workers=g_threads)

if EXTRACT_CAPTIONS:
    Path(CAPTIONS_FOLDER).mkdir(parents=True, exist_ok=True)
    res_dump_tar = res_dump_tar + thread_map(dump_captions, range(TOTAL_TAR_COUNT), max_workers=g_threads)

print(f"Files written: {len(res_dump_tar)}")