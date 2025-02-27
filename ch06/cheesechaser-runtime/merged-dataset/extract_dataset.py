import tarfile
import os.path

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# Assumed that everything is completed. It is just a simple script to extract everything (to ramdisk haha).

SRC_TAR_FOLDER_DANBOORU = "/run/media/user/Intel P4510 3/danbooru2024-webp-4Mpixel/kohyas_finetune"
DST_TAR_FOLDER_DANBOORU = "/dev/shm/astolfo_xl/dataset/danbooru"
SRC_TAR_FOLDER_E621 = "/run/media/user/Intel P4510 3/e621_newest-webp-4Mpixel/kohyas_finetune"
DST_TAR_FOLDER_E621 =  "/dev/shm/astolfo_xl/dataset/e621"

EXTRACT_NPZ_DANBOORU = True
EXTRACT_NPZ_E621 = True

TAR_COUNT = int(1e3)

g_threads = 48

file_delta = 0

EXT_WEBP = ".webp"
EXT_TXT = ".txt"
EXT_TAR = ".tar"
EXT_NPZ = ".npz"

R_WILDCARD = "r:*"

def file_in_list(f, l, ext):
    return os.path.basename(f).replace(ext, "") in l

def names_in_tar(folder, subfolder):
    tf = f"{folder}/{subfolder}{EXT_TAR}"
    with tarfile.open(tf, R_WILDCARD) as f:
        return f.getnames(), f.getmembers()

def extract_intersected_files_only(folder, subfolder, target_members, dst):
    tf = f"{folder}/{subfolder}{EXT_TAR}"
    with tarfile.open(tf, R_WILDCARD) as f:       
        f.extractall(dst, members=target_members, filter="data")    

def extract_single_pair(mod_1e3):
    subfolder = str(mod_1e3).zfill(4)

    # Extract all
    found_npz_danbooru, members_npz_danbooru = names_in_tar(SRC_TAR_FOLDER_DANBOORU, subfolder)
    found_npz_e621, members_npz_e621 = names_in_tar(SRC_TAR_FOLDER_E621, subfolder)

    file_delta = len(found_npz_danbooru) + len(found_npz_e621)

    extract_intersected_files_only(SRC_TAR_FOLDER_DANBOORU, subfolder, members_npz_danbooru, DST_TAR_FOLDER_DANBOORU)  
    extract_intersected_files_only(SRC_TAR_FOLDER_E621, subfolder, members_npz_e621, DST_TAR_FOLDER_E621)  

    return file_delta
    
res_extract = thread_map(extract_single_pair, range(TAR_COUNT), max_workers=g_threads)

print(f"Extracted: {len(res_extract)} iters")
print(f"Delta: {sum(res_extract)} files")