# Notes on "NF4", a new precision after FP8 #

## What is NF4? ##

- [Medium article on NF4, "NF data type builds on Quantile Quantization".](https://id2thomas.medium.com/ml-bitsandbytes-nf4-quantize-dequantize-analysis-1ad91d9912c9 )

## Why NF4 is introduced into SD community? ##

- [Reddit thread about "NF4" precision, and cpmparasion with FP8 and FP16.](https://www.reddit.com/r/StableDiffusion/comments/1eplvi8/the_image_quality_of_fp8_is_closer_to_fp16_than/)
- ["What we should learn from the Flux release"](https://www.reddit.com/r/StableDiffusion/comments/1eps53t/what_we_should_learn_from_the_flux_release/ )
- [CN article on NF4](https://bbs.nga.cn/read.php?tid=41235344&rand=547)

## How NF4 is used? ##

- [SD Forge about NF4 support on Flux.](https://github.com/lllyasviel/stable-diffusion-webui-forge/discussions/981)
- [NF4 on HF diffusers, with code example.](https://github.com/huggingface/diffusers/discussions/8746)

> bitsandbytes is only supported on CUDA GPUs for CUDA versions 11.0 - 12.5.

- Class name is `bitsandbytes.nn.Linear4bit`. *Also, it requires dedicated code / model implementation, because it is no longer native torch FP8.*
- Looks like it supports GTX 10 series, instead of newest RTX 40 series for FP8.
- It is no longer `torch` native therefore requires additional consideration in development (e.g. A1111 Extensions / Comfy Nodes / dedicated Trainer, Merger and Toolkits).

- [Class reference in HF diffusers.](https://huggingface.co/docs/bitsandbytes/reference/nn/linear4bit)
- [Online doc in Bitsandbytes repo.](https://github.com/bitsandbytes-foundation/bitsandbytes/blob/main/README.md)
- [Installing / building "bitsandbytes"](https://huggingface.co/docs/bitsandbytes/main/en/installation?source=Windows&backend=AMD+ROCm#multi-backend )
