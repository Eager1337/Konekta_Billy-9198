"""Render the approved Konekta launch film. Python 3 + Pillow/numpy/scipy + FFmpeg.
All paths are relative to this package. Personal voice samples are not required.
"""
from pathlib import Path
from functools import lru_cache
import argparse, json, math, subprocess
import numpy as np
from scipy.io import wavfile
from scipy.ndimage import maximum_filter1d, gaussian_filter1d
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
A = ROOT / 'assets'
OUT = ROOT / 'output'
W, H, FPS, LENGTH = 1080, 1920, 30, 30
INK, WHITE, BLUE = (16,17,20), (247,247,242), (37,99,235)
GRAY = (180,182,187)
STARTS = [0,3,7.8,13.6,17,22,26]
ENDS = [3,7.8,13.6,17,22,26,30]

@lru_cache(maxsize=200)
def font(size, bold=True):
    return ImageFont.truetype(str(A/'fonts'/('Manrope-800.ttf' if bold else 'Inter-400.ttf')),int(size))
def ease(p):
    p=max(0,min(1,p)); return 1-(1-p)**3
def txt(im,x,y,s,size,color=INK,bold=True):
    ImageDraw.Draw(im).text((round(x),round(y)),s,font=font(int(size),bold),fill=color)
def fitted(im,x,y,s,size,color=INK,width=895,bold=True):
    while font(size,bold).getlength(s)>width: size-=1
    txt(im,x,y,s,size,color,bold)
def reveal(im,x,y,s,size,color,t,start=.1):
    p=ease((t-start)/.6)
    if p<=0:return
    f=font(size);w=round(f.getlength(s))+10;h=round(size*1.4)
    layer=Image.new('RGBA',(w,h))
    ImageDraw.Draw(layer).text((0,round((1-p)*h)),s,font=f,fill=color)
    im.paste(layer,(round(x),round(y)),layer)
def cap(im,text,color=INK): txt(im,90,145,text,27,color,False)
def footer(im,idx,t,color=INK):
    d=ImageDraw.Draw(im)
    txt(im,92,1698,f'0{idx} / 07',24,color,False)
    txt(im,694,1698,'SIERRA LEONE',24,color,False)
    d.line((92,1776,985,1776),fill=(*color,),width=2)
    d.line((92,1776,92+int(893*min(1,t/30)),1776),fill=BLUE if color!=BLUE else WHITE,width=6)
logo=Image.open(A/'logo.png').convert('RGBA')
app=Image.open(A/'app-preview.webp').convert('RGBA')
@lru_cache(maxsize=8)
def photo_base(name):
    return ImageOps.fit(Image.open(A/name).convert('RGB'),(W+65,H+90),centering=(.70,.5))
def photo(name,t,length):
    p=max(0,min(1,t/length));x=round(15+33*p);y=round(35-22*p)
    return photo_base(name).crop((x,y,x+W,y+H))
@lru_cache(maxsize=3)
def scrim():
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    for y in range(H):
        alpha=int(215*max(0,min(1,(y-1070)/650)))
        if y<440:alpha=max(alpha,round(92*(1-y/440)))
        d.line((0,y,W,y),fill=(16,17,20,alpha))
    return layer
def shaded(im):return Image.alpha_composite(im.convert('RGBA'),scrim()).convert('RGB')
def paste_logo(im,x,y,h,color):
    m=ImageOps.contain(logo,(h,h))
    c=Image.new('RGBA',m.size,color);c.putalpha(m.getchannel('A'));im.paste(c,(x,y),c)
