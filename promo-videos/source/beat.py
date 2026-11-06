"""Original Afrobeats-style instrumental, synthesised from scratch.
usage: python3 beat.py <seconds> <out.wav>"""
import sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
BPM = 106
DUR = float(sys.argv[1]); OUT = sys.argv[2]
beat = 60 / BPM; s16 = beat / 4; bar = beat * 4
N = int((DUR + 1) * SR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    L[i:i+len(sig)] += sig * np.sqrt((1 - pan) / 2)
    R[i:i+len(sig)] += sig * np.sqrt((1 + pan) / 2)

def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)

def kick():
    n = int(.35 * SR); t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .16) * 1.1

def rim():
    n = int(.08 * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*1700*t) * .5 + bp(rng.standard_normal(n), 1500, 5000)) * env(n, .0005, .015)

def snare():
    n = int(.25 * SR); t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 900, 7000) * env(n, .001, .07) + np.sin(2*np.pi*190*t) * env(n, .001, .05) * .6)

def shaker(acc):
    n = int(.06 * SR)
    return hp(rng.standard_normal(n), 6000) * env(n, .004, .018) * acc

def conga(f):
    n = int(.25 * SR); t = np.arange(n) / SR
    return np.sin(2*np.pi*f*(1 + .15*np.exp(-t*40))*t) * env(n, .001, .09)

def logbass(f, d=.45):
    n = int(d * SR); t = np.arange(n) / SR
    fr = f * (1 + .6 * np.exp(-t * 35))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    x = np.sin(ph) + .25 * np.sin(2 * ph)
    return np.tanh(1.6 * x) * env(n, .002, d * .5)

def pluck(freqs, d=.5):
    n = int(d * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for h, a in ((1, 1), (2, .45), (3, .22), (4, .12)):
            x += a * np.sin(2*np.pi*f*h*t + rng.uniform(0, 6)) * np.exp(-t * (6 + 3*h))
    return lp(x, 3500) * env(n, .003, d) / len(freqs)

def pad(freqs, d):
    n = int(d * SR); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for det in (-.004, .004):
            x += np.sin(2*np.pi*f*(1+det)*t) + .3*np.sin(4*np.pi*f*(1+det)*t)
    a = np.minimum(1, t / .4) * np.minimum(1, (d - t) / .4)
    return lp(x, 1800) * a / len(freqs)

def marimba(f):
    n = int(.5 * SR); t = np.arange(n) / SR
    return (np.sin(2*np.pi*f*t) + .35*np.sin(2*np.pi*f*4*t)*np.exp(-t*30)) * env(n, .001, .22)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
# progression (A minor): Am  F  C  G
chords = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]
roots = [45, 41, 48, 43]
melody = [  # (16th index within 2 bars, midi)
    (0, 76), (3, 74), (6, 72), (8, 69), (10, 72), (14, 74),
    (16, 76), (19, 79), (22, 76), (24, 74), (26, 72), (28, 69)]

nbars = int(np.ceil(DUR / bar)) + 1
for b in range(nbars):
    t0 = b * bar
    ci = b % 4; full = b >= 2
    add(pad([hz(m) for m in chords[ci]], bar), t0, 0, .10 if full else .16)
    for k in range(16):  # shaker
        add(shaker(1.0 if k % 2 else .5), t0 + k * s16 + (.008 if k % 2 else 0), .35, .16)
    if b >= 1:
        for k in (2, 6, 10, 14):  # offbeat chord stabs
            add(pluck([hz(m + 12) for m in chords[ci]], .35), t0 + k * s16, -.25, .22)
    if not full:
        continue
    for k in (0, 7, 8, 12):  # kick
        add(kick(), t0 + k * s16, 0, .95 if k in (0, 8) else .7)
    for k in (4, 12):
        add(snare(), t0 + k * s16, .05, .38)
    for k in (0, 3, 6, 10, 12):  # 3-3-2 clave rim
        add(rim(), t0 + k * s16, -.4, .22)
    for k, f in ((5, 330), (9, 250), (13, 250), (15, 330)):
        add(conga(f), t0 + k * s16, .5, .25)
    r = roots[ci]
    for k, m, d in ((0, r, .5), (3, r, .3), (6, r + 12, .25), (10, r, .4), (14, r + 7, .3)):
        add(logbass(hz(m), d), t0 + k * s16, 0, .55)
    if b >= 4:
        off = 0 if b % 2 == 0 else 16
        for k, m in melody:
            if off <= k < off + 16:
                add(marimba(hz(m)), t0 + (k - off) * s16, .2, .17)

mix = np.stack([L, R], 1)[: int(DUR * SR)]
fo = int(2.0 * SR); mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
fi = int(.05 * SR); mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix = np.tanh(mix * 1.3) / np.tanh(1.3)
mix *= .89 / np.max(np.abs(mix))
wavfile.write(OUT, SR, (mix * 32767).astype(np.int16))
print('wrote', OUT, DUR)
