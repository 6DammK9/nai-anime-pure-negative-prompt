# "NAI Anine" Pure Negative Prompt #

A research about "NAI anime" art with pure negative prompt. Such observation may be useful for "data visualization" to show that how the "number" works.

[Pixiv album for storing the images](https://www.pixiv.net/en/tags/PureNegativePrompt/artworks)

### Core concept ###
- [UNCONDITIONAL DIFFUSION GUIDANCE](https://openreview.net/pdf?id=lsQCDXjOl3k) (I have no connection to any of the scholars.)
- The "solver" does a kind of [clustering](https://en.wikipedia.org/wiki/Cluster_analysis) which is a kind of [unsupervised learning](https://en.wikipedia.org/wiki/Unsupervised_learning).
- The [Gradient descent](https://en.wikipedia.org/wiki/Gradient_descent) inside the neural network is also somewhat a kind of [Reinforcement learning](https://en.wikipedia.org/wiki/Reinforcement_learning)
- Therefore you can "guide" the AI to somewhat generate waifu in a *almost pure random sense* without mentioning a positive prompt.

### How NovelAI / Stable Diffusion / CLIP works ###
- [Video](https://www.youtube.com/watch?v=1CIpzeNxIhU&ab_channel=Computerphile)
- [Lenghty explaination which is expected](https://blog.novelai.net/novelai-improvements-on-stable-diffusion-e10d38db82ac).

### Basic settings ###

- Network: `animefull-final-pruned` (with VAE)
- Skip CLIP layer: **2**
- Only `txt2img` is used.
- No high-res fix.
- Only output dimension, CFG and random seed is modified.
- **Training step will exceed 150**. Edit `ui-config.json` to increase the limit. Sometimes it failed to converge to a "reasonable" image. If you see pale background. Keep increasing STEP, until you see background. 
- **Cherry pick unless I'm sure how to generate with consistent quality** i.e. most of the contents inside is recognizable and approved by me.
- Therefore no scipt / notebook yet.

### Endless sampling step ###
In art sense, this AI (or this kind of AI aka "diffuser") doesn't have logic in counting or physic. However, we can create [Isometric projection](https://en.wikipedia.org/wiki/Isometric_projection) and fractal art such as [Affine transformation](https://en.wikipedia.org/wiki/Affine_transformation). With a RL approch and such kind of visual trick (and the "minor" datasets hidden inside the neural network), **we can create fine art with this approch**. Minimal positive prompt and BAM. **~~1000~~ 768 STEP is proven, comparing with 150 STEP as default maximum range.**

### Negative prompt used ###

- The **most general** you can find in the internet. However weighting may be adjusted.
- Somewhat they are really mandatory otherwise it create the image *exactly match the tags*.
- Also, **even negative prompt should keep minimal** (18 tokens). *It won't able to create art without creavity.* 

```txt
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name
```

- Step up: `node step [ratio] [full]`. `ratio` can be negative (exponential scale) or floating point (free type) or SD brackets (integer). `full` will apply the format to each word instead of whole sequence. See [this guide](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#attentionemphasis) for guessing the *step size*. Too large will unable to form an object but a simple pattern. 0.9 is somewhat balanced. The *hyperparameter* is regaulated under [https://en.wikipedia.org/wiki/No_free_lunch_theorem](https://en.wikipedia.org/wiki/No_free_lunch_theorem). Both side is abstract idea: *How to make sure the creativity lead into productivity?*

```txt
(lowres:0.9), (bad anatomy:0.9), (bad hands:0.9), (text:0.9), (error:0.9), (missing fingers:0.9), (extra digit:0.9), (fewer digits:0.9), (cropped:0.9), (worst quality:0.9), (low quality:0.9), (normal quality:0.9), (jpeg artifacts:0.9), (signature:0.9), (watermark:0.9), (username:0.9), (blurry:0.9), (artist name:0.9)
```

- This extended set can be a lot lower (81 tokens). Note that **I've dropped missing_x intentionally.**
```txt
(bad_anatomy:0.82), (bad_feet:0.82), (bad_hands:0.82), (bad_perspective:0.82), (bad_proportions:0.82), (comic:0.82), (cropped:0.82), (cropped_arms:0.82), (cropped_head:0.82), (cropped_legs:0.82), (cropped_shoulders:0.82), (cropped_torso:0.82), (english_text:0.82), (error:0.82), (extra:0.82), (low quality:0.82), (lowres:0.82), (no_humans:0.82), (normal quality:0.82), (outside_border:0.82), (speech_bubble:0.82), (text_focus:0.82), (worst quality:0.82)
```

- **Remove when it is solved** All underscore `_` in WebUI doesn't work! Do not pay attention on the prompts with `_`!
- e.g. `on_back` or `on back` will be split as `on` and `back` and getting irrelevant images.
- This will greatly alter the contents below. **22 tokens.** I keep `_` for "not being too gibberish".
- Meanwhile I revise the keywords extensively, and going to **bear risk** to mine fine arts.
```txt
(bad:0.564), (comic:0.564), (cropped:0.564), (error:0.564), (extra:0.564), (low:0.564), (lowres:0.564), (normal:0.564), (speech_bubble:0.564), (worst:0.564)
```
- In non WebUI style:
```txt
[[[[[[bad]]]]]], [[[[[[comic]]]]]], [[[[[[cropped]]]]]], [[[[[[error]]]]]], [[[[[[extra]]]]]], [[[[[[low]]]]]], [[[[[[lowres]]]]]], [[[[[[normal]]]]]], [[[[[[speech_bubble]]]]]], [[[[[[worst]]]]]]
```

- Obviously more prompts can be added, however I'm not going to generate fap material. They've already flooded the internet.

### (Optional) Force to have human (face) by limiting aspect ratio and area ###

- Some friend told me that [SD / NAI is being incoherent with total area more than 512x512](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/1025). **Also the tensors forced the unit of 64px**. I have added a script also `node aspect512.js [w] [h]`:

```txt
node aspect512.js [4] [3]
> [576, 384]
node aspect512.js [16] [9]
> [640, 384]
```

- Note that you usually unable to keep the expected aspect ratio. However I choose to *not following this guide* even it looks promising. **Also you may get cropped image.**

### Inference with SD prompts ###
- Maybe I can find some negative prompts EXCLUSIVE from SD dataset. ere is some positive prompts which is fun to play in NAI:
```txt
Mercedes-Benz, AMG
husky with heterochromia
apocalypse
```

### General result ###

- The range may varies across different random seed.

|Field|Content|Range|
|---|---|---|
|Random seed|Theme|`int()`|
|Dimension / area|*Count of objects*|No more than 3x area of 512x512|
|Aspect ratio|Pose (sometime count)|From 4:1 to 1:4|
|CFG|Brightnes, *scaled with detailing*|Somehow scale with dimension. 512x512 will be stable at 12~16|
|Solvers|Minor art style (major one is the network itself)|Currnetly **Eular** only|
|"W"|"Gradient of RL". *Density of objects*|1 for standard. Lower then 1 to introduce randomness. Currently 0.82 with modified prompt.|

- For the "0.91" approch, follow the scale with base 16.
- For the "0.82" (`2x[`) approch, follow the scale with base 12.
- For the "0.564" (`6x[`) approch, follow the scale with base 10.5.

|Dimension|CFG Range|CFG Recommended|
|---|---|---|
|512x512|12~16|~~12~~10.5|
|512x768|18~24|16|
|576x768|18~24|24|
|768x512|18~24|~~21~~16|
|768x576|18~24|18|
|1024x576|24~30|27|
|576x1024|12~30|27|
|768x768|27~36|~~27~~24|
|1408x512|27~36|27|
|512x1408|27~36|27|

|Dimension (Area fixed)|CFG Range|CFG Recommended|
|---|---|---|
|384x640|12~16|~~12~~10.5|
|640x384|12~16|~~12~~10.5|
|896x256|12~16|~~12~~10.5|
|256x896|12~16|~~12~~10.5|
|1024x256|12~16|~~12~~10.5|
|256x1024|12~16|~~12~~10.5|

|W|What will happen|
|---|---|
|0.9|A lot more objects and "human" may disappear. Maybe sceneary, but **I've got some cars and bulidings.**|
|0.95|The "human" will interact with objects|
|1.0|Average to what you usually seen in internet|
|1.05|"Object inside objects" will be only simple geometry|
|1.1|Almost no "Object inside objects"|
|2.0|Simple geometry with a unique bright sphere|

|Area over 512x512|What will happen|
|---|---|
|<1.0|**Cropped images**|
|1.0|Standatd object. Any traceable error will form tiny regular objects|
|1.5|Either rich background, or some malfromed objects|
|>2.0|Start having multiple objects. **Or anything above combined.**|

|Aspect ratio|What will happen|
|---|---|
|<0.5|Something may appear on top of the human's head.|
|0.6 to 0.75|~~Don't abuse OK?~~|
|>0.75|**1.0 inclued**. You may get human or objects with sceneary, ~~but sometimes malformed~~. Recommend to enlarge the area above 1.0|

### Bizzare result ###

- Looks like the "random stuffs" may refers to images in resnet / captcha. At least they really looks like something.  
- Converting them into postive prompts may favour for the AI, and useful to stablelize the result:

```
car
house
park
sky
```

- For example, combining the prompt **and the corrosponding aspect ratio** and a few more can generate some *nice* image with only a few token:

|Size|Prompt|
|---|---|
|768x576|`(miku:1.0), (1girl:0.91), (car:0.75)`|

- *Sequence of the words will create slight difference.* However no major difference is found. It is because the transformer itself was design for [NLP](https://en.wikipedia.org/wiki/Natural_language_processing), however both SD and NAI was trained heavily in [CLI](https://en.wikipedia.org/wiki/Command-line_interface) style ("tags" instead of paragraph corpus). 
- Try to arrange the tags in [SVO](https://en.wikipedia.org/wiki/Subject%E2%80%93verb%E2%80%93object_word_order) style, mark the strength according to the importance (person > plot > details), and finally arrange them in decreasing order.
- **Recommended to keep the weight into NEGATIVE EXPONENTIAL SCALE.** For example, 0.95 for the character, then 0.91 for some basic requirement, then 0.82 for characteristics, and 0.75 for "good to have" detail. AI will "choose" how to include the stuffs. 

### Bizzare result (in batch) ###

- For the `W=0.9` approch, sometimes it fails to generate human even it is in `512x512`. Probability will be shown in below.

|Dimension|Sample size|Pattern|Object or Sceneary|Malformed Human|Legit Human|Body shape|
|---|---|---|---|---|---|---|
|512x512|20|4|3|5|8|Normal|
|576x768|20|0|2|5|13|Thicc|
|1024x576|20|0|12|4|4|Normal|
|576x1024|20|0|2|2|16|Mixed|
|768x768|15|1|4|7|3|Normal|

### Awesome result ###

- See [astolfo_fate.md](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/astolfo_fate.md)
- Astolfo go racing. [astolfo_wrc.md](https://github.com/6DammK9/nai-anime-pure-negative-prompt/blob/main/astolfo_wrc.md)
