# Findings on Isotropic Merge #

## First glance ##

I will focus on `Iso-C` only. `Iso-CTS` is too complicated to implement.

![25060701.jpg](./img/25060701.jpg)

Parameter $\sigma$ can be further reduced to hyper parameter instead of calculated value. [Reference in a 3rd party merger.](https://tanganke.github.io/fusion_bench/algorithms/isotropic_merging/)

$\sigma=1.0$ still have minimal effect because of [denoising effect](https://medium.com/@maydos/image-processing-with-singular-value-decomposition-ce8db3f78ce0) (applies to any LR algo like PCA and tSNE).

The "sum task matrices" can be reduced to any merged state. If `n_average` $\Delta_{TA} = \frac{1}{r} \Sigma_{i=1}^r \theta_{i}$ works, "any working model or model state" will work also.

May have no effect. Also I'll make a PoC may not import sd_mecha because it is technically "a fix".

Paper: [No Task Left Behind: Isotropic Model Merging with Common and Task-Specific Subspaces](https://arxiv.org/abs/2502.04959)
