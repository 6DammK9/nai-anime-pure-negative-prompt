# (not) cheesechaser speedrun # 

- Respond to incident: [Huggingface is not an unlimited model storage anymore: new limit is 500 Gb per free account.](https://www.reddit.com/r/LocalLLaMA/comments/1h53x33/huggingface_is_not_an_unlimited_model_storage/)

- Speedrun to scrape [danbooru2024](htps://huggingface.co/datasets/deepghs/danbooru2024-webp-4Mpixel) and [e621](https://huggingface.co/datasets/deepghs/e621_newest-webp-4Mpixel) via ~~[cheesechaser](https://github.com/deepghs/cheesechaser)~~ hand crafted script.

- *Since I have no time to organize / code anything, this is just a guide, with some sample code to run.*

- Maybe I'll make some jupyter notebook again for "pseudo GUI" approach.

- ~~Observed from chat~~ "webp-4Mpixel" variant is recommended. I don't know if there should be conversion before finetune, but download first.

- No `.gitignore` here because I always do operations seperately.

- I have observed that Win10 has bug on previewing `*.webp`. File lock is still on after closing the preview, until system reboot or you have figured out the `photos.exe` and the `svchost.exe` to close. Better not to view it unless you really need to validate the logic.

## Shortcut for tldr ##

- Visit my HF repo to download the tags instead of building your own.

- [6DammK9/danbooru2024-tags-10ktar](https://huggingface.co/datasets/6DammK9/danbooru2024-tags-10ktar)

- [6DammK9/e621_2024-tags-10ktar](https://huggingface.co/datasets/6DammK9/e621_2024-tags-10ktar)

- Guides are cloned in [danbooru2024-webp-4Mpixel](./danbooru2024-webp-4Mpixel) and [e621_newest-webp-4Mpixel](./e621_newest-webp-4Mpixel)

## Setting up environment ##

- Safety first.

```sh
conda create -n cheesechaser-env python=3.12
conda activate cheesechaser-env

pip install cheesechaser
```

## Notes on danbooru2024 ##

- Create folder. 
```sh
mkdir danbooru2024-webp-4Mpixel
mkdir danbooru2024-webp-4Mpixel/data
mkdir danbooru2024-webp-4Mpixel/data/exp2_sutr
cd danbooru2024-webp-4Mpixel
```

- Manually down a few files first.

```log
./metadata.parquet
./meta.json
```

- It takes up to 70GB of RAM to load metadata.

```sh
python metadata-booru2024.py
```

- Now test for a few files. **I have edited this to limit to first 100 images, otherwise HF will block me for exceeding rate limit.**

```sh
python dl-booru2024-sample.py
```

```log
>python dl-booru2024-sample.py
[1039096, 1176244, 1307128, 1333515, 1342091, ...]
0096.json: 100%|█████████████████████████████████| 1.07M/1.07M [00:00<00:00, 28.2MB/s]
C:\Users\User\.conda\envs\cheesechaser-env\Lib\site-packages\huggingface_hub\file_download.py:139: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in F:\WORKS\HUGGINGFACE\hub\datasets--deepghs--danbooru2024-webp-4Mpixel. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development
  warnings.warn(message)
0244.json: 100%|███████████████████████████████| 1.07M/1.07M [00:00<00:00, 12.7MB/s]
0128.json: 100%|███████████████████████████████| 1.07M/1.07M [00:00<00:00, 26.0MB/s]
0515.json: 100%|███████████████████████████████| 1.06M/1.06M [00:00<00:00, 14.0MB/s]
...
2540959.webp: 100%|████████████████████████████| 83.5k/83.5k [00:00<00:00, 12.0MB/s] 
2542064.webp: 100%|████████████████████████████| 96.9k/96.9k [00:00<00:00, 13.0MB/s] 
0521.json: 100%|███████████████████████████████| 1.06M/1.06M [00:00<00:00, 6.95MB/s] 
2542518.webp: 100%|████████████████████████████| 164k/164k [00:00<00:00, 4.58MB/s] 
2542521.webp: 100%|████████████████████████████| 195k/195k [00:00<00:00, 756kB/s] 
Download Count: 100it [00:50,  2.00it/s]███████| 100/100 [00:50<00:00,  1.33it/s]
Files Downloaded: 100it [00:50,  2.00it/s]           | 0.00/164k [00:00<?, ?B/s]
Batch Downloading: 100%|███████████████████████| 100/100 [00:50<00:00,  2.00it/s]
```

- Then manually download `0000.tar` to inspect. (There are still way too many API calls which may have me blocked)

```log
./data/0000.tar
```

- And... looks like it is what I'm expecting for.

```log
> python dl-booru2024-hfhub.py
images/0001.json
0001.json: 100%|██████████████████████████████| 1.06M/1.06M [00:00<00:00, 17.6MB/s]
images/0001.tar
0001.tar: 100%|███████████████████████████████| 1.70G/1.70G [01:09<00:00, 24.6MB/s]
```

- Identical for E621.

```log
> python dl-e621-hfhub.py
0000.json: 100%|██████████████████████████████| 63.4k/63.4k [00:00<?, ?B/s]
0000.tar: 100%|███████████████████████████████| 114M/114M [00:04<00:00, 23.0MB/s]
```

- Now the harder part to extract tags. Straight from HF preview, other than the original `tag_string`, there is a groupped chunks like `tag_string_character`, which will be extra good for TE.

- I'll rearrange the tag as **character > copyright > artist > general > meta**. It is because I'm finetuning from a merged model, which can handle general `1girl 1boy` well. 

```log
> python metadata-booru2024-tags-old.py
> tail tags/1.txt
kousaka_tamaki, to_heart_(series), to_heart_2, kyogoku_shin, 1girl, 2000s_(style), ;p, animal_ear_fluff, animal_ears, aqua_panties, blue_bow, blush, border, bow, bow_panties, breasts, brown_eyes, cat_ears, cat_girl, cat_tail, collarbone, colored_stripes, cowboy_shot, groin, hands_up, kemonomimi_mode, large_breasts, long_hair, long_sleeves, looking_at_viewer, no_pants, one_eye_closed, orange_background, outside_border, panties, parted_bangs, pink_shirt, red_hair, red_sailor_collar, sailor_collar, school_uniform, serafuku, shirt, sidelocks, simple_background, smile, solo, standing, straight_hair, striped_background, striped_clothes, striped_panties, tail, thigh_gap, thighhighs, thighs, tongue, tongue_out, two_side_up, underwear, very_long_hair, w_arms, white_border, white_panties, white_thighhighs, bad_id, bad_link, commentary
```

- Since 8M files is too stressful for a disk drive, we convert back to `FFFF.tar` format.
- I have made some optimization and parallelization on the codes. There will be no console output before the task complete.

```log
> python metadata-booru2024-tags-parallel.py
Max ID in the dataset: 8360499
8005010it [00:32, 248097.52it/s]
Tags found: 8005010
100%|████████████████████████████████████████| 1000/1000 [14:53<00:00,  1.12it/s]
Files written: 1000
```

- Now we have the "metadata" to export `*.txt`, and the images for `*.webp`, which should be sufficient for basic finetuning.

![24120501.JPG](img/24120501.JPG)

- The [preferred trainer "khoyas-ss"](https://github.com/kohya-ss/sd-scripts) requires dedicated `meta_lat.json` with caption side preprocessing, we extract all the `*.tar` into the same directory. Since the `id.*` are aligned (**parquet Row ID = file name**), it will be fine.

- I have made some optimization and parallelization on the codes, but the performance boost is only little, meanwhile you cannot scale down the process (always full scale).

```log
> python extract-booru2024-parallel.py
100%|██████████████████████████████████████| 1000/1000 [6:48:15<00:00, 24.50s/it]
Extracted: 1000 iters
Delta: 0 files
```

- Finally, instead the [official guide](https://github.com/kohya-ss/sd-scripts/blob/main/docs/fine_tune_README_ja.md) (a bit messy), follow this [reddit post](https://www.reddit.com/r/StableDiffusion/comments/163097n/getting_started_fine_tuning/?rdt=34904) to **make the metadata JSON file (with ARB)** and start finetuning.

### How to nuke a folder (in there is bugsplash) ###

```powershell
Remove-Item foldertodelete -Recurse -Force -Confirm:$false
```

```cmd
rmdir foldertodelete /s /q
```

```sh
sudo rm -rf foldertodelete
```

### List how many files in a directory (fast) ###

- Do not use right click!

- NodeJS is fast: Less than 1 minute. `16010020 = 8005010 * 2`.

```log
PS H:\danbooru2024-webp-4Mpixel> node
Welcome to Node.js v20.15.0.
Type ".help" for more information.
> const fs = require('fs');
> console.log(fs.readdirSync("./khoyas_finetune").length);
16010020
```

## Notes on building E621 dataset ##

- It is more sparse than danbooru2023 / 2024.

- There is a strange cut in 2404, which there are total 4 repos to download.

- [deepghs/e621_newest](https://huggingface.co/datasets/deepghs/e621_newest) for tags after 2404
- [deepghs/e621_newest-webp-4Mpixel](https://huggingface.co/datasets/deepghs/e621_newest-webp-4Mpixel) for images after 2404
- [boxingscorpionbagel/e621-2024](https://huggingface.co/datasets/boxingscorpionbagel/e621-2024) for tags before 2404
- [NebulaeWis/e621-2024-webp-4Mpixel](https://huggingface.co/datasets/NebulaeWis/e621-2024-webp-4Mpixel) for images before 2404

- **Tag processing is unavailable.** This time will be raw tags with minimal alignment i.e. `anthro male` > `anthro, male`.

```log
> python metadata-e621-tags-parallel.py
Max ID in the dataset: 5217944
5187777it [00:20, 257027.48it/s]
Tags found: 5187777
100%|██████████████████████████████████████| 1000/1000 [09:43<00:00,  1.71it/s]
Files written: 1000
```

- Extracting is similar. I just hardcoded for both datasets.

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
> console.log(fs.readdirSync("./khoyas_finetune").length);
8883320
```

- The "8M+4M" description matchces.

### Query for a sample dataset ###

- You can definitely extract `*.tar` to obtain the files. However the "deleted" images may cause headache because either `*.webp` or `*.txt` was missing.

- Therefore I have made a script for Astolfo and it will also serves a PoC dataset for finetuning. Instead of SD1, *any non finetuned SDXL models are having trouble to show Astolfo with full elements.* 6k images are also a nice number to test the finetuning process and my rig.

```log
> python just-astolfo.py
6224 pairs to be copied.
Copying image-caption pairs: 100%|████████████████████████████████████████████████| 6224/6224 [01:27<00:00, 70.81it/s]
```
