# Findings on "DARE Merge" in SD #

- Paper: [Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch](https://arxiv.org/abs/2311.03099)

- Implementation: [Supermario merge(DARE).](https://github.com/martyn/safetensors-merge-supermario) [Ported to SD.](https://github.com/groinge/sd-webui-untitledmerger/)

- [Official Github repo](https://github.com/yule-BUAA/MergeLM/) **WOW it is in ICML 2024!** [OP](https://github.com/yule-BUAA/MergeLM/commit/6d49ad96fd69c92013654b837041b868aa806564)

- [EN article](https://medium.com/@minh.hoque/paper-explained-language-models-are-super-mario-2ebce6c2cf35), [CN article](https://zhuanlan.zhihu.com/p/668809641)

- Until I'm sure how [my primary merger implement this algorithm,](https://github.com/ljleb/sd-mecha/blob/main/examples/binomial_dropout_merge.py), I won't comment on the algorithms.

- However, there are some important glossaries: DARE as "**D**rop **A**nd **RE**scale", SFT as "**S**upervised **F**ine-**T**uning".

- Given the success of ~~modified~~ [TIES merging](./ties.md), and the author's experience in merging "Encoder-based LMs" (BERT), it sounds promising. *Spoiler: Added 20 Pony models, reaching 94 models, and the mix still function!*

![24050503.png](./img/24050503.png)

## TIES with DARE ##

- [This article describes the relationship between DARE, TIES, and a brunch of other merging algorithms,](https://slgero.medium.com/merge-large-language-models-29897aeb1d1a). *Relationship "with" is accurate in this case.*

- The description / algorithm expression of DARE paper is kind of messy ~~the idea is actually simple but exotic~~, let me make a *simple* description.

- DARE's core concept is **Prune > Merge > Rescale, without specifying what merge method to be used.** Meanwhile, TIES is a **merge method focusing on sign election.** Combining them together will be **Make delta > Bernoui dropout > TIES > Rescale from dropout > Rescale delta**.

- This is the *simple* part: $m^t \sim Bernoulli(p)$ means the "mask" under [Bernoulli distribution](https://en.wikipedia.org/wiki/Bernoulli_distribution), which is a binary matrix with random $1$ and $0$ s, then $\odot$ will be the [Hadamard product](https://en.wikipedia.org/wiki/Hadamard_product_(matrices)), i.e. "multiply the mask" to produce the [dropout](https://medium.com/@amarbudhiraja/https-medium-com-amarbudhiraja-learning-less-to-learn-better-dropout-in-deep-machine-learning-74334da4bfc5) effect.

- People may confused this distribution from [Binomial distribution](https://en.wikipedia.org/wiki/Binomial_distribution), however the paper is expecting *independent binary ouput for every trials*, hence $B(1,p)$. Also, as stated above, Bernoulli distribution doesn't have its own notation, e.g. $\mathcal{N}(\mu,\sigma^2)$ for [Normal distribution](https://en.wikipedia.org/wiki/Normal_distribution). [Wiki has clearly stated the relationship,](https://en.wikipedia.org/wiki/Bernoulli_distribution#Related_distributions)

![24050701.png](./img/24050701.png)

- The exotic part will be the *undocumented implicated merging operation* on $\tilde{\delta}^t$ and becomes $\theta_{DARE}$ i.e. $\tilde{\delta}^t\leftarrow\tau_m=TIES(\tau_t), \tau_t=\tilde{\delta}^t$. 

![24050702.png](./img/24050702.png)

- (Draft, prior to change) As seen in [author's code](https://github.com/yule-BUAA/MergeLM/blob/main/model_merging_methods/mask_weights_utils.py#L9), sinlge line of `torch.bernoulli` is *so simple*, and it can hit [one-liner](https://en.wikipedia.org/wiki/One-liner_program) if programmed nicely.

![photo_2024-05-07_07-55-55.jpg](./img/photo_2024-05-07_07-55-55.jpg)

- From the experience on [TIES-SOUP](./ties.md), *I expect hyperparameter change and even more on algorithm hack.* 
