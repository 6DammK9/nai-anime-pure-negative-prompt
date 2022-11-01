# Astolfo going to ~~WRC~~ interact: Fusing between SD and NAI #

## Pixiv links and figures (numbers)

- [WRC. Images up to 256 STEPS.](https://www.pixiv.net/en/artworks/102316214) 10 hours for 20 images with `1.5s/it`. Yield rate: 0.6 (legit images with ANY subjects), 0.3-0.4 (car with human)
- [Firearm. Up to 384 STEPS.](https://www.pixiv.net/en/artworks/102375552). Yield > 0.5
- [Firearm. Up to 384 STEPS.](https://www.pixiv.net/en/artworks/102411717). Yield < 0.2 *Prompt issue*
- [Motorcycle. 48 STEPS.](https://www.pixiv.net/en/artworks/102441940). Yield < 0.2 *Wrong image size*

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

## More findings

### WRC

- **I keep future findings here even it is not about the WRC car.**
- Only `WRC` (SD) doesn't work. `race` (NAI) must be included. Although not told explicitly, all prompts will have its own applicable area. **This kind of SVO optimization will be a NP-hard problem.**
- Found reliable sequence: **Object / Asset > Subject / Person > Relationship / Action** + **SD parse > NAI tags**. Proven for firearm / motorcycle also.

### Firearm

```
[[watch dogs]], [[frontline]], [[[firearm]]], [[[rifle]]], [[[pistol]]], [[[handgun]]], [face mask], [[[sunglasses]]], [[solo]], [[astolfo]], [[aiming]]
Negative prompt: [[[[[[bad]]]]]], [[[[[[comic]]]]]], [[[[[[cropped]]]]]], [[[[[[error]]]]]], [[[[[[extra]]]]]], [[[[[[low]]]]]], [[[[[[lowres]]]]]], [[[[[[speech]]]]]], [[[[[[worst]]]]]]
Steps: 768, Sampler: Euler, CFG scale: 10.5, Seed: 4043866474, Size: 512x512, Model hash: 925997e9, Clip skip: 2
```

- `[[[firearm]]], [[[rifle]]], [[[pistol]]], [[[handgun]]]` is a very ambiguous but proven sequence: `firearm` (SD), `rifle` (SD > NAI) > `pistal` (SD > NAI) > `handgun` (NAI). Meanwhile `sniper` **cannot be excluded** (`sniper` > `rifle`?), and `firearm` is used to "open the gate".
- `swat` is risky but nice to mention. 
- `watch dogs` (SD) applies for "style", but `frontline` (NAI, which includes `girls'_frontline`) is required to let the character actally hold the gun. Also, it should pair with `aiming`. 
- Somehow as side effect of `frontline`, I cannot deny `1girl`. Meanwhile adding `1boy` will shift towards `watch dogs` and ruin the entire image.

### Motorcycle

```
[[kawasaki ninja]], [[[watch dogs]]], [[1boy]], [[astolfo]], [[motorcycle]]
Negative prompt: [[[[[[bad]]]]]], [[[[[[comic]]]]]], [[[[[[cropped]]]]]], [[[[[[error]]]]]], [[[[[[extra]]]]]], [[[[[[low]]]]]], [[[[[[lowres]]]]]], [[[[[[speech]]]]]], [[[[[[worst]]]]]]
Steps: 32, Sampler: Euler, CFG scale: 10.5, Seed: 1668969449, Size: 384x640, Model hash: 925997e9, Clip skip: 2
```

- `motogp`... `isle of man tt`... `motorcycle`... `kawasaki` wait what? 6k images of a green motorcycle?
- `kawasaki ninja` works with NAI stuffs, meanwhile `kawasaki KX` still works alone.
- Just include `motorcycle` (SD + NAI) then it works. He is already *on* the motorcycle.
- I love this combination and sequence. So clean.  
