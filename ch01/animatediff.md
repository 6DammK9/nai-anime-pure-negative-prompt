# AnimateDiff #

## Introduction ##

- [Why I'm interested in using this (I will spend less to almost none time on image generation).](../ch97/vid2vid.md) I need some serious use case for my lovely [AstolfoMix](../ch05/README.MD).

- [The WebUI integration.](https://github.com/continue-revolution/sd-webui-animatediff) Academically not great, but it should be the best integration for community. It also make use of [ControlNet](./controlnet.md), which is also a popular application.

- It introduce a whole lot of new parameters to explore (including models), it will be tedious. I'll try my best to correlate the parameters I've used.

## Explorered hyperparameters ##

- It will be arranged in order from "do not touch" to "just change it".
- For "reasonable ranges", [this chapter (ch01)](./readme.md) should be enough, and [ch99](../ch99/readme.md) for "basic parameters". 
- It can (and it should) be aligned to the hyperparameters used in text2img. It actually try to respect the original "domain model".

![img/screencap-23102302.JPG](img/screencap-23102302.JPG)

### "Do not touch or it will break" ###

- Motion module: **Must be SD v1.4 based, NOT v1.5.** i.e. `mm_sd_v14`. [It is because NAI is rumored to be trained from SD 1.4.](../ch02/animevae_pt.md) I have tried v1.5 based, it malformed so hard. For realistic models, unless you are sure that it is finetuned from SD 1.5 (pure fine tune, no merge), don't use them. `mm-Stabilized_mid.pth` is plausible but it still breaks occasionally. `temporaldiff-v1-animatediff` and `mm_sd_v14` is not useable.

- Context batch size: **Stick with 16.** I've tried 24 and 32, it really breaks.

### It should be changed ###

- Sampler: **DDIM** from Euler. You will see `Setting DDIM alpha.` in console log. [Slight difference may be amplified in process.](../ch98/k_euler.md)

- CFG: **Slightly increase to 6** from 4. 8 is too high.

- Prompts: Since it is motion based, we will need something stable in motion. Currently I select `navel` to make sure core body is present.

- Closed loop / Stride: `N` / `1` because I'm not going to make GIF loop. It also damage diversity.

- Sampling Steps: "Keep it low" (24 or 48). I won't use 256 as usual.

- Dimension: 768x768. 1024x1024 will ~~give you OOM with 24GB card (currently 3090)~~ crash instantly. 

- Looks like it is not recoverable. Reboot WebUI then.

- Number of frames / FPS: 32 / 8 (For testing)

### No change from text2img ###

- [FreeU](./freeu.md) is compatable. 

- [Dynamic CFG](./dynamic_cfg.md) is compatable, but effect is not good. If you choose DDIM, it will automatically disabled because it doesn't support DDIM.

- VAE / UNET (original text2img model) / LoRA: *There shouldn't be limitation.*

## Result (text2vid) ##

- Off AnimateDiff. Note that [style LoRA](https://civitai.com/models/164160/ph-draw-style) has been used.

![img/231081-680973778-768-768-6-24-20231023173723.png](img/231081-680973778-768-768-6-24-20231023173723.png)

```
(aesthetic:0), (quality:0), (solo:0), (boy:0), [[navel]], (astolfo:0.98), <lora:ph_draw:0.9>
Negative prompt: (worst:0), (low:0), (bad:0), (exceptional:0), (masterpiece:0), (comic:0), (extra:0), (lowres:0), (breasts:0.5)
Steps: 24, Sampler: DDIM, CFG scale: 6, Seed: 680973778, Size: 768x768, Model hash: 41429fdee1, Model: 20-bpcga9-lracrc2oh-b11i75pvc-gf34ym34-sd, VAE hash: 551eac7037, VAE: vae-ft-mse-840000-ema-pruned.ckpt, Clip skip: 2, FreeU Stages: "[{\"backbone_factor\": 1.2, \"skip_factor\": 0.9}, {\"backbone_factor\": 1.4, \"skip_factor\": 0.2}]", FreeU Schedule: "0.0, 1.0, 0.0", FreeU Version: 2, Lora hashes: "ph_draw: 3e4f2671b6f7", Version: v1.6.0
```

![img/00030-680973778.gif](img/00030-680973778.gif)

```
(aesthetic:0), (quality:0), (solo:0), (boy:0), [[navel]], (astolfo:0.98), <lora:ph_draw:0.9>
Negative prompt: (worst:0), (low:0), (bad:0), (exceptional:0), (masterpiece:0), (comic:0), (extra:0), (lowres:0), (breasts:0.5)
Steps: 24, Sampler: DDIM, CFG scale: 6, Seed: 680973778, Size: 768x768, Model hash: 41429fdee1, Model: 20-bpcga9-lracrc2oh-b11i75pvc-gf34ym34-sd, VAE hash: 551eac7037, VAE: vae-ft-mse-840000-ema-pruned.ckpt, Clip skip: 2, FreeU Stages: "[{\"backbone_factor\": 1.2, \"skip_factor\": 0.9}, {\"backbone_factor\": 1.4, \"skip_factor\": 0.2}]", FreeU Schedule: "0.0, 1.0, 0.0", FreeU Version: 2, Lora hashes: "ph_draw: 3e4f2671b6f7", Version: v1.6.0
```

## Applying with ControlNet ##

- Read [the guide about ControlNet first](./controlnet.md). The parameter searching will based from there.

- Now we are good to go.