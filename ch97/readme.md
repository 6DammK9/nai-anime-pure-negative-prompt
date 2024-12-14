# Chapter 97: Uncategorized contents #

Usually "not article".

## Article for situational use ##

- A SoK on vid2vid(and seperate from text2vid): [vid2vid.md](vid2vid.md)

- A list shouldn't exist: [0299d.md](0299d.md)

- A flowchart about current "APP" making use of "AI art" ~~definitely not face swap~~ : [swap_face_app.md](swap_face_app.md)

- A quiz, meanwhile introduction to "SD in AI / ML": [quiz_4751.md](./quiz_4751.md)

- A block diagram about "RAG with Docuement versioning control": [rag_with_doc.md](rag_with_doc.md)

## Scripts (Convert to diffuser and upload to HuggingFace later) ##

- `convert_sdxl_to_diffusers.py`: My fork of [convert_sdxl_to_diffusers.py](https://github.com/Linaqruf/sdxl-model-converter/blob/main/convert_sdxl_to_diffusers.py). Added quick guide on the top.
- `convert_original_stable_diffusion_to_diffusers.py`: My fork of [convert_original_stable_diffusion_to_diffusers.py](https://github.com/huggingface/diffusers/blob/main/scripts/convert_original_stable_diffusion_to_diffusers.py). Added quick guide on the top.

## Scripts (surviving in the internet) ##

- `purgeme.py`: "/purgeme". Related to [trojblue/telegram-scraper](https://github.com/trojblue/telegram-scraper) but not scraping.
- `PixivDataAnalysis.py`: Statistics without Pixiv Premium. Prototype of [trojblue/pixivAnalytics](https://github.com/trojblue/pixivAnalytics).

## Scripts (manual scripts for webui) ##

- `step.js [step] [split_comma]`: **I use it frequently.** Generate global static emphasis level on the prompts.
- `node listseed [full_directory]`: Extract seeds inside the filenames, which reduce human error when iterlating mass image production. Use `[seed]-[width]-[height]-[cfg]-[steps]-[datetime]` as Settings > Images filename pattern.
- `aspect512.js [w] [h]`: Find actual width / height with aspect ratio `w:h` under 512x512 px also in unit of 64px.

## Scripts (broken shell scripts) ##

- `anifusion2_win11_vscode_miniconda.sh`: Install Anifusion-SD with Win11 + conda. Run it line by line in manual.

## Scripts (reading metadata for a model by batch) ##

- `extract_merge_info.js`: Extract the actual JSON from [safetensors_util](https://github.com/by321/safetensors_util). *Author closed my PR. Fine.*
- `batch_extract.cmd`: By batch. *May fail a lot.*