def line_icon(im,kind,x,y,size,color):
    d=ImageDraw.Draw(im);s=size/100
    def xy(points):return [(round(x+a*s),round(y+b*s)) for a,b in points]
    lw=max(3,round(4*s))
    if kind=='video':
        d.rounded_rectangle((x-31*s,y-22*s,x+16*s,y+23*s),radius=7*s,outline=color,width=lw)
        d.line(xy([(16,-10),(38,-23),(38,23),(16,10)]),fill=color,width=lw,joint='curve')
    elif kind=='voice':
        d.rounded_rectangle((x-12*s,y-32*s,x+12*s,y+10*s),radius=12*s,outline=color,width=lw)
        d.arc((x-25*s,y-19*s,x+25*s,y+24*s),0,180,fill=color,width=lw)
        d.line(xy([(0,24),(0,35),(-15,35),(15,35)]),fill=color,width=lw)
    elif kind=='chat':
        d.rounded_rectangle((x-34*s,y-25*s,x+34*s,y+17*s),radius=10*s,outline=color,width=lw)
        d.line(xy([(-19,17),(-27,34),(-2,17)]),fill=color,width=lw)
        for a in [-16,0,16]:d.ellipse((x+(a-2)*s,y-5*s,x+(a+2)*s,y-1*s),fill=color)
    elif kind=='shield':
        d.line(xy([(0,-38),(34,-21),(29,18),(0,40),(-29,18),(-34,-21),(0,-38)]),fill=color,width=lw,joint='curve')
        d.line(xy([(-16,0),(-4,13),(18,-12)]),fill=color,width=lw)
    elif kind=='home':
        d.line(xy([(-35,-2),(0,-34),(35,-2),(26,-2),(26,32),(-26,32),(-26,-2)]),fill=color,width=lw)
        d.rectangle((x-8*s,y+9*s,x+8*s,y+32*s),outline=color,width=lw)
    elif kind=='ticket':
        d.rectangle((x-36*s,y-23*s,x+36*s,y+23*s),outline=color,width=lw)
        for a in range(-19,22,10):d.line(xy([(11,a),(11,a+4)]),fill=color,width=lw)
    elif kind=='spark':
        d.line(xy([(0,-36),(10,-10),(35,0),(10,10),(0,36),(-10,10),(-35,0),(-10,-10),(0,-36)]),fill=color,width=lw)
    else:
        d.line(xy([(-24,-24),(24,24),(30,13),(13,30),(-24,-24)]),fill=color,width=lw)

def opening(t):
    im=Image.new('RGB',(W,H),WHITE);cap(im,'BUILT HERE. FOR US.')
    paste_logo(im,92,238,78,BLUE)
    reveal(im,85,441,'Sierra',170,INK,t,.05)
    reveal(im,85,633,'Leone,',170,INK,t,.18)
    reveal(im,85,998,'let’s',154,BLUE,t,.65)
    reveal(im,85,1174,'connect.',154,BLUE,t,.8)
    footer(im,1,t);return im

def marketplace(t):
    im=shaded(photo('freetown-shop.png',t,4.8));cap(im,'YOUR LOCAL POSSIBILITIES.',WHITE)
    reveal(im,84,1190,'Buy.',157,WHITE,t,.08)
    reveal(im,450,1190,'Sell.',157,WHITE,t,.32)
    reveal(im,84,1368,'Book.',157,WHITE,t,.6)
    txt(im,92,1587,'PRODUCTS / SERVICES / LAND & HOMES',27,WHITE,False)
    footer(im,2,3+t,WHITE);return im

@lru_cache(maxsize=1)
def service_panel():
    return ImageOps.fit(Image.open(A/'freetown-service.png').convert('RGB'),(W-180,695),centering=(.5,.25))

def calls(t):
    im=Image.new('RGB',(W,H),INK);cap(im,'CONNECT WITHOUT SHARING YOUR NUMBER.',WHITE)
    reveal(im,86,248,'Say hello.',144,WHITE,t,.08)
    reveal(im,86,405,'Your way.',144,WHITE,t,.23)
    panel=service_panel()
    shift=round(75*(1-ease(t/.55)))
    im.paste(panel,(90,656+shift))
    d=ImageDraw.Draw(im)
    # An animated waveform, graphic only—not a simulated call screen.
    for i in range(43):
        height=int(10+32*abs(math.sin(t*6+i*.62)))
        xx=90+i*21;d.line((xx,1395-height,xx,1395+height),fill=BLUE,width=6)
    labels=['Voice calls','Video calls','Voice notes','Private chat'];kinds=['voice','video','voice','chat']
    for i,(lab,kind) in enumerate(zip(labels,kinds)):
        x=180+i*240
        if t>.3+i*.25:
            d.ellipse((x-53,1495,x+53,1601),fill=BLUE)
            line_icon(im,kind,x,1548,67,WHITE)
            tw=font(25,False).getlength(lab);txt(im,x-tw/2,1620,lab,25,WHITE,False)
    footer(im,3,7.8+t,WHITE);return im

