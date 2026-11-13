import json,sys
P,V=sys.argv[1],sys.argv[2]
tpl=open(P+'/story_template.html').read()
FIX={"mama's":"Mama's","10":"Ten","favorite.":"favourite.","spicy":"Spicy","food":"Food"}
def words(v):
    d=json.load(open(f'{V}/{v}_timing.json'))
    return [[round(w['start'],2),round(w['end'],2),FIX.get(w['text'],w['text'])] for w in d['words'] if w.get('type')=='word']
def T(html,a,b,top=150,size=110,big=False): return dict(type='text',html=html,a=a,b=b,top=top,size=size,big=big)
def PH(src,a,b,z0=1.14,z1=1.02): return dict(type='photo',src='img/'+src,a=a,b=b,z0=z0,z1=z1)
G=lambda s:f'<span class="gold">{s}</span>'
cfg={}
# ---------- A: Mama's birthday
e=28.05
cfg['A']=dict(end=e,total=e+4.2,layers=[
 PH('crowd1.jpg',0,3.75,1.16,1.04), T("IT'S "+G("MAMA'S")+"<br>BIRTHDAY 🎂",.1,1.6,160,120), T("THE WHOLE FAMILY<br>IS "+G("COMING..."),1.7,3.7,160,100),
 dict(type='pot',a=3.75,b=10.6,**{'from':1}), T("AND "+G("YOU")+" WILL COOK<br>FOR EVERYBODY?!",4.2,7.9,620,104), T("AH! 😳",8.0,8.8,700,260,True),
 dict(type='fire',a=8.9,b=10.6), T("DON'T STRESS<br>"+G("YOURSELF!"),8.92,10.5,700,134),
 dict(type='bulk',a=10.6,b=13.95), dict(type='logo',a=10.74,b=11.9,top=760), T("SPICYFOOD WILL FEED<br>THE "+G("WHOLE CROWD!"),11.72,13.9,1270,84),
 dict(type='spread',n=20,a=14.14,b=18.5), T(G("20")+" FULL PACKS",14.14,18.45,120,120), dict(type='price',text='₦100,000',a=16.12,b=18.45,top=1440),
 PH('crowd2.jpg',18.6,24.4,1.12,1.0), dict(type='counter',a=18.72,b=21.5,top=110,steps=[[18.72,20,50],[20.06,50,100]]), T("GUESTS?",18.72,21.5,400,90),
 T("WE GO COVER<br>"+G("EVERYBODY!")+" 💪",21.6,24.3,150,110),
 PH('crowd1.jpg',24.4,e+.1,1.02,1.12), T("YOU? JUST DRESS UP &<br>"+G("ENJOY YOUR PARTY")+" 💃",24.52,e-.1,160,84),
 ],hits=[[8.0,24],[8.92,22],[16.12,34],[19.02,14],[20.36,16],[22.72,26],[e,20]],
 flashes=[[.05,.6],[3.75,.4],[8.92,.5],[10.6,.4],[14.14,.4],[16.12,.6],[18.6,.4],[21.6,.4],[24.4,.4],[e,.55]],conf=[16.12,22.72,e],
 sfx=[['hit',.05,.8],['whoosh',1.5,.5],['whoosh',3.5,.6],['boom',5.78,.6],['hit',8.0,.8],['boom',8.92,1.0],['fire',8.92,1.7],['whoosh',10.35,.6],['boom',10.74,.7],
  ['whoosh',13.9,.6]]+[['pop',14.3+i*.1,.35] for i in range(10)]+[['kaching',16.12,1.0],['boom',16.12,.8],['whoosh',18.4,.6],['boom',19.02,.6],['boom',20.36,.7],['boom',22.72,1.0],['chime',22.8,.7],['whoosh',24.2,.5],['hit',e,.8],['chime',e+.8,.6]])
