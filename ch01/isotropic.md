# Findings on Isotropic Merge #

## First glance ##

I will focus on `Iso-C` only. `Iso-CTS` is too complicated to implement.

![25060701.jpg](./img/25060701.jpg)

Paper: [No Task Left Behind: Isotropic Model Merging with Common and Task-Specific Subspaces](https://arxiv.org/abs/2502.04959)

Code: [iso.py](https://github.com/danielm1405/iso-merging/blob/main/src/utils/iso.py)

The "sum task matrices" can be reduced to any merged state. If `n_average` $\Delta_{TA} = \frac{1}{r} \Sigma_{i=1}^r \theta_{i}$ works, "any working model or model state" will work also.

However, after experiment, it suffers from failed to preserve attention. Content has lost focus and being deformed.

