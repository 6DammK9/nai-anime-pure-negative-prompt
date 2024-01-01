# Chapter 05-SD2: Astolfo mix SD2. #

- [(SD1) CivitAI model page.](https://civitai.com/models/155604) The style there is a bit different.

- [HuggingFace model page.](https://huggingface.co/6DammK9/AstolfoMix-SD2) The style is also different.

- [(SD1) CivitAI article page.](https://civitai.com/articles/3409) Summary of here.

## What is the mix? ##

- Currently, it is an ~~Ensemble averaging~~ Uniform merge of 10 UNETS + 4 CLIPS, picked from 23 discovered SD2.1 models.

- I will include *exclusive findings* here only. Read the ["master" article](./README.MD) for general ideas.

## Generated Images ##

- ["AstolfoMix" in Pixiv.](https://www.pixiv.net/en/tags/AstolfoMix/artworks)

## Why make a model? ##

- SD2.1 is the best proving ground for an original idea. Whole history of SD2 and its finetunes (especially WD1.5) is a total tragedy. If my mix *looks reasonable* out of merging total unuseable models, I will discover a lot more exlucsive findings, and *get closer to the ground truth.* 

>  Distance metric is not meaningful, **but the identity does.**

As the metaphor in [mega_cmp](../ch03/v2a/mega_cmp.ipynb), Ceiling (by Author of AnythingV3) is not meaningful, **but the ground truth does.**

## My discoveries ##

### Total disaster ###

- [ch02/model_history](../ch02/model_history.md): *Image there is irrelevant.* Started from WD1.5B2, I believe that it is *trainer problem along with A1111's runtime problem.* Most models at that era cannot generate any reasonable image, except the prompts mentioned in the demo case. As on 231231, I can't reproduce the [same image](https://www.pixiv.net/en/artworks/105946900) on 2303. Except [Replicant-V3.0](https://civitai.com/models/10701?modelVersionId=75540) and its variants, even the [PonyDiffusion](https://civitai.com/models/95367/pony-diffusion-v5), I cannot make any reasonable images out from demo prompts (most users don't aware of this because they are targeted users). *Therefore there must be something to improve.*

- [ch01/merge](../ch01/merge.md): Althouth there was some [tryhard merges](https://civitai.com/models/11420/quattro4mergei?modelVersionId=13518) which shared a similar thought, it is acting strange (later I found some essential prompts to include), and [there are some actual improvement from parent model.](https://civitai.com/models/68163?modelVersionId=78114) *There must be something really bad, was included in the mix, to make the result model being poor on understanding concepts.*

- [ch01/hires_fix](../ch01/hires_fix.md), [ch01/cfg_step](../ch01/cfg_step.md), [ch01/arb](../ch01/arb.md): Most finetuned models used 768x768 for training, therefore there is no "huge improvement" like what SD1.5 did. However my mix will be carried a lot faster. BTW the result CFG will be changed, due to the lower diversity of the implied training dataset.

- Remining stuffs will be [same as what I do in SD1](./README.MD).

### Merging models from different background ###

- Here is a list of merged, or "may be merged" of models. Explainantion of the selection will be listed in below session.

|Index|Model name (with URL)|UNET used?|CLIP used?|
|---|---|---|---|
|`_201`|[AllWorkForkRowk](https://civitai.com/models/136088?modelVersionId=233682)|||
|`_202`|[Artius V2.1 NSFW](https://civitai.com/models/15975/artius-v21-nsfw?modelVersionId=33119)|Y||
|`_203`|[E621 Rising v2](https://civitai.com/models/32423/e621-rising-v2-a-stable-diffusion-21-furry-model?modelVersionId=38862)|||
|`_204`|[hakoMayD](https://civitai.com/models/72668/hakomayd?modelVersionId=77394)|Y||
|`_205`|[Illuminati Diffusion v1.1](https://civitai.com/models/11193/illuminati-diffusion-v11?modelVersionId=13259)|||
|`_206`|[Mishi Anime](https://civitai.com/models/7742/mishi-anime?modelVersionId=9125)|Y||
|`_207`|[NijiDiffusion](https://civitai.com/models/55495/nijidiffusion?modelVersionId=59885)|||
|`_208`|[Plat Diffusion v1.3.1](https://huggingface.co/p1atdev/plat-diffusion)|||
|`_209`|[PVC v4](https://huggingface.co/p1atdev/pvc-v4/tree/checkpoints)|||
|`_210`|[Quattro4Merge+i](https://civitai.com/models/11420/quattro4mergei?modelVersionId=13518)|Y||
|`_211`|[Replicant-V3.0](https://civitai.com/models/10701?modelVersionId=75540)|Y||
|`_212`|[Pony Diffusion](https://civitai.com/models/95367/pony-diffusion-v5)|||
|`_213`|[Cool Japan Diffusion 2.1.2](https://huggingface.co/aipicasso/cool-japan-diffusion-2-1-2)||Y|
|`_214`|[WD 1.5 Beta 2](https://huggingface.co/waifu-diffusion/wd-1-5-beta2)|||
|`_215`|[WD 1.5 Beta 3](https://huggingface.co/waifu-diffusion/wd-1-5-beta3)||Y|
|`_216`|[YiffAI](https://civitai.com/models/3684/yiffai-2322?modelVersionId=6253)|||
|`_217`|[Stable Diffusion v2-1](https://huggingface.co/stabilityai/stable-diffusion-2-1)||Y|
|`_218`|[RuminationDiffusion](https://huggingface.co/JosephusCheung/RuminationDiffusion)|Y||
|`_219`|[Scream-SemiRealistic](https://civitai.com/models/99040/sd2scream-semirealistic?modelVersionId=140498)|Y||
|`_220`|[Realgar-v2.1](https://civitai.com/models/70713?modelVersionId=111486)||Y|
|`_221`|[RheaSilvia](https://civitai.com/models/68163?modelVersionId=78114)|Y||
|`_222`|[MuaccaMix](https://civitai.com/models/26087/muaccamix?modelVersionId=112322)|Y||
|`_223`|[hakoMayBoy](https://huggingface.co/852wa/hakoMay/blob/main/hakoMayBoy.safetensors)|Y||

- Instead of [abruptly replaced with SD1.4's Text Encoder](https://huggingface.co/6DammK9/bpmodel-sd14-merge), this time *I don't trust SD's original TE, and somehow eventually used it.*

- This time may not have "Extended" version unless I found including more models will be useful.

- Remining stuffs will be [same as what I do in SD1](./README.MD).

### Model selection ###

- Model seleciton is a **NP Hard** ( $O(N!)$ ) question. However with [pattern recognition](https://en.wikipedia.org/wiki/Pattern_recognition) by visual inspection (since total number is still 23), it reduced to a core concept of **"Replicant-V3 UNET + WD1.5B3 CLIP"**. With some further matching, **10 UNETs and 4 CLIP / TEs** are picked for this version of AstolfoMix.

- Builtin VAE will be `kl-f8-anime2.ckpt`. But I'm still using `vae-ft-mse-840000-ema-pruned.ckpt` for WebUI. Choose what you want.

- [ch03](../ch03): TTE may help bring some "anime" features to the foreground, *I must adjust my prompt, since most models are tagged with anime / real*, and AI chose to not blending the style like SD1 did.

- The actual steps of finding the model combination will be listed in below session.

### Verifying the merge is precise ###

- Since I use [parallel merge](https://en.wikipedia.org/wiki/Merge_algorithm) directly, it is 0.5 most of the time. I only need to "reset CLIP" for the last model.

## Finding on "SD2 Baseline Merge" ##

- *Stick with 768x768 with maximum 1.5x HiRes fix*. There are no 1024x1024 trained models in the wild.

![231236-802596511-1536-864-6-256-20231231171716.png](./img/231236-802596511-1536-864-6-256-20231231171716.png)

```
parameters
(aesthetic:0), (quality:0), (anime:0), (solo:0), (boy:0), [niqab], [[hijab]], [astolfo], [[afghanistan]]
Negative prompt: (worst:0), (low:0), (bad:0), (exceptional:0), (masterpiece:0), (comic:0), (extra:0), (lowres:0), (photorealisitc:0)
Steps: 256, Sampler: Euler, CFG scale: 6, Seed: 802596511, Size: 1024x576, Model hash: a85153fd84, Model: 209-AstolfoMix-207208-203te, VAE hash: df3c506e51, VAE: vae-ft-mse-840000-ema-pruned.ckpt, Denoising strength: 0.7, Clip skip: 2, FreeU Stages: "[{\"backbone_factor\": 1.1, \"skip_factor\": 0.9}, {\"backbone_factor\": 1.2, \"skip_factor\": 0.2}]", FreeU Schedule: "0.0, 1.0, 0.0", FreeU Version: 2, Hires upscale: 1.5, Hires steps: 64, Hires upscaler: Latent, Dynamic thresholding enabled: True, Mimic scale: 1, Separate Feature Channels: False, Scaling Startpoint: MEAN, Variability Measure: AD, Interpolate Phi: 0.3, Threshold percentile: 100, Version: v1.7.0
```

### Considering CLIP / TE combinations individually ###

- This time [stable-diffusion-webui-model-toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit) will be used frequently, because I need to keep extracting and importing UNETs / CLIPs together. It also saves the model as FP16 safetensors, which is commonly used, reliable and take less disk space. *Now I've generated 80+ models which is huge* ( $O(N)$ for space)

- [Effects on swapping CLIP / TE has been discovered in the SD1 version](./README.MD#swapping-clip--te-with-other-models). This time I used to discover any useful CLIP (somehow SD2.1's CLIP is still competitive for general purpose).

- Looking for images generated by original models are not useful. It only shows indentifible anime face (Astolfo?) or the car (Mercedes?), but not both of them. It shows that TTE made the model weights skewed so hard.

![img/xyz_grid-0542-2381024291-24576-1244-6-48-20231227011949.jpg](./img/xyz_grid-0542-2381024291-24576-1244-6-48-20231227011949.jpg)

- **Then I blindly merge all models together.** At that point, only 16 models are discovered. Obviously, it is a total mess. 

- For full receipe, see [receipe-215a.json](./receipe-215a.json).

![img/xyz_grid-0541-2381024291-24576-1230-6-48-20231227011817.jpg](./img/xyz_grid-0541-2381024291-24576-1230-6-48-20231227011817.jpg)

- Then I apply each receipe model's CLIP in to the blindly merged model. Notice that some highly similar images appeared. Also, it shows BOTH a car and a person (although the person is messed up).

- **Now I can identify the useful CLIPs.** Make sure repeat such batch image generation for different topics. Here I show only a single topic.

![img/xyz_grid-0543-2381024291-26112-1230-6-48-20231228011101.jpg](./img/xyz_grid-0543-2381024291-26112-1230-6-48-20231228011101.jpg)

- Finally merge all "useful CLIPs" as whole model, then **join all receipe models with the new merged CLIP**.

- **Now I can identify the useful UNETs.**

![img/xyz_grid-0568-2381024291-27648-1182-6-48-20231228234826.jpg](./img/xyz_grid-0568-2381024291-27648-1182-6-48-20231228234826.jpg)

- Finally **repeat the merge with the specified models**. Somehow the "model set" can be simplified to a "model variants merging to another model variants". Let's see the effect.

![img/xyz_grid-0580-2381024291-9216-1243-6-48-20231230002606.jpg](./img/xyz_grid-0580-2381024291-9216-1243-6-48-20231230002606.jpg)

- To expand the "set of models" I've find that I really need more models to "adjust the weight" even it is just an uniform merge. Somehow I've found 6 more models and repeated the whole process. Note that since it is parallel merge, I can "add" the new merge instead of deleting all intermediate models.

- For full receipe, see [receipe-209.json](./receipe-209.json). Note that [stable-diffusion-webui-model-toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit) doesn't preserve metadata, therefore I only show `209` instead of `209-203te`.

![img/xyz_grid-0593-3569717888-3072-1224-6-48-20231231031129.jpg](./img/xyz_grid-0593-3569717888-3072-1224-6-48-20231231031129.jpg)

- Since the model is biased to a model variant, I need to adjust the CFG, which is "CFG 4 mimic 1 scale 0.5" to "CFG 6 mimic 1 scale 0.3".

![img/xyz_grid-0597-640303058-4608-1060-6-256-20231231093520.jpg](./img/xyz_grid-0597-640303058-4608-1060-6-256-20231231093520.jpg)

### "Looking good" doesn't mean it is useful ###

- *The merge won't look great, but at least you won't get Miku Hatsune when prompting Suzumiya Haruhi, or having a black hair boy when prompting Link.*

![img/xyz_grid-0572-1197848513-19584-1517-4.5-48-20231229003857.jpg](./img/xyz_grid-0572-1197848513-19584-1517-4.5-48-20231229003857.jpg)

![img/xyz_grid-0566-1003151674-4608-1517-6-48-20231228231856.jpg](./img/xyz_grid-0566-1003151674-4608-1517-6-48-20231228231856.jpg)

### L2 graph is not working ###

- I may solve the tedious NP-hard question to "visualize" the model weights in a meaningful way. But this time PonyDiffusion (a big finetune) made the chart look skewed.

![sd2_unet_vg.png](../ch03/v2a/img/sd2_unet_vg.png)

![sd2_te_vg.png](../ch03/v2a/img/sd2_te_vg.png)

![sd2_vae_vg.png](../ch03/v2a/img/sd2_vae_vg.png)

## My action list ##

- **Docuement first.** If you see any content not covered in this article, it is either an idea just appeared, or I really havn't considered. Most idea in this article is original and relies on my own experience. 

- Continue what I did in SD1, but in a more efficient way. This time I'm not interested in the intermediate steps.

- *Make it support NSFW by merging the only 1 or 2 discovered NSFW models.*