# Findings on "DARE Merge" in SD #

- Paper: [Language Models are Super Mario: Absorbing Abilities from Homologous Models as a Free Lunch](https://arxiv.org/abs/2311.03099)

- Implementation: [Supermario merge(DARE).](https://github.com/martyn/safetensors-merge-supermario) [Ported to SD.](https://github.com/groinge/sd-webui-untitledmerger/)

- [Official Github repo](https://github.com/yule-BUAA/MergeLM/) **WOW it is in ICML 2024!** [OP](https://github.com/yule-BUAA/MergeLM/commit/6d49ad96fd69c92013654b837041b868aa806564)

- [EN article](https://medium.com/@minh.hoque/paper-explained-language-models-are-super-mario-2ebce6c2cf35), [CN article](https://zhuanlan.zhihu.com/p/668809641)

- Until I'm sure how [my primary merger implement this algorithm,](https://github.com/ljleb/sd-mecha/blob/main/examples/binomial_dropout_merge.py), I won't comment on the algorithms.

- However, there are some important glossaries: DARE as "**D**rop **A**nd **RE**scale", SFT as "**S**upervised **F**ine-**T**uning".

- Given the success of ~~modified~~ [TIES merging](./ties.md), and the author's experience in merging "Encoder-based LMs" (BERT), it sounds promising. *Spoiler: Added 20 Pony models, reaching 94 models, and the mix still function!*

![24050503.png](./img/24050503.png)