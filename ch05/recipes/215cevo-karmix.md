# Merge Log of "215c Evo" #

## Notice ##

- I do not put in the [README_XL](../README_XL.MD) because it needs to be explored, meanwhile it starts to be not 100% original idea. This time I rely on [Karmix](../../ch02/karmix.md) and [9527R](https://civitai.com/models/176449/9527-detail-realistic-xl) (the realistic finetune over 215c).

- *From the experience in ch05, all "0.5" are enhanced with "BasinAvg". Math proof... [Rebasin](../../ch01/readme.md) has expected value in 0.5 obviously*

${BasinAvg}(A,B) \leftarrow ( 0.5 (0.5A + 0.5B) + 0.5 Rebasin(A,B) )$

- It has been used since 215c and 255c. Note: 215a = "DGMLA-216", "amp" is the [amplify_diff](../../ch05/amplify_diff.ipynb), and the "base" is the base model "SDXL1.0". 1EP is the result in [finetuned model](../../ch06/) from 255c with 1EP.

${215c} \leftarrow {BasinAvg}(215a,amp(215a,base,2.0))$

- Since BasinAvg takes around an hour, but the native 0.5 is just 10 seconds, I can decide if it works the "phase shift".

- My accept criteria is still "man with car" which represents knowledge preservation from the base model. Realife location is optional (that is not a single concept from background). Mainstream "character / artist style recognition" will be ignored because I think [NoobAI-XL](https://civitai.com/models/833294/noobai-xl-nai-xl) has made a great job here ~~especially it really requires dozens of EPs.~~

## Merge Log ##

- "215cEvo-AstolfoMix-1ep-25052801": BasinAvg(215c, 1EP). Generally tends towards 215c but with enhanced varity of content. However still poor in character / artist style recognition.

- [215cEvo-Karmix-pcatv-25052802](https://huggingface.co/6DammK9/AstolfoMix-XL/blob/main/215cEvo-Karmix-pcatv-25052802.safetensors): 0.7 "Karmix pca-tv-mtd" + 0.3 "215cEvo-AstolfoMix-1ep-25052801". Works fine, with some images broken.

- "215cEvo-Karmix-pcatv-25060103": BasinAvg("215cEvo-AstolfoMix-1ep-25052801", "Karmix pca-tv-mtd"). *Completely broken.*

- "215cR-AstolfoMix-9527-25060104": (215c + 9527R) / 2. [Uncanny valley](https://en.wikipedia.org/wiki/Uncanny_valley) occurs, maybe 9527R alone is fine.

- "215cR-Evo-AstolfoMix-1ep-25060105": (215cR + 1EP) / 2. Generally tends towards 215cEvo but with enhanced character anatomy. Probably anthro only and not feral.