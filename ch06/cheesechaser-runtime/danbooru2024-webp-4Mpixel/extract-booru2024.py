import tarfile
import os.path

from tqdm.auto import tqdm
from tqdm.contrib.concurrent import thread_map

# File structure should be "image/FFFF.tar/FFFFFFF.png" > "image/FFFFFFF.png"
# Fine Tune in kohyas_ss is a bit strict in methodology.
# https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904

SRC_TAR_FOLDER_WEBP = "H:/test/images"
SRC_TAR_FOLDER_TXT = "H:/test/tags"
DST_TAR_FOLDER = "H:/danbooru2024-webp-4Mpixel/kohyas_finetune_0000"

TAR_COUNT = 10 # int(1e3)

file_delta = 0
extracted_members = 0

EXT_WEBP = ".webp"
EXT_TXT = ".txt"
EXT_TAR = ".tar"

R_WILDCARD = "r:*"

def file_in_list(f, l, ext):
    return os.path.basename(f).replace(ext, "") in l

def names_in_tar(folder, subfolder):
    tf = "{}/{}{}".format(folder, subfolder, EXT_TAR)
    with tarfile.open(tf, R_WILDCARD) as f:
        return f.getnames(), f.getmembers()

def extract_intersected_files_only(folder, subfolder, target_members):
    tf = "{}/{}{}".format(folder, subfolder, EXT_TAR)
    with tarfile.open(tf, R_WILDCARD) as f:       
        f.extractall(DST_TAR_FOLDER, members=target_members, filter="data")    

#res_cmp = thread_map(exec_cmp, [(pab, ofp0) for pab in cmp_mapping[0][1]], max_workers=g_threads)

for i in tqdm(range(TAR_COUNT), desc="Extracting *.tar Files", position=0):
    subfolder = str(i).zfill(4)

    #I don't know if trainer can detect missing image / caption, so I extract strictly in intersected entries
    found_webp, members_webp = names_in_tar(SRC_TAR_FOLDER_WEBP, subfolder)
    found_txt, members_txt = names_in_tar(SRC_TAR_FOLDER_TXT, subfolder)
    
    webp_list = [os.path.basename(w).replace(EXT_WEBP, "") for w in found_webp]
    txt_list = [os.path.basename(t).replace(EXT_TXT, "") for t in found_txt]

    target_members_webp = [m for m in members_webp if file_in_list(m.name, txt_list, EXT_WEBP)]
    target_members_txt = [m for m in members_txt if file_in_list(m.name, webp_list, EXT_TXT)]

    extracted_members = extracted_members + len(target_members_webp) + len(target_members_txt)
    file_delta = file_delta + abs(len(found_txt) - len(found_webp))

    extract_intersected_files_only(SRC_TAR_FOLDER_WEBP, subfolder, target_members_webp)
    extract_intersected_files_only(SRC_TAR_FOLDER_TXT, subfolder, target_members_txt)    
    
print("Extracted: {} pairs".format(int(extracted_members / 2)))
print("Delta: {} files".format(file_delta))