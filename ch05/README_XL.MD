# Chapter 05-XL: AstolfoMix-XL. #

- [CivitAI model page.](https://civitai.com/models/309514) The style there is a bit different.

- [HuggingFace model page.](https://huggingface.co/6DammK9/AstolfoMix-XL) The style is also different.

- (Coming soon) [CivitAI article page.](https://civitai.com/articles/3409) Summary of here (as additional content with SD1).

## What is the mix? ##

- Currently, it is an experimental merge with [immediately accessible merging algorithms](https://github.com/ljleb/sd-mecha/blob/main/sd_mecha/merge_methods.py) under discovered SDXL models.

- Baseline model will be *ensemble averaging*, same as "model soup".

- I will include *exclusive findings* here only. Read the ["master" article](./README.MD) and ["SD2" article](./README_SD2.MD) *(yes it applies also)* for general ideas.

## Generated Images ##

- ["AstolfoMix" in Pixiv.](https://www.pixiv.net/en/tags/AstolfoMix/artworks)

## Why make such a model? ##

- Given the ~~asserted~~ success of previous experience (SD1 and SD2), I think I shuold keep it up on recent architecture, SDXL ~~Turbo / LCM will be examined  later~~, which is larger and more complicated then both SD1 and SD2, and try to make the model as *useful* as the SD2 version.

## My discoveries ##

### Coincidence, now I can cite on something ###

- [Do the Frankenstein, or how to achieve better out-of-distribution performance with manifold mixing model soup](https://arxiv.org/abs/2309.08610)

![photo_2024-03-19_12-31-39.jpg](img/photo_2024-03-19_12-31-39.jpg)

- *Note: ValAcc(ζ) is close to the Reward Model used in AutoMBW / Bayesian Merging.*

- **Important: It only shows improvement! It won't "solve" specified tasks e.g. Importing Pony V6's NSFW into Animagine v3.1!**

### It is using the exact same CLIP as SD1 ###

- [ch03/view_unet/view_unet.ipynb](../ch03/view_unet/view_unet.ipynb): You will find that [the config of TE0 from SDXL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/text_encoder/config.json) is the exact same of [the config in SD1](https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/text_encoder/config.json). 

This is directly quoted from HuggingFace (SDXL):

> Model Description: This is a model that can be used to generate and modify images based on text prompts. It is a Latent Diffusion Model that uses two fixed, pretrained text encoders (OpenCLIP-ViT/G and CLIP-ViT/L).

And then SD1:

> Model Description: This is a model that can be used to generate and modify images based on text prompts. It is a Latent Diffusion Model that uses a fixed, pretrained text encoder (CLIP ViT-L/14) as suggested in the Imagen paper.

It is the *same* ViT-L. However we all noticed "finetuned models" are all "SD models". Can we have other methods to check?

- Yes. Once again we use [stable-diffusion-webui-model-toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit) by *exporting CLIP (not CLIP-AUX) from SDXL and then import it to SD1.* And... it shows the clean `0000` hash. Note that `21b` is the latest model in SD1, and `x39a` is the current version of merged SDXL, and `_x25` is the original SDXL model, `te2` means "both CLIPs are explicitly imported".

![240206.JPG](img/240206.JPG)

- Making the mixed CLIP from `x39a` will obviously yield a different image. `x25a` is same as `_x25`.

![xyz_grid-0669-3972813705-3072-817-4-48-20240131004251.png](img/xyz_grid-0669-3972813705-3072-817-4-48-20240131004251.png)

### Will Greedy approach work? ###

- [Started from the discovery of "associative property"](./README.MD#associative-property), [and the independent consideration of model components](./README_SD2.MD#considering-clip--te-combinations-individually), I think it is plausible to follow a [greedy approach](https://en.wikipedia.org/wiki/Greedy_algorithm). By [breaking the massive problem into subproblems](https://medium.com/@srosamazaid/the-greedy-algorithm-pattern-an-in-depth-analysis-7bb28d5dbfa7), and naively choose the best (or good) results, brings me towards the desired effect. Also, [the special case of add diff and convergence of averaging](./README.MD#findings-on-astolfomix-21b) supports my view to not considering too much on [covariance](https://en.wikipedia.org/wiki/Covariance) between components. *I have not experiened any unexpected result yet, when I confirm I'm following my procedure correctly.*

- Also, [since model selection is a combination optimization problem](./README_SD2.md#model-selection), choosing it by *intuition* may not work when the model count is large (**currently discovered 44 models**), such greedy approach can *estimate* and make prediction from a NP time complexity into linear time ( $O(N)$ ), with only a few iterlations of comparasions, ~~and control the space complexity even it already used over 1TB on storing intermediate merged models. Unless I develop a N-way merger from scratch,~~ space requirement will outnumber the traditional fine tune approach also even I have a N-way merger (see below). ~~Looks like I'm trying to rationalize a random approach, but I really don't have solid idea since there is absolutely no reference in this world.~~

- *I may try applying score metric, or algorithms on model comparasions on model selection, instead of human evalulation, although it is effective. Hopefully I don't have to code everything from scratch.*

- Therefore, the procedure is further extended from SD2 (and SD1): Since SDXL has 2 CLIPs, I compare the CLIPs seperately. The starting point is still blindly average out all discovered models.

### I have the N-way merger! ###

- An **E2E single-click solution** has been found. ~~Sorry I'm too lazy to write code.~~ See [this notebook](./astolfo_mix_e2e.ipynb) for details. **Efficiency has been increased very much** because I have saved so many disk space, and merging time reduced from 60+ minutes to around 8 minutes for 40 models. However I still need a few sets of models for components comparasion, hence the space complexity remains unchanged.

- Although I'm too lazy to implement the binary tree approach and let floating point error propogates through the math series approach, it is still looking almost identical, because *it overcome the limitation on A1111 WebUI*.

![xyz_grid-0704-972751457-2048-1287-4.5-48-20240214000418.png](img/xyz_grid-0704-972751457-2048-1287-4.5-48-20240214000418.png)

### I also "fixed" the pruned models ###

- Some models **cannot be swapped between components, or mergeable.** A1111's OG merger requires valid model metadata to operate, which some models may have its own metadata and fails the merge, meanwhile some models have deviation in model structure (even it may works well in WebUI) and make the toolkit failed to swap components from them.

- For example, it will show "VAE-v1-BROKEN" when parsing the model: 

![24020901.JPG](./img/24020901.JPG)

- And it may throw error while merging:

![24020902.JPG](./img/24020902.JPG)

- After some investigation (along with `sd-mecha`'s development), I've found that the root cause if "VAE-v1-BROKEN" is **pruned SDXL models**. It is easy to fix with A1111 OG merger, just use original SDXL as base model (model A) and apply M=1.0 a.k.a take all weights from foreigner model.

![24021801.webp](img/24021801.webp)

- For the models **both have custom metadata and pruned**, I modify the N-way merger (using customized `meh` as backend) to perform the merge.

![24021802.jpg](img/24021802.JPG)

- Then the image is close to identical:

![xyz_grid-0713-972751457-3072-1343-4.5-48-20240218161936.png](img/xyz_grid-0713-972751457-3072-1343-4.5-48-20240218161936.png)

![xyz_grid-0715-972751457-3072-1343-4.5-48-20240218164110.png](img/xyz_grid-0715-972751457-3072-1343-4.5-48-20240218164110.png)

### More findings on merging CLIP and MBW layers ###

- *This is discovered by chance.* From paper ["Localizing and Editing Knowledge in Text-to-Image Generative Models"](https://arxiv.org/abs/2310.13730), concepts are being represented by scattered activated neuron / layers in UNET with distribution, but being centralized within a single neuron in CLIP.

> Notably, we find a distinct distribution of causal states across visual attributes in the UNet, while the text-encoder maintains a single causal state.

![24020903.JPG](img/24020903.JPG)

![24020904.JPG](img/24020904.JPG)

- It implies the great risk and scarification with "Train Text Encoder" option while fintuning a massive base model, and more important, **merging with different finetuned CLIPs**. This problem is dodged in SD1, [because I sticked with the OG CLIP](./README.MD#the-power-of-the-original-sd-1xs-text-encoder), and experienced in SD2. Agressively merging 2 CLIPs in the SDXL will make the model failed to understand most concepts. More in the next section.

### Changing docuement style ###

- I didn't expect model selection across ongoing community developement will involve so many iterlations. It yields so many docuements and making this page too large for a mobile to load (I view this othen in outdoor). I'll move most boring stuffs to other places.

- Read docuemnts there for how I derive the model selection from the discovered models. I'll do put the statistic here.

|Round|Model Name|RAW|UNET|TE0|TE1|Recipe|
|---|---|---|---|---|---|---|
|01|`x17-AstolfoMix-x13te0x14te1.safetensors`|42|32|14|21|[json](./recipes/recipe-x39a.json)|
|02|`x43-AstolfoMix-x22te0x31te1.safetensors`|50|44|22|31|[mecha](./recipes/x43-AstolfoMix-x21te0x30te1-e2e-240222-60d0764.mecha)|
|03|`x45-AstolfoMix-x39te0x39te1-e2e-240222-60d0764.safetensors`|52|46|40|40|[mecha](./recipes/x45-AstolfoMix-x39te0x39te1-e2e-240222-60d0764.mecha)|
|04|`x63-AstolfoMix-x60te0x41te1-e2e-240407-feefbf4.safetensors`|70|52|61|42|[mecha](./recipes/x63-AstolfoMix-x60te0x41te1-e2e-240407-feefbf4.mecha)|

## Discovered models ##

- Moved to [AstolfoMix-XL: Discovered models](./xl_docs/discovered_models.md)

## Deriving the "recipe" a.k.a model selection (Round 1, x39a) ##

- Moved to [AstolfoMix-XL: Model selection Round 1 (x39a)](./xl_docs/r01_x39a.md).

## Model selection Round 2, x49a ##

- Moved to [AstolfoMix-XL: Model selection Round 2 (x49a)](./xl_docs/r02_x49a.md).

## Finding on "SDXL Baseline Merge" ##

- *I will have a "round 2" soon, because there are so many model released recently, along with merging tools. The docuement here is referring "x39a" only.*

### Compromised model merge ###

- From the "recipe" above, you will find that I've dropped `_x14-ponyDiffusionV6XL_v6` and `_x08-animagineXLV3_v30`, which have became the most popular anime models recently. Both of their model weights are far beyond to the majority models, and making the `x39a` generate random contents instead of prompted contents.

- As stated by the author (no reference yet), `_x14-ponyDiffusionV6XL_v6` has been trained with **large learning rate** to steer the model weights away, and it can be shown in L2 diagrams. Also, from the dual CLIP structure, the image will break with low L2 (below 20).

- *I have a WS powerful enough to include all models, see next chapter.*

<details>
    <summary>Gallery of L2 diagrams. Click to open.</summary>

- sdxl0 = models from `_x01` to `_x10`, with `_x25` for reference.

![sdxl0_unet_vg.png](../ch03/v2a/img/sdxl0_unet_vg.png)

![sdxl0_te0_vg.png](../ch03/v2a/img/sdxl0_te0_vg.png)

![sdxl0_te1_vg.png](../ch03/v2a/img/sdxl0_te1_vg.png)

- sdxl1 = models from `_x11` to `_x20`, with `_x25` for reference.

![sdxl1_unet_vg.png](../ch03/v2a/img/sdxl1_unet_vg.png)

![sdxl1_te0_vg.png](../ch03/v2a/img/sdxl1_te0_vg.png)

![sdxl1_te1_vg.png](../ch03/v2a/img/sdxl1_te1_vg.png)

- sdxl2 = models from `_x21` to `_x30`, with `_x25` for reference.

![sdxl2_unet_vg.png](../ch03/v2a/img/sdxl2_unet_vg.png)

![sdxl2_te0_vg.png](../ch03/v2a/img/sdxl2_te0_vg.png)

![sdxl2_te1_vg.png](../ch03/v2a/img/sdxl2_te1_vg.png)

- sdxl3 = models from `_x31` to `_x41`, with `_x25` for reference.

![sdxl3_unet_vg.png](../ch03/v2a/img/sdxl3_unet_vg.png)

![sdxl3_te0_vg.png](../ch03/v2a/img/sdxl3_te0_vg.png)

![sdxl3_te1_vg.png](../ch03/v2a/img/sdxl3_te1_vg.png)

- sdxl4 = 10 handpicked models, with `_x25` for reference.

![sdxl4_unet_vg.png](../ch03/v2a/img/sdxl4_unet_vg.png)

![sdxl4_te0_vg.png](../ch03/v2a/img/sdxl4_te0_vg.png)

![sdxl4_te1_vg.png](../ch03/v2a/img/sdxl4_te1_vg.png)

- sdxl5 = models from `_x41` to `_x50`, with `_x25` for reference.

![sdxl5_unet_vg.png](../ch03/v2a/img/sdxl5_unet_vg.png)

![sdxl5_te0_vg.png](../ch03/v2a/img/sdxl5_te0_vg.png)

![sdxl5_te1_vg.png](../ch03/v2a/img/sdxl5_te1_vg.png)

</details>

![img/xyz_grid-0698-3416143198-5120-1332-6-48-20240204012805.jpg](img/xyz_grid-0698-3416143198-5120-1332-6-48-20240204012805.jpg)

- Such "randomess" is soon discovered that the CLIPs should be filtered and work within a "limited range" of model weights.

![img/xyz_grid-0700-1355548248-10080-1631-4.5-48-20240204013956.jpg](img/xyz_grid-0700-1355548248-10080-1631-4.5-48-20240204013956.jpg)

- As soon as getting the `x17`, it understand well in most concepts, *but it failed to understand characteristics of anime characters.* Making the "more nsfw" `x11c` (which is a subset of `x17` actually) make it understands a bit better, but as consequence, non anime concepts are understand worse.

![img/xyz_grid-0701-1222745577-10080-1631-4.5-48-20240204014105.jpg](img/xyz_grid-0701-1222745577-10080-1631-4.5-48-20240204014105.jpg)

- Before dumping GPU hours to the AutoMBW part, I need to explore either **more models** (yes, it reached 50!) or **more methods**, which [happened just in time](../ch01/rebasin.md). Git Re-Basin was once considered *not a merging method for SD* by me, but as soon as I've found and watch the seminar, I think the existing implementation is not applying well, or there is some misconception to prevent merging whole model with the algorithm.

### Quality tags are not required anymore ###

- *It also applies to both SD1 and SD2 version.*

- Quality tags only being requied if the model training involves quality tagging intentionally. Once it is not exist, *or I merge the models which contradicts in model weights*, they will be no longer effective, returning the desired contents regardless "quality control". 

![xyz_grid-0679-359783617-3072-1332-6-48-20240203104728.png](img/xyz_grid-0679-359783617-3072-1332-6-48-20240203104728.png)

## My action list (after Baseline merge) ##

- *Wait* for the [upcoming merger](https://github.com/ljleb/sd-mecha) and [modified toolkit](https://github.com/silveroxides/stable-diffusion-webui-model-toolkit-revisited)

- Keep exploring more models and algorithms

- And see if situation changes drastically in round 2. *Yes*

- ~~[Built a workstation for merging, which is by chance.](../ch04/ice_lake_ws.md)~~

## Findings on "SDXL Extended FP64 Merge" ##

*I decided to split the chapter. Technically it is no longer the OG pairwise merge, solely using external tools.*

- *The new Workstation is lit!*

![24040601.jpg](./img/24040601.jpg)

### Refreshed global L2 chart ###

<details>
    <summary>Gallery of L2 diagrams. Click to open.</summary>

![sdxl6_unet_vg.png](../ch03/v2a/img/sdxl6_unet_vg.png)

![sdxl6_te0_vg.png](../ch03/v2a/img/sdxl6_te0_vg.png)

![sdxl6_te1_vg.png](../ch03/v2a/img/sdxl6_te1_vg.png)

![sdxl6_vae_vg.png](../ch03/v2a/img/sdxl6_vae_vg.png)

![sdxl6_unet_xy.png](../ch03/v2a/img/sdxl6_unet_xy.png)

![sdxl6_te0_xy.png](../ch03/v2a/img/sdxl6_te0_xy.png)

![sdxl6_te1_xy.png](../ch03/v2a/img/sdxl6_te1_xy.png)

![sdxl6_vae_xy.png](../ch03/v2a/img/sdxl6_vae_xy.png)

</details>

## Model selection Round 3, x52a ##

- The stuffs similar to previous rounds has been moved to [AstolfoMix-XL: Model selection Round 3 (x52a)](./xl_docs/r03_x52a.md).

- Since [sd-mecha](https://github.com/ljleb/sd-mecha) is in active development, meanwhile there is a script to "merge CLIP" seperately, **also the generated images are being different** because of "structure autofix" along with **fp64 merging**, I think I can rewrite the script to *generate all intermediate models* in full auto. [And... I am really doing it.](./astolfo_mix_e2e.ipynb) Now I'm totally not operating WebUI to merge models. [As shown in the recipe](x45-AstolfoMix-x39te0x39te1-e2e-240222-60d0764.mecha), it is in serialized form, which looks like [assembly code](https://en.wikipedia.org/wiki/Assembly_language).

- I've found that **the output image is no longer same as the previously merged model.** It is possibly caused by *close to perfect precision* (FP64 merge with pure floating point ratio), which *dual CLIP structure is extra sensitive here,* and the un-pruning process (directly predefine known good structure) is different from A1111's "union of discovered layers".

![xyz_grid-0737-1355548248-5376-1081-4.5-48-20240222003354.jpg](./img/xyz_grid-0737-1355548248-5376-1081-4.5-48-20240222003354.jpg)

- This is a test of merging 4 random models, which exclude the floating point error:

![xyz_grid-0740-1355548248-4032-1039-4.5-48-20240222011443.jpg](./img/xyz_grid-0740-1355548248-4032-1039-4.5-48-20240222011443.jpg)

- After whole procedss, I found that even casting FP16 from FP64 for a few times will cause difference also, the `e2e` is true FP64 merge for the whole process:

![xyz_grid-0763-755545524-2688-1081-4.5-48-20240228073427.png](./img/xyz_grid-0763-755545524-2688-1081-4.5-48-20240228073427.png)

- Another round (round 3.5) of model selection, this time is exclusion instead of inclusion.
Looks like add-diff is a bad thing: Most merged model's CLIP have been dropped. Example: Kohaku (07,29,44), a2 (15), AID (34), 218 (40), and js2prony (48)

![xyz_grid-0757-755545524-28224-1623-4.5-48-20240227074913.jpg](./img/xyz_grid-0757-755545524-28224-1623-4.5-48-20240227074913.jpg)

## Model selection Round 4, x63a ##

- The stuffs similar to previous rounds has been moved to [AstolfoMix-XL: Model selection Round 4 (x69a)](./xl_docs/r04_x69a.md).

- Situation is getting similar after I scaled up the model pool, with adding more models in 2403. Pony series models are not mergible at this moment. 

- Human details is slightly more refeined, but the *background* is a lot more rich and realistic (content wise, not style).

![xyz_grid-0794-2049335707-8064-1623-4.5-256-20240413165049.jpg](./img/xyz_grid-0794-2049335707-8064-1623-4.5-256-20240413165049.jpg)

![xyz_grid-0795-2049335707-8064-1623-4.5-256-20240413165435.jpg](./img/xyz_grid-0795-2049335707-8064-1623-4.5-256-20240413165435.jpg)