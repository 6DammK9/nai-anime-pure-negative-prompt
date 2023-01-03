# Anifusion-SD. 大膽的嘗試. #

**Prompt augmentation** 一定要開! ~~而且數字數! ~~ 不用數了

~~這樣 `Max prompt length after augmentation` = 18 (17 個 `,`)~~ 拉爆 50 個，不好少，空格會破壞畫風
```
all_fours, doggystyle, sex_from_behind, fucked_silly, handsfree_ejaculation, ejaculating_while_penetrated, stomach_bulge, otoko_no_ko, astolfo_(fate), heart-shaped_pupils, rolling_eyes, tears, torogao, cum, anus, ass, yaoi, male_focus
```

rating_s / q / e 只會影響餘下的 prompt （空格數量），所以畫風可以超級 nsfw，但別跟它談唯美，laion 成份是零。

所以最好先搜尋 danbooru。另外括號不用 esacpe，跟足那個 tag 的大小寫 + 符號即可。

需要用人家的魔改 webui。
所以我主要是分享入面的 insight。
注意：~~對現在的作畫是零影響~~  大爆射。

https://medium.com/@enryu9000/anifusion-sd-91a59431a6dd

作者有全盤考慮整個 diffusion 的結構，然後決定搞 tte，因為 sd2.x 一來搞砸了，二來社群們全部都是只搞 unet.

Win11 的我:
https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/ch99/anifusion2_win11_vscode_miniconda.sh

ps: email 作者後, 人家不打算參與任何群組.