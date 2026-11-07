import sys,glob,os,numpy as np
from PIL import Image, ImageFilter
from concurrent.futures import ProcessPoolExecutor
src,dst=sys.argv[1],sys.argv[2]; os.makedirs(dst,exist_ok=True)
def tone(x):  # s-curve on 0..1
    return np.clip(x + 0.18*np.sin(np.pi*(x-0.5))*(x*(1-x))*4*0.5, 0, 1)
def proc(f):
    im=Image.open(f).convert('RGB'); a=np.asarray(im).astype(np.float32)/255
    a=tone(a)
    # warm highlights / cool-ish shadows split tone
    lum=(a@np.array([.299,.587,.114],np.float32))[...,None]
    hi=np.clip((lum-.5)*2,0,1); sh=np.clip((.5-lum)*2,0,1)
    a=a+hi*np.array([.045,.02,-.03],np.float32)+sh*np.array([-.02,0,.025],np.float32)
    # saturation
    a=lum+(a-lum)*1.12
    a=np.clip(a,0,1)
    # glow: blurred bright parts, screen blend
    small=Image.fromarray((a*255).astype(np.uint8)).resize((450,720),Image.BILINEAR)
    b=np.asarray(small.filter(ImageFilter.GaussianBlur(10))).astype(np.float32)/255
    b=np.clip((b-.55)/.45,0,1)**1.2
    b=np.asarray(Image.fromarray((b*255).astype(np.uint8)).resize(im.size,Image.BICUBIC)).astype(np.float32)/255
    a=1-(1-a)*(1-b*.5*np.array([1,.85,.6],np.float32))
    Image.fromarray((np.clip(a,0,1)*255+.5).astype(np.uint8)).save(dst+'/'+os.path.basename(f),quality=95)
fs=sorted(glob.glob(src+'/*.jpg'))
with ProcessPoolExecutor(8) as ex: list(ex.map(proc,fs,chunksize=8))
print('done',len(fs))