def payments(t):
    im=Image.new('RGB',(W,H),WHITE);cap(im,'KONEKTA PROTECTION')
    reveal(im,86,335,'Pay in-app.',139,INK,t,.08)
    reveal(im,86,503,'Stay protected.',102,BLUE,t,.22)
    d=ImageDraw.Draw(im)
    x1,y1,x2,y2=250,902,825,1180
    p=ease((t-.25)/1.2)
    d.line((x1+62,y1+34,x2-68,y2-28),fill=(205,207,210),width=5)
    # An abstract currency token moves into escrow and stays held.
    xx=x1+(x2-x1)*p;yy=y1+(y2-y1)*p
    d.ellipse((xx-66,yy-66,xx+66,yy+66),fill=BLUE)
    txt(im,xx-42,yy-27,'NLe',39,WHITE)
    line_icon(im,'shield',825,1180,175,INK)
    txt(im,110,825,'WALLET',26,INK,False)
    txt(im,725,1320,'ESCROW',26,INK,False)
    txt(im,92,1493,'Held until you confirm delivery.',35,INK,False)
    txt(im,92,1563,'Terms and dispute process apply.',25,(100,101,108),False)
    footer(im,4,13.6+t);return im

def business(t):
    im=shaded(photo('freetown-business.png',t,5));cap(im,'YOUR BUSINESS. MORE POSSIBILITIES.',WHITE)
    # Existing app screens slide onto the counter area, not onto a fake device.
    preview=ImageOps.contain(app,(360,375));p=ease((t-1)/.7)
    if p>0:
        px=round(100+(1-p)*450);py=1040
        layer=Image.new('RGBA',preview.size);layer.alpha_composite(preview)
        layer.putalpha(layer.getchannel('A').point(lambda a:round(a*p)))
        im.paste(layer,(px,py),layer)
    reveal(im,84,1395,'Find customers.',106,WHITE,t,.12)
    txt(im,92,1557,'CATALOGS / CHAT / BUSINESS CONNECTIONS',25,WHITE,False)
    # Blue connection dots link the catalog to customer connection copy.
    d=ImageDraw.Draw(im)
    for i in range(4):
        x=560+i*109;d.ellipse((x,1275,x+13,1288),fill=BLUE)
    footer(im,5,17+t,WHITE);return im

def more(t):
    im=Image.new('RGB',(W,H),INK);cap(im,'EVEN MORE IN ONE APP.',WHITE)
    reveal(im,86,290,'More ways',138,WHITE,t,.05)
    reveal(im,86,450,'to Konekta.',125,WHITE,t,.22)
    d=ImageDraw.Draw(im)
    items=[('SERVICES','service',830),('LAND & HOMES','home',1060),('EVENT TICKETS','ticket',1290),('KONEKTA AI','spark',1520)]
    for i,(label,kind,y) in enumerate(items):
        p=ease((t-.3-i*.4)/.5)
        if p<=0:continue
        d.line((92,y-70,985,y-70),fill=(58,60,66),width=2)
        line_icon(im,kind,153,y,105,BLUE)
        fitted(im,253+round(40*(1-p)),y-42,label,51,WHITE,width=740)
        txt(im,929,y-30,'↗',46,WHITE,False)
    footer(im,6,22+t,WHITE);return im

def ending(t):
    im=Image.new('RGB',(W,H),BLUE);cap(im,'YOUR NEXT CONNECTION STARTS HERE.',WHITE)
    paste_logo(im,92,280,104,WHITE);txt(im,217,296,'konekta',78,WHITE)
    reveal(im,84,650,'Connect',158,WHITE,t,.06)
    reveal(im,84,838,'with',158,WHITE,t,.19)
    reveal(im,84,1026,'Konekta.',158,WHITE,t,.31)
    p=ease((t-.5)/.5)
    if p>0:
        d=ImageDraw.Draw(im);dy=round((1-p)*30)
        d.rounded_rectangle((92,1401+dy,985,1535+dy),radius=9,fill=WHITE)
        txt(im,145,1434+dy,'Get it on Google Play',45,INK,False)
        d.line((908,1490+dy,945,1450+dy),fill=INK,width=4)
        d.line((908,1450+dy,945,1450+dy,945,1490+dy),fill=INK,width=4)
        txt(im,92,1590,'konekta.website',41,WHITE,False)
    footer(im,7,26+t,WHITE);return im

