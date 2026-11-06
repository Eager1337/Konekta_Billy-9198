"""Thirty-second Konekta product-motion film with official Play Store screens."""
from pathlib import Path
from functools import lru_cache
import argparse, importlib.util, math, subprocess
from PIL import Image, ImageDraw
import styleframes as s
import real_assets as real

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'
spec=importlib.util.spec_from_file_location('preview',ROOT/'render-preview.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
smooth,out,mix,alpha,type_line=p.smooth,p.out,p.mix,p.alpha,p.type_line
FPS=30;LENGTH=30
AUDIO=ROOT/'audio'/'approved-soundtrack.m4a'
STARTS=[0,7.8,13.6,17,22,26];ENDS=[7.8,13.6,17,22,26,30]

def feature_title(im,t,line1,line2,dark=True,size1=116,size2=105):
    type_line(im,line1,90,190,size1,s.WHITE if dark else s.INK,t,.06)
    type_line(im,line2,90,343,size2,s.WHITE if dark else s.BLUE,t,.24)

@lru_cache(maxsize=8)
def card(kind,title,sub):return s.call_card(kind,title,sub)

def calls(t):
    im=s.stage();feature_title(im,t,'Closer.','In a tap.')
    move=smooth(t/.8)
    s.project(im,real.phone(3),mix(675,831,move),1160+7*math.sin(t*.7),.86,mix(19,-20,move),7,-9)
    items=[('mic','Voice calls','Talk directly',.4),('video','Video calls','See the connection',1.1),('chat','Private chat','Keep it in Konekta',1.9)]
    for i,(kind,title,sub,start) in enumerate(items):
        q=out((t-start)/.65)
        if q>0:s.project(im,alpha(card(kind,title,sub),q),mix(710,371,q),mix(880+i*190,760+i*265,q),mix(.68,.99,q),mix(-20,6,q),-3,mix(-9,-3,q))
    q=out((t-3.45)/.6)
    if q>0:
        wave=Image.new('RGBA',(530,140));s.rr(wave,(0,0,529,139),70,s.BLUE);s.icon(wave,'mic',55,70,48,s.WHITE)
        d=ImageDraw.Draw(wave)
        for i in range(34):
            amp=8+28*abs(math.sin(i*.72+t*6));xx=115+i*9;d.line((xx,70-amp,xx,70+amp),fill=s.WHITE,width=5)
        s.text(wave,438,55,'Voice',22,s.WHITE,False)
        s.project(im,alpha(wave,q),mix(750,397,q),1538,1.09,4,0,-3)
        type_line(im,'Voice notes',110,1650,31,s.WHITE,t,3.6)
    real.footer(im,True);return im

def protection(t):
    im=s.stage(False);feature_title(im,t,'Pay in-app.','Stay protected.',False,111,92)
    q=out(t/.9)
    s.project(im,real.phone(4),mix(831,705,q),1040,.70,mix(-20,14,q),4,7)
    shield=Image.new('RGBA',(310,340));s.rr(shield,(0,0,309,339),68,(255,255,255),(212,222,238),2)
    s.icon(shield,'shield',155,136,163);s.center(shield,249,'Protection',30)
    r=out((t-.4)/.7)
    if r>0:s.project(im,alpha(shield,r),mix(690,247,r),1040,1.13,-11,-4,-7)
    token=Image.new('RGBA',(215,130));s.rr(token,(0,0,214,129),65,s.BLUE);s.center(token,32,'NLe',52,s.WHITE)
    r=smooth((t-.8)/1.3)
    if t>.8:s.project(im,alpha(token,out((t-.8)/.3)),mix(552,259,r),mix(1420,1228,r),1,-8,0,-4)
    type_line(im,'Held in escrow.',92,1524,42,s.INK,t,.7)
    type_line(im,'Release conditions and dispute terms apply.',92,1615,25,(111,128,150),t,1)
    real.footer(im);return im

def business(t):
    im=s.stage();feature_title(im,t,'Your business.','More connections.',True,92,77)
    q=out(t/.8)
    s.project(im,real.phone(2),mix(705,536,q),1140+5*math.sin(t),.84,mix(14,-9,q),3,-3)
    for i,kind in enumerate(['laptop','tester','service']):
        r=out((t-(.65+i*.5))/.8)
        if r<=0:continue
        target=[(225,917),(829,1230),(252,1343)][i]
        s.project(im,alpha(real.photo_card(kind,True),r),mix(540,target[0],r),mix(1135,target[1],r),mix(.6,1.04,r),mix(-9,13 if i!=1 else -13,r),3,-8 if i!=1 else 8)
    r=out((t-2.45)/.7)
    if r>0:s.project(im,alpha(s.call_card('chat','Customer connections','Catalogs • Chat • Business',570),r),540,1580+50*(1-r),1,-6,0,-3)
    real.footer(im,True);return im

@lru_cache(maxsize=2)
def ticket():
    im=Image.new('RGBA',(660,310));s.rr(im,(0,0,659,309),39,s.BLUE);d=ImageDraw.Draw(im)
    for y in range(25,285,24):d.line((474,y,474,y+10),fill=(150,188,255),width=3)
    s.text(im,38,42,'EVENT TICKETS',24,s.WHITE,False);s.text(im,38,110,'Be there.',69,s.WHITE)
    s.text(im,505,66,'K',86,s.WHITE);return im

@lru_cache(maxsize=1)
def ai_card():
    im=Image.new('RGBA',(790,270));s.rr(im,(0,0,789,269),52,(255,255,255),(216,225,239),2)
    s.icon(im,'spark',81,79,52);s.text(im,134,47,'Konekta AI',41)
    s.text(im,49,151,'Ask. Explore. Connect.',41,(93,107,128),False)
    return im

def more(t):
    im=s.stage(False);feature_title(im,t,'One app.','More possibility.',False,125,82)
    q=out((t-.2)/.75)
    if q>0:s.project(im,alpha(ticket(),q),mix(970,559,q),mix(1100,887,q),mix(.75,1.15,q),mix(42,-9,q),-6,mix(20,-6,q))
    r=out((t-.9)/.75)
    if r>0:s.project(im,alpha(ai_card(),r),mix(110,541,r),mix(1530,1295,r),mix(.55,.98,r),mix(-25,5,r),4,mix(-14,4,r))
    for i,(kind,title) in enumerate([('home','Homes'),('bag','Products'),('service','Services')]):
        a=out((t-(1.5+i*.2))/.5)
        if a>0:
            layer=Image.new('RGBA',(s.W,s.H));s.icon(layer,kind,218+i*326,1570+30*(1-a),48)
            s.text(layer,165+i*326,1631+30*(1-a),title,27,(100,114,136),False);im.alpha_composite(alpha(layer,a))
    real.footer(im,False,True);return im

def ending(t):
    im=s.stage(False);q=out(t/.8)
    n=round(mix(105,166,q));s.logo_at(im,540-n//2,265,n)
    type_line(im,'Connect',0,589,132,s.INK,t,.16,True)
    type_line(im,'with Konekta.',0,755,111,s.INK,t,.37,True)
    r=out((t-.7)/.65)
    if r>0:
        layer=Image.new('RGBA',(s.W,s.H));dy=round(40*(1-r))
        s.rr(layer,(148,1150+dy,931,1300+dy),75,s.BLUE)
        s.center(layer,1194+dy,'Get it on Google Play',43,s.WHITE,False)
        s.center(layer,1408+dy,'konekta.website',43,(92,109,133),False)
        s.center(layer,1638+dy,'Made for Sierra Leone.',28,(126,139,157),False)
        im.alpha_composite(alpha(layer,r))
    return im

SCENES=[p.frame,calls,protection,business,more,ending]

def frame(t):
    i=max(i for i,v in enumerate(STARTS) if t>=v)
    local=t-STARTS[i];im=SCENES[i](local).convert('RGBA')
    if i and local<.25:
        previous=SCENES[i-1](ENDS[i-1]-STARTS[i-1]-.001).convert('RGBA')
        # Short optical match transition retains the prior object while the next UI arrives.
        im=Image.blend(previous,im,smooth(local/.25))
    return im.convert('RGB')

def render(stills=False):
    OUT.mkdir(parents=True,exist_ok=True)
    times=[1.8,6,10.8,15.6,20,24.5,28.5]
    sheet=Image.new('RGB',(4*270,2*540),(238,241,246))
    for i,t in enumerate(times):
        im=frame(t);im.save(OUT/f'final-scene-{i+1}.jpg',quality=94)
        sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),((i%4)*270,(i//4)*540))
        s.text(sheet,(i%4)*270+16,(i//4)*540+495,f'{t:.1f}s',22)
    sheet.save(OUT/'real-product-contact-sheet.jpg',quality=94)
    ending(3).convert('RGB').save(OUT/'konekta-motion-cover.png')
    if stills:return
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{s.W}x{s.H}','-r',str(FPS),'-i','-','-i',str(AUDIO),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-t',str(LENGTH),'-movflags','+faststart',str(OUT/'konekta-product-motion-30sec.mp4')]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for k in range(FPS*LENGTH):
            process.stdin.write(frame(k/FPS).tobytes())
            if k%150==0:print(f'{k}/{FPS*LENGTH}',flush=True)
    finally:process.stdin.close()
    assert process.wait()==0

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stills',action='store_true')
    render(parser.parse_args().stills)