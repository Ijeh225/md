import sys,json
src=open(sys.argv[1]).read().split('# timeline (matches pack.html)')[0]
exec(src.replace("music_path, out_path = sys.argv[1], sys.argv[2]","music_path, out_path = sys.argv[2], sys.argv[3]"))
def pop_():
    n=int(.15*SR); t=np.arange(n)/SR; f=900*np.exp(-t*25)+300
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.6
def kaching():
    n=int(1.0*SR); t=np.arange(n)/SR
    bell=sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*d) for f,a,d in ((2093,.5,5),(2637,.4,6),(3136,.35,7),(4186,.2,9)))
    return (bell+bp(rng.standard_normal(n),2000,8000)*np.exp(-t*80)*.8)*.7
def ding():
    n=int(.5*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*1318*t)+.5*np.sin(2*np.pi*1976*t))*np.exp(-t*9)*.4
def fire(d):
    n=int(d*SR); t=np.arange(n)/SR; x=bp(rng.standard_normal(n),300,4000)*.25
    cr=(rng.random(n)>.9990)*rng.standard_normal(n)*3
    return (x+bp(cr,1200,8000))*np.minimum(1,t/.3)*np.minimum(1,(d-t)/.5)*.7
ev=json.load(open(sys.argv[4]))['events']
M={'hit':lambda:hit(.4),'boom':lambda:boom(.9,110,38),'whoosh':lambda:whoosh(.4,400,6000),'pop':pop_,'kaching':kaching,'ding':ding,'chime':chime}
for k,tt,g in ev:
    at(fire(1.6) if k=='fire' else M[k](), tt, g)
mix = m * .55 + fx[:, None] * .9
mix = np.tanh(mix * 1.2) / np.tanh(1.2)
mix /= max(1e-6, np.abs(mix).max()) / .9
wavfile.write(out_path, SR, (mix * 32767).astype(np.int16)); print('ok', out_path)
