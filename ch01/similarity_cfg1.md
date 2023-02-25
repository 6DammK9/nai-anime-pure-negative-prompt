# "Similarity" based on CFG 1.0 #

- Assumed you're read [the thesis](https://arxiv.org/abs/2207.12598).

- [A similarity](https://huggingface.co/JosephusCheung/ASimilarityCalculatior) based from [Cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) from the output of random blocks are funny. It can only shows that if the finetuned model is "well done" or "raw".

- Just [directly compare the images](https://towardsdatascience.com/image-similarity-with-deep-learning-c17d83068f59) based from a **common input with certain output**. "Maybe treat the blackbox as a [person](https://en.wikipedia.org/wiki/Personal_identity)". **I'm not talking about the strong AI. The task has been clearly specified.**

- "CFG 1 = No CFG". Look for math derive [CN](https://kexue.fm/archives/9257/comment-page-1) [EN](https://benanne.github.io/2022/05/26/guidance.html). Minimal prompts = greatest degree on "viewing the prior implemented on the model". Aka "draw what AI has been learnt". See [prior.md](prior.md) for details.

- Now here is the **ground truth from the famous model**:

```
parameters
Negative prompt: (bad:0), (comic:0), (cropped:0), (error:0), (extra:0), (low:0), (lowres:0), (speech:0), (worst:0)
Steps: 256, Sampler: Euler, CFG scale: 1, Seed: 1337, Size: 512x512, Model hash: 925997e9, Clip skip: 2
```

![img/22102403-1337-512-512-1-256-20230108215347.png](img/22102403-1337-512-512-1-256-20230108215347.png)

- Then here are the results, **including the prototypes**:

![img/xy_grid-0101-1337-8704-591-1-256-20230108231531.png](img/xy_grid-0101-1337-8704-591-1-256-20230108231531.png)

- Note that models based from SD2.x are omitted. [Example](https://huggingface.co/JosephusCheung/RuminationDiffusion). Train a model from [AI generated images](https://www.pixiv.help/hc/en-us/articles/11866167926809-What-are-display-settings-for-AI-generated-work-) are completely in grey area and nothing can be proven formally.

- You may see text / capes / human face / resturant with open kitchen / chairs etc. Given such variety on the interpreption of an "abstract art", the similarity is a lot more obvious to understand without looking for figures.

- There is some [research on forgery](https://arxiv.org/abs/2212.03860)on investigaing such effect, and some attempts of [DAC control](https://en.wikipedia.org/wiki/Discretionary_access_control) such as [GLAZE](https://arxiv.org/abs/2212.03860) has been proposed, but looks like there is no definitive mehods to justify such issue.

- [mega_cmp_v3](../ch03/mega_cmp_v3.ipynb) will be based from this method.