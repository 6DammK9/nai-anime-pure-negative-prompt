# Findings on "Automagic Optimizer" #

- As on 250506, it is still a developing optimizer. There is also no academic discussion (e.g. math formula) yet, we can treat it as "Ostris' optimizer".

## Primary Source of the optimizer ~~abstract~~ ##

- The [automagic.py](https://github.com/ostris/ai-toolkit/blob/main/toolkit/optimizers/automagic.py), and [commit history](https://github.com/ostris/ai-toolkit/commits/main/toolkit/optimizers/automagic.py), hinted that it started on 2411.

- The [tweet](https://x.com/ostrisai/status/1917679501909057777) on 240501.

> built in stochastic rounding
>
> gradient accumulation
>
> auto adjusts (learning rate)
>
> scaled 8bit learning rate for every parameter... singly
>
> binary polarity mask for every parameter... speed up learning for parameters traveling a fixed direction

- The only major change is **Binary polarity mask**. See next session.

## Inspection of the base algorithm ~~Related works~~ ##

- By direct code comparasion between the initial version and current version of the `automagic.py`, there is **direct code reference** to [adafactor](https://arxiv.org/abs/1804.04235).

- [Adafactor](https://paperswithcode.com/method/adafactor) is a stochastic optimization already in general.

> In several recently proposed stochastic optimization methods (e.g. RMSProp, Adam, Adadelta)...
>
> At each step, we receive a stochastic realization...

- The "rounding" part need further study: [copy_stochastic](https://github.com/ostris/ai-toolkit/blob/main/toolkit/optimizers/optimizer_utils.py#L117). It could be related to [Stochastic rounding variance and probabilistic bounds](https://arxiv.org/abs/2207.10321) and [Stochastic Rounding 2.0](https://arxiv.org/abs/2410.10517v1).

- "Relative step" has been removed without reason. However [community opinion](https://www.reddit.com/r/StableDiffusion/comments/1cyxvjh/lora_training_prodigy_or_adafactor_learning_rate/?rdt=45965) is generally negative either.

- RMS part, and weight decay is preserved. ~~inherited from adamw.~~

- The major difference is  **Binary polarity mask**. It try to *control learning rate by sign agreement*. [signSGD](https://arxiv.org/abs/1802.04434) and [TIES-Merging](https://arxiv.org/abs/2306.01708) has considerations of sign agreement also, which prevents fluctuation while learning. 

![25050601.jpg](./img/25050601.jpg)

## Potential improvements ~~more related works~~ ##

- From [a discord message](https://discord.com/channels/1077423770106597386/1093732075355525331/1368812620496506910), it can be combined with "confidence factor" from [CAME](https://arxiv.org/abs/2307.02047) and [SPD](https://arxiv.org/abs/2411.01713) which remove RMS part.

- ~~It may appears as Kohyas PR so I decided to leave the screenshot raw.~~

![25050602.jpg](./img/25050602.jpg)
