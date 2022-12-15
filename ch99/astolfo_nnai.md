# Astolfo in NNAI #

- [WRC (failure)](https://www.pixiv.net/en/artworks/102945246)
- [Benz (still failure)](https://www.pixiv.net/en/artworks/102995368)
- [WRC (fine)](https://www.pixiv.net/en/artworks/103177023)
- [Benz (fine)](https://www.pixiv.net/en/artworks/103111722)

### Still NAI, but biased ###

```txt
[[mercedes]], [[race queen]], [male], [astolfo]
```

```txt
[[[WRC]], [[race queen]], [male], [astolfo], [[standing]]
```

- Somehow the bias only does mild effect on prompts / art styles. The streadgy for NAI remains the same, with the negative prompt streangth minimized.
- (Faith) For biased model, use `male` instead of `boy`, otherwise the shape is too girly.
- `bulge` is ineffective. Believed that `race queen` limited the "featrue".
- Yield is similar to NAI. Even the face is similar to NAI. But when you **paying attention on his face**, there is a slight difference (<10%): 
1. The pupil is larger
2. Facial expression (smug) is wider
3. Hair style a little bit asymmetric (I like this most: VAE tends to make it symmetric)

- Well, it *may be a good bias*. Now I can generate a "detailed" image with the similar prompt in NAI. It is **richer in sceneary (WITH SUBJECT)**, and **higher chance to obtain a detailed subject**. As by-product it may be * Multi Point Perspective*. 
