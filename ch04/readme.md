# Chapter 04: A (very dumb) batch script for multiple WebUI instances #

Self explained. Written for ex-mining rig if I can get one of them eventually. 

- Place all `*.bat` to the WebUI directory.
- Modify the scripts if necessary. [Tested with 5 cards, and PCH bottleneck is confirmed.](https://www.instagram.com/p/CwcZQLhy1ad/)
- In case you don't have idea: `COMMANDLINE_ARGS`, `CARD_COUNT`, `DELAY`.
- Double click `webui-user-x.bat` to start.
- Try install [VSCode](https://code.visualstudio.com/) and manually create Terminals to run all of them. At least you won't be blocked by focusing in Window's UI.
- [Yes, it is counted from 0.](https://en.wikipedia.org/wiki/Zero-based_numbering)

# Chapter 04b: (Extra) Making use of M40 24GB for generating LARGE images #

- [Brief description as Youtube Video.](https://www.youtube.com/watch?v=bVbqSobos04&ab_channel=NovaspiritTech) [(CN) A guide to make it perform some simple 3D tasks (not my case).](https://www.youtube.com/watch?v=K1emL7pwDH0&ab_channel=%E7%A5%9E%E5%90%9B%E5%90%9B) [(EN) Got a much older guide.](https://www.reddit.com/r/pcmasterrace/comments/m6evvp/gaming_on_a_tesla_m40_gtx_titan_x_performance_for/)
- [Attempts on hardware mod.](https://extremehw.net/topic/1228-trying-to-improve-a-tesla-m40/) *However I have a [dead 1070](https://www.hkepc.com/16077/Dual_Slot%E9%9B%99%E9%A2%A8%E6%89%87%E8%A8%AD%E8%A8%88_Inno3D_GeForce_GTX_1070_Ti_X2) which makes things really easy.* [(ch2.2) Some more compatable models. Any 900 / 10 Reference PCB models with dual fan / triple fan will work.](https://zhuanlan.zhihu.com/p/536850498)
- *Will try adding PCB parts for display because I have dead cards, for example, Titan X. Hope no software mod is needed.*
- [Bought 2 on 230914, and successfully made it working.](https://www.instagram.com/p/CxLtCNRS__i/?igshid=MWZjMTM2ODFkZg==) **"Above 4G Decoding" is a must. CSM is optional.** Then manually install driver, and be patient on each windows boot. **1280x1280 hires 2.0x will take 32it per hour (110s/it)!** And it uses 19GB VRAM without `xformer` (`--opt-sdp-attention` is not tested yet). If you have trouble paring with newer cards, remove the new card and boot with M40 first.

|Card Models with 16+ GB VRAM|Speculated Price on 230914 ($CNY)|Remarks|
|---|---|---|
|[Tesla M40 24GB](https://zhuanlan.zhihu.com/p/584409286)|$600|**SLOW**|
|[Tesla P100 16GB](https://zhuanlan.zhihu.com/p/635327525)|$1000|**HBM**|
|[Tesla P40 24GB](https://www.bilibili.com/read/cv22426319/)|$900|**Slower then P100**|
|[GeForce RTX 2080 Ti 22GB](https://www.bilibili.com/read/cv22426319/](https://zhuanlan.zhihu.com/p/628356617)https://zhuanlan.zhihu.com/p/628356617)|$2400|**[Hardware mod.](https://www.chiphell.com/forum.php?mod=viewthread&tid=2503364&extra=page%3D1&mobile=no)**|
|[GeForce RTX 3080 Ti 20GB](https://www.extremetech.com/gaming/nvidia-geforce-rtx-3080-ti-with-20gb-of-vram-goes-up-for-sale)|$4000|**Limited Driver**|

- *[Renting cloud service is always a choice.](https://www.autodl.com/)*
