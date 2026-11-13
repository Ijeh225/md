"""usage: python3 gen_vo.py <script.txt> <outprefix> <takes>  -> prefix_takeN.mp3, _align.json, _select.txt, _words.json"""
import sys,json,subprocess,base64
vid='reGkImJki7uJOve2F4A0'; t=open(sys.argv[1]).read(); pre=sys.argv[2]; n=int(sys.argv[3])
for take in range(1,n+1):
    body={'text':t,'model_id':'eleven_v3','voice_settings':{'stability':0.0,'similarity_boost':0.85,'style':0.0,'use_speaker_boost':True}}
    r=subprocess.run(['curl','-sS','-X','POST',f'https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128','-H','Content-Type: application/json','-d',json.dumps(body)],capture_output=True,text=True)
    d=json.loads(r.stdout)
    if 'audio_base64' not in d: print(take,r.stdout[:300]); continue
    open(f'{pre}_take{take}.mp3','wb').write(base64.b64decode(d['audio_base64'])); al=d['alignment']
    ch=al['characters']; st=al['character_start_times_seconds']; en=al['character_end_times_seconds']
    words=[];cur='';t0=t1=None;intag=False
    for c,a,b in zip(ch,st,en):
        if c=='[': intag=True
        if intag:
            if c==']': intag=False
            continue
        if c.strip()=='':
            if cur: words.append([t0,t1,cur]); cur=''
        else:
            if not cur: t0=a
            cur+=c; t1=b
    if cur: words.append([t0,t1,cur])
    cuts=[]
    for i in range(1,len(words)):
        if words[i][0]-words[i-1][1]>0.32: cuts.append((words[i-1][1]+0.11, words[i][0]-0.11))
    if words[0][0]>0.15: cuts.insert(0,(0.0,words[0][0]-0.05))
    open(f'{pre}_take{take}_select.txt','w').write("aselect='not("+'+'.join(f'between(t,{a:.3f},{b:.3f})' for a,b in cuts)+")',asetpts=N/SR/TB" if cuts else "anull")
    def mapt(x): return (x-sum(max(0,min(x,b)-a) for a,b in cuts if a<x))/1.07
    json.dump([(round(mapt(a),2),round(mapt(b),2),w) for a,b,w in words],open(f'{pre}_take{take}_words.json','w'))
    print(pre.split('/')[-1],'take',take,'ok')
