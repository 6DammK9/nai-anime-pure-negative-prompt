# Notes on making NLP captions from TIPO and Minthy/ToriiGate-v0.4-7B #

- TIPO here points to an [undisclosed dataset](https://discord.com/channels/1027129024054575174/1027407524334411816/1331702641285398529). The gated public version is [KBlueLeaf/danbooru2023-metadata-database](https://huggingface.co/datasets/KBlueLeaf/danbooru2023-metadata-database). *There are 480k delta to my current 2024 set, so I need to think about how to blend 2 approaches.*

- "ToriiGate" points to directly using [this model](https://huggingface.co/Minthy/ToriiGate-v0.4-7B) for caption generation. I will avoid generating files inplace, maybe using the `meta_cap_dd.json` for index tracing, then merge the `meta_lat.json`, then finally generate `1ktar.tar` inplace.

- The [HF repo](https://huggingface.co/Minthy/ToriiGate-v0.4-7B) do not mention how exactly to run the model. It requires some understanding on using [the pretrained model](https://huggingface.co/Qwen/Qwen2-VL-7B).

- The `conda environment` can be reused. However pay attention to the library versions.

```sh
conda activate kohyas-env
# pip install transformers==4.48.2
pip install -U transformers 
pip install qwen-vl-utils
pip install cheesechaser
```

- Dumping captions from danbooru2023 is easy. Notice that I have modified the sequence, which artist name is mentioned first.

```log
> python metadata-booru2023-meta-parallel.py
dumping tags: 7827640it [00:26, 296151.42it/s]
Tags found: 7827640
Dump complete.
```
- Merging the existing captions to `meta_lat.json` is also easy.

```log
> python merge_tag_and_caption_to_meta.py
loading JSON_ID
loading JSON_TAGS
loading JSON_CAPTION
loading JSON_LATENT
start merging
merging json files: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8005010/8005010 [00:37<00:00, 211000.01it/s] 
ids: 8005010, missing tags: 0, missing caption: 479366, missing latent: 0
writing OUTPUT_JSON
writing MISSING_JSON
Merge complete.
```

- However the "2024 exclusive" 0.5M captions is hard. **It will spend days to generate.** Meanwhile the output of the caption model is inconsistint. I have manually used templates to mention artists. Currently it is in progress.

```log
> python batch_nlp_caption.py
Preparing the tagging database
Preparing the targeted ids
First id: 7866720
Preparing caption model
`Qwen2VLRotaryEmbedding` can now be fully parameterized by passing the model config through the `config` argument. All other arguments will be removed in v4.46
Loading checkpoint shards: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:27<00:00,  6.96s/it] 
preparing prompts
making prompt messages: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [00:00<00:00, 277.78it/s] 
sorting
making caption: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 10/10 [01:57<00:00, 11.78s/it] 
Outputing JSON
Dump complete.
```

- For multiGPU support, first split the input and output JSON:

```sh
python split_missing.py
```

- After rewriting the scripts, use process arguement:

```sh
python batch_nlp_caption.py --parquet_path "H:/danbooru2024-webp-4Mpixel/metadata.parquet" --device "cuda:0" --fp16 --prompt_threads 48 --img_dir "H:/danbooru2024-webp-4Mpixel/kohyas_finetune/" --in_json "./missing.json" --out_json_good "./meta_cap_2024_toriigate_good.json" --out_json_bad "./meta_cap_2024_toriigate_bad.json" --start_index 3075 --end_index 3079
```
