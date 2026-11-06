# SpicyFood.CF promo clips

15-second ad clips built from the meal photos, prices, logo and contact details on https://spicyfood.com.ng.

| File | Size | Use for |
|---|---|---|
| `spicyfood_15s_vertical_9x16.mp4` | 1080×1920 | TikTok, Instagram Reels and Stories, YouTube Shorts, WhatsApp Status |
| `spicyfood_15s_square_1x1.mp4` | 1080×1080 | Instagram and Facebook feed |
| `spicyfood_15s_landscape_16x9.mp4` | 1920×1080 | YouTube, Facebook, website |

The clips have a silent audio track. Add trending music in TikTok, Instagram or CapCut when you post.

## Scenes
1. 0–2.3 s: logo, "Hungry?", "Rich flavours, freshly made, delivered fast."
2. 2.3–4.9 s: Jollof + Half Chicken, ₦3,500 (Bestseller)
3. 4.9–7.3 s: Jollof + Big Turkey, ₦6,000
4. 7.3–9.7 s: Fried Rice, Coconut Rice and Spaghetti, from ₦3,500
5. 9.7–12.1 s: Egusi + Pounded Yam, ₦7,000
6. 12–15 s: "Order in 20–30 mins", WhatsApp 0904 042 2964, spicyfood.com.ng, delivery areas

## Editing
Text, prices and timing are in the `dishes` list in `source/ad.html`. To re-render (needs Playwright and ffmpeg):

```
node source/render.js "$PWD/source" video 1080 1920 /path/to/frames
ffmpeg -framerate 30 -i /path/to/frames/f%04d.jpg -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
```
