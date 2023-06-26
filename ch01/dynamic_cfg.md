# Dynamic CFG / CFG rescale #

- [Dynamic CFG](https://github.com/mcmonkeyprojects/sd-dynamic-thresholding)
- [CFG rescale](https://github.com/AUTOMATIC1111/stable-diffusion-webui/pull/10555)
- Both are referencing to paper [Common Diffusion Noise Schedules and Sample Steps are Flawed](https://arxiv.org/abs/2305.08891).
- User ~~artist~~ are expected to have [found the optimal static CFG first](./cfg_step.md).

## Dynamic CFG ##

- Is an extension. ~~I will revisit later, no hands on experience yet.~~

## CFG rescale ##

- **Do not** switch to branch `cfg-rescale` (it is 77 commits behind already, and not being maintained).
- `git cherry-pick e508db474a579aff4d2aa42c4d16f074de333766`
- Before XYZ plot, "add config entries" by "Settings > Classifier-Free Guidance Rescale φ"
- Paper recommended to use φ=0.7, A1111 also shows similar result, however **it is based from a modified SD 2.X model**.
- From my experience, it is better to choose $\phi=0.3$.
- Original static CFG implies to $\phi=0.0$.

|Too low|Just right|Too high|
|---|---|---|
|No sinificant change|Minor detais improvement *without major detail loss*|Major detail loss (background), color tone is heavily shifted.|

![IMG_9400.jpg](./img/IMG_9400.jpg)

- For the "just right" value, I see the facial expresson is even more ~~irregular~~ natural, instead of something mediocore. ~~"Closer to the mean of a cluster."~~

*Original images and prompts coming soon.*
