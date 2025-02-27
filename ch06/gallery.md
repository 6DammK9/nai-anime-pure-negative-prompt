# Finetune findings (and gallery) #

![24121501.jpg](./img/24121501.jpg)

- *Since most of my recipe are models finetuned from the same dataset (with different tags)*, it converges quite fast. Astolfo got his facial features back within 1EP.

- **Training loss (L2 / Huber) has no correlation to image content.** It is fine when it doesn't rise / drop drastically. [From common practice](https://www.stablediffusion-cn.com/sd/sd-knowledge/1761.html), 0.1 is a good reference. The training loss here applies to the inference for each denoising step, under the MDP chain inside the SD model. Advanced validation loss are required, *or just be responsible to art and be the first audience*.

- TTE off may have lower loss, although it is close to meaningless to end result.

## When TTE is off ##

- If the concept is recognizable already (usually incomplete, e.g. Astolfo vs generic pink hair and slight hair intake), styles / details can be recovered well.

- Most unrelated but recognizable concept are mostly untouched. Cars, other characters, costumes, locations, are having style change only.

- However, if the concept is unrecognizable before train, it won't be effective. For example, some characters, artists, NSFW concepts, were wiped out while merging.

![xyz_grid-0011-460372993-14784-1081-6-48-20241215174033.jpg](./img/xyz_grid-0011-460372993-14784-1081-6-48-20241215174033.jpg)

![xyz_grid-0014-744089893-14784-1081-6-48-20241215223339.jpg](./img/xyz_grid-0014-744089893-14784-1081-6-48-20241215223339.jpg)

## When TTE is on ##

- It will be effective when the concept is unrecognizable before train. For example, *Astolfo is a boy now*.

- However, with improper parameter and data distribution, concepts recognizable before train can be forgotten. Characters, costumes may survive, but cars, locations may be gone.

![xyz_grid-0003-460372993-14784-1081-6-48-20241214220917.jpg](./img/xyz_grid-0003-460372993-14784-1081-6-48-20241214220917.jpg)

![xyz_grid-0006-744089893-14784-1081-6-48-20241215003045.jpg](./img/xyz_grid-0006-744089893-14784-1081-6-48-20241215003045.jpg)

## When TTE only ##

- It will be similar with TTE off. Notice that the content will change, instead of the representation of content. Academically training alternatively between UNET and TE and freezing each others is safe, however it requires double effort. Otherwise I need to seperate the dataset for parts for different stages.

![xyz_grid-0024-460372993-14784-1081-6-48-20250201143401.jpg](./img/xyz_grid-0024-460372993-14784-1081-6-48-20250201143401.jpg)

![xyz_grid-0025-744089893-14784-1081-6-48-20250201145322.jpg](./img/xyz_grid-0025-744089893-14784-1081-6-48-20250201145322.jpg)

## When TTE is on with only part of UNET (63%) is trained ##

- *The learning rate has been reduced, which is referenced from similar models.* I believe that the learning rate of UNET may be smaller than TE, but it requires extentsive testing.

![xyz_grid-0017-460372993-14784-1081-6-48-20250130174425.jpg](./img/xyz_grid-0017-460372993-14784-1081-6-48-20250130174425.jpg)

![xyz_grid-0026-744089893-14784-1081-6-48-20250201152012.jpg](./img/xyz_grid-0026-744089893-14784-1081-6-48-20250201152012.jpg)

![xyz_grid-0019-3501057452-14784-1081-6-48-20250131000434.jpg](./img/xyz_grid-0019-3501057452-14784-1081-6-48-20250131000434.jpg)

## Some personal direct quotes (need time to consolidate) ##

