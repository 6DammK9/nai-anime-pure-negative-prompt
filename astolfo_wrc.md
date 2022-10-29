# Astolfo going to WRC: Fusing between SD and NAI #

## Pixiv links and figures (numbers)

- [Images up to 256 STEPS.](https://www.pixiv.net/en/artworks/102316214) 10 hours for 20 images with `1.5s/it`. Yield rate: 0.6 (legit images with ANY subjects), 0.3-0.4 (car with human)


## Prommpts

- ~~You can stop reading if you are not interested or unable to understand the absurd throry below.~~

```txt
parameters
[[WRC]], [race queen], [astolfo], [1boy], [[standing]]
Negative prompt: [[[[[[bad]]]]]], [[[[[[comic]]]]]], [[[[[[cropped]]]]]], [[[[[[error]]]]]], [[[[[[extra]]]]]], [[[[[[low]]]]]], [[[[[[lowres]]]]]], [[[[[[normal]]]]]], [[[[[[speech_bubble]]]]]], [[[[[[worst]]]]]], [breast]
Steps: 384, Sampler: Euler, CFG scale: 24, Seed: 1274018323, Size: 1024x576, Model hash: 925997e9, Clip skip: 2
```

## Theory

- [The weak negative prompts, and discovering the pros (car) in NAI.](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/README.md)
- [Playing Astolfo with some weird stuffs.](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/astolfo_fate.md)
- This time only replacing ~~segs~~ with some legit stuffs (`car` > `WRC`). [There is so many WRC images in the SD dataset therefore it is good on WRC / rally cars](https://www.reddit.com/r/rally/comments/x1yj6w/ai_stable_diffusion_rally_car/). [Someone try to mod with Tesla images and it still works.](https://www.xiaote.com/r/63182dbd73206168b2f7a5d4). **Therefore placing a human inside should be fesible.**
- This time the prompts are weak enough to let SD kick in. Therefore the sequence is important. **Main character must come first.** ~~Sorry Astolfo.~~ Banning `bad` is somehow most effective as there are sufficient datasets supporting it. 
- `race_queen` (danbooru tag) works, `racer` / `crew` (SD tag) doesn't. The prompt is unique enough to be effective.
- To keep *his* existance, the rules in NAI still applies. `standing` should be added to reduce the "area" to let the WRC car has a good shape. The "AI" (diffusion) do not have unerstanding for properties higher than 2D. The image will crash if the "areas" interfering (collided) too hard.
- For the `WRC` side, it can be replaced by just `car` (will transform into random race car), or even `LMP1`. However **short car** can reduce the area and raise the stability.
- I've tried multiple image size. **1024x576 (2.25x area of 512x512) is suitable for placing 2 subjects**, comparing to 640x384 (1x area). CFG scale is *rounded up* for ~~swag~~ no scientific reason. 23.5 is more accurate.
- **STEP count only stops when the image is stable with minor detail changes.** ~~Early stopping with subjective parameter is impossible, which is unfourtunate.~~ All I can do is keep "training" and pray for the rig (ROG R5E + MSI 1080Ti Gaming + open bench) doesn't toasted in the midway.
