# SpicyFood.CF promo videos

Built from the meal photos, prices, logo and contact details on https://spicyfood.com.ng/menu.

| File | Size | Use for |
|---|---|---|
| `spicyfood_60s_vertical_9x16.mp4` | 1080×1920 | TikTok, Instagram Reels and Stories, YouTube Shorts, WhatsApp Status |
| `spicyfood_60s_square_1x1.mp4` | 1080×1080 | Instagram and Facebook feed |
| `spicyfood_60s_landscape_16x9.mp4` | 1920×1080 | YouTube, Facebook, website |

All videos include an original Afrobeats-style instrumental (106 BPM), generated from scratch by `source/beat.py`, so it is royalty-free. The music alone is in `music/`.

## 36-second ad cut
`spicyfood_36s_ad_*.mp4` (same three sizes): intro, Jollof + Half Chicken, Jollof + Big Turkey, Coconut Rice + Full Chicken, Egusi Soup (Garri, Semo, Pounded Yam), Okro Soup (Garri, Semo, Pounded Yam), Big Boss Combo, then the order details.
Render it with `source/ad.html?keep=0,1,2,5,7,9,10,13` (scene numbers from the full list below, starting at 0).

## Scenes (full 62-second version)
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
