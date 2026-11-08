import sys, numpy as np
from PIL import Image
def coeffs(dst, src):  # maps output(dst) -> input(src)
    A=[];b=[]
    for (x,y),(u,v) in zip(dst,src):
        A.append([x,y,1,0,0,0,-u*x,-u*y]); b.append(u)
        A.append([0,0,0,x,y,1,-v*x,-v*y]); b.append(v)
    return np.linalg.solve(np.array(A,float),np.array(b,float))
def run(src,out,quad,W=760,H=1040,m=0,M=220):
    im=Image.open(src).convert('RGBA')
    dst=[(M,M),(W+M,M),(W+M,H+M),(M,H+M)]
    c=coeffs(dst,quad)
    o=im.transform((W+2*M,H+2*M),Image.PERSPECTIVE,c,Image.BICUBIC)
    from PIL import ImageDraw, ImageFilter
    mk=Image.new('L',o.size,0); d=ImageDraw.Draw(mk)
    d.rounded_rectangle([M-6,M-6,W+M+6,H+M+6],radius=40,fill=255)
    d.rectangle([M+40,0,W+M-40,M+40],fill=255)   # allow turkey poking above the rim
    mk=mk.filter(ImageFilter.GaussianBlur(2))
    a=Image.fromarray((np.asarray(o.getchannel('A'),float)*np.asarray(mk,float)/255).astype(np.uint8)); o.putalpha(a)
    a=o.getchannel('A').point(lambda v:255 if v>20 else 0); o=o.crop(a.getbbox()); o.save(out); print(out,o.size)
d=sys.argv[1]
run(f'{d}/img/spag.png', f'{d}/img/spag_top.png', [(445,22),(1085,195),(845,948),(5,698)])
run(f'{d}/img/fried.png',f'{d}/img/fried_top.png',[(792,0),(1285,232),(645,665),(0,292)])
