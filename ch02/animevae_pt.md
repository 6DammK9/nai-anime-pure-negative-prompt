# Animevae.pt #

[Original message link.](https://t.me/StableDiffusion_CN/646507)

- Thanks ["AO"](https://github.com/AdjointOperator) for the detective work.

```python
for k in sd14_vae['state_dict'].keys():
    assert torch.eq(nai_vae['state_dict'][k],sd14_vae['state_dict'][k]).all()
```
![img/photo_2023-01-08_16-36-59.jpg](img/photo_2023-01-08_16-36-59.jpg)

- More proof on the [model comparasion](../ch03/v1/json/nai_sd144g_nai4g.json) [comparasion script](../ch03/v1/mega_cmp.ipynb). Exact match confirmed. See `first_stage_model`(line 407) for details.
- You can accuse people relies on "NAI leak" by mentioning `animevae.pt` (appears in mid Nov - early Dec 2022), but it doesn't proof that a model is really developed from "NAI leak". 
- WD has its own `kl-f8-anime2.ckpt` so if you're so scared from the trouble (medieval time, witch hunt *wink), use theirs. You only have some minor effects (sharpness / contrast) for the final result.

## Extra: Text Encoder ##

- *This is discovered as same as writing [ch03](../ch03/), it is the exact same [model comparasion](../ch03/v1/json/nai_sd144g_nai4g.json).* Since NAI has changed some layer names comparing to common SD models, (`cond_stage_model.transformer` to `"cond_stage_model.transformer.text_model`), I have manually traced and redo the comparasion as `nai.cond_stage_model.transformer`. As it showns, **it is identical also.** This gives so many hints: So many danbooru tags is failed to remember, but it does remember lots of anime stuffs with its own "dictionary".
