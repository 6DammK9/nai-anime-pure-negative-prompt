# Chapter 06: Finetuning in vanilla approach. #

[MONICA!](https://tenor.com/8v1P.gif)

- [cheesechaser-runtime](./cheesechaser-runtime): Definitely not dataset speedrun via [deepghs/cheesechaser](https://github.com/deepghs/cheesechaser).
- [sd-scripts-runtime](./sd-scripts-runtime): Definitely not finetune speedrun via [kohya-ss/sd-scripts](https://github.com/kohya-ss/sd-scripts).

## Hey ChatGPT, what is Astolfo saying about? ##

- It is about [finetuning](https://huggingface.co/learn/diffusion-course/unit2/1) SDXL with *the most straight forward approach*. This will be a step by step guide with community tools.

- Instead of the [community guide in CivitAI](https://civitai.com/articles?view=feed&tags=128645), which are focused in LoRAs under particular topic, mine is **full scale finetune** with **full scale dataset** (theoretically).

- There are some **primary sources** involved (and coding), so I'm confident that previous attempts are [as few as we have seen](../ch02/model_history.md#model-history-sdxl).

- Instead of any customization throught the process, I decided to execute in the [vanilla way](https://www.investopedia.com/terms/v/vanilla-strategy.asp). There should be a [reproducible](https://en.wikipedia.org/wiki/Reproducibility) [baseline](https://medium.com/@preethi_prakash/understanding-baseline-models-in-machine-learning-3ed94f03d645) for further research, especially the topic is being [abstract and psychological](../ch01/aesthetic.md).

- With a clear and easy guide to follow, all you need is gather some sponser, or just save some earnings to make this with lowest risk. Technology is never mature, you have rights to justify what is correct in science.

- The "toy dataset" will be the 6k images with "Astolfo". Without only little idea on creation (e.g. I only know a little artists / characters / animate series), [knowing the data distribution](https://huggingface.co/tasks/unconditional-image-generation), will help me to identify if the model learn the "denoising process" (not "draw thing") effectively. There is **close to no correlation** between the low level training loss (L2 / Huber) and abstract validation loss (CCIP / ImageReward / "XP" loss) without tedious model evaluation (image generation). Therefore, such vanilla approach, with "common tools", [and a "general" magic number](https://www.stablediffusion-cn.com/sd/sd-knowledge/1761.html) will help me to focus the "AI" side of this training task.

- Finally, here is my hypothesis: Model merging, as a subcategory of [PEFT](https://huggingface.co/docs/peft/developer_guides/model_merging), if have a [proper merge](../ch01/merge.md#blue-pill-but-in-academic-paper), you can iterlate between both "merging" and "finetuning" to archieve the learning task with huge efficiency. Instead, although lack of academic discussion, it is hard to finetune from a *burnt model*, even a [burnt distillated model](https://www.reddit.com/r/StableDiffusion/comments/1fuukwz/fluxdevdedistill_an_undistilled_version_of_flux/?rdt=33807), meanwhile finetuning from pretrianed model (the SDXL 1.0) will be inefficient. 

- Therefore, I'm here to explore for any options, under limited resources, and hopefully empower more people to join without processional knowledge. ~~It shouldn't be limited to full time student and researchers. I hate the "gate".~~

## Why now, why so late? ##

- *I have bought 4x RTX3090 blower without dedicated use case.* My [career](../ch97/rag_with_doc.md) may require them, however it is likely to use (OpenAI) API because of [commercial reason](https://www.atlassian.com/agile/project-management/project-baseline).

- *I rushed for datase* because of the [fear of banning the great contents](https://huggingface.co/docs/hub/storage-limits#storage-plans), meanwhile the "Best-effort" is [indicating the target](https://github.com/deepghs/cyberharem).

- *I have a workstation already* for [merging in large scale](../ch05/README_XL.MD).

- *I have professional knowledge* even I treat this as a [hobby](../ch00/about_me.md).

- Therefore, *this is a great chance for me to contribute*. I can do it for art, instead for the [rat race](https://en.wikipedia.org/wiki/Rat_race). *I just have limited spare time and motivation,* before I [mentally break down](https://en.wikipedia.org/wiki/Health_of_Vincent_van_Gogh) with such a dumb idea.

- Lore of the "Best-effort" (it ends up in this [HF discussion post](https://huggingface.co/posts/julien-c/388331843225875) after their discord server is blown): 

![24121401.jpg](./img/24121401.jpg)