# ---------- B: Family lunch
e=22.9
cfg['B']=dict(end=e,total=e+4.2,layers=[
 PH('ten.jpg',0,8.2,1.16,1.0), T("FAMILY "+G("LUNCH")+" 🍽️",.16,1.8,150,124), T(G("10")+" PEOPLE<br>AT THE TABLE",1.9,4.0,150,112),
 T("EVERYBODY IS<br>"+G("HUNGRY...")+" 😋",4.14,5.95,150,108), T("AND NOBODY WANTS<br>TO "+G("COOK!")+" 😩",6.04,8.1,150,100),
 T("SO YOU MADE<br>"+G("ONE CALL")+" 📞",8.3,10.75,110,104), dict(type='chat',a=8.2,b=10.78,msgs=[['out','Hi SpicyFood! Food for 10 people please 🙏',8.55],['in','10 full packs, coming up! 🔥',9.35],['in','Done ✅',10.05]]),
 dict(type='spread',n=10,a=10.88,b=19.95), T(G("10")+" FULL PACKS",10.88,19.9,120,120),
 dict(type='chips',items=[["🍛 SMOKY RICE",12.58,13.85],["🍗 JUICY TURKEY",13.96,15.15],["🥤 COLD DRINKS",15.26,16.1],["🥗 SALAD",16.2,17.5]]),
 dict(type='price',text='₦50,000',a=17.96,b=19.9,top=1440),
 PH('ten.jpg',20.0,e+.1,1.0,1.12), T("NOW YOU ARE<br>EVERYBODY'S "+G("FAVOURITE")+" ❤️",20.1,e-.1,150,92),
 ],hits=[[6.04,14],[9.68,16],[17.96,34],[e,20]],flashes=[[.05,.6],[8.2,.4],[10.88,.4],[17.96,.6],[20.0,.4],[e,.55]],conf=[17.96,e],
 sfx=[['hit',.05,.8],['pop',1.9,.6],['pop',4.14,.6],['boom',6.04,.6],['whoosh',8.0,.6],['ding',8.55,.7],['ding',9.35,.7],['ding',10.05,.7],['whoosh',10.7,.6]]+[['boom',11.05+i*.1,.4] for i in range(10)]+[['pop',12.58,.7],['pop',13.96,.7],['pop',15.26,.7],['pop',16.2,.7],['kaching',17.96,1.0],['boom',17.96,.8],['whoosh',19.8,.5],['chime',20.96,.6],['hit',e,.8],['chime',e+.8,.6]])
# ---------- C: Friends are coming
e=7.55
cfg['C']=dict(end=e,total=e+5.2,layers=[
 PH('five.jpg',0,3.7,1.14,1.02), T("YOUR "+G("5")+" FRIENDS ARE<br>COMING ON "+G("SATURDAY"),.08,2.3,150,84),
 dict(type='fire',a=2.4,b=3.6), T("DON'T<br>"+G("STRESS!")+" 😎",2.42,3.62,150,150,True),
 dict(type='spread',n=5,a=3.74,b=e), T(G("5")+" FULL PACKS",3.74,e-.05,120,120), dict(type='price',text='₦25,000',a=5.52,b=e-.05,top=1440),
 ],hits=[[2.42,22],[5.52,34],[e,20]],flashes=[[.05,.6],[2.42,.5],[3.74,.4],[5.52,.6],[e,.55]],conf=[5.52,e],
 sfx=[['hit',.05,.8],['boom',2.42,.9],['fire',2.42,1.2],['whoosh',3.55,.6]]+[['boom',3.9+i*.2,.5] for i in range(5)]+[['kaching',5.52,1.0],['boom',5.52,.8],['hit',e,.8],['chime',e+.8,.6]])
for v,c in cfg.items():
    c['words']=words(v); sfx=c.pop('sfx')
    json.dump(dict(total=c['total'],events=sfx),open(f'{P}/story_{v}_sfx.json','w'))
    open(f'{P}/story_{v}.html','w').write(tpl.replace('__CFG__',json.dumps(c)))
    print(v,'total',round(c['total'],2),'layers',len(c['layers']))
