# SpicyFood.CF promo videos

Built from the meal photos, prices, logo and live website at https://spicyfood.com.ng. The goal is to send people to the website to order.

| File | Length | Use for |
|---|---|---|
| `spicyfood_40s_ad_vertical_9x16.mp4` | 40 s | Paid ads: Reels, Stories, TikTok |
| `spicyfood_40s_ad_square_1x1.mp4` | 40 s | Paid ads: Facebook and Instagram feed |
| `spicyfood_40s_ad_landscape_16x9.mp4` | 40 s | Paid ads: YouTube, Facebook in-stream |
| `spicyfood_70s_full_*.mp4` | 70 s | Normal posts on your pages, website, YouTube |

All videos include an original Afrobeats-style instrumental (106 BPM), generated from scratch by `source/beat.py`, so it is royalty-free. The music alone is in `music/`.

## 40-second ad
Intro, Jollof + Half Chicken (₦3,500), Coconut Rice + Full Chicken (₦6,500), Egusi Soup (Garri ₦5,000 / Semo ₦6,000 / Pounded Yam ₦7,000), Okro Soup (same options), Big Boss Combo (₦7,500), **website demo** (phone screen: menu, meal, Add to Cart, cart), then **"Order now at spicyfood.com.ng"** (WhatsApp shown small as a backup).

## 70-second full version
Intro, 6 rice and pasta dishes, Egusi / Vegetable / Okro soups each with Garri, Semo and Pounded Yam, Big Boss Combo, Mini Odogwu, extras, website demo, then "Order now at spicyfood.com.ng".

## Editing
Scenes, text, prices and durations are in the `S` list in `source/ad.html`. Choose scenes with `?keep=` (numbers start at 0):
- full: `ad.html?keep=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14`
- ad: `ad.html?keep=0,1,5,7,9,10,13,14`

```
node source/render.js "$PWD/source/ad.html?keep=0,1,5,7,9,10,13,14" video 1080 1920 /path/to/frames
python3 source/beat.py 40 music.wav
ffmpeg -framerate 30 -i /path/to/frames/f%04d.jpg -i music.wav -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -shortest out.mp4
```
