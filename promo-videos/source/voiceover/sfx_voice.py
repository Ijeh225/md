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

def pop_():
    n=int(.15*SR); t=np.arange(n)/SR; f=900*np.exp(-t*25)+300
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.6
def kaching():
    n=int(1.0*SR); t=np.arange(n)/SR
    bell=sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*d) for f,a,d in ((2093,.5,5),(2637,.4,6),(3136,.35,7),(4186,.2,9)))
    click=bp(rng.standard_normal(n),2000,8000)*np.exp(-t*80)*.8
    drawer=np.sin(2*np.pi*120*t)*np.exp(-np.maximum(t-.12,0)*25)*(t>.12)*.6
    return (bell+click+drawer)*.7
T=dict(know=.05,all=5.41,jollof=8.01,zobo=11.25,plantain=12.77,salad=14.28,sw=16.66,fried=17.32,spag=18.92,malt=21.05,fanta=22.06,coke=22.9,zobo2=24.12,yway=25.96,price=28.5,thats=31.33,hund=35.96,order=39.06,url=40.06,end=42.6)
at(hit(.4),T['know'],.6)
at(riser(1.2),T['all']-1.2,.8); at(boom(1.4,110,32),T['all'],1.3); at(hit(.5),T['all'],.7)
for k in ('jollof','zobo','plantain'): at(whoosh(.45),T[k]-.45,.6); at(boom(.7,100,40),T[k],.75)
at(whoosh(.3,400,7000),10.12-.3,.6); at(boom(.6,110,45),10.12,.65)
at(whoosh(.3,500,6000),T['salad']-.3,.5); at(pop_(),T['salad'],.6)
at(whoosh(.35,400,7000),T['sw']-.1,.7)
for k in ('fried','spag'): at(whoosh(.3,400,7000),T[k]-.3,.7); at(boom(.6,110,45),T[k],.7)
for k in ('malt','fanta','coke','zobo2'): at(pop_(),T[k],.9)
at(hit(.4),T['yway'],.6); at(kaching(),T['price'],1.0); at(boom(.9,110,40),T['price'],.6)
at(whoosh(.45,300,3000),T['thats']-.2,.6)
for k in range(4): at(boom(.6,110,40),T['thats']+.15+.22*k,.6)
at(chime(),T['hund'],.7); at(boom(1.0,100,35),T['hund'],.7)
at(whoosh(.45,500,6000),T['order']-.3,.6); at(pop_(),T['url'],.8); at(hit(.5),T['end'],.8); at(chime(),T['end']+.9,.5)
mix = m * .55 + fx[:, None] * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-6, np.abs(mix).max()) / .9
wavfile.write(out_path, SR, (mix * 32767).astype(np.int16))
print('ok', out_path)
