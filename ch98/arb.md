# Effectiveness of "Aspect Ratio Bucketing" #

先答你那個 "直圖" / "橫圖":
- SD / DB 默認是跑 CenterCrop, 所以 BOOM
- Ref: https://github.com/huggingface/diffusers/blob/main/examples/dreambooth/train_dreambooth.py

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

然後 "ARB" (機制) 除了分 bucket:
- Bucket 權重有做分配
- RandomCrop 
- Ref: https://github.com/CCRcmcpe/scal-sdt/blob/main/modules/dataset/datasets.py

```py
image: torch.Tensor = transforms.Compose(
    [
        transforms.Resize(dim, interpolation=transforms.InterpolationMode.LANCZOS),
        transforms.CenterCrop(dim) if self.center_crop else transforms.RandomCrop(dim),
        transforms.ToTensor()
    ]
)(pil_image)
```

那個 "效果", 除了確保某個 RandomCrop 會有對應的人物外, 權重上會有所保留. 單個物件不明顯, 但有多個物件時, 例如 "人在背景中", 如果圖集中, 人的位置不是永遠正中的話, ARB 整套機制會由 "沒人 / 半個人" 優化成 "人在旁邊".

ARB 原文: https://blog.novelai.net/novelai-improvements-on-stable-diffusion-e10d38db82ac

RandomCrop / Distibution 算不算 ARB 的一部份 有效成份

先交給群友
