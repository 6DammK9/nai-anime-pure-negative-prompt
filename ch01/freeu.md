# FreeU #

- [WebUI Extension](https://github.com/ljleb/sd-webui-freeu), [arxiv paper](https://arxiv.org/abs/2309.11497)

- Paper: Didn't read yet. Seems that it *change the connection of the layers of UNET*, and *provided codes* to make quick downstream development possible. Also [it may not work with Control Net which is using the same method](./controlnet.md) 

- Hyperparameter: *4 numbers are too much for me. Just use default.* **All 1.0** $b_1=s_1=b_2=s_2=1$ = Off FreeU

- **Use with [Dynamic CFG](./dynamic_cfg.md)**. Change the $\varphi$ instead. For my case, with author's recommended value (also extension's default), I'll use **0.7 instead of 0.3**, which returns to another author's recommended value. *What a coincidence.*

![xyz_grid-0126-3179120067-7392-8011-4.5-48-20230924000030.jpg](img/xyz_grid-0126-3179120067-7392-8011-4.5-48-20230924000030.jpg)


![xyz_grid-0127-1986506139-5120-1754-4.5-192-20230924004356.jpg](img/xyz_grid-0127-1986506139-5120-1754-4.5-192-20230924004356.jpg)

