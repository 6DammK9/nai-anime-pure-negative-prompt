import tarfile
import os.path

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# File structure should be "image/FFFF.tar/FFFFFFF.png" > "image/FFFFFFF.png"
# Fine Tune in kohyas_ss is a bit strict in methodology.
# https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904

SRC_TAR_FOLDER_WEBP = "G:/raw_files/images"
SRC_TAR_FOLDER_TXT = "G:/tags"
SRC_TAR_FOLDER_NPZ = "G:/latents"
DST_TAR_FOLDER = "H:/danbooru2024-webp-4Mpixel/kohyas_finetune"

EXTRACT_WEBP = True
EXTRACT_TXT = True
EXTRACT_NPZ = True

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

def extract_intersected_files_only(folder, subfolder, target_members):
    tf = f"{folder}/{subfolder}{EXT_TAR}"
    with tarfile.open(tf, R_WILDCARD) as f:       
        f.extractall(DST_TAR_FOLDER, members=target_members, filter="data")    

def extract_single_pair(mod_1e3):
    subfolder = str(mod_1e3).zfill(4)

    #I don't know if trainer can detect missing image / caption, so I extract strictly in intersected entries
    found_webp, members_webp = names_in_tar(SRC_TAR_FOLDER_WEBP, subfolder)
    found_txt, members_txt = names_in_tar(SRC_TAR_FOLDER_TXT, subfolder)
    found_npz, members_npz = names_in_tar(SRC_TAR_FOLDER_NPZ, subfolder)
    
    webp_list = [os.path.basename(w).replace(EXT_WEBP, "") for w in found_webp]
    txt_list = [os.path.basename(t).replace(EXT_TXT, "") for t in found_txt]
    npz_list = [os.path.basename(t).replace(EXT_NPZ, "") for t in found_npz]

    intersected_list = list(set(webp_list) & set(txt_list) & set(npz_list))

    target_members_webp = [m for m in members_webp if file_in_list(m.name, intersected_list, EXT_WEBP)]
    target_members_txt = [m for m in members_txt if file_in_list(m.name, intersected_list, EXT_TXT)]
    target_members_npz = [m for m in members_npz if file_in_list(m.name, intersected_list, EXT_NPZ)]

    file_delta = 0
    file_delta = file_delta + len(found_webp) - len(intersected_list)
    file_delta = file_delta + len(found_txt) - len(intersected_list)
    file_delta = file_delta + len(found_npz) - len(intersected_list)

    extract_intersected_files_only(SRC_TAR_FOLDER_WEBP, subfolder, target_members_webp)
    extract_intersected_files_only(SRC_TAR_FOLDER_TXT, subfolder, target_members_txt)  
    extract_intersected_files_only(SRC_TAR_FOLDER_NPZ, subfolder, target_members_npz)  

    return file_delta
    
res_extract = thread_map(extract_single_pair, range(TAR_COUNT), max_workers=g_threads)

print(f"Extracted: {len(res_extract)} iters")
print(f"Delta: {sum(res_extract)} files")