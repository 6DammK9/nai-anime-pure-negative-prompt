sample = 'python batch_nlp_caption_exl.py --parquet_path "F:/danbooru2024-webp-4Mpixel/metadata.parquet" --device "cuda:{}" --prompt_threads 6 --model_local_path "C:/Users/User/.cache/huggingface/hub/models--Minthy--ToriiGate-v0.4-7B-exl2-8bpw/snapshots/db4ff9e988b09765c98d9ef5485afeb60a0054e6" --img_dir "F:/danbooru2024-webp-4Mpixel/kohyas_finetune/" --in_json "F:/tipo-toriigate-runtime/split_files/missing_{}.json" --out_json_good "F:/tipo-toriigate-runtime/split_files/meta_cap_2024_toriigate_good_{}.json" --out_json_bad "F:/tipo-toriigate-runtime/split_files/meta_cap_2024_toriigate_bad_{}.json"' 
for cuda in range(4):
    s = ""
    for missing in range(20 + cuda, 64, 4):
        s = s + sample.format(cuda,missing,missing,missing) + "\n"
    with open("./forreal_{}.cmd".format(cuda), "w") as outfile:
        outfile.write(s)