import json,sys
P,V=sys.argv[1],sys.argv[2]
tpl=open(P+'/retarget_template.html').read()
FIX={"spicy":"Spicy","food":"Food"}
d=json.load(open(V+'/R_stt1.json'))
W=[[round(w['start'],2),round(w['end'],2),FIX.get(w['text'],w['text'])] for w in d['words'] if w.get('type')=='word']
G=lambda s:f'<span class="gold">{s}</span>'
def T(html,a,b,top=150,size=110,big=False): return dict(type='text',html=html,a=a,b=b,top=top,size=size,big=big)
def C(n,a,b,off=0,rate=1,z0=1.04,z1=1.1,mx=None): return dict(type='clip',dir=f'clip{n}',a=a,b=b,off=off,rate=rate,z0=z0,z1=z1,max=mx)
MX={1:222,2:291,3:342,4:190,5:187}
e=41.3
L=[C(4,0,3.62,0,.9,1.08,1.16,MX[4]), T("STILL "+G("THINKING?")+" 🤔",.2,1.75,170,120), T("OR YOU DON'T<br>"+G("TRUST US?")+" 👀",1.8,3.55,170,120),
 C(3,3.62,9.5,0,1,1.04,1.12,MX[3]), T("WATCH "+G("THIS")+" 👇",3.64,4.7,170,130), dict(type='badge',html='✅ REAL ORDER · 30 PACKS',a=4.76,b=9.4,top=520),
 T("FROM OUR KITCHEN<br>TO THE "+G("PARTY!")+" 🎉",7.02,9.4,1240,92),
 C(1,9.5,16.5,0,1,1.02,1.08,MX[1]), T(G("4 FULL SPOONS")+"<br>IN EVERY PACK",9.78,14.3,150,104),
 dict(type='scoops',times=[9.75,11.1,12.9,14.78],a=9.75,b=16.3), dict(type='badge',html='✅ 4 PORTIONS IN EVERY PACK',a=14.38,b=16.4,top=1040),
 T("WHAT YOU SEE IS<br>"+G("WHAT YOU GET!"),15.0,16.4,150,104),
 C(2,16.5,18.75,1.2,1,1.05,1.12,MX[2]), dict(type='chips',items=[["🍗 JUICY CHICKEN ON EVERY PACK",16.58,18.6]]),
 C(3,18.75,22.2,6.0,1,1.06,1.14,MX[3]), dict(type='chips',items=[["🍌 SWEET PLANTAIN · FULL & GENEROUS",18.78,22.1]]),
 C(4,22.2,24.75,2.6,1,1.05,1.12,MX[4]), dict(type='chips',items=[["✅ SEALED WITH THE SPICYFOOD STAMP",22.24,24.65]]),
 C(5,24.75,28.75,1.0,1,1.04,1.1,MX[5]), dict(type='chips',items=[["🥤 DELIVERED WITH COLD DRINKS",24.88,28.6]]),
 dict(type='photo',src='img/five.jpg',a=28.75,b=35.2,z0=1.14,z1=1.02), T("NOW IT'S<br>"+G("YOUR TURN!")+" 🎉",28.78,30.85,170,124),
 T("FEED "+G("5")+" PEOPLE<br>FOR JUST",30.9,35.15,230,120), dict(type='price',text='₦25,000',a=33.06,b=35.15,top=1380),
 dict(type='photo',src='img/crowd1.jpg',a=35.2,b=37.3,z0=1.14,z1=1.06), dict(type='photo',src='img/crowd2.jpg',a=37.3,b=39.5,z0=1.04,z1=1.1),
 T(G("30")+" PACKS?",35.26,39.45,170,150), dict(type='price',text='₦150,000',a=36.64,b=39.45,top=1380),
 dict(type='photo',src='img/bulk.png',a=39.5,b=e+.05,z0=1.02,z1=1.1), T("ORDER A<br>"+G("DAY BEFORE")+" 📅",39.54,e-.05,170,130)]
cfg=dict(end=e,total=44.6+3.6,layers=L,words=W,
 hits=[[1.8,14],[4.76,24],[9.75,10],[11.1,10],[12.9,10],[14.78,14],[14.38,18],[33.06,34],[36.64,36],[e,20]],
 flashes=[[.05,.6],[3.62,.4],[9.5,.4],[16.5,.35],[18.75,.35],[22.2,.35],[24.75,.35],[28.75,.45],[33.06,.6],[35.2,.5],[36.64,.6],[37.3,.4],[39.5,.4],[e,.55]],conf=[28.78,33.06,36.64,e])
sfx=[['hit',.2,.7],['pop',1.8,.7],['whoosh',3.4,.6],['hit',3.64,.6],['boom',4.76,.9],['chime',4.9,.6],['pop',7.02,.6],['whoosh',9.3,.6]]+[['pop',x,.9] for x in (9.75,11.1,12.9,14.78)]+[['ding',14.38,.7],['pop',15.0,.6],
 ['whoosh',16.3,.6],['pop',16.58,.7],['whoosh',18.55,.6],['pop',18.78,.7],['whoosh',22.0,.6],['pop',22.24,.7],['whoosh',24.55,.6],['pop',24.88,.7],['whoosh',28.55,.6],['boom',28.78,.9],
 ['pop',30.9,.6],['kaching',33.06,1.0],['boom',33.06,.8],['whoosh',35.0,.7],['boom',35.26,.8],['kaching',36.64,1.0],['boom',36.64,.9],['whoosh',37.2,.5],['whoosh',39.3,.6],['pop',39.54,.7],['hit',e,.8],['chime',e+.8,.6]]
json.dump(dict(total=cfg['total'],events=sfx),open(P+'/retarget_sfx.json','w'))
open(P+'/retarget.html','w').write(tpl.replace('__CFG__',json.dumps(cfg))); print('total',cfg['total'])
