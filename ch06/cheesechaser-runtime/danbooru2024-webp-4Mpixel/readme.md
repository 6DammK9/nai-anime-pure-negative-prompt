# Danbooru 2024 tags only in 10k tar #

- Dedicated dataset to align [deepghs/danbooru2024-webp-4Mpixel](https://huggingface.co/datasets/deepghs/danbooru2024-webp-4Mpixel).

- How to use / why I create this: [my speedrun to build the dataset](https://github.com/6DammK9/nai-anime-pure-negative-prompt/tree/main/ch06/cheesechaser-runtime)

## How to build the "dataset" with speed ##

- *Get at least 4TB of storage, and around 75GB of RAM. Always make a venv / conda environment for each task.*

- (Optional) Download this directly: [metadata.parquet](https://huggingface.co/datasets/deepghs/danbooru2024-webp-4Mpixel/blob/main/metadata.parquet)

- Download all 10k tarfile with webp via [dl-booru2024-hfhub.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/danbooru2024-webp-4Mpixel/dl-booru2024-hfhub.py)

- **Rerun that script for this repo (another 10k tarfile).**

- (Optional) Otherwise build this dataset via [metadata-booru2024-tags-parallel.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/danbooru2024-webp-4Mpixel/metadata-booru2024-tags-parallel.py)

- Run [extract-booru2024-parallel.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/danbooru2024-webp-4Mpixel/extract-booru2024-parallel.py) to extract all tars into a single directory.

```log
> python extract-booru2024-parallel.py
100%|██████████████████████████████████████| 1000/1000 [6:48:15<00:00, 24.50s/it]
Extracted: 1000 iters
Delta: 0 files
```

```log
PS H:\danbooru2024-webp-4Mpixel> node
Welcome to Node.js v20.15.0.
Type ".help" for more information.
> const fs = require('fs');
> console.log(fs.readdirSync("./khoyas_finetune").length);
16010020
```

- (Done?) Finally, instead the [official guide](https://github.com/kohya-ss/sd-scripts/blob/main/docs/fine_tune_README_ja.md) (a bit messy), follow this [reddit post](https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904) to **make the metadata JSON file (with ARB)** and start finetuning.

