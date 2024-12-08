import tarfile
import os.path

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

# File structure should be "image/FFFF.tar/FFFFFFF.png" > "image/FFFFFFF.png"
# Fine Tune in khoyas_ss is a bit strict in methodology.
# https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904

# Notice that it is 2 datasources.
SRC_TAR_FOLDER_WEBP1 = "G:/original"
SRC_TAR_FOLDER_WEBP2 = "G:/images"
SRC_TAR_FOLDER_TXT = "G:/tags2"
DST_TAR_FOLDER = "H:/e621_newest-webp-4Mpixel/khoyas_finetune"

TAR_COUNT = int(1e3)

g_threads = 48

file_delta = 0
extracted_members = 0

EXT_WEBP = ".webp"
EXT_TXT = ".txt"
EXT_TAR = ".tar"

R_WILDCARD = "r:*"

def file_in_list(f, l, ext):
    return os.path.basename(f).replace(ext, "") in l

def names_in_tar(folder, subfolder, tarfile_prefix):
    tf = f"{folder}/{tarfile_prefix}{subfolder}{EXT_TAR}"
    with tarfile.open(tf, R_WILDCARD) as f:
        return f.getnames(), f.getmembers()

def extract_intersected_files_only(folder, subfolder, target_members, tarfile_prefix):
    tf = f"{folder}/{tarfile_prefix}{subfolder}{EXT_TAR}"
    with tarfile.open(tf, R_WILDCARD) as f:       
        f.extractall(DST_TAR_FOLDER, members=target_members, filter="data")    

def extract_single_pair(mod_1e3):
    subfolder = str(mod_1e3).zfill(4)

    # I don't know if trainer can detect missing image / caption, so I extract strictly in intersected entries
    # Meanwhile I prefer just hardcode it, I don't think the code will explode: Who know how many datasets exist next year?
    found_webp1, members_webp1 = names_in_tar(SRC_TAR_FOLDER_WEBP1, subfolder, "data-")
    found_webp2, members_webp2 = names_in_tar(SRC_TAR_FOLDER_WEBP2, subfolder, "")
    found_txt, members_txt = names_in_tar(SRC_TAR_FOLDER_TXT, subfolder, "")
    
    webp_list1 = [os.path.basename(w).replace(EXT_WEBP, "") for w in found_webp1]
    webp_list2 = [os.path.basename(w).replace(EXT_WEBP, "") for w in found_webp2]
    txt_list = [os.path.basename(t).replace(EXT_TXT, "") for t in found_txt]

    target_members_webp1 = [m for m in members_webp1 if file_in_list(m.name, txt_list, EXT_WEBP)]
    target_members_webp2 = [m for m in members_webp2 if file_in_list(m.name, txt_list, EXT_WEBP)]
    target_members_txt1 = [m for m in members_txt if file_in_list(m.name, webp_list1, EXT_TXT)]
    target_members_txt2 = [m for m in members_txt if file_in_list(m.name, webp_list2, EXT_TXT)]

    #extracted_members = extracted_members + len(target_members_webp) + len(target_members_txt)
    file_delta = abs(len(found_txt) - len(found_webp1) - len(found_webp2))

    extract_intersected_files_only(SRC_TAR_FOLDER_WEBP1, subfolder, target_members_webp1, "data-")
    extract_intersected_files_only(SRC_TAR_FOLDER_WEBP2, subfolder, target_members_webp2, "")
    extract_intersected_files_only(SRC_TAR_FOLDER_TXT, subfolder, target_members_txt1 + target_members_txt2, "")   

    return file_delta
    
res_extract = thread_map(extract_single_pair, range(TAR_COUNT), max_workers=g_threads)

print(f"Extracted: {len(res_extract)} iters")
print(f"Delta: {sum(res_extract)} files")