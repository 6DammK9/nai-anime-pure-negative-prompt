# Chapter 97: Uncategorized contents #

Usually "not article".

## Article for situational use ##

- A SoK on vid2vid(and seperate from text2vid): [vid2vid.md](vid2vid.md)

## Scripts (surviving in the internet) ##

- `purgeme.py`: "/purgeme"
- `PixivDataAnalysis.py`: Statistics without Pixiv Premium
- `0299d.md`: A list shouldn't exist

## Scripts (manual scripts for webui) ##

- `step.js [step] [split_comma]`: **I use it frequently.** Generate global static emphasis level on the prompts.
- `node listseed [full_directory]`: Extract seeds inside the filenames, which reduce human error when iterlating mass image production. Use `[seed]-[width]-[height]-[cfg]-[steps]-[datetime]` as Settings > Images filename pattern.
- `aspect512.js [w] [h]`: Find actual width / height with aspect ratio `w:h` under 512x512 px also in unit of 64px.

## Scripts (broken shell scripts) ##
- `anifusion2_win11_vscode_miniconda.sh`: Install Anifusion-SD with Win11 + conda. Run it line by line in manual.