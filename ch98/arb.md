# Effectiveness of "Aspect Ratio Bucketing" #

先答你那個 "直圖" / "橫圖":
- SD 默認是跑 CenterCrop, 所以 BOOM

然後 "ARB" (機制) 除了分 bucket:
- Bucket 權重有做分配
- RandomCrop 

那個 "效果", 除了確保某個 RandomCrop 會有對應的人物外, 權重上會有所保留. 單個物件不明顯, 但有多個物件時, 例如 "人在背景中", 如果圖集中, 人的位置不是永遠正中的話, ARB 整套機制會由 "沒人 / 半個人" 優化成 "人在旁邊".

原文: https://blog.novelai.net/novelai-improvements-on-stable-diffusion-e10d38db82ac

圖: https://github.com/CCRcmcpe/scal-sdt/blob/main/modules/dataset/datasets.py

RandomCrop / Distibution 算不算 ARB 的一部份 有效成份

先交給群友
