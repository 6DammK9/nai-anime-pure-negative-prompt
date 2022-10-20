# Generating Explicit images about Astolfo who is a popular trap #

- [ROT13 Encrypted](https://rot13.com/).

- [NSFW demo pic](https://www.pixiv.net/en/artworks/102059177).
- [NSFW trail "before production"](https://www.pixiv.net/en/artworks/102077685).
- [Procuction (questionable)](https://www.pixiv.net/en/artworks/102101077)
- [Procuction (NSFW)](https://www.pixiv.net/en/artworks/102101135)

```txt
cnenzrgref
(nfgbysb_\(sngr\):0.95), (shgnanev_znfgheongvba:0.91), (cravf:0.82), (shgnanev:0.71), (znfgheongvba:0.71)
Artngvir cebzcg: (onq_nangbzl:0.82), (onq_srrg:0.82), (onq_unaqf:0.82), (onq_crefcrpgvir:0.82), (onq_cebcbegvbaf:0.82), (pbzvp:0.82), (pebccrq:0.82), (pebccrq_nezf:0.82), (pebccrq_urnq:0.82), (pebccrq_yrtf:0.82), (pebccrq_fubhyqref:0.82), (pebccrq_gbefb:0.82), (ratyvfu_grkg:0.82), (reebe:0.82), (rkgen:0.82), (ybj dhnyvgl:0.82), (ybjerf:0.82), (ab_uhznaf:0.82), (abezny dhnyvgl:0.82), (bhgfvqr_obeqre:0.82), (fcrrpu_ohooyr:0.82), (grkg_sbphf:0.82), (jbefg dhnyvgl:0.82),(chffl:0.95),(ynetr_oernfgf:0.95),(2obl:0.91),(2tvey:0.91)
Fgrcf: 1024, Fnzcyre: Rhyre, PST fpnyr: 12, Frrq: 3711082872, Fvmr: 384k640, Zbqry unfu: 925997r9, Pyvc fxvc: 2
```

```txt
cnenzrgref
(nfgbysb_\(sngr\):0.95),(1obl:0.91),(lnbv:0.82),(onat:0.82),(frk:0.82),(nff:0.75),(onersbbg:0.71),(cravf:0.71),(nahf:0.71)
Artngvir cebzcg: (onq_nangbzl:0.82), (onq_srrg:0.82), (onq_unaqf:0.82), (onq_crefcrpgvir:0.82), (onq_cebcbegvbaf:0.82), (pbzvp:0.82), (pebccrq:0.82), (pebccrq_nezf:0.82), (pebccrq_urnq:0.82), (pebccrq_yrtf:0.82), (pebccrq_fubhyqref:0.82), (pebccrq_gbefb:0.82), (ratyvfu_grkg:0.82), (reebe:0.82), (rkgen:0.82), (ybj dhnyvgl:0.82), (ybjerf:0.82), (ab_uhznaf:0.82), (abezny dhnyvgl:0.82), (bhgfvqr_obeqre:0.82), (fcrrpu_ohooyr:0.82), (grkg_sbphf:0.82), (jbefg dhnyvgl:0.82),(chffl:0.95)
Fgrcf: 50, Fnzcyre: Rhyre, PST fpnyr: 12, Frrq: 418647112, Fvmr: 384k640, Zbqry unfu: 925997r9, Pyvc fxvc: 2
```

## Theory ##

- Already explained in [README.md](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/README.md). Otherwise, ~~I know you won't.~~ It's fine.

- **Dimension, CFG and Sampling method is fixed.** It is proven with random topics.
- All prompts has strength in **negative log** from 1.0.
- Base negative prompts (0.82) doesn't change.
- Positive prompts are **adjusted and arranged** carefully.
- Effects on most combinations are observed in **batch (20) and low steps (20)**.
- Record the *yield* and "good random seeds". Then try to increase the STEP.
- Alternatively, **XY plot** with STEP size (Currently in exponential scale `16,24,32,64,256,1024`) with a constant batch. Time consuming.
- Hand pick the good result and enjoy!

### Fusing contradict tags ###
- As seen if you ROT13-ed back into plaintext.
- **Make sure the subject still exists.** (0.95)
- Fusing contradict tags (0.91) will requires [Set theory and Information Theory](https://en.wikipedia.org/wiki/Information_theory_and_measure_theory) to "stablelize the result".
- Some contradict tags (-0.91~-0.95) will be strongly rejected (they will become greyish noise again), but some superset (data instead of tag) can be tolerated (0.71~0.82).
- Obviously some individual images will fail to produce (e.g. some "blank area" failed to fill in contents, yea the tag is so OP). Try to produce in batch to see the *yield*. This example lies on *20% success rate* which is very good.
- Fusing the tags is a [dual problem](https://en.wikipedia.org/wiki/Duality_(optimization)). **Best results lies on a variable STEP size**. Observe the result closely and don't jump to the conclusion.

### Yield rate ###
- Sample size: 20. Pass rate: 0.65, Pass with R-18: 0.35. So scary.

|Failed|16|24|32|64|256|1024|
|---|---|---|---|---|---|---|
|7|1|1|3|3|3|2|
