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
B=lambda k:5.2+k*6.4
FIN=B(4); CUS=FIN+7.2; PH=CUS+4.0; END=PH+5.4
def sizzle(d):
    n=int(d*SR); t=np.arange(n)/SR; x=bp(rng.standard_normal(n),2500,9000)
    crack=(rng.random(n)>.9985)*rng.standard_normal(n)*3
    env=np.minimum(1,t/.3)*np.minimum(1,(d-t)/.4)
    return (x*.35+bp(crack,1500,8000))*env*.6
at(sizzle(2.2),0.05,.8)
at(boom(.7,80,40),1.0,.35)
at(boom(1.1,105,35),2.25,1.15); at(hit(.4),2.25,.6)
at(whoosh(.3,400,7000),2.7,.8); at(hit(.3),2.95,.45)
at(whoosh(.3,400,7000),3.3,.8); at(hit(.3),3.55,.45)
at(riser(.5),3.95,.7); at(chime(),4.1,.6)
for k in range(4):
    b=B(k); at(clunk(),b,1.0)
    tt=b+.2
    while tt<b+2.0:
        at(tick(),tt,.65); prog=(tt-b-.2)/1.8; tt+=.04+.1*prog**2
    for r,(st,f) in enumerate(zip((1.3,1.65,2.0),(1568,1760,2093))): at(ding(f),b+st,.9)
    at(chime(),b+2.05,.8)
    for r,land in enumerate((2.75,3.2,3.65)):
        at(whoosh(.55),b+land-.55,.65); at(boom(.8 if r==0 else .6, 90 if r==0 else 120, 40),b+land,1.0 if r==0 else .75)
    at(shutter(),b+4.32,1.0)
    at(whoosh(.5,600,6000),b+5.65,.45); at(whoosh(.4,300,3000),b+6.0,.5)
at(whoosh(.55,300,3000),FIN,.7)
for k in range(4): at(boom(1.0,110,35),FIN+1.05+.45*k,1.0); at(hit(.4),FIN+1.05+.45*k,.55)
at(boom(1.3,110,32),FIN+2.7,1.15); at(chime(),FIN+2.8,.9)
for i in range(4): at(pop_(),FIN+4.2+.35*i,.9)
at(whoosh(.45,300,3000),CUS-.1,.6)
for i in range(4): at(pop_(),CUS+.6+.32*i,.8)
at(boom(.8,110,40),CUS+2.3,.9); at(chime(),CUS+2.4,.6)
at(whoosh(.45,500,6000),PH-.1,.6); at(tick(),PH+3.25,1.0); at(pop_(),PH+3.3,.6); at(chime(),PH+3.8,.4)
at(hit(.5),END,.8); at(chime(),END+1.55,.6)
mix = m * .55 + fx[:, None] * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-6, np.abs(mix).max()) / .9
wavfile.write(out_path, SR, (mix * 32767).astype(np.int16))
print('ok', out_path)
