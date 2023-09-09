# Discussion about Aspect Ratio Bucketing #

## (New) Finding models trained with ARB ##

- It can be found in [metadata inside model header](https://github.com/by321/safetensors_util). However there is limitation, old SD1.X models are not applicable. Seems that there is no proof unless the original training script is given. [My findings.](https://github.com/by321/safetensors_util/pull/3) SDXL will be fine.

## Original description of ARB ##

- [NovelAI's article.](https://blog.novelai.net/novelai-improvements-on-stable-diffusion-e10d38db82ac) [Cited in SDXL's paper.](https://arxiv.org/abs/2307.01952)

## Effectiveness of "Aspect Ratio Bucketing" ##

- SD1.X / DB use `CenterCrop` by default. Entity's information (or its segment, "part of it") may not able to capture effectively by selecting center in brute force. With "ARB", entity's information will have a fair chance to be captured and learnt by the model, and finally able to construct the relationship between the entities and the whole canvas. For example, "positional relationship", and even "important features" in corners instead of the whole blob.

"ARB" (mechanism) is more then assigning buckets:
- Bucket weights is not uniform
- Using `RandomCrop` instead of `CenterCrop` 
- [Ref (DB)](https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/train_dreambooth.py)
- [Ref (ND)](https://github.com/Mikubill/naifu-diffusion/blob/main/scripts/encode_to_latent.py)

```py
self.image_transforms = transforms.Compose(
    [
        transforms.Resize(size, interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.CenterCrop(size) if center_crop else transforms.RandomCrop(size),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ]
)
```

- [Ref (SSDT)](https://github.com/CCRcmcpe/scal-sdt/blob/main/modules/dataset/datasets.py)

```py
image: torch.Tensor = transforms.Compose(
    [
        transforms.Resize(dim, interpolation=transforms.InterpolationMode.LANCZOS),
        transforms.CenterCrop(dim) if self.center_crop else transforms.RandomCrop(dim),
        transforms.ToTensor()
    ]
)(pil_image)
```
