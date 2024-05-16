# Anifusion-SD. Innovative try. #

- [Medium article by author](https://medium.com/@enryu9000/anifusion-sd-91a59431a6dd)

- **Dedicated WebUI is reuqired.**

- My implementation script on Win11:

[anifusion2_win11_vscode_miniconda.sh](../ch97/anifusion2_win11_vscode_miniconda.sh)

- [Gallery of my experience](https://www.pixiv.net/en/tags/Anifusion_SD/artworks)

## Technical findings ##

- Author has reviewed the structure of SD / LDM, and decided to TTE on a distinct CLIP, because SD2.x was screwed up, meanwhile communities was only skilled on training UNET ~~still true in 2405~~.

## Prompt findings ##

**Prompt augmentation** is mandatory! Fill up all 50 tags, otherwise the image style (quality) will screw up!

- Example:
```
all_fours, doggystyle, sex_from_behind, fucked_silly, handsfree_ejaculation, ejaculating_while_penetrated, stomach_bulge, otoko_no_ko, astolfo_(fate), heart-shaped_pupils, rolling_eyes, tears, torogao, cum, anus, ass, yaoi, male_focus
```

- `rating_s / q / e` only affects generated prompt (after manual input), so it can be NSFW eventually. 
- Art style is fixed, also not artistic at all, it is because it has absolutely no Laion content (pretrained material from SD).
- Therefore always look for danbooru tags. No need to esacpe brackets, and follow the tags in case sensitive.

## Side notes ##

- Contacted author via email, he won't join any SD community.