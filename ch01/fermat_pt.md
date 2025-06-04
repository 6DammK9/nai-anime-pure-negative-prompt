# Findings on Geometric Median over merging models (LLM assisted) #

## Disclaimer ##

- I am not PhD student or professional researchers (*cough [still Msc](../ch00/about_me.md)). From amateur persecptive, formal [mathmatical proof](https://en.wikipedia.org/wiki/Mathematical_proof) will be impossible (I'm poor at algebra / calculus / statistic like LLM!). Meanwhile, many technical reports / [white papers](https://en.wikipedia.org/wiki/White_paper) in [engineering field](https://engineering.ubc.ca/spotlight/why-engineering/engineering-or-science-whats-best-path-for-you) does rely on [empirical evidence](https://en.wikipedia.org/wiki/Empirical_evidence). ~~a.k.a experiment, or even subjective content creation!~~ Like the DDPM ("diffusion") before flow matching paper, some fact may hold true but being discovered (e.g. probablity vectors extends from vector field). It is a kind of [limitation](https://blog.wordvice.com/how-to-present-study-limitations-and-alternatives/) "I am facing right now". For example, I just rewrote [euler (method) sampler](./k_euler.md), where "default euler sampler is a modified sampler" remanins true, but the modificaiton, citation, and even the "theory", can be all non factual.

- Instead of [vibe researcing](http://en.wikipedia.org/wiki/Vibe_coding) which just relies on LLM, I am completely inverted the process: Basic proof in general articles abundant in internet (not limited to CS, maybe physics, math, or even economy, any subjects), experimented with positive result (take months!), make sure it works consistintly in a certain conditions (no luck assumed), and finally ask LLM for and exisitng papers / articles which can be related.

- For example, **assuming not conducting rigorous (mathmatical) proof**, with *trust* in some sources in internet (arxiv with international academic conference, lecture notes from MIT, whatever), you can "estimate" with **updated LLM** (either 2024 or 2025, just after 2010) that the discussion about [flow matching](./flowmatching.md) on diffusion models are very likely true and factual. However, until I derive the entire math proof myself, or by [comptuer assisted proof](https://en.wikipedia.org/wiki/Computer-assisted_proof), it can't be absoultely certain.

## Properties of Geometric Median and relationship on Machine Learning ##

- ~~TBC, 3am right now. Better make a comparasion with centroid / mean / center of mass, because robustness is an abstract concept.~~

- L1 regularization, Mean Absolue Error, linear eulcidian distance instead of squared distance, mean absolute error, *Multivariate median*, *sparsity on task vectors*, *robust statistics*.
