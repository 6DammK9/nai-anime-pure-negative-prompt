---
license: mit
task_categories:
- image-classification
- zero-shot-image-classification
- text-to-image
language:
- en
- ja
tags:
- art
- anime
- not-for-all-audiences
size_categories:
- 1M<n<10M
annotations_creators:
- no-annotation
source_datasets:
- e621
---

# E621 2024 captions only in 1k tar #

- Raw captions jointed from [lodestones/e621-captions](https://huggingface.co/datasets/lodestones/e621-captions/tree/main)

- It doesn't align to any dataset yet.

- `meta_cap.json` has been provided [in compressed format](https://huggingface.co/datasets/6DammK9/e621_2024-captions-1ktar/blob/main/meta_cap.tar.gz) if you want to train with kohyas triner. Currently I'm trying to merge this with [my 2024 version](https://huggingface.co/datasets/6DammK9/e621_2024-latents-sdxl-1ktar/blob/main/meta_lat.tar.gz).

## Core logic ##

- [The script building this 1ktar](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/e621-captions/dump_captions_json.py)

- There is not much choice, I don't have GPU to run for 1M captions with VLM so I just "take it or leave it".

```py
rearranged_tags = [row.regular_summary, row.brief_summary] if row.response_finish_reason == "STOP" else [row.tags]
must_exist = [tag for tag in rearranged_tags if tag]
caption = " ".join(must_exist).replace("\n","").replace("\r","")
```

## How to build the "dataset" with speed ##

- Refer to [the tags-1ktar repo](https://huggingface.co/datasets/6DammK9/e621_2024-tags-1ktar).

- *This repo is still in develeopment.* [My current task of building the dataset for "pretraining".](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/readme.md)

## Warning: Many records here are not NLP captions actally ##

- I don't want to spend weeks to run the VLM again.

- There should be almost 1M of records are tags. (Here is a lot more than 0.18M).

```log
>python merge_tag_and_caption_to_meta.py
loading JSON_ID
loading JSON_TAGS
loading JSON_CAPTION
loading JSON_LATENT
start merging
merging json files: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4441660/4441660 [00:27<00:00, 163941.22it/s]
ids: 4441660, missing tags: 0, missing caption: 178162, missing latent: 0
writing OUTPUT_JSON
writing MISSING_JSON
Merge complete.
```
