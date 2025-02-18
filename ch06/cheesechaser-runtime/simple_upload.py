import os.path
from huggingface_hub import HfApi

# Notice that the 1ktar is actually inside latents_vae_sdxl/latents. "/latents" are appended for upload_large_folder.
LOCAL_TAR_FOLDER = "H:/danbooru2024-webp-4Mpixel/tmp"
HF_TAR_FOLDER = "captions"

HF_REPO_ID = "6DammK9/danbooru2024-captions-1ktar"
HF_REPO_TYPE = "dataset"

TOTAL_TAR_COUNT = int(1e3)
EXT_TAR = ".tar"

#https://huggingface.co/docs/huggingface_hub/guides/upload
api = HfApi()

if True:
    first_file = f"{LOCAL_TAR_FOLDER}/{HF_TAR_FOLDER}/0000{EXT_TAR}"
    if os.path.exists(first_file):
        api.upload_large_folder(
            folder_path=LOCAL_TAR_FOLDER,
            repo_id=HF_REPO_ID,
            repo_type=HF_REPO_TYPE,
            allow_patterns=f"*{EXT_TAR}",
        )
    else:
        raise Exception(f"Move files and make the first file visible: {first_file}")

# It hangs
if False:
    api.upload_folder(
        folder_path=LOCAL_TAR_FOLDER,
        path_in_repo=HF_TAR_FOLDER,
        repo_id=HF_REPO_ID,
        repo_type=HF_REPO_TYPE,
        allow_patterns=f"*{EXT_TAR}",
    )

# O(N) commits, bad
if False:
    for mod_1e3 in range(TOTAL_TAR_COUNT):
        subfolder = str(mod_1e3).zfill(4)
        
        local_tar = f"{LOCAL_TAR_FOLDER}/{subfolder}{EXT_TAR}"
        hf_tar = f"{HF_TAR_FOLDER}/{subfolder}{EXT_TAR}"

        api.upload_file(
            path_or_fileobj=local_tar,
            path_in_repo=hf_tar,
            repo_id=HF_REPO_ID,
            repo_type=HF_REPO_TYPE,
        )