"""Render the approved 7.8-second phone/marketplace motion proof.
Uses the existing final soundtrack without regenerating or remixing voices.
"""
import argparse, math, subprocess
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw
import styleframes as s
import real_assets as real

FPS=30
DURATION=7.8
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
AUDIO=ROOT/'audio'/'approved-soundtrack.m4a'

def clamp(x):return max(0,min(1,x))
def smooth(x):
    x=clamp(x);return x*x*x*(x*(x*6-15)+10)
def out(x):return 1-(1-clamp(x))**3
def mix(a,b,p):return a+(b-a)*p
def alpha(im,p):
    im=im.copy();im.putalpha(im.getchannel('A').point(lambda a:round(a*clamp(p))));return im

def type_line(im,txt,x,y,size,color,t,start,center=False):
    p=out((t-start)/.55)
    if p<=0:return
    layer=Image.new('RGBA',(s.W,s.H))
    if center:s.center(layer,y+round((1-p)*36),txt,size,color)
    else:s.text(layer,x,y+round((1-p)*36),txt,size,color)
    im.alpha_composite(alpha(layer,p))

@lru_cache(maxsize=1)
def cards():
    return [real.photo_card('laptop'),real.photo_card('home')]

def phone_texture(t):
    im=real.phone(2).copy();d=ImageDraw.Draw(im)
    # Controlled specular roll only on the frame edges, never across the UI text.
    y=round(170+740*clamp(t/3))
    d.line((19,max(70,y-105),19,min(1170,y+105)),fill=(119,170,255),width=4)
    d.line((620,max(70,y-80),620,min(1170,y+80)),fill=(79,120,186),width=3)
    return im

def frame(t):
    # The same rigid phone moves continuously through reveal, macro approach and pull-back.
    light=smooth((t-2.72)/.6)
    im=Image.blend(s.stage(True),s.stage(False),light)
    logo_layer=Image.new('RGBA',(s.W,s.H))
    s.logo_at(logo_layer,90,138,49,s.WHITE);s.text(logo_layer,158,142,'konekta',34,s.WHITE)
    im.alpha_composite(alpha(logo_layer,1-smooth((t-2.35)/.4)))
    if t<3.4:
        opening=Image.new('RGBA',(s.W,s.H))
        type_line(opening,'Your world.',0,299,107,s.WHITE,t,.12,True)
        type_line(opening,'Connected.',0,425,107,s.WHITE,t,.6,True)
        im.alpha_composite(alpha(opening,1-smooth((t-2.35)/.45)))
    rise=out(t/1.9)
    cx=540;cy=mix(1510,1190,rise)
    scale=mix(.72,.86,rise);yaw=mix(-48,-22,rise);pitch=mix(18,9,rise);roll=mix(-17,-9,rise)
    # Motivated push into the UI, then pull out as cards detach from the screen.
    zoom=smooth((t-2.25)/.8)
    scale=mix(scale,1.36,zoom);cy=mix(cy,1430,zoom)
    yaw=mix(yaw,2,zoom);pitch=mix(pitch,1,zoom);roll=mix(roll,-1,zoom)
    settle=smooth((t-3.25)/1.35)
    cx=mix(cx,675,settle);cy=mix(cy,1160,settle)
    scale=mix(scale,.86,settle);yaw=mix(yaw,19,settle)
    pitch=mix(pitch,6,settle);roll=mix(roll,9,settle)
    if t>4.6:
        drift=math.sin((t-4.6)*.65)
        cy+=drift*7;yaw+=drift*1.2
    s.project(im,phone_texture(t),cx,cy,scale,yaw,pitch,roll)
    # UI layers emerge from positions on the device, rather than appearing as a new slide.
    for i,texture in enumerate(cards()):
        p=smooth((t-(3.6+i*.7))/.95)
        if p<=0:continue
        if i==0:origin=(545,1005);target=(222,940);sc=1.04;yr=-12;pi=-7;ro=-7
        else:origin=(760,1270);target=(232,1350);sc=.95;yr=-8;pi=5;ro=-5
        s.project(im,alpha(texture,out(p*2)),mix(origin[0],target[0],p),mix(origin[1],target[1],p),mix(.70,sc,p),mix(19,yr,p),mix(6,pi,p),mix(9,ro,p))
    if t>=3:
        type_line(im,'Buy. Sell.',91,185,118,s.INK,t,3.16)
        type_line(im,'Find more.',91,333,99,s.BLUE,t,3.72)
        # Service beat enters after the marketplace phrase, before the property card settles.
        p=out((t-4.85)/.6)
        if p>0:
            chip=Image.new('RGBA',(330,92));s.rr(chip,(0,0,329,91),46,s.BLUE)
            s.icon(chip,'service',49,46,39,s.WHITE);s.text(chip,88,25,'Book services',27,s.WHITE)
            s.project(im,alpha(chip,p),286,1595+30*(1-p),1,3,0,-3)
    label_layer=Image.new('RGBA',(s.W,s.H))
    color=tuple(round(mix(a,b,light)) for a,b in zip((121,137,164),(137,148,166)))
    s.center(label_layer,1795,'Konekta • Official app screens',20,color,False)
    im.alpha_composite(label_layer)
    return im.convert('RGB')

def render(stills=False):
    OUT.mkdir(parents=True,exist_ok=True)
    times=[0,.5,1.7,2.5,2.95,3.3,3.9,4.5,5.4,6.4,7.5]
    sheet=Image.new('RGB',(4*270,3*550),(238,241,246))
    for i,t in enumerate(times):
        im=frame(t);im.save(OUT/f'proof-{t:.2f}.jpg',quality=92)
        sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),((i%4)*270,(i//4)*550))
        s.text(sheet,(i%4)*270+15,(i//4)*550+500,f'{t:.2f}s',22)
    sheet.save(OUT/'moving-proof-contact-sheet.jpg',quality=93)
    frame(6.4).save(OUT/'moving-proof-cover.png')
    if stills:return
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{s.W}x{s.H}','-r',str(FPS),'-i','-','-i',str(AUDIO),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-t',str(DURATION),'-movflags','+faststart',str(OUT/'konekta-motion-preview.mp4')]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for k in range(round(DURATION*FPS)):
            process.stdin.write(frame(k/FPS).tobytes())
            if k%60==0:print(f'{k}/{round(DURATION*FPS)} frames',flush=True)
    finally:process.stdin.close()
    assert process.wait()==0

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stills',action='store_true')
    render(parser.parse_args().stills)