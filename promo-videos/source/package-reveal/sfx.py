"""Synthesised sound effects for the package video, mixed over the music.
usage: python3 sfx.py music.wav out.wav"""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 44100
music_path, out_path = sys.argv[1], sys.argv[2]
sr, m = wavfile.read(music_path); m = m.astype(np.float32) / 32768
N = len(m); fx = np.zeros(N, np.float32)
rng = np.random.default_rng(3)
def at(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: fx[i:j] += sig[: j - i] * g
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def boom(d=.9, f0=90, f1=38):
    n = int(d * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 9)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    click = lp(rng.standard_normal(n), 2500) * np.exp(-t * 60) * .5
    return np.tanh(2.2 * (s + click)) * .9
def whoosh(d=.5, lo=300, hi=4000):
    n = int(d * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); out = np.zeros(n)
    seg = 512
    for k in range(0, n, seg):  # sweep band upward
        fr = lo + (hi - lo) * (k / n)
        out[k:k+seg] = bp(x[k:k+seg+256], fr * .7, min(fr * 1.4, SR/2 - 100))[:len(out[k:k+seg])]
    env = np.sin(np.pi * np.minimum(1, t / d)) ** 1.5
    return out * env * .6
def riser(d=.65):
    n = int(d * SR); t = np.arange(n) / SR
    f = 200 * (6 ** (t / d))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25 + bp(rng.standard_normal(n), 2000, 9000) * .3 * (t / d)
    return s * (t / d) ** 1.5
def hit(d=.4):
    n = int(d * SR); t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 800, 8000) * np.exp(-t * 18) * .8 + np.sin(2*np.pi*180*t) * np.exp(-t*20) * .5)
def chime():
    n = int(1.2 * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f, a in ((1568, .4), (2093, .3), (2637, .25), (3136, .2)):
        s += a * np.sin(2*np.pi*f*t) * np.exp(-t * 4)
    return s * .5
# timeline (matches pack.html)
at(hit(), .10, .9)
for drop, imp in ((2.35, 2.9), (5.1, 5.6), (7.7, 8.2)):
    at(whoosh(imp - drop), drop, .8)
    at(boom(), imp, 1.0)
at(riser(), 9.9, 1.0)
at(boom(1.4, 110, 32), 10.55, 1.3); at(hit(.6), 10.55, 1.0)
at(chime(), 10.7, .7)
at(whoosh(.45, 500, 6000), 12.95, .6)
at(hit(), 13.15, .6)
at(whoosh(.4, 500, 6000), 15.0, .5); at(chime(), 16.6, .5)
mix = m * .55 + fx[:, None] * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-6, np.abs(mix).max()) / .9
wavfile.write(out_path, SR, (mix * 32767).astype(np.int16))
print('ok', out_path)
