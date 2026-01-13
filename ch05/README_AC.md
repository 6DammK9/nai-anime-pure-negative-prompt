# Chapter 05-AC: AstolfoCarmix #

**Warning**: The following sections are more towards art performance, instead of pure inference between AI / ML theories. Because of the **asymmetry** of training / inferencing in this generation task (i.e. text-to-image), the theories are drifting away from academic world, my "insight" / "intiution" about how the poor model works may be inaccurate, or scientific to relate to obvious general knowledge. The findings below are heavily relies on the concepts on [flow matching and vector field](https://arxiv.org/abs/2210.02747), even the "SDXL VPred" is **opposite** from there (score matching and markov chain with modified objective function "vpred").

## "AstolfoCarmix": vpred merge ##

- [Got it running in A1111](../ch01/vpred.md#extra-sdxl-vpred-in-a1111) in 2508, downloaded a new model pool, and the findings doesn't align to the eps side (i.e. current work). Need to figure out what is the "survive condition" again.

- *Hopefully not tunnelvision (especially I made quite a lot of drama / feud with others)*, it should points to some fundamental properties and conditions, instead of brute force / fancy algorithm. I should have enough information already to figure out how the merge works.

- Currently blending all vpred models together is working as intended (my eps model treated as outlier successfully).

![xyz_grid-0029-3011153084-4032-1098-3-64-20250825070002.jpg](./img/ac/xyz_grid-0029-3011153084-4032-1098-3-64-20250825070002.jpg)

- For "vpred vs eps" debate, I think vpred is overexaggerated. Colors are mostly from latent offset (model bias), meanwhile users are not aware / desire for rich contents.

![xyz_grid-0034-1844435476-1536-1657-4-48-20250826080801.jpg](./img/ac/xyz_grid-0034-1844435476-1536-1657-4-48-20250826080801.jpg)

## Merging burnt VPred Lycoris with AK: Inspiration ##

- *Discovered in 2508, but went hiatus for 2 months.*

- The hypothesis is something like "EPS to VPRED conversion" is a "relatively easy task (ML task)" which only touchs little model weights. [It was verified in 250902](https://discord.com/channels/1077423770106597386/1093732075355525331/1412429017868537887). However to protect the author (yet the LoRA itself is unuseable other than this niche task), the "LoRA weight" remains private (closest approximation is [this IL2.0 based LoRA](https://civitai.com/models/536954?modelVersionId=2173556)). Instead, [merge log](./xl_docs/vpred_merge_25110301.log) and the [merged model](https://civitai.com/models/1898715/astolfocarmix-vpredxl) can be released.

![25110301.png](./img/ac/25110301.png)

![xyz_grid-0060-2739800406-4032-1081-4-48-20251103012833.jpg](./img/ac/xyz_grid-0060-2739800406-4032-1081-4-48-20251103012833.jpg)

## Cracking the way how vpred works ##

- External reading: [Trainning log. Still need to merge.](../ch06/sd-scripts-runtime/logs/readme.md#2511-cracking-the-way-how-vpred-works).

- Although VPred from EPS is an easy task, it is not "obvious". Given a broken image instead of numbers, I still need to guess how and why it breaks. *More like educated guess and informed decision?*

- Blindly run vpred mode over eps model will yield to "blur image" with no content. It looks like this xy plot, however I have trained 6k 10EP over it. *There must be something wrong.*

![xyz_grid-0102-1781861418-16128-1081-4-48-20251113080206.jpg](./img/ac/xyz_grid-0102-1781861418-16128-1081-4-48-20251113080206.jpg)

- First to confirm (and it is the hardest one) is *the trainer code works as intended*. Although I have restrucutred the trainer code (see CH06), eps-eps and vpred-vpred training works as intended.

![xyz_grid-0098-1781861418-14784-1081-4-48-20251111074158.jpg](./img/ac/xyz_grid-0098-1781861418-14784-1081-4-48-20251111074158.jpg)

![xyz_grid-0103-1781861418-8064-1081-4-48-20251114074026.jpg](./img/ac/xyz_grid-0103-1781861418-8064-1081-4-48-20251114074026.jpg)

- However, when I trained on the "working merged eps-vpred model by accident a.k.a AC-NIL-0.1", it just shows colored fragments, implies that it works after merge.

![xyz_grid-0104-1781861418-8064-1081-4-48-20251114222906.jpg](./img/ac/xyz_grid-0104-1781861418-8064-1081-4-48-20251114222906.jpg)

![xyz_grid-0105-2011028800-4096-1327-4-48-20251114230137.jpg](./img/ac/xyz_grid-0105-2011028800-4096-1327-4-48-20251114230137.jpg)

- For the merge, when I merge "AC-NoobAI base" with "AK-NIL-1.2", it only works for 90:10, which implies that I may just underfit in the conversion.

![xyz_grid-0110-1781861418-6720-1081-4-48-20251115081358.jpg](./img/ac/xyz_grid-0110-1781861418-6720-1081-4-48-20251115081358.jpg)

![xyz_grid-0111-750033958-8064-1039-4-48-20251115165850.jpg](./img/ac/xyz_grid-0111-750033958-8064-1039-4-48-20251115165850.jpg)

- After my friend [hinablue](https://civitai.com/user/hinablue/models) decided to take my codes ~~and an A100x1 instance~~ to have a few EPs with his "1girl 1k 10x repeat" dataset, I confirm that it will be good to perform the mega 1EP finetune with a [grid search](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) on merge ratio.

![xyz_grid-0000-1781861418-9408-1081-4-48-20251117225526.jpg](./img/ac/xyz_grid-0000-1781861418-9408-1081-4-48-20251117225526.jpg)

![xyz_grid-0001-1781861418-6720-1097-4-48-20251117231637.jpg](./img/ac/xyz_grid-0001-1781861418-6720-1097-4-48-20251117231637.jpg)

![xyz_grid-0002-1781861418-6720-1039-4-48-20251117233009.jpg](./img/ac/xyz_grid-0002-1781861418-6720-1039-4-48-20251117233009.jpg)

- After 11k / 778k of "production run", I can still barely see the progress, however it may not working at all.

![xyz_grid-0003-1921513145-5120-1343-4-48-20251118234829.jpg](./img/ac/xyz_grid-0003-1921513145-5120-1343-4-48-20251118234829.jpg)

- Yep, *it just doesn't work*. Currently the working condition is unclear. Looks like the dataset must be aligned to the base model, which is not exist for a merged model like this.

![xyz_grid-0015-1781861418-11264-1343-4-48-20251121003442.jpg](./img/ac/xyz_grid-0015-1781861418-11264-1343-4-48-20251121003442.jpg)

![xyz_grid-0016-2838127623-11264-1343-4-48-20251121004518.jpg](./img/ac/xyz_grid-0016-2838127623-11264-1343-4-48-20251121004518.jpg)

![xyz_grid-0018-1781861418-6720-1055-4-48-20251121073725.jpg](./img/ac/xyz_grid-0018-1781861418-6720-1055-4-48-20251121073725.jpg)

![xyz_grid-0019-1781861418-8064-1055-4-48-20251122011417.jpg](./img/ac/xyz_grid-0019-1781861418-8064-1055-4-48-20251122011417.jpg)

- Swapping to the "merged-trained-merged" model doesn't work either. I even hit `nan` in loss curve.

![25112301.png](./img/ac/25112301.png)

- *Currently returning to [EPS trainning](../ch06/gallery_2511.md).* I have watched some generation preview (available in A1111) and find that the denoise process just snapped in early steps, which implies that it probably really can't handle my raw dataset. Same issue appears in the "working vpred merge" which the model may need a strong bias to generate with vpred process instead of the low bias in eps (eps blur but vpred just go straight into noise).

![25112302.jpg](./img/ac/25112302.jpg)

## Retry with the AK-Evo 2EP ##

- Vpred from 2EP is basically no luck.

![xyz_grid-0118-1781861418-8064-1081-4-48-20260110225944.jpg](./img/ac/xyz_grid-0118-1781861418-8064-1081-4-48-20260110225944.jpg)

- However, vpred from the merged AK-Evo 2EP, since it has already have the original dataset burnt in, the "6k Astolfo" **subset** works quite well.

![xyz_grid-0123-1781861418-8064-1055-4-48-20260112073558.jpg](./img/ac/xyz_grid-0123-1781861418-8064-1055-4-48-20260112073558.jpg)

- After some grid search on ratio, it fits with 0.85, which is between 0.75 and 0.9. *It looks like underfit, by comparing with the work in 2511.*

![xyz_grid-0124-1781861418-6720-1055-4-48-20260112074918.jpg](./img/ac/xyz_grid-0124-1781861418-6720-1055-4-48-20260112074918.jpg)

![xyz_grid-0132-1781861418-5376-1039-4-48-20260112225112.jpg](./img/ac/xyz_grid-0132-1781861418-5376-1039-4-48-20260112225112.jpg)

- Switching prompts are having similar result. It is just uncertain for the optimal ratio.

![xyz_grid-0126-1781861418-5376-1039-4-48-20260112221021.jpg](./img/ac/xyz_grid-0126-1781861418-5376-1039-4-48-20260112221021.jpg)

![xyz_grid-0128-1781861418-5376-1039-4-48-20260112222931.jpg](./img/ac/xyz_grid-0128-1781861418-5376-1039-4-48-20260112222931.jpg)

- By comparing with more prompts, the optimal ratio is more certain.

![xyz_grid-0131-2934581839-4096-1327-4-48-20260112224654.jpg](./img/ac/xyz_grid-0131-2934581839-4096-1327-4-48-20260112224654.jpg)
