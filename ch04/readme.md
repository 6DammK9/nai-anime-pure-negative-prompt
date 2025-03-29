# Chapter 04: Infrastructure / Hardware related stuffs #

## Chapter 04a: A (very dumb) batch script for multiple WebUI instances ##

Self explained. Written for ex-mining rig if I can get one of them eventually. 

- Place all `*.bat` to the WebUI directory.
- Modify the scripts if necessary. [Tested with 5 cards, and PCH bottleneck is confirmed.](https://www.instagram.com/p/CwcZQLhy1ad/)
- In case you don't have idea: `COMMANDLINE_ARGS`, `CARD_COUNT`, `DELAY`.
- Double click `webui-user-x.bat` to start.
- Try install [VSCode](https://code.visualstudio.com/) and manually create Terminals to run all of them. At least you won't be blocked by focusing in Window's UI.
- [Yes, it is counted from 0.](https://en.wikipedia.org/wiki/Zero-based_numbering)

## Chapter 04b: Making use of M40 24GB for generating LARGE images ##

- [Brief description as Youtube Video.](https://www.youtube.com/watch?v=bVbqSobos04&ab_channel=NovaspiritTech) [(CN) A guide to make it perform some simple 3D tasks (not my case).](https://www.youtube.com/watch?v=K1emL7pwDH0&ab_channel=%E7%A5%9E%E5%90%9B%E5%90%9B) [(EN) Got a much older guide.](https://www.reddit.com/r/pcmasterrace/comments/m6evvp/gaming_on_a_tesla_m40_gtx_titan_x_performance_for/)
- [Attempts on hardware mod.](https://extremehw.net/topic/1228-trying-to-improve-a-tesla-m40/) *However I have a [dead 1070](https://www.hkepc.com/16077/Dual_Slot%E9%9B%99%E9%A2%A8%E6%89%87%E8%A8%AD%E8%A8%88_Inno3D_GeForce_GTX_1070_Ti_X2) which makes things really easy.* [(ch2.2) Some more compatable models. Any 900 / 10 Reference PCB models with dual fan / triple fan will work.](https://zhuanlan.zhihu.com/p/536850498)
- *Will try adding PCB parts for display because I have dead cards, for example, Titan X. Hope no software mod is needed.*
- [Bought 2 on 230914, and successfully made it working.](https://www.instagram.com/p/CxLtCNRS__i/?igshid=MWZjMTM2ODFkZg==) [Coverted into "Inno3D iChill Tesla M40 24GB Hybird"](https://www.instagram.com/p/CxtzLg9yGI4/) **"Above 4G Decoding" is a must. CSM is optional.** Then manually install driver, and be patient on each windows boot. **1280x1280 hires 2.0x will take 32it per hour (110s/it)!** And it uses 19GB VRAM without `xformer` (`--opt-sdp-attention` **is not supported**). If you have trouble paring with newer cards, remove the new card and boot with M40 first.
- ~~[I have received my very first informal sponser.](https://www.instagram.com/p/Cx3HM5xyx85)~~ Technically I'm not owning her, but it is a unique chance for me.

|Card Models with 16+ GB VRAM|Speculated Price on 230914 ($CNY)|Remarks|
|---|---|---|
|[Tesla M40 24GB](https://zhuanlan.zhihu.com/p/584409286)|$600|**SLOW**|
|[Tesla P100 16GB](https://zhuanlan.zhihu.com/p/635327525)|$1000|**HBM**|
|[Tesla P40 24GB](https://www.bilibili.com/read/cv22426319/)|$900|**Slower then P100**|
|[GeForce RTX 2080 Ti 22GB](https://www.bilibili.com/read/cv22426319/](https://zhuanlan.zhihu.com/p/628356617)https://zhuanlan.zhihu.com/p/628356617)|$2400|**[Hardware mod.](https://www.chiphell.com/forum.php?mod=viewthread&tid=2503364&extra=page%3D1&mobile=no)**|
|[GeForce RTX 3080 Ti 20GB](https://www.extremetech.com/gaming/nvidia-geforce-rtx-3080-ti-with-20gb-of-vram-goes-up-for-sale)|$4000|**Limited Driver**|

- *[Renting cloud service is always a choice.](https://www.autodl.com/)*

## Chapter 04c: My setup scripts ##

- There are popular [Google Colab scripts](https://github.com/camenduru/stable-diffusion-webui-colab).

- However since I'm using [physical PC / WS](./ice_lake_ws.md) and typcial Winodws / Nvidia combo, I made myself [a install command](./local-install-env.md).

- Now I have added a [dedicated training rig](./4x3090_v2.md) with [manjaro linux installed](../ch06/manjaro/readme.md). It trains the entire SDXL with compromised setting.

## Chapter 04d: How to gather "decomissioned server parts" ##

- *Based from my experience.* I'll try to write down general statements but actual procurement will differs from location / policies / society preference.

- If you see the item from Amazon / Ebay / AliExpress / Wish etc. with random brand names, Google it directly and it is probably link to Chinese websites. If that is the case, Taobao / Xianyu will definitely has lower price even with shipping.

- If it appears in Amazon or Aliexpress, try Taobao. If it appears in Ebay, try Xianyu. Xianyu is generally "second hand market" of Taobao (under same company).

- Both Taobao / Xianyu, or *most* "Chinese Mobile Apps", are having little web content due to implied regulation. You'll need a dedicated mobile phone and phone number to receive SMS. Both of them requires Alipay for transaction. Credit card is possible, but not Paypal, likely to link to Alipay first.

- If you are able to reach local salvage brokers (or some retailers / individual deals), you already get the cheapest price. I bought some server RAMs which are cheaper than Xianyu. Notice that low price from Taobao / Xianyu are mainly because of [EMH](https://en.wikipedia.org/wiki/Efficient-market_hypothesis) and the major international salvage parts marketplace. For counter example, local price of RTX 4090(D) may be chaper than Taobao / Xianyu because of high demand and tariff.

- Logistic preference between Taobao / Xianyu are different. Taobao has "official logistic agent" while Xianyu doesn't. Also there is an unique "Consolidated Consignment (集運)" system to reduce logistic cost, instead of conventional courier which is usually direct shipping. 

- For "consolidated consignment": First seller send the good to assigned storage, which is owned by the consolidator, then you tell the consolidator to send the goods to the detination, which is usually pickup points owned by the consolidator also. For some bizzare cases (preffered by me), the "pickup point" can be lockers in some public space (e.g. laundry shop, bus terminals) open for 24/7, then pickup the goods in midnight. Sometimes direct shipping is not applicable for insecure places.

- If the "checkout process" is blocked in Taobao with official logistic agent (due to regulatory reason), **first dobule check the good is legit**. The condition changes frequently, which may not consistent across time. Sometimes it is blocked because of title (e.g. "T-Shirt with meme *A100 H100 advanced AI* generated image"). Other than language barrier, *be brave to notice sellers that you are not from [Mainland China](https://en.wikipedia.org/wiki/Mainland_China).* There should be "special arrangement" for the process. Many sellers have related experience and dedicated pracice especially for non-consumer parts. If you are buying parts from individuals, you may need to feed some "information" and let them decide. Skipping informing the seller, and sending to consolidator *may works* (**repeat, dobule check the good is legit first!**), but you may risk being rejected from there.

- Finally, it is same as buying stuffs unseen. Warrenty is not likely. The goods can be DOA because of poor container. *Cheap price comes with risk.*