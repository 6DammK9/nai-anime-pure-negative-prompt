# Notes on making NLP captions from Minthy/ToriiGate-v0.4-7B #

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

## EXL2 approach ##

- *Would be faster.* But need rewrite codes.

- [Model path.](https://huggingface.co/Minthy/ToriiGate-v0.4-7B-exl2-8bpw) (exl2)

- [Compatable with huggingface API.](https://python.langchain.com/docs/integrations/llms/exllamav2/)

- [Explit set CUDA_VISIBLE_DEVICES to assign GPU.](https://github.com/turboderp-org/exllamav2/issues/349)

- [Requires Ampere GPU or later](https://github.com/turboderp-org/exllamav2/issues/480)

= [flash-attention wheels](https://huggingface.co/lldacing/flash-attention-windows-wheel/tree/main), [triton wheels](https://huggingface.co/madbuda/triton-windows-builds/tree/main)

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

- However the (commited / reserved) system RAM usage is high. *Meanwhile GPU VRAM controller load is high.* Pay attention to VRAM temperature especially on RTX 3090.

## TIPO approach ##

- *Need to hack for the NLP output.*

- [Sample code (claimed was DTG, so it is close to no docuement).](https://github.com/KohakuBlueleaf/KGen/blob/main/scripts/example.py)