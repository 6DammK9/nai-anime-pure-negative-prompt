# Merging models #

### Current materials before ranting ###

- Merge with any recognizable patterns: [sd-webui-supermerger](https://github.com/hako-mikan/sd-webui-supermerger)

- Some explaination (how to use instead of why): [BlockMergeExplained](https://rentry.org/BlockMergeExplained)

- Current meta: Merging multiple LoRAs. I don't know the procedure because I never do either LoRA or merging.

### Nice merges ###

- [Chilloutmix](https://huggingface.co/TASUKU2023/Chilloutmix): Cosplay model. However there is no cosplayer in dataset. Just merging "real photo" and "anime" together.

- [AbyssOrangeMix2](https://huggingface.co/WarriorMama777/OrangeMixs#abyssorangemix2_nsfw-aom2n): Realistic anime style. More focus on muscle and proportions, which is lack in most anime models. Merging "real photo" and "anime" also.

- [PastelMix](https://huggingface.co/andite/pastel-mix): At least there is a clear theme, without owning the dataset.

- [Lawlas's yiffymix](https://huggingface.co/Airic/lawlas-yiff-mix): There is way too many speices to train. AI will get confused. [yiffy-e18](https://huggingface.co/Doubleyobro/yiffy-e18) is an example.

- [AnythingV3](https://huggingface.co/Linaqruf/anything-v3.0): SOTA for hitting the perfect spot of the market desire.

### Merge by attention blocks (exclusive) ###

- [Swapping attention per layers](https://gist.github.com/crosstyan/95d14111e8e1eeb3348ef947818b338f) [ref](https://github.com/CCRcmcpe/scal-sdt/blob/e3e6a945fccb04245ad06b4ea1983852a93c7ea6/ckpt_tool.py#L254-L347). 

- [Some hints to perform such merge](https://t.me/StableDiffusion_CN/730058):
```
targets:
  - index: ["attentions"]
    targets:
      - targets:
          - index: ["attn1"]
```

- "CC" found that there is *no clear pattern* per model, as some models contribute by "FF", meanwhile some others are "sattn / xattn". [Twitter post](https://twitter.com/cross_tyan/status/1616437854208684036).

### Start ranting ###

- We had a hard tome to find something related. [Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time](https://arxiv.org/abs/2203.05482)

- Oh my god there is some discussion. [Robust fine-tuning of zero-shot models](https://arxiv.org/abs/2109.01903)

- [Some Chinese articles](https://www.zhihu.com/question/521497951)

- As stated in [6569e224.md](../ch99/6569e224.md), *try to theorize things formally.* You may archive more if a more appropriate mechanism is applied.

- [A nice merge: WD1.4 with SD2.1 TTE.](https://huggingface.co/p1atdev/wd-fix). ~~The TTE in WD1.4 is awful. No astolfo must be a failure. No execuses.~~

## Try to read thesis and don't try to dream about the blackbox. ##

- [Why We Will Never Open Deep Learning’s Black Box.](https://towardsdatascience.com/why-we-will-never-open-deep-learnings-black-box-4c27cd335118)

- [Nope.](https://twitter.com/butamanyasan/status/1608763093659832321)

![img/photo_2023-01-01_02-45-25.jpg](img/photo_2023-01-01_02-45-25.jpg)

- [Where is the bleach?](https://t.me/StableDiffusion_CN/625588) [However there is visualization tools.](https://github.com/hnmr293/stable-diffusion-webui-dumpunet) [There is always people interested.](https://medium.com/sfu-cspmp/unveiling-the-hidden-layers-of-neural-networks-6269615fb8a9) [Make sure what you're doing.](https://www.quora.com/Is-there-any-way-to-interpret-the-meanings-of-hidden-layers-and-reasoning-them-what-the-unit-values-account-for-possible-in-neural-network-learning)

![img/photo_2023-01-01_03-02-49.jpg](img/photo_2023-01-01_03-02-49.jpg)

- [The bruteforced result (Layer 7) is not useful for other tasks...](https://huggingface.co/syaimu/7th_Layer), [even it is supported by another popular merge model (AOM2)...](https://huggingface.co/WarriorMama777/OrangeMixs)

![img/0af5496675d3d85b8879bf46b3602b79e3a3c7c0160f98448b01c16b5242801f.png](img/0af5496675d3d85b8879bf46b3602b79e3a3c7c0160f98448b01c16b5242801f.png)

