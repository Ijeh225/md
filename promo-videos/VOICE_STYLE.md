# SpicyFood.CF house voice

Default voiceover for all SpicyFood promo videos (approved by the owner).

## Voice
- **ElevenLabs voice:** Ifeoma Odumodu, Nigerian English female
- **Voice ID:** `reGkImJki7uJOve2F4A0`
- **Model:** `eleven_v3` (expressive)
- **Settings:** stability 0.0, similarity_boost 0.85, style 0.0, use_speaker_boost true
- **Output format:** `mp3_44100_128` (Starter plan)

## Delivery: "super energy", normal pace
Put an emotion tag on every line, for example:
`[shouting excitedly]`, `[super excited, loud]`, `[very energetic, loud]`, `[playful, loud]`, `[hyped, shouting]`.
Stress key words in CAPS ("ALL OF THIS", "YOUR way", "STILL", "Order NOW").
Write prices in words: "five thousand five hundred naira".
Say "chicken or turkey", not "big chicken" or "big turkey".

## Post-processing (ffmpeg)
1. Shorten pauses longer than 0.32 s down to about 0.22 s
2. `atempo=1.07` (slightly faster, not rushed)
3. `highpass=f=90`, presence boost `equalizer=f=3000:t=q:w=1.2:g=2.5`
4. `acompressor=threshold=-26dB:ratio=6:attack=2:release=50:makeup=6`
5. Gain to about -9 LUFS, then `alimiter=limit=0.93`

## Music bed
- ElevenLabs Music, energetic **Afropop / Highlife**, about 115 BPM, instrumental
  (talking drums, brass stabs, highlife guitar, made to sit under a female announcer)
- Duck the music under the voice (sidechain ratio 10, release about 380 ms)
- Final mix about -11 LUFS
- Sound effects on key words: a boom on the reveal, whooshes on drops, pops on drinks, ka-ching on the price

Reference: `source/voiceover/` (script, scene file, effects script, speech check)
