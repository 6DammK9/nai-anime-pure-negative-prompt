# Chapter 05: Astolfo mix. #

- [CivitAI model page.](https://civitai.com/models/155604) The style there is a bit different.

- [HuggingFace model page.](https://huggingface.co/6DammK9/AstolfoMix) The style is also different.

## What is the mix? ##

- Currently, it is an ~~Ensemble averaging of 10 neural networks~~ Uniform Merge of 10 SD models.

## Generated Images ##

- ["AstolfoMix" in Pixiv.](https://www.pixiv.net/en/tags/AstolfoMix/artworks)

## Why make a model? ##

- I have found that the potential of *community supported* SD1.X model still not fully explorered. Meanwhile, although SDXL is greatly improved, it is still lack of *THE proper anime finetune* (e.g. "full danbooru"). Therefore, would there be something to be explorered by making a model with my own discoveries (theory)?

## My discoveries ##

### Merge model is feasible for me ###

- [ch01/merge](../ch01/merge.md): Even it is not well theorized, merging models is an relatively effective method to "ensemble" models without prior knowledge, includes dataset, and training procedures. 

- *Finetuning SDXL has been a engineering challenge*, without any publicized models trained with 1M+ images after a month. The largest scale of [pure finetune](https://civitai.com/models/136719/nekorayxl) or [mixed approach](https://civitai.com/models/136389/kohaku-xl) are only 300k images, way less then the [publicized 4M "full danbooru" dataset](https://huggingface.co/datasets/animelover/danbooru2022). For me not investing on expensive GPUs, e.g. [8x A40 for WD](https://gist.github.com/harubaru/f727cedacae336d1f7877c4bbe2196e1#training-process), or even a single RTX4090, finetuning, or even LoRA, sounds impossible for me. Also, given *my hiatus for 2 months because of other hobbies (hint: PC hardware)*, I won't have time to explore the hyperparameters for model finetuning, or even image tagging, and gathering dataset. Therefore brutally merging models sounds feasible for me.

### Imporvement on model structure vs learnt experience ###

- [ch02/model_history](../ch02/model_history.md): Given the rich history since "NAI" and other datasets, SD1.X models after many iterations are still comparable to the new SDXL models with only a few iterations.

- [ch01/hires_fix](../ch01/hires_fix.md), [ch01/cfg_step](../ch01/cfg_step.md), [ch01/arb](../ch01/arb.md): The most noticeable (slight) difference is the lowerbound CFG and the upper bound of resolution. My recent artwork in both [SD1.X based](https://www.pixiv.net/en/artworks/111379481) and [SDXL based](https://www.pixiv.net/en/artworks/111558772) models are sharing similar parameters and image content (although the car shape in this comparasion is a lot wacky). With the claimed "1024 ARB" (and "trained with 2048x2048 images") for SD1.x models, comparing with "1024 ARB" SDXL models, generating images with 768x768 hires 2.0x or 1024x1024 hires 1.5x images still yields similar details. *However  "1024 ARB" SD1.x models are rare, and no one has merge them before.*

- *It is hard to compare, especially I don't have nice metrics to compare.* It will be benchmarked by [ch01/my_procedure](../ch01/my_procedure.md), to keep my justification consistant.

### Merging models from different background ###

- Here is a list of merged, or "may be merged" of models:

|Index|Model Name|Model source|Merged yet? (Baseline / Extended / In review)|
|---|---|---|---|
|01|[VBP](../ch02/f59359c175.md)|"NAI SFW"|Baseline|
|02|[CBP](../ch02/ae2b38ac14.md)|"NAI NSFW"|Baseline|
|03|[MzPikas TMND Enhanced](https://huggingface.co/ashen-sensored/mzpikas_tmnd_enhanced)|NAI + [OpenNiji](https://huggingface.co/ShoukanLabs/OpenNiji-V2) *Speculated*|Baseline|
|04|[DreamShaperV8](https://civitai.com/models/4384/dreamshaper)|"A>R" Merge, realistic nxxes|Baseline|
|05|[CoffeeWithLiquor](https://huggingface.co/StereoBartender/CoffeeWithLiquor)|NAI (Lots of LoRAs)|Baseline|
|06|[BreakDomain](https://civitai.com/models/117192/breakdomainowners-model-i-have-no-rights-if-he-want-it-will-be-taken-down)|NAI|Baseline|
|07|[AIWMix](https://civitai.com/models/74165?modelVersionId=78888)|["SD"](../ch97/0299d.md), |Baseline|
|08|[Ether Blu Mix](https://civitai.com/models/17427/ether-blu-mix)|Merges of famous A|Baseline|
|09|[majicMIX realistic](https://civitai.com/models/43331?modelVersionId=94640)|Merges of MJ + "2.5" + [NWSJ](https://civitai.com/models/53601/nwsjrealistic)|Baseline|
|10|[Silicon29](https://huggingface.co/Xynon/SD-Silicon)|MBW of "2.5"|Baseline|
|11|[BP](https://huggingface.co/Crosstyan/BPModel)|[ACertainty](ACertainty)|Extended|
|12|[CGA9](https://t.me/StableDiffusion_CN/1170018)|AutoMBW|Extended|
|13|[LimeREmix](https://civitai.com/models/153081?modelVersionId=23379)|Human evaluated merge|Extended|
|14|[CyberRealistic Classic](https://civitai.com/models/71185/cyberrealistic-classic)|Pure Realistic Merge|Extended
|15|[ORCHIDHEART](https://huggingface.co/reroti/ORCHIDHEART)|Similar to CGA|Extended|
|16|[BB95 Furry Mix](https://civitai.com/models/17649/bb95-furry-mix)|[E621](https://knowyourmeme.com/memes/sites/e621)|Extended|
|17|[Indigo Furry mix](https://civitai.com/models/34469?modelVersionId=167882)|[E621](https://knowyourmeme.com/memes/sites/e621)|Extended|
|18|[AOAOKO [PVC Style Model]](https://civitai.com/models/15509/aoaoko-pvc-style-model)|[PVC](https://huggingface.co/datasets/p1atdev/pvc)|Extended|
|xx|[ALunarDream](https://discord.com/channels/930499730843250783/1087111248447017172)|NAI (Style Blending)|*In review*|
|xx|[Dreamlike Anime](https://huggingface.co/dreamlike-art/dreamlike-anime-1.0)|Non NAI based Anime|*Rejected (legal issue)*|
|xx|[Marbel V182](https://discord.com/channels/1027129024054575174/1155074634274844693)|Human evaluated merge|*In review*|
|xx|[AIDv2.10](https://civitai.com/models/16828/aidv210-anime-illust-diffusion)|NAI (Style Blending)|*In review*|

- Note that all models are [abruptly replaced with SD1.4's Text Encoder.](https://huggingface.co/6DammK9/bpmodel-sd14-merge) Original desired contents (e.g. specific anime contents) will be disabled.

|Merge Batch|Description|
|---|---|
|Baseline|This model is **capable to output images well with 1024x1024 native, with great varity contents.** *Identifying Astolfo is a plus* (LAION has a few images of him).|
|Extended|This model is **either** capable to do any one of them above. It means that the model has experienced radical finetuning, and the output diversity is damaged. ~~(Or it is just too late to be spotted, such as 13)~~ |
|In review|This model **sounds** that it has been finetuned in a menaingful way. It is mostly not effective with great tradeoff, and it need to be carefully merged **under sequence** (i.e. very last).|

- Given the success of ["2.99D" models](../ch02/4de704d8.md) and ["2.5D" models](https://huggingface.co/WarriorMama777/OrangeMixs), I expect there will be suprise when I merge them together (however it is hard to preprocess the model, see below).

- Note that some of them are also merges of other models, I expect that I can be benefied from the inherited contents also, for example, *style embeddings* and more keywords.

- (Not proven) The *inheritance* is not straightforward, it may requires replacing the Text Encoder with the child's instead of the master SD1.x's. See below for how I discover the phenomenon.

### Nice merge will introduce "union" effect on prompt interpretation ###

- [ch01/merge](../ch01/merge.md): Although the MBW / LBW theory lacks of scientific proof, [autombw](https://github.com/Xerxemi/sdweb-auto-MBW) / [autombw v2](https://github.com/Xerxemi/auto-MBW-rt) reconstructed the optimization task / [model selection](https://en.wikipedia.org/wiki/Model_selection) into a ML task, treating MBW / LBW as a *framework with simplified parameter*, instead of directly applying domain knowledge.

- There are nice models based from manual MBW, such as [majicMIX](https://civitai.com/models/43331/majicmix-realistic), [GhostMix](https://civitai.com/models/36520?modelVersionId=76907), and autombw models such as [SD-Silicon](https://huggingface.co/Xynon/SD-Silicon) and [MzPikas TMND Enhanced](https://huggingface.co/ashen-sensored/mzpikas_tmnd_enhanced), and an unreleased "CGA" model, *they are showing ability to know more entities without sacrificing too much existing knowledges* (See [this artwork based from majicMIX](https://www.pixiv.net/en/artworks/110065358)). Seems that the variance can be a lot greater, resembling [my guess long time ago](../ch99/925997e9.md). Therefore it would support the "suprise" I have expected.

### The power of the original SD 1.X's Text Encoder ###

- [ch02/animevae_pt](../ch02/animevae_pt.md#extra-text-encoder): Other then VAE, *NAI also used SD's orignal TE*. This is special for SD1.X because the CLIP / ViT used *was trained with uncropped LAION dataset, including the NSFW words*. It is in theory knowing most vocabulary, even the token count is less then SDXL. It shuold be reminded that NSFW SDXL / SD2.X models are *almost inexist*, with a [little exception](https://cafeai.notion.site/WD-1-5-Beta-2-Release-Notes-2852db5a9cdd456ba52fc5730b91acfd). [Rare artwork done by me.](https://www.pixiv.net/en/artworks/105947222). It further supports "nice content may be better then nice structure".

- [ch03](../ch03): Hhowever, most finetuned models used [TTE (train text encoder)](https://github.com/kohya-ss/sd-scripts) to create "triger word" effect, but variance has been greatly sacrificed. Note that it is *highly doubtful* because most models are TTE enabled, and it is hard to proof or even verify.

### Verifying the merge is precise ###

- I experienced [floating point error](https://www.geeksforgeeks.org/floating-point-error-in-python/) while merging. *It is not merger error. This is natural for most programming languages.* The merged model must be verified with [toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit) to make sure **the offset counter must be (XXXX/0000/0000).** 

- I further verify [with the scripts extracting metadata in model](../ch97/extract_merge_info.js) [by batch](../ch97/batch_extract.cmd) to make sure I am merging the right model (however the "merge chain" is wiped when I reset the Text Encoder):

```json
{
    "__metadata__": {
        "sd_merge_recipe": {
            "type": "webui",
            "primary_model_hash": null,
            "secondary_model_hash": "aba1307666acb7f5190f8639e1bc28b2d4a1d23b92934ab9fc35abf703e8783d",
            "tertiary_model_hash": null,
            "interp_method": "Weighted sum",
            "multiplier": 0.125,
            "save_as_half": true,
            "custom_name": "08-vcbpmt_d8cwlbd_aweb5-sd",
            "config_source": 0,
            "bake_in_vae": "None",
            "discard_weights": "",
            "is_inpainting": false,
            "is_instruct_pix2pix": false
        },
        "format": "pt",
        "sd_merge_models": {
            "fe38511e88a8b7110a61658af6a0ff6a6b707852ff2893a38bc8fa0f92b3ace4": {
                "name": "07-vcbp_mtd8cwl_bdaw-sd.safetensors",
                "legacy_hash": "72982c20",
                "sd_merge_recipe": null
            },
            "aba1307666acb7f5190f8639e1bc28b2d4a1d23b92934ab9fc35abf703e8783d": {
                "name": "etherBluMix5-sd-v1-4.safetensors",
                "legacy_hash": "25d4f007",
                "sd_merge_recipe": null
            }
        }
    }
}
```

- For full receipe, see [receipe-10a.json](./receipe-10a.json).Replace with SD original CLIP / VAE to obtain "10", *however the equivalence may not in file hash precision because of floating point error.*

- Personally I prefer using [vae-ft-mse-840000-ema-pruned](https://huggingface.co/stabilityai/sd-vae-ft-mse-original/blob/main/vae-ft-mse-840000-ema-pruned.ckpt) for VAE, but I'll keep it neutral while merging.

- For the merge ratio, I *round to 3 d.p.* which is engough for the first 20 merges.

## My action list ##

- **Docuement first.** If you see any content not covered in this article, it is either an idea just appeared, or I really havn't considered. Most idea in this article is original and relies on my own experience. 

- **Recover, and even replace TE.** [Models have been uploaded to HuggingFace.](https://huggingface.co/6DammK9/bpmodel-sd14-merge) Thanks *@gesen2gee (Discord)* for mentioning [stable-diffusion-webui-model-toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit). After some simple test (make sure it can run, can being merged afterward), **I'll post into HuggingFace for reference.** [Here is the scirpt segment to remove TE.](https://github.com/CCRcmcpe/scal-sdt/blob/963ac6a20151139b90f4d0dc7216c036a57964cd/ckpt_tool.py#L40) Recovering them is unknown. Probably need to program it myself. [Here is a script potentially useful.](https://github.com/kohya-ss/sd-scripts/blob/main/tools/convert_diffusers20_original_sd.py) 

- **Baseline merge: Uniform merge a.k.a bagging.** [Models have been uploaded to HuggingFace.](https://huggingface.co/6DammK9/AstolfoMix) As easy as the "Checkpoint Merger" does. To make sure all of them are in [uniform distribution](https://en.wikipedia.org/wiki/Discrete_uniform_distribution), merge with weight $1/x$ for $x > 1$. Therefore 50% for the 2nd model, 33% for the 3rd model, and so on. The process should be **parameterless**. 

- **Proposed merge: autombw.** Use [autombw v2](https://github.com/Xerxemi/auto-MBW-rt). Technical details are under analysis. It has been known as *memory intensive* instead of *GPU intensive*. I have some ex-mining SSDs which may help the process. **This will not happen soon.** I didn't expect for merging 10+ models. [Boosting](https://chih-sheng-huang821.medium.com/%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-ensemble-learning%E4%B9%8Bbagging-boosting%E5%92%8Cadaboost-af031229ebc3) in such scale requires a new software from ground up. *I am still using pure GUI with minimum coding.*

- [Get a capable GPU to output such kind of images.](../ch04/readme.md#chapter-04b-extra-making-use-of-m40-24gb-for-generating-large-images) I'm suprised that *it pulls 19GB of VRAM already*.

## Finding on "Baseline Merge" ##

### Boosted Resolution ###

- *Current resolution limit is 1280x1280 (native T2I), hires 1.4x (2080Ti 11G), or 2.0x (Tesla M40)*.

![230958-132385090-2688-1536-4.5-256-20230930203540.png](img/230958-132385090-2688-1536-4.5-256-20230930203540.png)

```
parameters
(aesthetic:0), (quality:0), (solo:0), (boy:0), (ushanka:0.98), [[braid]], [astolfo], [[moscow, russia]] 
Negative prompt: (worst:0), (low:0), (bad:0), (exceptional:0), (masterpiece:0), (comic:0), (extra:0), (lowres:0), (breasts:0.5) 
Steps: 256, Sampler: Euler, CFG scale: 4.5, Seed: 132385090, Size: 1344x768, Model hash: 6ffdb39acd, Model: 10-vcbpmtd8_cwlbdaw_eb5ms29-sd, VAE hash: 551eac7037, VAE: vae-ft-mse-840000-ema-pruned.ckpt, Denoising strength: 0.7, Clip skip: 2, FreeU Stages: "[{\"backbone_factor\": 1.2, \"skip_factor\": 0.9}, {\"backbone_factor\": 1.4, \"skip_factor\": 0.2}]", FreeU Schedule: "0.0, 1.0, 0.0", Hires upscale: 2, Hires steps: 64, Hires upscaler: Latent, Dynamic thresholding enabled: True, Mimic scale: 1, Separate Feature Channels: False, Scaling Startpoint: MEAN, Variability Measure: AD, Interpolate Phi: 0.7, Threshold percentile: 100, Version: v1.6.0
```

### Associative property ###

- [Associative property](https://en.wikipedia.org/wiki/Associative_property) has been observed. First, these are comparasion between 10 models without pre processing:

![xyz_grid-0184-3972813705-25600-2067-4.5-48-20230929235846.jpg](img/xyz_grid-0184-3972813705-25600-2067-4.5-48-20230929235846.jpg)

- And then mixing them together, you will find the [intelligence agent](https://en.wikipedia.org/wiki/Intelligent_agent) *successfully choose to "draw" the most confident one*:

![xyz_grid-0183-3972813705-25600-2067-4.5-48-20230929231817.jpg](img/xyz_grid-0183-3972813705-25600-2067-4.5-48-20230929231817.jpg)

- This time all models are replaced with original SD's CLIP / Text Encoder:

![xyz_grid-0182-3972813705-25600-2069-4.5-48-20230929185331.jpg](img/xyz_grid-0182-3972813705-25600-2069-4.5-48-20230929185331.jpg)

- Finally mixing them together again, now it is capable to "draw" in 1344x768x2.0, which SD was supposed to be trained with 512px images:

![xyz_grid-0181-3972813705-25600-2067-4.5-48-20230929010338.jpg](img/xyz_grid-0181-3972813705-25600-2067-4.5-48-20230929010338.jpg)

```
(aesthetic:0), (quality:0), (car:0), [[mercedes]], (1girl:0), (boy:0), [astolfo] Negative prompt: (worst:0), (low:0), (bad:0), (exceptional:0), (masterpiece:0), (comic:0), (extra:0), (lowres:0), (breasts:0.5) Steps: 48, Sampler: Euler, CFG scale: 4.5, Seed: 3972813705, Size: 1024x576, Model hash: 8cbe307462, Model: VBP23-1024-ep49-sd-v1-4, VAE hash: 551eac7037, VAE: vae-ft-mse-840000-ema-pruned.ckpt, Denoising strength: 0.7, Clip skip: 2, FreeU Stages: "[{\"backbone_factor\": 1.2, \"skip_factor\": 0.9}, {\"backbone_factor\": 1.4, \"skip_factor\": 0.2}]", FreeU Schedule: "0.0, 1.0, 0.0", Hires upscale: 2.5, Hires upscaler: Latent, Dynamic thresholding enabled: True, Mimic scale: 1, Separate Feature Channels: False, Scaling Startpoint: MEAN, Variability Measure: AD, Interpolate Phi: 0.7, Threshold percentile: 100, Script: X/Y/Z plot, X Type: Checkpoint name, X Values: "VBP23-1024-ep49-sd-v1-4.safetensors [8cbe307462],02-vbp23-cbp2-sd.safetensors [6075160ea7],03-vcbp-mzpikas_tmnd-sd.safetensors [4f4da1e956],04-vcbp_mzpt_d8-sd.safetensors [4b36d29be3],05-vcbp_mtd8_cwl-sd.safetensors [84c1865c1e],06-vcbp_mtd8cwl_bd-sd.safetensors [dd1d0b7fc4],07-vcbp_mtd8cwl_bdaw-sd.safetensors [fe38511e88],08-vcbpmt_d8cwlbd_aweb5-sd.safetensors [b21ea2b267],09-vcbpmt_d8cwlbd_aweb5m-sd.safetensors [f32f9b8e99],10-vcbpmtd8_cwlbdaw_eb5ms29-sd.safetensors [6ffdb39acd]", Version: v1.6.0
```

- (*Diagram coming soon*) The "merge pipeline" is drawn below. With "uniform merge", merge order is arbitrary, you will get the same mixture eventually. *You can verify if you "bag of SD" is performing as expected.*

$$merge(merge(model_1,model_2,\tfrac{1}{2}),model_3,\tfrac{1}{3}) \equiv merge(merge(model_2,model_3,\tfrac{1}{2}),model_1,\tfrac{1}{3}) \equiv merge_3(model_1,model_2,model_3,\tfrac{1}{3}) $$

- Also, merging 10 "CLIP / TE reseted" models is same as merg 10 models and then "reset CLIP / TE". *In practice, you may suffer [floating point error](https://www.geeksforgeeks.org/floating-point-error-in-python/), making the "hash" is different in [toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit)*:

$$ResetCLIP(merge(model_1,model_2,\tfrac{1}{2})) \equiv merge(ResetCLIP(model_1),ResetCLIP(model_2),\tfrac{1}{2})$$

### Swapping CLIP / TE with other models ###

- You can switch Text Encoder to what you're familiar with. The model still remember how it looks. However it tends to be effective for an entity instead of abstract art style (including nsfw).

![xyz_grid-0106-978318572-3072-1012-4.5-48-20230922003223.png](img/xyz_grid-0106-978318572-3072-1012-4.5-48-20230922003223.png)

```
parameters
(aesthetic:0), (quality:0), (solo:0), (1girl:0), (gawr_gura:0.98)
Negative prompt: (worst:0), (low:0), (bad:0), (exceptional:0), (masterpiece:0), (comic:0), (extra:0), (lowres:0)
Steps: 48, Sampler: Euler, CFG scale: 4.5, Seed: 978318572, Size: 768x768, Model hash: d94d7363a0, Model: 08-vcbpmt_d8cwlbd_aweb5-cwl, VAE hash: 551eac7037, VAE: vae-ft-mse-840000-ema-pruned.ckpt, Clip skip: 2, Version: v1.6.0
```

### "Uniform merge" as a variant of bagging / ensemble averaging ### 

- [This is random gold medal Kaggle notebook using an ensemble of 10 models with average weight first, then further optimize with Regressor OVER the weights.](https://www.kaggle.com/code/ipythonx/tf-keras-hybrid-efficientnet-swin-transformer-tpu). 

- ["Ensemble" is a well known method on ML field, and it is possible to have ensemble over neural networks.](https://towardsdatascience.com/ensembles-the-almost-free-lunch-in-machine-learning-91af7ebe5090#2871) ["Ensemble averaging" without soft voting is the most simple approach, it shows improvement on ML tasks by resolving bias-variance dilemma in the fundamental way.](https://towardsdatascience.com/ensemble-averaging-improve-machine-learning-performance-by-voting-246106c753ee) [Hinted by "evolutionary computing",](https://en.wikipedia.org/wiki/Ensemble_averaging_(machine_learning)) ["polyak averaging" (average out models in different aspect, including time) makes the model easier to converge while transversing in high dimensional latent space, i.e. generating sementic fragements from noise.](https://machinelearningmastery.com/polyak-neural-network-model-weight-ensemble/) [Althoguh it is a technique in RL field,](https://arxiv.org/abs/2112.14582) *it is applicable on open-end, real-world problem which communities keep envolving / iterlating the same SD model in their "artistic way" across this year (2022 Aug - 2023 Sept).* [Such artistic problem has been discused, and attempted to be formulated ("latent space") before SD or even LDA model, as soon as StyleGAN in 2019, I believe that such complex problem can be related in interdisciplinary manner, like computer vision / computer graphic in BIM / GIS / CFD, and even acoustic.)](../ch01/aesthetic.md) 

### Phenomenon: Convergent to a equilibrium in an arbitary space ###

- **Note that it is not validated or verified, even if it is possible to do so in CS + Art manner.** This should depends on [model selection](https://en.wikipedia.org/wiki/Model_selection), but the [dimensionless]( dimensionless) [MSE](https://en.wikipedia.org/wiki/Mean_squared_error) somehow show [correlation](https://en.wikipedia.org/wiki/Correlation) to the image difference in the xy plots (Astolfo with Mercedes) above. *If the correlation is legit*, the equilibrium will let the intelligence agent try to draw most objects with lowest variance disregarding any art style it have learnt (almost no impact on bias). 

![am0_unet_vg.png](../ch03/v2a/img/am0_unet_vg.png)

![am2_unet_vg.png](../ch03/v2a/img/am2_unet_vg.png)

- The proof of correlation should be an extended work in [ch03](../ch03/readme.md) but I have no time to write the script. Image difference can be calculated with MSE with [SIFT](https://en.wikipedia.org/wiki/Scale-invariant_feature_transform) or encoded by [Swin Transformer](https://huggingface.co/docs/transformers/model_doc/swin). [So the proof is left as an exercise](https://matheducators.stackexchange.com/questions/1896/are-the-words-easy-basic-clearly-obviously-etc-ever-helpful).
