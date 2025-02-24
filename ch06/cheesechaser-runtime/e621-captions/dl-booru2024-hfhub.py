from huggingface_hub import hf_hub_download

REPO_ID = "lodestones/e621-captions"
REPO_TYPE = "dataset"
#REPO_DIR = ["images"] #root
REPO_DIR_FORMAT = [".jsonl"]

LOCAL_DIR = "C:/temp/e621-captions" #Anywhere you want.

def dl_single_file(filename):
    #print(filename)
    #This is no thorw and have progress bar, should be safe.
    hf_hub_download(repo_id=REPO_ID, repo_type=REPO_TYPE, filename=filename, local_dir=LOCAL_DIR)

def dl_all():
    #Brute force!
    for y in range(2007, 2024 + 1):
        for m in range(1, 12 + 1):
            sm = str(m).zfill(2)
            for r_df in REPO_DIR_FORMAT:
                dl_json = "{}-{}_grouped{}".format(y,sm,r_df)
                try:
                    dl_single_file(dl_json)
                except:
                    pass


if __name__ == "__main__":
    dl_all()

