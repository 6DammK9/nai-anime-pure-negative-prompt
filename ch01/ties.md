# Findings on "TIES Merge" in SD #

Paper: [TIES-Merging: Resolving Interference When Merging Models](https://arxiv.org/abs/2306.01708)

- [Merger code](https://github.com/ljleb/sd-mecha/blob/main/sd_mecha/__init__.py#L139-L167) is directly referring to the Algorithm session in the paper. *I don't validate line by line yet, but from end result, it should be valid.*

![24042301.png](./img/24042301.png)

- *Since picking hyperparameter is tedious*, which is NP-Hard with weeks per trial, I naively set $\lambda=1.0and $k=100which is between paper and my experiance.

![24042302.PNG](./img/24042302.PNG)

- Notice that **MEMORY USAGE is huge!**. Seems that model soup (averaging) is $O(1)meanwhile TIES is close to $O(N)in space complexity.

![photo_2024-04-22_07-45-58.jpg](./img/photo_2024-04-22_07-45-58.jpg)

- From the dev of the merger, using CPU won't be too slow, and... it merges faster then GPU. WS OP.

- Will be continued in ["AstolfoMix-XL TIES"](../ch05/README_XL.MD)

<hr>

### Sample code ###

- Will create PR.

## Commnet / LaTeX translation by DammK ##
### add_difference_ties ###
- `base`: $\theta_{init}$
- `*models`: $\{\theta_{init}\}_{t=1}^n$
- `models` after `subtract`: $\tau_t$
- `alpha`: $\lambda$
- `k`: $k $( From $\% $to $1 $)
- `res`: $\lambda * \tau_m$
- `return`: $\theta_m$
### ties_sum ###
- `delta`: $\hat{\tau}_t$
- `signs`: $\gamma_t $
- `final_sign`: $\gamma_m $
- `delta_filters`: $\{ \gamma_t^p = \gamma_m^p \}$
- `param_counts`: $|A^p|$
- `filtered_delta`: $\sum_{t\in{A^p}} \hat{\tau}_t^p$
- `return`: $\lambda * \tau_m$

```
def add_difference_ties(
    base: RecipeNodeOrPath,
    *models: RecipeNodeOrPath,
    alpha: float,
    k: float = 0.2,
    device: Optional[str] = None,
    dtype: Optional[torch.dtype] = None,
) -> recipe_nodes.RecipeNode:
    # $\{\theta_{init}\}_{t=1}^n$
    base = path_to_node(base)
    models = tuple(path_to_node(model) for model in models)
    
    # Create task vectors.
    # $\tau_t$
    models = tuple(
        subtract(model, base)
        if model.merge_space is MergeSpace.BASE else
        model
        for model in models
    )

    # step 1 + step 2 + step 3
    res = ties_sum(
        *models,
        alpha=alpha,
        k=k,
        device=device,
        dtype=dtype,
    )

    # Obtain merged checkpoint
    return add_difference(
        base, res,
        alpha=1.0,
        device=device,
        dtype=dtype,
    )

def ties_sum(  # aka add_difference_ties
    *models: Tensor | LiftFlag[MergeSpace.DELTA],
    alpha: Hyper,
    k: Hyper = 0.2,
    **kwargs,
) -> Tensor | LiftFlag[MergeSpace.DELTA]:
    
    # Step 1: Trim redundant parameters

    # $\hat{\tau}_t $O(N) in space
    keep_topk_reset_rest_to_zero = torch.func.vmap(filter_top_k)
    deltas = keep_topk_reset_rest_to_zero(models)
    deltas = torch.stack(deltas, dim=0)

    # $\gamma_t $
    signs = torch.sign(deltas)

    # $\mu_t $NOT USED
    # mu_t = torch.abs(deltas)

    # Step 2: Elect Final signs.

    # $sgn(\sum_{t=1}^n \gamma_t) $WRONG
    #final_sign = torch.sign(torch.sum(signs, dim=0))

    # $\gamma_m = sgn(\sum_{t=1}^n \hat{\tau}_t) $CORRECT
    final_sign = torch.sign(torch.sum(deltas, dim=0))
    
    # Step 3: Disjoint merge.

    # $\{ \gamma_t^p = \gamma_m^p \}$
    delta_filters = (signs == final_sign).float()
    
    # $|A^p|$
    param_counts = torch.sum(delta_filters, dim=0)

    # $\sum_{t\in{A^P}} \hat{\tau}_t^p $(Questionable)
    filtered_delta = (deltas * delta_filters).sum(dim=0)

    # $\lambda * \tau_m$
    return alpha * torch.nan_to_num(filtered_delta / param_counts)

# Obvious.
# $keep_topk_reset_rest_to_zero(\tau_t, k)$
def filter_top_k(a: Tensor, k: float):
    k = max(int((1 - k) * torch.numel(a)), 1)
    k_value, _ = torch.kthvalue(torch.abs(a.flatten()).float(), k)
    top_k_filter = (torch.abs(a) >= k_value).float()
    return a * top_k_filter

# Obvious.
def subtract(
    a: Tensor | LiftFlag[MergeSpace.BASE],
    b: Tensor | LiftFlag[MergeSpace.BASE],
    **kwargs,
) -> Tensor | LiftFlag[MergeSpace.DELTA]:
    return a - b

# Obvious.
def add_difference(
    a: Tensor | SameMergeSpace,
    b: Tensor | LiftFlag[MergeSpace.DELTA],
    *,
    alpha: Hyper = 0.5,
    **kwargs,
) -> Tensor | SameMergeSpace:
    return a + alpha * b
```
