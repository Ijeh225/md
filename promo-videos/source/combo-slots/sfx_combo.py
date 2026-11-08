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

def tick():
    n=int(.03*SR); t=np.arange(n)/SR
    return bp(rng.standard_normal(n),2000,7000)*np.exp(-t*160)*.6
def ding(f=1760):
    n=int(.6*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.01*t))*np.exp(-t*7)*.45
def clunk():
    n=int(.25*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*120*t)*np.exp(-t*25)+lp(rng.standard_normal(n),1500)*np.exp(-t*40)*.6)*.8
def shutter():
    n=int(.18*SR); t=np.arange(n)/SR; x=bp(rng.standard_normal(n),1500,9000)
    return x*(np.exp(-t*90)+np.exp(-np.maximum(t-.07,0)*90)*(t>.07))*.7
def pop_():
    n=int(.15*SR); t=np.arange(n)/SR; f=900*np.exp(-t*25)+300
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.6
B=lambda k:2.0+k*4.7
FIN,PH,END=16.1,21.4,25.4
for a in (.08,.32,.62,.85): at(boom(.6,100,45),a,.75); at(hit(.3),a,.5)
for k in range(3):
    b=B(k); at(clunk(),b,1.0)
    tt=b+.15
    while tt<b+1.4:
        at(tick(),tt,.7); prog=(tt-b-.15)/1.25; tt+=.035+.09*prog**2
    for r,f in zip(range(3),(1568,1760,2093)): at(ding(f),b+.9+.25*r,.9)
    at(chime(),b+1.45,.8)
    for r in range(3):
        land=b+1.95+.35*r; at(whoosh(.45),land-.45,.7); at(boom(.8 if r==0 else .6, 90 if r==0 else 120, 40),land,1.0 if r==0 else .75)
    at(shutter(),b+3.12,1.0)
    at(whoosh(.4,600,6000),b+3.95,.45); at(whoosh(.35,300,3000),b+4.3,.55)
at(whoosh(.45,300,3000),FIN,.7)
for k in range(3): at(boom(1.0,110,35),FIN+.55+.3*k,1.1); at(hit(.4),FIN+.55+.3*k,.6)
at(boom(1.3,110,32),FIN+1.5,1.2); at(chime(),FIN+1.6,.9)
for i in range(4): at(pop_(),FIN+3.2+.22*i,.9)
at(whoosh(.45,500,6000),PH-.1,.6); at(tick(),PH+2.55,1.0); at(pop_(),PH+2.6,.6)
at(hit(.5),END,.8); at(chime(),END+1.3,.6)
mix = m * .55 + fx[:, None] * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-6, np.abs(mix).max()) / .9
wavfile.write(out_path, SR, (mix * 32767).astype(np.int16))
print('ok', out_path)