- [Discussion of TTE in UD.](https://discord.com/channels/1010980909568245801/1011105234820542554/1326822489153863764)

## Comparasion between community finetuned models ##

- [I have compared with 2 recent community finetuned models.](./readme.md#comparasion-with-similar-large-scale-finetune)

- *AnimagineV4 tends to add quality tags to the back*, meanwhile *NoobAI-XL tends to add quality tags to the front*. **My "test" model has quality tags absent.** The effect of the position of the tags matters, as discussed in the SD1.5 era.

- I expect my "at most 1EP" may not able to describe the characters well, but pretrained content (e.g. cars) will be preserved.

![xyz_grid-0020-3501057452-5376-1081-6-48-20250131001456.jpg](./img/xyz_grid-0020-3501057452-5376-1081-6-48-20250131001456.jpg)

![xyz_grid-0021-460372993-5376-1081-6-48-20250131002136.jpg](./img/xyz_grid-0021-460372993-5376-1081-6-48-20250131002136.jpg)

## Comparasion between TTE settings (on / off / only) ##

- See [model description](./sd-scripts-runtime/logs/readme.md). Generally forgetting pretrained knowledge can be avoided with proper learning rate and absent of quality tags, which **"quality tags" is a kind of misalignment**.

![xyz_grid-0023-3501057452-8064-1081-6-48-20250201135700.jpg](./img/xyz_grid-0023-3501057452-8064-1081-6-48-20250201135700.jpg)

- For effects on artist, **TTE is recommended**. The following 2 are `(1boy:0), [astolfo]` and `cle_masahiro, (1boy:0), [astolfo]`. Notice that the artist tag in this 6k dataset only appears once or twice.

![xyz_grid-0028-3033572388-6144-1327-6-48-20250201163358.jpg](./img/xyz_grid-0028-3033572388-6144-1327-6-48-20250201163358.jpg)

![xyz_grid-0029-3033572388-6144-1327-6-48-20250201164231.jpg](./img/xyz_grid-0029-3033572388-6144-1327-6-48-20250201164231.jpg)

## Unconditional Image Generation ##

<details>
    <summary> It still works. </summary>

    ![250205-3581144351-1024-1024-6-48-20250201111839.png](./img/250205-3581144351-1024-1024-6-48-20250201111839.png)

    ```txt
    parameters

    Steps: 48, Sampler: DDIM CFG++, Schedule type: Automatic, CFG scale: 6, Seed: 3581144351, Size: 1024x1024, Model hash: a22204df31, Model: last, VAE hash: 235745af8d, VAE: sdxl-vae-fp16-fix.vae.safetensors, Clip skip: 2, SEG Active: True, SEG Blur Sigma: 11, SEG Start Step: 0, SEG End Step: 2048, PAG Active: True, PAG SANF: True, PAG Scale: 1, PAG Start Step: 0, PAG End Step: 2048, Version: v1.10.1
    ```
</details>

## Effect in dual caption / tags, and exploring on learning rate ##

These images are arrange in order.

- `model_out_25022101`: SDXL, 6k dataset, Dual Tag (pick caption or tags), TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022102`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 63% UNET, 5e-6 + 3e-6
- `model_out_25022103`: SDXL, 6k dataset, Dual Tag (concat, a1111 token trick), TTE on + 63% UNET, 1e-6 + 1e-5

![xyz_grid-0005-744089893-13440-1081-6-48-20250222135824.jpg](./img/xyz_grid-0005-744089893-13440-1081-6-48-20250222135824.jpg)

![xyz_grid-0015-744089893-14784-1081-6-48-20250223154144.jpg](./img/xyz_grid-0015-744089893-14784-1081-6-48-20250223154144.jpg)

![xyz_grid-0010-744089893-14784-1081-6-48-20250223023958.jpg](./img/xyz_grid-0010-744089893-14784-1081-6-48-20250223023958.jpg)

- The disussion is listed in [the session with the codes.](./sd-scripts-runtime/kohyas.md#how-dual-tags--caption-will-be-passed-into-the-model) General pretrained knowledge has been preserved a lot more when the input text is a lot more diversified. Notice that generated captions is a kind of synthetic data, which has risk on [model collapse](https://en.wikipedia.org/wiki/Model_collapse). Make sure the content must be [monitored closely](./tipo-toriigate-runtime/readme.md).

![xyz_grid-0003-460372993-13440-1081-6-48-20250222135822jpg](./img/xyz_grid-0003-460372993-13440-1081-6-48-20250222135822.jpg)

![xyz_grid-0008-460372993-14784-1081-6-48-20250223023855.jpg](./img/xyz_grid-0008-460372993-14784-1081-6-48-20250223023855.jpg)

![xyz_grid-0013-460372993-14784-1081-6-48-20250223153945.jpg](./img/xyz_grid-0013-460372993-14784-1081-6-48-20250223153945.jpg)

## Effect of gradient accumulation (full UNET) ##

![IMG_7431](./img/IMG_7431.jpg)

- The noticeable difference is the loss curve is smooth in the first half of the training progress, then it fluctuates. Although the magnitude of the MSE has no correlation to the image content, *it fluctuates when the learning process is completed,* with the magnitude stays at a constant range, and sometimes spikes for some outliers. It ensembles to a longitudinal wave, which looks like a typical loss cure while finetuning, but within a constant range.

- To further *imagine* the root cause, may be the (artistic) task in *unsupervised learning approach* (pre-trianing with many objectives, close to pattern matching) is really expect the model to "overfit", or being "confident" enough to not being distracted / confused to "predict" what the model has been learnt.

- For the "longitudinal wave", the "stablization of content" in XY plot matches the "longitudinal wave" in the loss curve.

- The image still break when the learning rate is too high (the learning rate has been doubled).

![xyz_grid-0018-460372993-14784-1081-6-48-20250224235114.jpg](./img/xyz_grid-0018-460372993-14784-1081-6-48-20250224235114.jpg)

![xyz_grid-0020-744089893-14784-1081-6-48-20250224235313.jpg](./img/xyz_grid-0018-460372993-14784-1081-6-48-20250224235114.jpg)

## Effect of gradient accumulation (part of UNET, 71%) ##

- There was a discussion to increase learning rate when gradient accumulation is enabled. [Ref.](https://stackoverflow.com/questions/75701437/why-do-we-multiply-learning-rate-by-gradient-accumulation-steps-in-pytorch) However, *turns out I don't have to increse it, meanwhile it converges better.*

- Since it boosted the efficiency, I have found the optimal learning rate which can **balance learned intended content and preserve general pretrained knowledge.** 

- ~~The prompt has an artist name, which consist of only 1-2 images out of 6.2k. Meanwhile the "rin with rx7" is not even included in the dataset.~~

![xyz_grid-0037-3033572388-11264-1327-6-48-20250227205829.jpg](./img/xyz_grid-0037-3033572388-11264-1327-6-48-20250227205829.jpg)

![xyz_grid-0038-460372993-14784-1081-6-48-20250227212554.jpg](./img/xyz_grid-0038-460372993-14784-1081-6-48-20250227212554.jpg)

![xyz_grid-0041-744089893-14784-1081-6-48-20250227212557.jpg](./img/xyz_grid-0041-744089893-14784-1081-6-48-20250227212557.jpg)

- Check for [model description](./sd-scripts-runtime/logs/readme.md) for the setting of the corrosponding model name. Although there is no clear definition to describe "overfitting" in T2I or even generative task (some may call that "it just learnt effectively, unrelated content should not be cared"), I still call it "overfit" when the model start forgetting general contents which is out of the finetuning dataset ~~I think this is both (large) finetuning and (small) pretrain~~.

- However the model still requiree **more than 1 epoch** to learn the entire dataset effectively, which ranges from 6-9 epochs. *Maybe I should really rent a powerful mahcine when the first EP is a success.* 

![xyz_grid-0044-3033572388-9216-1327-6-48-20250227215821.jpg](./img/xyz_grid-0044-3033572388-9216-1327-6-48-20250227215821.jpg)

![xyz_grid-0045-460372993-12096-1081-6-48-20250227215822.jpg](./img/xyz_grid-0045-460372993-12096-1081-6-48-20250227215822.jpg)

![xyz_grid-0046-744089893-12096-1081-6-48-20250227215822.jpg](./img/xyz_grid-0046-744089893-12096-1081-6-48-20250227215822.jpg)
