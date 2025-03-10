from huggingface_hub import hf_hub_download

REPO_ID = "NebulaeWis/e621-2024-webp-4Mpixel"
REPO_TYPE = "dataset"
REPO_DIR = ["original"] #"embs/SwinV2_v3"
REPO_DIR_FORMAT = [".json", ".tar"]

LOCAL_DIR = "H:/e621_old" #Anywhere you want.

def dl_single_file(filename):
    #print(filename)
    #This is no thorw and have progress bar, should be safe.
    hf_hub_download(repo_id=REPO_ID, repo_type=REPO_TYPE, filename=filename, local_dir=LOCAL_DIR)

def dl_all():
    #Brute force!
    for i in range(1000):
        suffix = str(i).zfill(4)
        for r_d in REPO_DIR:
            for r_df in REPO_DIR_FORMAT:
                dl_json = "{}/data-{}{}".format(r_d,suffix,r_df)
                dl_single_file(dl_json)


if __name__ == "__main__":
    dl_all()

