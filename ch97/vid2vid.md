# Blue pill on vid2vid on 2305 #

## Abstract ##

- "Blue pill" (極簡版 [SoK](https://blog.csdn.net/u010970698/article/details/109106690)) 一枚. 因為格式問題, 暫時丟來 ch98.
- **大部份展示皆含代碼.**

## Introduction ##

### 基本版 text2video ###
- [Huggingface 的解說連展示](https://huggingface.co/blog/text-to-video)
- [nateraw/stable-diffusion-videos](https://github.com/nateraw/stable-diffusion-videos#readme)

### 或者能談合作的 text2video ###
- [damo-vilab/text-to-video-ms-1.7b](https://huggingface.co/damo-vilab/text-to-video-ms-1.7b)
- [人家 demo](https://huggingface.co/spaces/damo-vilab/modelscope-text-to-video-synthesis)

### (231023 更新) 整合至 SD, 帶有 motion module 的 text2video ###
- [AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning](https://arxiv.org/abs/2307.04725)
- [WebUI 整合](https://github.com/continue-revolution/sd-webui-animatediff)

### (231028 更新) m2m / mov2mov 相關 ###

- *小心一詞多義.*
- [video-to-video](https://stable-diffusion-art.com/video-to-video/)
- [mov2mov](https://github.com/Scholar01/sd-webui-mov2mov)
- [controlnet-m2m](https://github.com/lllyasviel/ControlNet/issues/184), [link](https://github.com/Mikubill/sd-webui-controlnet/discussions/546), [x](https://twitter.com/toyxyz3/status/1632731437941268481)

## Methods ##

### 每幀 i2i 的 v2v (用了 anythingv3) ###
- [人家 demo](https://huggingface.co/spaces/doevent/video_to_video_diffusion)
- [同技術的解說](https://www.youtube.com/watch?v=sVmi2Yp43c0&ab_channel=MDMZ)

### 這個用了 CN + optical flow 優化 ###

> "比vid2vid唯一優勢就是controlnet mask是完美的，因為可以從blender直接導出"

- [volotat/SD-CN-Animation](https://github.com/volotat/SD-CN-Animation)
- [VTuber 系的 vid2vid (解說)](https://note.com/alone1m/n/n5579c1b170c7)
- [效果展示](https://twitter.com/kaizirod/status/1655420585714028551)

### "對練" 模型 (人家有 B 站) ###
- [AC 系列](https://huggingface.co/JosephusCheung/ACertainty)
- [專門出人物可以用這個 (同系列)](https://huggingface.co/JosephusCheung/ACertainThing)

### A / R 雙修的大佬 ###
- [WD](https://huggingface.co/waifu-diffusion/wd-1-5-beta2-extra)
- [AIpicasso](https://huggingface.co/aipicasso/cool-japan-diffusion-2-1-2)
- [MAJIC](https://civitai.com/models/41865/majicmix-fantasy)
- [Dreamlike-art](https://huggingface.co/dreamlike-art/dreamlike-photoreal-2.0)


### LLaMA 禁商用, 但可以用 lora 繞過 (含中文) ###
- [例子, Guanaco 系列](https://huggingface.co/KBlueLeaf/guanaco-7B-leh)
- [另一個 LLaMA](https://github.com/ymcui/Chinese-LLaMA-Alpaca)

## Related Works ##

- [AI 協助的 CG "Ai MoCap"](https://www.rokoko.com/)
- [學術上的 video diffusion (模型不通用)](https://github.com/lucidrains/video-diffusion-pytorch)
- [Deforum SD](https://github.com/deforum-art/deforum-stable-diffusion)
- [偏向理論的 SD 介紹 (當刻的影像生成模型皆是 LDM)](https://www.zhihu.com/question/575509366)

## Conclusion ##

- 最好無視生成文本 (text) 跟成品視頻 (video) 的關係, 分開生成. (數學) 模型用途不能更改.
- 風格 merge / 大型 finentune + LoRA / EMB 細節補充為 *獨立題目*.

## Ackowledgement ##

- [感謝 RL 對此的持續研究。](https://github.com/ReaLifecyborg/MaskAnimationDiffusion/blob/main/README.md) 

## Reference ##

*互聯網*

## Appendix ##

[人家 demo](https://huggingface.co/spaces/damo-vilab/modelscope-text-to-video-synthesis) 的 [例子](https://imgur.com/a/85UvVGN)

![https://i.imgur.com/y7nGFvL.png](https://i.imgur.com/y7nGFvL.png)
