# Quick Survey on the rectified flow #

- Originated in [this paper](https://arxiv.org/abs/2209.03003). [Codebase](https://github.com/gnobitab/RectifiedFlow/blob/main/ImageGeneration/sampling.py#L68) shows that it expects plain Euler sampler only. It also expects [flow matching](./flowmatching.md) and [v-prediction](./vpred.md). This will be discussed again in below.

- [Interactive article explaining the theory and comparasions.](https://diffusionflow.github.io/)

![26010403.jpg](./img/26010403.jpg)

- Featured and cited in [SD3](https://arxiv.org/abs/2403.03206). [SD3 used many new theories, not just RF.](https://github.com/mini-sora/minisora/blob/main/notes/SD3_zh-CN.md)

- In contrast, original SD use *probability flow*. 

- [A1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/16030) supports SD3 out of the box. From the [issue](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/16378) regarding flux support, sampler should be limited to [Euler](./k_euler.md) only. Besides A1111, ComfyUI and [ReForge](https://github.com/Panchovix/stable-diffusion-webui-reForge) should support Flux out of the box, implies to Rectified Flow also. See [flow matching](./flowmatching.md#training--inference-with-sdxl-models) for details.

> (RD LoRA) Sampling method: Euler, DPM

> (NAI-RF) Sampler: Euler, Euler CFG++ DO NOT USE ANCESTRAL SAMPLERS!

- For trainer support, there is no direct indication, but from [this PR](https://github.com/kohya-ss/sd-scripts/pull/2037), it is probably supported as part of SD3 / Flux? [This fork](https://github.com/bluvoll/sd-scripts) has mentioned rectified flow also.

- [Rectified Diffusion](https://arxiv.org/abs/2410.07303) has been proposed afterward, [codebase](https://github.com/G-U-N/Rectified-Diffusion) and [kohyas based training script](https://github.com/RimoChan/NoobAIXL-Rectified) are developed and yielding a [LoRA](https://civitai.com/models/1355945) suppressing the oridinary timestep distillation training.

![26010401.jpg](./img/26010401.jpg)

- This raise a question: Does the objective / direction aligned across the *Rectification* approach?

> (SD3) Compared to diffusion models, they can result in ODEs that are faster to simulate than the probability flow ODE associated with diffusion models. Nevertheless, they do not result in optimal transport solutions, and multiple works aim to minimize the trajectory curvature further.

> (RD) Comprehensive comparisons on rectification, distillation and phased OED segmentation demonstrate our method achieves superior trade-off between generation quality and training efficiency over rectified flow-based models.

> (RD LoRA) *Sampling steps: 4. CFG scale: 1~1.5.*

> (NAI-RF) Rectified Flow is indeed the next step in SDXL's improvement efforts... *Steps: 20-28*

- From SD3 paper, it has perfomed some basic comparasion across `eps/linear`, `v/linear`, and `rf/lognorm(0,1)`.

> Rectified flow formulations generally perform well and, compared to other formulations, their performance degrades less when reducing the number of sampling steps.

![26012501.jpg](./img/26012501.jpg)

- Meanwhile, there is no direct indication that *inference code must be adapted when the training timestep distribution has been changed.*

- See [my further study](../ch06/sd-scripts-runtime/readme.md#260125-code-review-before-training) on additional algorithms used by SD3 / Flux, without switching models. [This blog](https://zhouyifan.net/2024/09/03/20240809-flux1/) and [this article](https://github.com/mini-sora/minisora/blob/main/notes/SD3_zh-CN.md) will be very useful to understand addtional concepts. I'll keep this article RF exclusive.

### Examples of SDXL Rectified flow ### 

- [Experimental NoobAI with Rectified Flow + EQ-VAE](https://civitai.com/models/2071356/experimental-noobai-with-rectified-flow-eq-vae?modelVersionId=2343811) by the author of the trainer fork.

- [CabalResearch/NoobAI-RectifiedFlow-Experimental](https://huggingface.co/CabalResearch/NoobAI-RectifiedFlow-Experimental) by the... *same author*?

- [WAI-illustrious-Rectified-4Steps](https://civitai.com/models/1355945). Note: *Rectified Diffusion*.

- [Wahtastic_FLOW_V10](https://huggingface.co/VelvetToroyashi/WahtasticMerge/blob/main/Wahtastic_FLOW_V10.safetensors) from [VelvetToroyashi/WahtasticMerge](https://huggingface.co/VelvetToroyashi/WahtasticMerge).

### Examples of non-sdxl Rectified flow ### 

- ["GRINP"](https://huggingface.co/yoinked/wan-22-experiments/blob/main/not-wan/GRINP.comfy.2.safetensors) *Added by request, unknown arch*

### Extra: EQ-VAE ###

- Written to have any chance to run the bundled "NAI-RF" model.

- Origin of EQ-VAE: [arxiv paper](https://arxiv.org/abs/2502.09509), [EQ-SDXL-VAE](https://huggingface.co/KBlueLeaf/EQ-SDXL-VAE).

> This model is heavily finetuned from SDXL-VAE and introduce a totally new latent space. YOU CAN'T USE THIS ON YOUR SDXL MODEL.

- ["EQB7" VAE](https://huggingface.co/Anzhc/MS-LC-EQ-D-VR_VAE/blob/main/EQB7.safetensors), bundled [Noobai11EQB7](https://huggingface.co/Anzhc/Noobai11-EQ/blob/main/Noobai11EQB7.safetensors). [CivitAI mirror](https://civitai.com/models/1835161/noob11eps-eq).

- The behaviour matches the model description. Both "oversharpening and ringing" and "blurry" are identified.

> This is a finetuned SDXL VAE, adapted with new regularization, and other techniques. You can use this with your existing SDXL model, but image will be quite artefacting, particularly - oversharpening and ringing. This VAE is supposed to be used for finetune, after that images will become normal. But be aware, compatibility with old VAEs, that are not EQ, will be lost(They will become blurry).

- However, the required *reflection padding* may tolerate *zero padding* as well. [Code reference in A1111.](https://github.com/AUTOMATIC1111/stable-diffusion-webui/blob/master/modules/sd_hijack.py#L318)

![xyz_grid-0079-1363847456-2112-2954-4-48-20260104120802.jpg](./img/xyz_grid-0079-1363847456-2112-2954-4-48-20260104120802.jpg)

### Image comparasion ###

- 48 steps as usual. The vpred config has applied (so I compared with [AC](../ch05/README_AC.md)).

![xyz_grid-0081-1363847456-2112-2954-4-48-20260104124840.jpg](./img/xyz_grid-0081-1363847456-2112-2954-4-48-20260104124840.jpg)

- Lowered to 8 steps. *I believe that A1111 should have some works to do for flow matching, however the VAE / vpred part is solved.*

![xyz_grid-0082-1363847456-2112-2954-4-8-20260104125121.jpg](./img/xyz_grid-0082-1363847456-2112-2954-4-8-20260104125121.jpg)

- Joining the original [~~flow matching~~ rf](https://huggingface.co/nyanko7/nyaflow-xl-alpha) model. Notice the difference of sampling steps. *It is hard to imagine the middle model is trained from SDXL 0.9 instead of NoobAI, meanwhile approaches are very different. Model publish time: 2511, 2407, 2510.*

![xyz_grid-0086-1363847456-2880-5706-4-4-20260104174810.jpg](./img/xyz_grid-0086-1363847456-2880-5706-4-4-20260104174810.jpg)

- Switch to short prompt, in 8 steps.

![xyz_grid-0085-2976896777-2304-1674-4-48-20260104173333.jpg](./img/xyz_grid-0085-2976896777-2304-1674-4-48-20260104173333.jpg)

- Further to confirm in ReForge with **Comfy Backend "ldm-patched" and the SD3 sampler (RF with timeshift)**. Corresponding old config is **Discrete sampler with v-prediction and zstnr**. It is very close to A1111 backend (however the yaml approach may be lost).

![26020801.jpg](./img/26020801.jpg)