SCENES=[opening,marketplace,calls,payments,business,more,ending]
def frame(t):
    i=max(j for j,s in enumerate(STARTS) if s<=t)
    im=SCENES[i](t-STARTS[i])
    if i>0 and t-STARTS[i]<.24:
        prev=SCENES[i-1](ENDS[i-1]-STARTS[i-1]-.01)
        cut=round(W*ease((t-STARTS[i])/.24))
        if cut:prev.paste(im.crop((W-cut,0,W,H)),(W-cut,0))
        im=prev
    return im

def master_audio():
    sr,voice=wavfile.read(ROOT/'audio/dialogue.wav');sr2,music=wavfile.read(ROOT/'audio/music.wav')
    assert sr==sr2==48000
    voice=voice.astype(float)/32768;music=music.astype(float)/32768
    n=sr*LENGTH;v=np.zeros(n)
    # Preserve each voice's timing. Edit only in silence between conversation beats.
    segments=[(0,2.47,.4),(2.66,6.91,3.30),(6.94,12.65,7.86),(12.72,15.64,13.86),(15.72,18.08,17.20),(18.20,22.03,22.08),(22.10,25.28,26.30)]
    for a,b,at in segments:
        part=voice[round(a*sr):round(b*sr)].copy();f=min(240,len(part)//2);r=np.linspace(0,1,f)
        part[:f]*=r;part[-f:]*=r[::-1];start=round(at*sr);v[start:start+len(part)]+=part[:n-start]
    rms=np.sqrt(np.mean(v[v!=0]**2));v*=.12/max(rms,1e-9)
    block=240;env=np.array([np.sqrt(np.mean(v[j:j+block]**2)) for j in range(0,n,block)])
    active=maximum_filter1d((env>.013).astype(float),size=35)
    duck=np.interp(np.arange(n),np.arange(len(env))*block,gaussian_filter1d(active,10))
    # Generators can return a bed shorter than requested; extend with a smooth loop.
    while len(music)<n:
        overlap=min(sr,len(music)//4)
        ramp=np.linspace(0,1,overlap)[:,None]
        join=music[-overlap:]*(1-ramp)+music[:overlap]*ramp
        music=np.concatenate((music[:-overlap],join,music[overlap:]))
    bed=music[:n].copy();bed*=.052/max(np.sqrt(np.mean(bed**2)),1e-9)
    bed*=np.expand_dims(1-.73*duck,1)
    fades=np.minimum(1,np.arange(n)/(sr*.25))*np.minimum(1,(n-1-np.arange(n))/(sr*.45))
    bed*=fades[:,None]
    audio=bed+v[:,None];audio*=min(1,.87/max(np.max(abs(audio)),1e-9))
    wavfile.write(OUT/'soundtrack.wav',sr,(audio*32767).astype(np.int16))
    (OUT/'audio-edit.json').write_text(json.dumps({'segments':segments,'peak_dbfs':float(20*np.log10(np.max(abs(audio))))},indent=2))

def render(preview=False):
    OUT.mkdir(parents=True,exist_ok=True)
    times=[1.8,5.2,10.4,15.5,20,24.4,28.4]
    sheet=Image.new('RGB',(1512,3840),WHITE)
    for i,t in enumerate(times):
        im=frame(t);im.save(OUT/f'scene-{i+1}.jpg',quality=93)
        sheet.paste(im.resize((504,896),Image.Resampling.LANCZOS),((i%3)*504,(i//3)*1280))
        txt(sheet,(i%3)*504+30,(i//3)*1280+930,f'{t:.1f}s',36,INK,False)
    sheet.crop((0,0,1512,3600)).save(OUT/'contact-sheet.jpg',quality=93)
    ending(2).save(OUT/'launch-cover.png')
    if preview:return
    master_audio()
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',str(OUT/'soundtrack.wav'),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(LENGTH),'-movflags','+faststart',str(OUT/'konekta-launch-30sec.mp4')]
    p=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for k in range(FPS*LENGTH):
            p.stdin.write(frame(k/FPS).tobytes())
            if k%150==0:print(f'{k}/{FPS*LENGTH} frames',flush=True)
    finally:p.stdin.close()
    assert p.wait()==0
    print('Rendered 30-second film.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true')
    render(parser.parse_args().preview)