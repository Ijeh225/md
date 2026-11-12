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
    return (bell+click)*.7
def ding():
    n=int(.5*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*1318*t)+.5*np.sin(2*np.pi*1976*t))*np.exp(-t*9)*.4
def fire(d):
    n=int(d*SR); t=np.arange(n)/SR; x=bp(rng.standard_normal(n),300,4000)*.25
    cr=(rng.random(n)>.9990)*rng.standard_normal(n)*3
    return (x+bp(cr,1200,8000))*np.minimum(1,t/.3)*np.minimum(1,(d-t)/.5)*.7
T=dict(stop=.05,feed=1.69,price0=3.44,dont=5.45,party=6.95,bday=7.6,here=8.6,spicy=10.17,whole=11.81,five=13.38,p25=20.55,ten=21.83,p50=22.52,twenty=24.67,p100=25.87,fifty=30.99,hundred=31.82,twoh=33.04,bring=34.38,cover=36.36,custom=39.34,jollof=40.57,fried=41.86,spag=42.83,drink=43.91,ns0=46.0,ns1=47.1,ns2=48.47,order=49.9,day=50.54,call=52.43,n0=53.9,n1=56.29,n2=57.99,url=61.11,end=64.35)
at(hit(.4),T['stop'],.8); at(whoosh(.4,400,6000),T['feed']-.25,.6)
at(riser(.6),T['price0']-.6,.6); at(kaching(),T['price0'],1.0); at(boom(1.1,110,36),T['price0'],1.0); at(fire(3.2),T['price0'],.8)
at(boom(.8,110,40),T['dont'],.8)
for k in ('party','bday','here'): at(pop_(),T[k],.8)
at(hit(.4),T['spicy'],.6); at(whoosh(.45,300,3000),T['whole']-.4,.7); at(boom(.9,100,38),T['whole'],.9)
at(whoosh(.4,400,6000),T['five']-.25,.6)
for i in range(5): at(whoosh(.3),T['five']-.1+i*.22,.45); at(boom(.5,120,45),T['five']+.2+i*.22,.6)
at(kaching(),T['p25'],.7); at(boom(.7,110,40),T['p25'],.5)
for k in ('p50','p100'): at(kaching(),T[k],1.0); at(boom(.9,110,40),T[k],.7)
at(whoosh(.4,400,6000),T['ten']-.25,.6); at(whoosh(.4,400,6000),T['twenty']-.2,.6)
for i in range(10): at(pop_(),T['twenty']+.05+i*.07,.35)
at(whoosh(.45,300,3000),T['fifty']-.3,.7)
for k in ('fifty','hundred','twoh'): at(boom(.6,120,45),T[k]+.3,.7); at(hit(.25),T[k]+.3,.4)
at(whoosh(.4,400,6000),T['bring']-.25,.6); at(boom(1.3,110,32),T['cover'],1.1); at(chime(),T['cover']+.1,.7)
at(whoosh(.4,400,6000),T['custom']-.2,.5)
for k in ('jollof','fried','spag'): at(pop_(),T[k],.8)
for i in range(4): at(pop_(),T['drink']+i*.16,.6)
for k in ('ns0','ns1','ns2'): at(whoosh(.25,500,6000),T[k]-.2,.5); at(hit(.3),T[k]+.15,.55)
at(whoosh(.4,400,6000),T['order']-.2,.5); at(pop_(),T['order']+.3,.7); at(pop_(),T['day']+.25,.7)
at(whoosh(.45,500,6000),T['call']-.3,.6)
for i in range(5): at(ding(),T['call']+.45+i*.95,.7)
for k in ('n0','n1','n2'): at(pop_(),T[k],.8)
at(pop_(),T['url'],.8); at(ding(),T['url']+.5,.6); at(hit(.5),T['end'],.8); at(chime(),T['end']+.8,.6)
mix = m * .55 + fx[:, None] * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-6, np.abs(mix).max()) / .9
wavfile.write(out_path, SR, (mix * 32767).astype(np.int16))
print('ok', out_path)
