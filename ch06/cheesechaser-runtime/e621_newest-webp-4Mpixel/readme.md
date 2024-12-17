# E621 2024 tags only in 10k tar #

- Dedicated dataset to align both [NebulaeWis/e621-2024-webp-4Mpixel](https://huggingface.co/datasets/NebulaeWis/e621-2024-webp-4Mpixel) and [deepghs/e621_newest-webp-4Mpixel](https://huggingface.co/datasets/deepghs/e621_newest-webp-4Mpixel).

- How to use / why I create this: [my speedrun to build the dataset](https://github.com/6DammK9/nai-anime-pure-negative-prompt/tree/main/ch06/cheesechaser-runtime)

## How to build the "dataset" with speed ##

- *Get at least 4TB of storage, and around 75GB of RAM. Always make a venv / conda environment for each task.*

- (Optional) Download this directly: [posts-2024-04-07.parquet](https://huggingface.co/datasets/boxingscorpionbagel/e621-2024/blob/main/metadata/posts-2024-04-07.parquet) and [table.parquet](https://huggingface.co/datasets/deepghs/e621_newest/blob/main/table.parquet)

- Download all 10k tarfile with webp via [dl-e621-hfhub-nw.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/e621_newest-webp-4Mpixel/dl-e621-hfhub-nw.py) and [dl-e621-hfhub-dgs.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/e621_newest-webp-4Mpixel/dl-e621-hfhub-dgs.py)

- **Rerun that script for this repo (another 10k tarfile).**

- (Optional) Otherwise build this dataset via [metadata-e621-tags-parallel.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/e621_newest-webp-4Mpixel/metadata-e621-tags-parallel.py)

- Run [extract-e621-parallel.py](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch06/cheesechaser-runtime/e621_newest-webp-4Mpixel/extract-e621-parallel.py) to extract all tars into a single directory.

```log
> python extract-e621-parallel.py
100%|██████████████████████████████████████| 1000/1000 [2:30:51<00:00,  9.05s/it]
Extracted: 1000 iters
Delta: 744438 files
```

```log
PS H:\e621_newest-webp-4Mpixel> node
Welcome to Node.js v20.15.0.
Type ".help" for more information.
> const fs = require('fs');
> console.log(fs.readdirSync("./kohyas_finetune").length);
8883320
```

- (Done?) Finally, instead the [official guide](https://github.com/kohya-ss/sd-scripts/blob/main/docs/fine_tune_README_ja.md) (a bit messy), follow this [reddit post](https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904) to **make the metadata JSON file (with ARB)** and start finetuning.
