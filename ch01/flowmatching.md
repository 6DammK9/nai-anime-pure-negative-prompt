# Findings on flow matching #

- [The paper from Meta](https://arxiv.org/abs/2210.02747), and [from SD3](https://arxiv.org/abs/2403.03206).

- [The MIT lecture series on flow matching](https://diffusion.csail.mit.edu/) *Relies on this, but I didn't complete the labs.*

- [Medium article in 2505](https://harshm121.medium.com/flow-matching-vs-diffusion-79578a16c510).

- [CN article in 2412 (incomplete)](https://zhuanlan.zhihu.com/p/12591930520).

- Maybe just look at [Diffusion Model](https://en.wikipedia.org/wiki/Diffusion_model) in wiki (not applicable years ago!)

## Comparasion with "score matching" ##

- *They can be easily validated by updated online LLM, because they just scrape all the contents above.*

- "Diffusion" in application, or products, or in "user space" / layman sense, are specified as DDPM or DDIM. They are specified in some details over generalized rules. **The original paper did not mention any generalized concepts!** It is likely that the author doesn't even know the relationships.

- For example, [Normalizing Flows (2019)](https://arxiv.org/abs/1912.02762) exists before the [DDPM (2020)](https://arxiv.org/abs/2006.11239), meanwhile [Score based SDE (2020)](https://arxiv.org/abs/2011.13456) appears almost in parallel, exposing both [probablity flow](https://en.wikipedia.org/wiki/Probability_current) and [vector field](https://en.wikipedia.org/wiki/Vector_field) ~~borrowed from QFT but removed physical quantity~~, but [flow matching (2022)](https://arxiv.org/abs/2210.02747) appears a bit later with consolidated relationships, which DDPM utilitizes [discrete time markov chain](https://en.wikipedia.org/wiki/Discrete-time_Markov_chain) *without realizing* (Countable state space a.k.a [Standard Borel space](https://en.wikipedia.org/wiki/Standard_Borel_space)), and proposing [Continuous Normalizing Flows(2018)](https://arxiv.org/abs/1709.01179) with [continuity equation](https://en.wikipedia.org/wiki/Continuity_equation) and [Fokker-Planck equation](https://en.wikipedia.org/wiki/Fokker%E2%80%93Planck_equation) in contrast (as "Optimal Transport objective"). Nevertheless, [it spreads on 2024](https://arxiv.org/abs/2403.03206), as a technical report.

- Vector field can be easily rewritten as another [gradient](https://en.wikipedia.org/wiki/Gradient#Gradient_of_a_vector_field), **but do not confuse with the common gradient descent!** [Latent space](https://en.wikipedia.org/wiki/Latent_space) is different from [Parameter space](https://en.wikipedia.org/wiki/Parameter_space) even they are both [Euclidean space](https://en.wikipedia.org/wiki/Euclidean_space) and depends on data. Pixels are all real numbers without physical quantity / [geodesic](https://en.wikipedia.org/wiki/Geodesic). *Folding protein may consider quantum mechanic or gravity field, but in common folding models, they are still lies on classicial physics, which are still in Euclidean space.* Predicting the image via denoising is not considered as [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) which refers to [optimization algorithm](https://en.wikipedia.org/wiki/Global_optimization) instead of "following the continuity and probablity flow". **Repeat: No physical quantity involved.**

## Guess ##

- *It is likely to implement flow matching on training SDXL (DDPM based model)*, without affecting the prediction / sampling process. However existing trainer codes (either [kohyas](https://github.com/kohya-ss/sd-scripts/tree/sd3) or [naifu](https://github.com/Mikubill/naifu)) are confusing.
