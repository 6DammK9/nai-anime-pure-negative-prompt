# Observation from NovelAIDiffusionV3 #

- *Observation only.* I don't have membership, and I have no hands on experience about this.

- Do not mixed up with [V1](../ch99/925997e9.md) and V2, which is based from SD1.X.

- [My opinion on V3 (not my tweet). NAI should explain why so many artists and copyright materials are trained.](https://x.com/laz75n/status/1725042286088880587?s=20)

## Prompts ##

- Given the "modified" prompt system (apart from A1111 and comfyUI, closer to [Nijijourney](https://nijijourney.com/en/)), **long prompts will be ineffective.** Although officially clarified, *it was once considered that some prompt segments are actually mapping to trigger LoRAs.* The swapping performance is fast (compared with PCs) because of the large H100 cluster. 

![img/photo_2023-11-17_23-42-37.jpg](img/photo_2023-11-17_23-42-37.jpg)

- By observating in [SDCN](https://t.me/StableDiffusion_CN), **do the exact opposite of general / original contents.** Identify danbooru tags, especially `artist:xxx`, `official_art`, `anime_screencap`, and copyrighted materials (`umamusume`) etc., to obtain "nice images". *Explicit contents are effective, all you need is keep rolling the dice.* ~~(Less then 100? The hype train is rapid)~~ It is believed that **there is no filter** this time, and dumped effective GPU hours. ~~(When I'm making AstolfoMix, I've found that SDXL is too large. NAI V3 supports my speculation.)~~ **Logos, signatures, key visual features etc. are well reproduced.** For the claimed "structal change" and "intensive training", it is effective ~~and designed to dodge the bullet, now the base model should be generic like AstolfoMix.~~

- For quality tag (`absurdres`, `amazing quality`, `very aesthetic`), see [WD 1.5's release note](https://saltacc.notion.site/saltacc/WD-1-5-Beta-3-Release-Notes-1e35a0ed1bb24c5b93ec79c45c217f63) for idea. It is similar, but WD's execution is too bad *faceplam to justify the impact on model performance. You can see [NekoRayXL](https://civitai.com/models/136719/nekorayxl) which does not have such system applied.

![img/23111401.png](img/23111401.png)

- *My generic prompts may work also.* However SDXL's original contents, such as `wrc`, `ice cube`, are faded.

## Preview ##

- I didn't made this PNG, but *technically there is no copyright...?*

<details>
    <summary>Click to open the PNG (SFW but meh)</summary>

![{granblue_fantasy,official_art_},_year_2022,_pantyhose,{1girl},.png](img/{granblue_fantasy,official_art_},_year_2022,_pantyhose,{1girl},.png)

</details>

```
{"prompt": "{granblue fantasy,official art }, year 2022, pantyhose,{1girl}, fellatio gesture, oral invitation,blush,half-closed eyes,look at viewer,from side,tongue out,smile,upper body, best quality, amazing quality, very aesthetic, absurdres", "steps": 28, "height": 1216, "width": 832, "scale": 5.0, "uncond_scale": 1.0, "cfg_rescale": 0.0, "seed": 3816166865, "n_samples": 1, "hide_debug_overlay": false, "noise_schedule": "native", "sampler": "k_euler", "controlnet_strength": 1.0, "controlnet_model": null, "dynamic_thresholding": false, "dynamic_thresholding_percentile": 0.999, "dynamic_thresholding_mimic_scale": 10.0, "sm": false, "sm_dyn": false, "skip_cfg_below_sigma": 0.0, "lora_unet_weights": null, "lora_clip_weights": null, "uc": "nsfw, lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, artistic error, username, scan, [abstract], {{{1male,cock,pov,1boy}}}", "request_type": "PromptGenerateRequest"}
```