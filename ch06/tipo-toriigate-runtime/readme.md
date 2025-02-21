# Notes on making NLP captions from TIPO and Minthy/ToriiGate-v0.4-7B #

- TIPO here points to an [undisclosed dataset](https://discord.com/channels/1027129024054575174/1027407524334411816/1331702641285398529). The gated public version is [KBlueLeaf/danbooru2023-metadata-database](https://huggingface.co/datasets/KBlueLeaf/danbooru2023-metadata-database). *There are 480k delta to my current 2024 set, so I need to think about how to blend 2 approaches.*

- "ToriiGate" points to directly using [this model](https://huggingface.co/Minthy/ToriiGate-v0.4-7B) for caption generation. I will avoid generating files inplace, maybe using the `meta_cap_dd.json` for index tracing, then merge the `meta_lat.json`, then finally generate `1ktar.tar` inplace.

- The [HF repo](https://huggingface.co/Minthy/ToriiGate-v0.4-7B) do not mention how exactly to run the model. It requires some understanding on using [the pretrained model](https://huggingface.co/Qwen/Qwen2-VL-7B).

## Extracting captions from danbooru2023 parquet ##

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
merging json files: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████| 8005010/8005010 [00:37<00:00, 211000.01it/s] 
ids: 8005010, missing tags: 0, missing caption: 479366, missing latent: 0
writing OUTPUT_JSON
writing MISSING_JSON
Merge complete.
```

- [From the experience of kohyas trainer], line seperaters should be trimmed (I have done it at my side), to enable "pick caption or tags", or "blend them all".

```log
python patch_line_sep.py --in_json "/run/media/user/Intel P4510 3/danbooru2024-webp-4Mpixel/meta_lat_has_sep.json" --out_json "/run/media/user/Intel P4510 3/danbooru2024-webp-4Mpixel/meta_lat.json"
patching entries: 100%|████████████████████████████████████████████████████████████████████████████████████████████████| 8005010/8005010 [00:09<00:00, 821429.68it/s]
writing to out_json
Patch complete.
```

## ToriiGate 0.4: Transformers approach ##

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

## ToriiGate 0.4: EXL2 approach ##

- *Would be faster.* But need rewrite codes.

- [Model path.](https://huggingface.co/Minthy/ToriiGate-v0.4-7B-exl2-8bpw) (exl2)

- [Compatable with huggingface API.](https://python.langchain.com/docs/integrations/llms/exllamav2/)

- [Explit set CUDA_VISIBLE_DEVICES to assign GPU.](https://github.com/turboderp-org/exllamav2/issues/349)

- [Requires Ampere GPU or later](https://github.com/turboderp-org/exllamav2/issues/480)

- [flash-attention wheels](https://huggingface.co/lldacing/flash-attention-windows-wheel/tree/main), [triton wheels](https://huggingface.co/madbuda/triton-windows-builds/tree/main)

```sh
conda create -n exl2-env python=3.12
conda activate exl2-env
pip install torch==2.5.1 torchvision==0.20.1 xformers --index-url https://download.pytorch.org/whl/cu124
#pip install https://github.com/turboderp-org/exllamav2/releases/download/v0.2.7/exllamav2-0.2.7+cu121.torch2.5.0-cp312-cp312-win_amd64.whl
pip install triton-3.0.0-cp312-cp312-win_amd64.whl
pip install -r exl_requirements.txt
#pip install flash-attn==2.5.7
pip install flash_attn-2.7.0.post2+cu124torch2.5.0cxx11abiFALSE-cp312-cp312-win_amd64.whl
pip install exllamav2-0.2.7+cu121.torch2.5.0-cp312-cp312-win_amd64.whl
pip install cheesechaser
```

```sh
python batch_nlp_caption_exl.py --parquet_path "F:/danbooru2024-webp-4Mpixel/metadata.parquet" --device "cuda:0" --model_local_path "C:/Users/User/.cache/huggingface/hub/models--Minthy--ToriiGate-v0.4-7B-exl2-8bpw/snapshots/db4ff9e988b09765c98d9ef5485afeb60a0054e6" --img_dir "F:/just_astolfo/_test/" --in_json "./test_ids.json" --out_json_good "./exl_good_8.json" --out_json_bad "./exl_bad_8.json"
```

- Speed comparasion: Control Test = 12-20s/it, **4bpw = 3-5s/it, 8bpw = 4.3-8.7s/it**. Tag quality: Tends to be general for 4bpw, however "grounding" helps.

- Notice that image embeddings are bundled with prompt generation. It will be **0.7-1.5s/it**. Can be minimalized with proper execution sequence (hint: trigger GC on function exit)

- However the (commited / reserved) system RAM usage is high. *Meanwhile GPU VRAM controller load is high.* Pay attention to VRAM temperature especially on RTX 3090. Sadly even I have lowered the VRAM frequency (-502Mhz to the left!), the VRAM is still power hungry, I need to set the power limit around 65% (225W / 350W) to make it barely runs with base clock (1395 Mhz). Setting it to 60% will stall at 900Mhz, making it 20% slower.

## ToriiGate 0.4: Manual editing invalid JSON strings and join the results together ##

- **Manual edit** the `meta_cap_2024_toriigate_bad_*.json` into  `meta_cap_2024_toriigate_edited_*.json`, then recaption into `meta_cap_2024_toriigate_fixed_*.json`, and finally merge them into a single `meta_lat.json`.

- Right now the observed frequency is aruond *1 in 6000*.

```log
> python parse_edited_json.py
Preparing the tagging database
Remaking captions from edited files: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 64/64 [00:00<00:00, 318.26it/s]
Dump complete.
```

## TIPO: Plan C ##

- *Need to hack for the NLP output.*

- [Sample code (claimed was DTG, so it is close to no docuement).](https://github.com/KohakuBlueleaf/KGen/blob/main/scripts/example.py)

## Merging the generated dataset back to current dataest ##

- First we make `meta_cap.json` by [merge_meta_caption.py](./merge_meta_caption.py). Notice that `meta_cap_2024_toriigate_fixed_*.json` may not exist for all 64 splits.

- After a few passes with a few manually created captions, finally I got the number right. There are 7.65 + 0.48 = 8.13M captions.

```log
>python merge_meta_caption.py
merge meta_cap.json
Keys count: 7827640 > 7652007
merging good json: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████| 70/70 [00:05<00:00, 11.93it/s]
Keys count: 8135996
merging fixed json:   0%|                                                                                                            | 0/70 [00:00<?, ?it/s]Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_2.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_3.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_4.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_15.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_29.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_32.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_34.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_36.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_42.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_44.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_50.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_56.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_58.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_61.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_62.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_64.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_65.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_66.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_67.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_68.json
Not extst (skip): F:/tipo-toriigate-runtime/split_files_fix/meta_cap_2024_toriigate_fixed_69.json
merging fixed json: 100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████| 70/70 [00:00<00:00, 5006.50it/s]
Keys count: 8136093 > 8136093
Outputing merged json.
Merge complete.
```

- (Optional) We split the `meta_cap.json` back to 1k `*.tar` again, by [convert_meta_to_tar.py](./convert_meta_to_tar.py). You can skip this when using Kohyas along with `meta_lat.json`.

```log
python convert_meta_to_tar.py
Reading source JSON
Keys count: 8136011
max id: 8360499
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 1000/1000 [07:32<00:00,  2.21it/s]
Files written: 1000
```

- For file based operation in Kohyas (maybe other trainers also), "captions" are usually saved as `*.caption` instead of `*.txt`, which prefers to be text. It is optional in program layer, however this will aligns to the online docuements.

- Finally we merge again with [merge_tag_and_caption_to_meta.py](./merge_tag_and_caption_to_meta.py). The result will be **14GB**.

```log
>python merge_tag_and_caption_to_meta.py
loading JSON_ID
loading JSON_TAGS
loading JSON_CAPTION
loading JSON_LATENT
start merging
merging json files: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████| 8005010/8005010 [00:51<00:00, 155076.84it/s]
ids: 8005010, missing tags: 0, missing caption: 0, missing latent: 0
writing OUTPUT_JSON
writing MISSING_JSON
Merge complete.
```

- *Extract the Astolfo 6k test dataset again, and move back to the finetune rabbit hole.

```log
>python merge_tag_and_caption_to_meta.py
loading JSON_ID
loading JSON_TAGS
loading JSON_CAPTION
loading JSON_LATENT
start merging
merging json files: 100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████| 6224/6224 [00:00<00:00, 160243.99it/s]
ids: 6224, missing tags: 0, missing caption: 0, missing latent: 0
writing OUTPUT_JSON
writing MISSING_JSON
Merge complete.
```