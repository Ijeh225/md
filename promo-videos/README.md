# SpicyFood.CF promo video (62 seconds)

Built from the meal photos, prices, logo and contact details on https://spicyfood.com.ng/menu.

| File | Size | Use for |
|---|---|---|
| `spicyfood_60s_vertical_9x16.mp4` | 1080×1920 | TikTok, Instagram Reels and Stories, YouTube Shorts, WhatsApp Status |
| `spicyfood_60s_square_1x1.mp4` | 1080×1080 | Instagram and Facebook feed |
| `spicyfood_60s_landscape_16x9.mp4` | 1920×1080 | YouTube, Facebook, website |

The video has a silent audio track. Add music when you post.

## Scenes
| Time | Scene |
|---|---|
| 0:00 | Logo, "Hungry?", "Rich flavours, freshly made, delivered fast." |
| 0:04 | Jollof + Half Chicken, ₦3,500 |
| 0:08 | Jollof + Big Turkey, ₦6,000 |
| 0:12 | Jollof + Fish, ₦5,500 |
| 0:15 | Fried Rice + Big Turkey, ₦6,000 |
| 0:19 | Coconut Rice + Full Chicken, ₦6,500 |
| 0:23 | Spaghetti + Big Turkey, ₦4,000 |
| 0:27 | Egusi Soup with Garri ₦5,000, Semo ₦6,000, Pounded Yam ₦7,000 |
| 0:32 | Vegetable Soup with Garri ₦5,000, Semo ₦6,000, Pounded Yam ₦7,000 |
| 0:38 | Okro Soup with Garri ₦5,000, Semo ₦6,000, Pounded Yam ₦7,000 |
| 0:44 | Big Boss Combo, ₦7,500 |
| 0:48 | Mini Odogwu, ₦5,500 |
| 0:52 | Extras: Plantain ₦500, Goat Meat ₦1,000, Big Gizzard ₦1,500, Salad ₦500 |
| 0:57 | "Order in 20–30 mins", WhatsApp 0904 042 2964, spicyfood.com.ng |

## Editing
Scenes, text, prices and durations are in the `S` list in `source/ad.html`. To re-render (needs Playwright and ffmpeg):

```
node source/render.js "$PWD/source/ad.html" video 1080 1920 /path/to/frames
ffmpeg -framerate 30 -i /path/to/frames/f%04d.jpg -c:v libx264 -crf 20 -pix_fmt yuv420p out.mp4
```
