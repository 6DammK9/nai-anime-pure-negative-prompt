# Observation from NovelAIDiffusionV5 #

*Actually there should be no suprise at all.* ~~Paid scientists / engineers won't make the mistake as in [anima](./anima.md).~~

## Dataset / architecture change ##

*tldr: Worth re-evalulate prompts from 3 or 4.5.*

### Unified training dataset ###

- (Not new) The "furry button" is no longer switching model or applying LoRA. It is just a prompt addition as described in [official guide](https://docs.novelai.net/en/image/tags#dataset-tags).

- Then the guess (or the bias to be explored) is very straight forward:
  - Basic illustration concepts (including art / character design) would be categorized in *color, shape, and positions*.
  - Basic entities in prompts (artist / character / dataset / ~~quality or time~~) would map on the category above.
  - Prompt styles (symbols / made up syntax / legit tags or natural languages) will handle the rest: Mapping raw prompts into entities, finally the illustration.
  - ~~No guardrail / backend API intrusion has been considered.~~

- Dataset tag like `fur_dataset` should does something.
- Artist tag like `abmayo` (known Miku Hatsune one trick with obvious shapes), or `horokusa0519` (known Kemo / furry contents with obvious shape) will do something.
  - Notice that `horokusa0519` does not appear in danbooru because of furry contents. This is important ~~I though I had a hard time to find such tag~~.
- Character tag like `astolfo` (random pink hair boy) or `hatsune_miku` (random cyan hair girl) will also do something.
- General category tag like `1boy` (implies to human) and `anthro` (implies to non human) will do what it intends for, since it is no longer an entity.

- However **model bias** determines how they blends, from evenly distributed mapping ([my AstolfoRF](../ch06/gallery_2602.md)), or having quantized effect (anima).
  - Obviously if the tag is never seen, or just being too infrequent, model will not learn and **ignore the tag**.
  - Sure, if you throw absolutely no tag, [unconditional image generation](https://huggingface.co/tasks/unconditional-image-generation) happens and you will see general  illustration (at least for NAI models), or just fragmented stuffs.

- Since there are 3 / 4 dimensions to test, I just eliminate the character dimension ~~pink hair furry femboy incoming~~ to show that what V5 has been overcomed.

- Unless specified, all are generated via a discord bot, on mobile phone, with my poor copy and paste skill (and discord app bug).
  - `[model_name]` in X axis, others in Y axis.
  - The bot is obviously not public so don't ask for link.
  - `-QU -UC Heavy` has been dropped for showing model bias.
  - `horokusa0519` on `nai-diffusion-5-full` is switched to `nai-diffusion-5-curated` for clearer explnantion.
  - Most images are just generated with 1-2 tries without cherry picking.

```txt
AI.novelai 

"1boy, [entity], astolfo, [non_entity]"

""

-W 1024 -H 1024 -images 1 --model [model_name] -steps 24 -scale 6
```

|`[entity]`|`nai-diffusion-5-full`|`nai-diffusion-4-5-full`|`nai-diffusion-3`|
|---|---|---|---|
|`fur_dataset`|![fur_dataset_50.png](./img/fur_dataset_50.png)|![fur_dataset_45.png](./img/fur_dataset_45.png)|![fur_dataset_30.png](./img/fur_dataset_30.png)|
|`abmayo`|![abmayo_50.png](./img/abmayo_50.png)|![abmayo_45.png](./img/abmayo_45.png)|![abmayo_30.png](./img/abmayo_30.png)|
|`horokusa0519`|![horokusa0519_50.png](./img/horokusa0519_50.png)|![horokusa0519_45.png](./img/horokusa0519_45.png)|![horokusa0519_30.png](./img/horokusa0519_30.png)|
|(all empty)|![null_50.png](./img/null_50.png)|![null_45.png](./img/null_45.png)|![null_30.png](./img/null_30.png)|
