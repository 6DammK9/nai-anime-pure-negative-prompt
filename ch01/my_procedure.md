# My procedure from scratch to posting to PIXIV #

- Thie is **standarized and stable procedure** for all SD-based (including NAI based because it is) models. ~~I am lazy.~~ 
- "Postmodernism art: This is not Astolfo, not a model test."

### Example ###

- "Lunar new year" Astolfo: https://www.pixiv.net/en/artworks/104740639

### Procedure (before prompt engineering) ###

- Find a model you're interested (I prefer non merged or TTE-ed, preferable original FT approaches with absolutely no idea on results). [ABPModel](https://huggingface.co/AnnihilationOperator/ABPModel) is a good testing subject.
- Prior knowledge (heard from author, observation in discussion): Trained with artists with rich background. Feels "overfit" (`ep99`). This case: `sample-nd-epoch59`.
- [CFG-STEP scan.](./cfg_step.md) Result: CFG 7 in 512 x 512, CFG 16 in 768 x 768.
- Must have Astolfo. Thershold: SD 1.4 **pass**, WD 1.4 **fail**. Look for pink hair, and tends to be a boy. If it "fails", TERMINATE THE TEST. Don't waste time. Report to author.
- Reason: Astolfo is the 2nd male character (`1boy`) in Danbooru. He has around 5.5k or arts. Just below Link (8k), and Touhou / Vocaloid characters.
- For non animate models (excluding "realistic mix"): Just try to reconstruct `astolfo`. I have no idea on making art without Astolfo. EARLY EXIT.

### Procedure (prompt engineering) ###

- **Ignore model instruction (sometime there isn't).** [Standard negative prompt first](./prompt.md). [Model prior / bias will be shown](./prior.md). Skip if you have prior knowledge.
- **Keep ignore model instruction (independent test).** Make postive prompt from standard. Must include: **Interactive objects** (clothes / accessories / cars / guns etc.), **subject characters** (Astolfo / your LoRA character), **background sceneary** (a location).
- **Fix Astolfo.** `uc: breasts`
- **ALWAYS VERIFY WITH DATASET!** Now it is: `qipao`, `astolfo`, `kowloon`. If you have a special theme, add it also (`lunar new year`).
- **CHECK AGAIN WITH NLP!** `cheongsam` (Pixiv) > `china_dress` (Danbooru) > `qipao` (LAION). `happy_new_year ` (Danbooru) > `lunar new year` (LAION) > `lunar` + `new year` (CLIP).
- **KEEP BRAINSTORMING!** `lunar` + `new year` (CLIP) > `lunar` (night) + `new year` + `victoria harbor` (WIKI) > `lunar new year` + `kowloon` (LAION)
- **Adjust prompt weights and sequences!** It may be NP-hard. Position first (as attention ordering.) `qipao` > `astolfo` > `lunar new year` > `kowloon`. Then `(qipao:0.98), [astolfo], [[lunar new year]], [[[[kowloon]]]]`. *Sometimes `kowloon` comes first (e.g. TTE models, "any3")*
- **Test with low STEPS!** Usually STEP 48 batch 4.

### Procedure (after prompt engineering) ###
- Find a stable PC (RTX 2080ti with 33% TDP cap), count for expected time amount (6 hours), divide by large STEPS (STEP 256 batch 200).
- **HAVE A GOOD SLEEP, OR A GOOD DAY.** ("generative art")
- Cluster 200 images (glitched / missing detail / bad aesthetic / just not good enough etc.) and **pick at most best 20 images.** This requires extensive art sense. See [aesthetic.md](aesthetic.md) to try learn the formal aesthetic.
- Post to Pixiv. Done.

![img/104740639_p11.png](img/104740639_p11.png)

```
parameters
(qipao:0.98), [astolfo], [[lunar new year]], [[[[kowloon]]]]
Negative prompt: (bad:0), (comic:0), (cropped:0), (error:0), (extra:0), (low:0), (lowres:0), (speech:0), (worst:0), [[breasts]]
Steps: 256, Sampler: Euler, CFG scale: 16, Seed: 1575368210, Size: 768x768, Model hash: 26a06a9b82, Model: sample-nd-epoch59, Clip skip: 2
```
