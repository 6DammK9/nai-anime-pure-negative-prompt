# "AstolfoMix" Unconditional Image Generation (and more) #

![cover2.png](cover2.png)

```
parameters

Steps: 48, Sampler: Euler, Schedule type: Automatic, CFG scale: 3, Seed: 3649863581, Size: 1024x1024, Model hash: e276a52700, Model: x72a-AstolfoMix-240421-feefbf4, VAE hash: 26cc240b77, VAE: sd_xl_base_1.0.vae.safetensors, Clip skip: 2, FreeU Stages: "[{\"backbone_factor\": 1.1, \"skip_factor\": 0.6}, {\"backbone_factor\": 1.2, \"skip_factor\": 0.4}]", FreeU Schedule: "0.0, 1.0, 0.0", FreeU Version: 2, Dynamic thresholding enabled: True, Mimic scale: 1, Separate Feature Channels: False, Scaling Startpoint: MEAN, Variability Measure: AD, Interpolate Phi: 0.3, Threshold percentile: 100, PAG Active: True, PAG Scale: 1, Version: v1.9.3
```

An *informal* research about [unconditional image generation](https://huggingface.co/tasks/unconditional-image-generation) with Stable Diffusion, or "AI". Such observation may be useful for "data visualization" to show that how the "number" works. **Please be skeptic on this repo.** [My explanantion in CivitAI.](https://civitai.com/articles/5149/untitled-denoising-to-the-random-content)

<details>
    <summary> Old Title. Move on. </summary>

# "NAI Anine" Pure Negative Prompt (and more) #

![cover.png](cover.png)

```
Negative prompt: (bad:0), (comic:0), (cropped:0), (error:0), (extra:0), (low:0), (lowres:0), (speech:0), (worst:0)
Steps: 32, Sampler: Euler, CFG scale: 10.5, Seed: 1337, Size: 512x512, Model hash: 925997e9, Clip skip: 2
```

An *informal* research about "NAI anime" art with pure negative prompt. Such observation may be useful for "data visualization" to show that how the "number" works. **Please be skeptic on this repo.**
</details>

[Pixiv album for storing the images](https://www.pixiv.net/en/tags/PureNegativePrompt/artworks)

[(New) Observation on PonyXL V6](ch02/pony_sd.md)

## Major contents ##
**No explaination. Read the articles instead.**
- **Generic research methods** (CFG-STEP scan) when an *unknown anime model* is received.
- My hands-on experience on [txt2img](https://en.wikipedia.org/wiki/Text-to-image_model) *only*. **Another prompting research.**
- **Generic prompting guide** for a [webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) compatable "anime model". Core concept (heck what application will support negative prompts?) is viable.
- **Docuementry, journal and ranting.** Read for drama. Actually some of them are *primary sources*. 
- ~~**Astolfo is a good boy.**~~
- Beware of **random docuement style** because I don't have time to explain or even expand it.
- Also beware [model hasing algorithm has been changed into SHA256 for entire model.](https://github.com/AUTOMATIC1111/stable-diffusion-webui/commit/a95f1353089bdeaccd7c266b40cdd79efedfe632) I'll use the new hash, but old hash remains (usually they are famous model isn't it?)

## Index ##
**Too lazy to update constantly. Just iterlate the directories. You will find the pattern.**
- [ch00](ch00): ~~My content is probably not popular / legit and even completely non-sense. You shold leave if you want nice AI art.~~ Why I'm writing all these stuffs.
- [ch01](ch01): Common content across models. **Most theory / explaination / derive goes there.**
- [ch02](ch02): Model specific contents. **Assumed you've already read ch01 and know the context.**
- [ch03](ch03): **Data analysis.**  Usually involves model comparasion.
- [ch04](ch04): *A (very dumb) batch script for multiple WebUI instances.*
- [ch05](ch05): *Astolfo mix. Existing technology, original idea.*
- [ch97](ch97): **Uncategorized contents.** Usually "not article".
- ch98: ~~Backup from discord server because I think it is not safe to leave them there forever.~~ **Removed. Merged / moved to different articles.**
- [ch99](ch99): Old segments. I didn't expect this repo draws stars and some attention. The format is being unsuitable again.

## So where to start? ##
- Take the *blue pill* to return the major comminuty and continue drawing. Take the [red pill](ch00/red_pill.md) if you're prepared to my ~~observation with some legit ML / NLP / AI knowledge~~ complete non-sense (or somewhat closest to the ~~reality of bugs / expolits / [Undefined behavior](https://en.wikipedia.org/wiki/Undefined_behavior)~~ dystopia of the released AI models).

## Contact ##
**Seriously? I'm no different than a random anon in this field.**
- Discord: 6DammK9#2533
- GMail: 6DammK9@gmail.com
- Pixiv: [6DammK9](https://www.pixiv.net/en/users/11525730)
