# Chapter 05-XL: Astolfo mix XL. #

- (Coming soon) [CivitAI model page.](https://civitai.com/models/255754) The style there is a bit different.

- [HuggingFace model page.](https://huggingface.co/6DammK9/AstolfoMix-XL) The style is also different.

- (Coming soon) [CivitAI article page.](https://civitai.com/articles/3409) Summary of here (as additional content with SD1).
## What is the mix? ##

- Currently, it is an Ensemble averaging ~~Uniform merge~~ of 32 UNETS + (19+26) CLIPS (from 21 models), selected from 44 discovered SDXL models.

- I will include *exclusive findings* here only. Read the ["master" article](./README.MD) and ["SD2" article](./README_SD2.MD) *(yes it applies also)* for general ideas.

## Generated Images ##

- ["AstolfoMix" in Pixiv.](https://www.pixiv.net/en/tags/AstolfoMix/artworks)

## Why make such a model? ##

- Given the ~~asserted~~ success of previous experience (SD1 and SD2), I think I shuold keep it up on recent architecture, SDXL ~~Turbo / LCM will be examined  later~~, which is larger and more complicated then both SD1 and SD2, and try to make the model as *useful* as the SD2 version.

## My discoveries ##

### It is using the exact same CLIP as SD1 ###

- [ch03/view_unet/view_unet.ipynb](../ch03/view_unet/view_unet.ipynb): You will find that [the config of TE0 from SDXL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/text_encoder/config.json) is the exact same of [the config in SD1](https://huggingface.co/runwayml/stable-diffusion-v1-5/blob/main/text_encoder/config.json). 

This is directly quoted from HuggingFace (SDXL):

> Model Description: This is a model that can be used to generate and modify images based on text prompts. It is a Latent Diffusion Model that uses two fixed, pretrained text encoders (OpenCLIP-ViT/G and CLIP-ViT/L).3

And then SD1:

> Model Description: This is a model that can be used to generate and modify images based on text prompts. It is a Latent Diffusion Model that uses a fixed, pretrained text encoder (CLIP ViT-L/14) as suggested in the Imagen paper.

It is the *same* ViT-L. However we all noticed "finetuned models" are all "SD models". Can we have other methods to check?

- Yes. Once again we use [stable-diffusion-webui-model-toolkit](https://github.com/arenasys/stable-diffusion-webui-model-toolkit) by *exporting CLIP (not CLIP-AUX) from SDXL and then import it to SD1.* And... it shows the clean `0000` hash. Note that `21b` is the latest model in SD1, and `x39a` is the current version of merged SDXL, and `_x25` is the original SDXL model, `te2` means "both CLIPs are explicitly imported".

![240206.JPG](img/240206.JPG)

- Making the mixed CLIP from `x39a` will obviously yield a different image. `x25a` is same as `_x25`.

![xyz_grid-0669-3972813705-3072-817-4-48-20240131004251.png](img/xyz_grid-0669-3972813705-3072-817-4-48-20240131004251.png)

### Will Greedy approach work? ###

- [Started from the discovery of "associative property"](./README.MD#associative-property), [and the independent consideration of model components](./README_SD2.MD#considering-clip--te-combinations-individually), I think it is plausible to follow a [greedy approach](https://en.wikipedia.org/wiki/Greedy_algorithm). By [breaking the massive problem into subproblems](https://medium.com/@srosamazaid/the-greedy-algorithm-pattern-an-in-depth-analysis-7bb28d5dbfa7), and naively choose the best (or good) results, brings me towards the desired effect. Also, [the special case of add diff and convergence of averaging](./README.MD#findings-on-astolfomix-21b) supports my view to not considering too much on [covariance](https://en.wikipedia.org/wiki/Covariance) between components. *I have not experiened any unexpected result yet, when I confirm I'm following my procedure correctly.*

- Also, [since model selection is a combination optimization problem](./README_SD2.md#model-selection), choosing it by *intuition* may not work when the model count is large (**currently discovered 44 models**), such greedy approach can *estimate* and make prediction from a NP time complexity into linear time ($O(N)$), with only a few iterlations of comparasions, and control the space complexity even **it already used over 1TB on storing intermediate merged models.** Unless I develop a N-way merger from scratch, space requirement will outnumber the traditional fine tune approach also. ~~Looks like I'm trying to rationalize a random approach, but I really don't have solid idea since there is absolutely no reference in this world.~~

- *I may try applying score metric, or algorithms on model comparasions on model selection, instead of human evalulation, although it is effective. Hopefully I don't have to code everything from scratch.*

- Therefore, the procedure is further extended from SD2 (and SD1): Since SDXL has 2 CLIPs, I compare the CLIPs seperately. The starting point is still blindly average out all discovered models.

### More findings on merging CLIP and MBW layers ###

- *This is discovered by chance.* From paper ["Localizing and Editing Knowledge in Text-to-Image Generative Models"](https://arxiv.org/abs/2310.13730),*concepts are being represented by scattered activated neuron / layers in UNET with distribution, but being centralized within a single neuron in CLIP.

> Notably, we find a distinct distribution of causal states across visual attributes in the UNet, while the text-encoder maintains a single causal state.

![24020903.JPG](img/24020903.JPG)

![24020904.JPG](img/24020904.JPG)

- It implies the great risk and scarification with "Train Text Encoder" option while fintuning a massive base model, and more important, **merging with different finetuned CLIPs**. This problem is dodged in SD1, [because I sticked with the OG CLIP](./README.MD#the-power-of-the-original-sd-1xs-text-encoder), and experienced in SD2. Agressively merging 2 CLIPs in the SDXL will make the model failed to understand most concepts. More in the next section.

## Discovered models ##

- There is 44 models discovered, with some of them **cannot be swapped between components, or mergeable.** A1111's OG merger requires valid model metadata to operate, which some models may have its own metadata and fails the merge, meanwhile some models have deviation in model structure (even it may works well in WebUI) and make the toolkit failed to swap components from them.

- For example, it will show "VAE-v1-BROKEN" when parsing the model: 

![24020901.JPG](./img/24020901.JPG)

- And it may throw error while merging:

![24020902.JPG](./img/24020902.JPG)

- Here is a full list of discovered models: 

<details>
    <summary>Table with 40+ rows. Click to open.</summary>

*mega table coming soon*

```log
_x01-deepDarkHentaiMixNSFW_v12.safetensors
_x02-animeAntifreezingSolutionXL_v10.safetensors
_x03-hsxl_base_1.0.f16.safetensors
_x04-OpenDalleV1.1.safetensors
_x05-copaxTimelessxlSDXL1_v8.safetensors
_x06-juggernautXL_v8Rundiffusion.safetensors
_x07-kohakuXLBeta_beta7.safetensors
_x08-animagineXLV3_v30.safetensors
_x09-animeboysxl_v10.safetensors
_x10-dreamshaperXL_alpha2Xl10.safetensors
_x11-SDXLRonghua_v40.safetensors
_x12-bluePencilXL_v310.safetensors
_x13-leosamsHelloworldSDXL_helloworldSDXL32DPO.safetensors
_x14-ponyDiffusionV6XL_v6.safetensors
_x15-animagineXL_v20.safetensors
_x16-wdxl-aesthetic-0.9.safetensors
_x17-leosamsHelloworldSDXLModel_helloworldSDXL10.safetensors
_x18-nekoray-xl-1.5m-fp16mixed_e02.safetensors
_x19-nekoray-xl-1.5m-pdg32_e02.safetensors
_x20-explicitFreedomNSFW_beta.safetensors
_x21-nd-run8-weighted-3.safetensors
_x22-kohakuXL_alpha7.safetensors
_x23-nekorayxl_v06W3.safetensors
_x24-SwimInLatent-alpha.fp16.safetensors
_x25-sd_xl_base_1.0.safetensors
_x26-enjoyXLAdvancedEdition_v7AdvancedVersion.safetensors
_x27-explicitFreedomNSFW_alpha.safetensors
_x28-heartOfAppleXL_v10.safetensors
_x29-kohakuXLGamma_rev1.safetensors
_x30-aamXLAnimeMix_v10.safetensors
_x31-counterfeitxl_v25.safetensors
_x32-enjoyPandoraXL_v10.safetensors
_x33-4Guofeng4XL_v12.safetensors
_x34-animeIllustDiffusion_v061.safetensors
_x35-brightprotonukeBPNNo_bpn13.safetensors
_x36-devlishphotorealism_sdxl15.safetensors
_x37-himawarimix_xlV4.safetensors
_x38-aio_v10.safetensors
_x39-sakumix_v10.safetensors
_x40-218xl_.safetensors
_x41-riotDiffusionXLLeagueOfLegendsSplash_v20.safetensors
_x42-himawarimix_xlV5.safetensors
_x43-SDXLAnimeBulldozer_v20.safetensors
_x44-kohakuXLGamma_rev2.safetensors
_x45-awmo-xl.safetensors
_x46-realvisxlV30Turbo_v30Bakedvae.safetensors
```

</details>

## Deriving the "recipe" a.k.a model selection ##

- For selecting CLIPs, UNET is `x39a` which is the global average model. VAE is the original VAE of SDXL.

- First I choose **CLIP**, or `conditioner.embedders.0`:

![xyz_grid-0657-755545524-18144-1446-4.5-48-20240128171125.jpg](./img/xyz_grid-0657-755545524-18144-1446-4.5-48-20240128171125.jpg)

![xyz_grid-0660-755545524-20160-1446-4.5-48-20240128190750.jpg](./img/xyz_grid-0660-755545524-20160-1446-4.5-48-20240128190750.jpg)

![xyz_grid-0663-755545524-20160-1446-4.5-48-20240129024005.jpg](./img/xyz_grid-0663-755545524-20160-1446-4.5-48-20240129024005.jpg)

![xyz_grid-0666-755545524-14784-963-4.5-48-20240130011803.jpg](./img/xyz_grid-0666-755545524-14784-963-4.5-48-20240130011803.jpg)

- Then I choose *CLIP-AUX**, or `conditioner.embedders.1`:

![xyz_grid-0658-755545524-18144-1446-4.5-48-20240128171148.jpg](./img/xyz_grid-0658-755545524-18144-1446-4.5-48-20240128171148.jpg)

![xyz_grid-0661-755545524-20160-1446-4.5-48-20240128191024.jpg](./img/xyz_grid-0661-755545524-20160-1446-4.5-48-20240128191024.jpg)

![xyz_grid-0664-755545524-20160-1446-4.5-48-20240129024047.jpg](./img/xyz_grid-0664-755545524-20160-1446-4.5-48-20240129024047.jpg)

![xyz_grid-0667-755545524-14784-963-4.5-48-20240130011818.jpg](./img/xyz_grid-0667-755545524-14784-963-4.5-48-20240130011818.jpg)

- For reference, I also see what will happen when I apply both CLIPs:

![xyz_grid-0659-755545524-18144-1446-4.5-48-20240128172917.jpg](./img/xyz_grid-0659-755545524-18144-1446-4.5-48-20240128172917.jpg)

![xyz_grid-0662-755545524-20160-1446-4.5-48-20240128192923.jpg](./img/xyz_grid-0662-755545524-20160-1446-4.5-48-20240128192923.jpg)

![xyz_grid-0665-755545524-20160-1446-4.5-48-20240129025805.jpg](./img/xyz_grid-0665-755545524-20160-1446-4.5-48-20240129025805.jpg)

![xyz_grid-0668-755545524-14784-963-4.5-48-20240130013447.jpg](./img/xyz_grid-0668-755545524-14784-963-4.5-48-20240130013447.jpg)

- For selecting UNETs, CLIPs will be the merged model which is `x13te0` and `x14te1`. Note that I have reused the merge models to save disk space.

![xyz_grid-0684-755545524-12096-974-4.5-48-20240203134450.jpg](./img/xyz_grid-0684-755545524-12096-974-4.5-48-20240203134450.jpg)

![xyz_grid-0685-755545524-13440-1098-4.5-48-20240203134527.jpg](./img/xyz_grid-0685-755545524-13440-1098-4.5-48-20240203134527.jpg)

![xyz_grid-0686-755545524-13440-963-4.5-48-20240203135733.jpg](./img/xyz_grid-0686-755545524-13440-963-4.5-48-20240203135733.jpg)

![xyz_grid-0687-755545524-14784-963-4.5-48-20240203135824.jpg](./img/xyz_grid-0687-755545524-14784-963-4.5-48-20240203135824.jpg)

- Afterthat, I record all the accept model IDs and start merging pairwise. 

- This time [parallel merge](https://en.wikipedia.org/wiki/Merge_algorithm) **is required.** Storing around 6x40 SDXL models requires **around 1.5TB in disk space**, therefore I must try to reuse models as much as possible. Moreover, with this shear amount of model counts, making image preview on them are not fesiable.

### Selected models ###

- `te0`: Models selected for using the **CLIP**, or `conditioner.embedders.0`. 

- `te1`: Models selected for using the **CLIP-AUX**, or `conditioner.embedders.1`. 

- `te2`: Models looks acceptable with both CLIPs applied. Not for selection, just for reference.

- `=sd`: Models has the exact same CLIP pair as the original SDXL `_x25`.

- `--` is used for placeholder because I need to figure out the model pairs to be merged.

- Total / subtotal count will be shown as `=xx`.

- `xxa` e.g. `09a` is the merge of `_x17` and `_x18`, because of model deviation. It introduce some error on expected model weight, but will be negligible when the scale is large.

```
te0: --,--,03,05,--,10,11,--,--,16,17,09a,10a,20,11a,22,23,24,25,26,27,32,--,36,--,--,41,--=19
te1: 01,02,03,05,06,10,--,12,14,16,17,09a,10a,20,11a,22,--,24,25,26,27,32,33,36,37,38,41,42=26
te2: 01,--,03,05,06,10,--,--,--,16,17,09a,10a,20,11a,22,--,24,25,--,27,32,33,36,37,38,41,--=21
=sd: --,--,03,--,--,10,--,12,--,16,--,-18,-19,--,---,--,--,--,25,--,--,--,--,--,--,--,--,--=7
```
- Excluding the `=sd` for the actual merge will be shown below. Intermediate model name will be `x01te1-AstolfoMix-_x01_x02`.

```
te0:--,--,05,--,11,--,--,17,20,11a,22,23,24,25,26,27,32,--,36,--,--,41,--=14
te1:01,02,05,06,--,12,14,17,20,11a,22,--,24,25,26,27,32,33,36,37,38,41,42=21
```

- `unet`: Models selected for using the UNET.

- `nsfw`: Models selected for using the UNET. This time I used a NSFW prompt for test.

- To keep it easy to trace (originaly it is 33 / 15), I adjust it to be a perfect $2^n$. It will be handy for future merge, when new model appears.

- `x01a`: Model pairs which are already available for merge. Therefore I can reuse for saving disk space, a lot.

```
unet: 01,02,06,07,09,10,11,12,13,15,16,17,20,21,22,23,25,26,27,28,30,31,32,33,34,--,37,38,39,40,42,43,44=32
nsfw: 01,--,06,07,--,--,11,12,13,15,--,--,20,21,22,23,--,--,27,--,--,31,--,--,--,36,--,--,--,40,--,43,--=16
x01a: 01,02,--,--,09,10,11,12,--,15,16,--,--,21,22,--,25,26,27,28,--,31,32,33,34,--,37,38,39,40,--,43,44
```
- Finally here is the result model name:

```
base=x17-AstolfoMix-x13te0x14te1.safetensors
nsfw=x11c-AstolfoMix-x13te0x14te1.safetensors
```

- File list as the full merging list will be provided soon.

## Finding on "SDXL Baseline Merge" ##

- Merging a pair of SDXL models requires around 60-75 seconds. Swapping components also takes another 60 seconds to operate. Total merging time reached almost 2 hours.

*coming soon*

![img/xyz_grid-0700-1355548248-10080-1631-4.5-48-20240204013956.jpg](img/xyz_grid-0700-1355548248-10080-1631-4.5-48-20240204013956.jpg)