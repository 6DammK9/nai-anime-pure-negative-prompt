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

- [Started from the discovery of "associative property"](./README.MD#associative-property), [and the independent consideration of model components](./README_SD2.MD#considering-clip--te-combinations-individually), I think it is plausible to follow a [greedy approach](https://en.wikipedia.org/wiki/Greedy_algorithm). Breaking the massive problem into subproblems, and naively choose the best (or good) results, does bring me towards the desired effect. Also, [the special case of add diff and convergence of averaging](./README.MD#findings-on-astolfomix-21b) supports my view to not considering too much on [covariance](https://en.wikipedia.org/wiki/Covariance) between components. *I have not experiened unexpected result yet, when I confirm I'm following my procedure correctly.*

- Then, the procedure is further extended from SD2 (and SD1): Since SDXL has 2 CLIPs, I compare the CLIPs seperately. The starting point is still blindly average out all discovered models.

## CLIP Recipe ##

```
te0: --,--,03,05,--,10,11,--,--,16,17,09a,10a,20,11a,22,23,24,25,26,27,32,--,36,--,--,41,--=19
te1: 01,02,03,05,06,10,--,12,14,16,17,09a,10a,20,11a,22,--,24,25,26,27,32,33,36,37,38,41,42=26
te2: 01,--,03,05,06,10,--,--,--,16,17,09a,10a,20,11a,22,--,24,25,--,27,32,33,36,37,38,41,--
=sd: --,--,03,--,--,10,--,12,--,16,--,-18,-19,--,---,--,--,--,25,--,--,--,--,--,--,--,--,--

12te0

te0:--,--,05,--,11,--,--,17,20,11a,22,23,24,25,26,27,32,--,36,--,--,41,--
te1:01,02,05,06,--,12,14,17,20,11a,22,--,24,25,26,27,32,33,36,37,38,41,42

x01te1-AstolfoMix-_x01_x02

unet: 01,02,06,07,09,10,11,12,13,15,16,17,20,21,22,23,25,26,27,28,30,31,32,33,34,--,37,38,39,40,42,43,44=32
nsfw: 01,--,06,07,--,--,11,12,13,15,--,--,20,21,22,23,--,--,27,--,--,31,--,--,--,36,--,--,--,40,--,43,--=16
x01a: 01,02,--,--,09,10,11,12,--,15,16,--,--,21,22,--,25,26,27,28,--,31,32,33,34,--,37,38,39,40,--,43,44

base=x17-AstolfoMix-x13te0x14te1.safetensors
nsfw=x11c-AstolfoMix-x13te0x14te1.safetensors
```

![img/xyz_grid-0700-1355548248-10080-1631-4.5-48-20240204013956.jpg](img/xyz_grid-0700-1355548248-10080-1631-4.5-48-20240204013956.jpg)