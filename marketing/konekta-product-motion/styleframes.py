"""Konekta product-motion direction: deterministic illustrated UI and 3D card planes.
Static approval frames only. No footage from reference creators is reused.
"""
from pathlib import Path
from functools import lru_cache
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'; OUT=ROOT/'output'
W,H=1080,1920
BLUE=(37,99,235); INK=(12,15,22); WHITE=(249,250,252)

@lru_cache(maxsize=120)
def font(n,bold=True):
    return ImageFont.truetype(str(ASSETS/'fonts'/('Manrope-800.ttf' if bold else 'Inter-400.ttf')),int(n))

def text(im,x,y,s,n=40,c=INK,bold=True):
    ImageDraw.Draw(im).text((int(x),int(y)),s,font=font(n,bold),fill=c,spacing=5)

def center(im,y,s,n=40,c=INK,bold=True):
    text(im,(im.width-font(n,bold).getlength(s))/2,y,s,n,c,bold)

def rr(im,box,r,fill,outline=None,width=1):
    ImageDraw.Draw(im).rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)

@lru_cache(maxsize=3)
def ground(dark=True):
    yy,xx=np.mgrid[0:H,0:W].astype(float)
    if dark:
        base=np.zeros((H,W,3))+np.array([7,10,16])
        glow=np.exp(-(((xx-570)/490)**2+((yy-1100)/710)**2)*1.6)
        base+=glow[:,:,None]*np.array([5,29,77])
        top=np.exp(-(((xx-190)/400)**2+((yy-140)/280)**2)*2)
        base+=top[:,:,None]*np.array([11,13,22])
    else:
        base=np.zeros((H,W,3))+np.array(WHITE)
        glow=np.exp(-(((xx-650)/700)**2+((yy-1220)/650)**2)*2)
        base-=glow[:,:,None]*np.array([21,14,0])
    return Image.fromarray(np.clip(base,0,255).astype('uint8'),'RGB')

def stage(dark=True):return ground(dark).copy().convert('RGBA')

@lru_cache(maxsize=20)
def logo(n,c=BLUE):
    original=Image.open(ASSETS/'logo.png').convert('RGBA').resize((n,n),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',original.size,c);out.putalpha(original.getchannel('A'));return out

def logo_at(im,x,y,n=64,c=BLUE):im.alpha_composite(logo(n,c),(int(x),int(y)))

def icon(im,kind,x,y,n,c=BLUE):
    d=ImageDraw.Draw(im);r=n/2;lw=max(3,int(n/17))
    if kind=='home':
        d.line([(x-r,y),(x,y-r),(x+r,y),(x+r*.7,y),(x+r*.7,y+r*.8),(x-r*.7,y+r*.8),(x-r*.7,y)],fill=c,width=lw,joint='curve')
        d.rectangle((x-r*.2,y+r*.2,x+r*.2,y+r*.8),outline=c,width=lw)
    elif kind=='video':
        d.rounded_rectangle((x-r,y-r*.6,x+r*.45,y+r*.6),radius=n/9,outline=c,width=lw)
        d.line([(x+r*.45,y-r*.2),(x+r,y-r*.6),(x+r,y+r*.6),(x+r*.45,y+r*.2)],fill=c,width=lw)
    elif kind=='chat':
        d.rounded_rectangle((x-r,y-r*.6,x+r,y+r*.4),radius=n/7,outline=c,width=lw)
        d.line([(x-r*.6,y+r*.4),(x-r*.8,y+r*.8),(x,y+r*.4)],fill=c,width=lw)
    elif kind=='shield':
        d.line([(x,y-r),(x+r*.8,y-r*.6),(x+r*.7,y+r*.4),(x,y+r),(x-r*.7,y+r*.4),(x-r*.8,y-r*.6),(x,y-r)],fill=c,width=lw,joint='curve')
        d.line([(x-r*.4,y),(x-r*.1,y+r*.3),(x+r*.45,y-r*.25)],fill=c,width=lw)
    elif kind=='spark':
        d.line([(x,y-r),(x+r*.25,y-r*.25),(x+r,y),(x+r*.25,y+r*.25),(x,y+r),(x-r*.25,y+r*.25),(x-r,y),(x-r*.25,y-r*.25),(x,y-r)],fill=c,width=lw,joint='curve')
    elif kind=='bag':
        d.rounded_rectangle((x-r*.75,y-r*.35,x+r*.75,y+r*.85),radius=n/8,outline=c,width=lw)
        d.arc((x-r*.4,y-r*.9,x+r*.4,y),180,360,fill=c,width=lw)
    elif kind=='mic':
        d.rounded_rectangle((x-r*.3,y-r,x+r*.3,y+r*.2),radius=n/5,outline=c,width=lw)
        d.arc((x-r*.65,y-r*.3,x+r*.65,y+r*.6),0,180,fill=c,width=lw)
        d.line([(x,y+r*.6),(x,y+r*.95)],fill=c,width=lw)
    else:
        d.line([(x-r*.7,y-r*.7),(x+r*.7,y+r*.7)],fill=c,width=lw)
        d.arc((x-r,y-r,x,y),0,270,fill=c,width=lw)

def pill(im,x,y,w,label,dark=False,active=False):
    fill=BLUE if active else ((30,36,49) if dark else (237,240,245))
    rr(im,(x,y,x+w,y+56),28,fill)
    text(im,x+20,y+12,label,21,WHITE if (dark or active) else (85,94,108),False)

@lru_cache(maxsize=10)
def product_art(kind,w=250,h=190):
    im=Image.new('RGBA',(w,h),(232,237,245));d=ImageDraw.Draw(im)
    if kind=='headphones':
        d.arc((w*.24,h*.15,w*.76,h*.87),180,360,fill=(39,44,53),width=17)
        for x in [w*.25,w*.65]:
            d.rounded_rectangle((x,h*.4,x+w*.12,h*.85),radius=12,fill=(28,33,44),outline=(75,84,101),width=4)
    elif kind=='sofa':
        rr(im,(w*.15,h*.3,w*.85,h*.71),18,(110,129,157))
        rr(im,(w*.10,h*.52,w*.90,h*.8),13,(94,113,144))
        for x in [.2,.75]:d.rectangle((w*x,h*.78,w*(x+.05),h*.9),fill=(58,63,70))
        d.line((w*.5,h*.36,w*.5,h*.67),fill=(142,156,181),width=3)
    elif kind=='house':
        d.polygon([(w*.15,h*.50),(w*.5,h*.18),(w*.85,h*.50)],fill=(49,65,86))
        d.rectangle((w*.22,h*.49,w*.79,h*.91),fill=(239,231,213))
        d.rectangle((w*.44,h*.62,w*.57,h*.91),fill=BLUE)
        for x in [.29,.64]:d.rectangle((w*x,h*.6,w*(x+.1),h*.76),fill=(147,185,214))
    else:
        d.polygon([(w*.34,h*.17),(w*.2,h*.23),(w*.08,h*.49),(w*.27,h*.6),(w*.32,h*.44),(w*.32,h*.9),(w*.68,h*.9),(w*.68,h*.44),(w*.73,h*.6),(w*.92,h*.49),(w*.8,h*.23),(w*.66,h*.17)],fill=BLUE)
        d.arc((w*.34,h*.07,w*.66,h*.3),0,180,fill=(24,56,126),width=5)
    return im

def listing(kind,title,subtitle='Local possibilities',dark=False):
    im=Image.new('RGBA',(300,310))
    rr(im,(0,0,299,309),26,(27,33,46) if dark else (255,255,255), (53,62,80) if dark else (218,224,233),2)
    im.alpha_composite(product_art(kind,268,182),(16,16))
    text(im,20,215,title,25,WHITE if dark else INK)
    text(im,20,255,subtitle,17,(164,176,198) if dark else (105,115,132),False)
    return im

@lru_cache(maxsize=4)
def screen(mode='market'):
    im=Image.new('RGBA',(560,1150),(246,248,251));d=ImageDraw.Draw(im)
    text(im,32,24,'9:41',20,INK)
    rr(im,(446,28,496,45),4,None,(80,89,103),2);rr(im,(450,31,485,42),2,(80,89,103))
    logo_at(im,28,87,43);text(im,87,88,'konekta',39)
    text(im,31,155,'Your local world.',38)
    rr(im,(28,217,532,284),33,(231,236,244));text(im,56,237,'Search Konekta',22,(113,124,141),False)
    for i,(lab,w) in enumerate([('Products',130),('Services',128),('Homes',110)]):pill(im,28+i*167,310,w,lab,active=(i==0))
    text(im,28,408,'Find your next connection',28)
    for i,(kind,name) in enumerate([('headphones','Everyday finds'),('sofa','Make it home'),('shirt','Local businesses'),('house','Land & homes')]):
        card=listing(kind,name).resize((242,250),Image.Resampling.LANCZOS)
        im.alpha_composite(card,(28+(i%2)*262,467+(i//2)*275))
    rr(im,(0,1040,560,1150),0,(255,255,255));d.line((0,1040,560,1040),fill=(223,229,238),width=2)
    for i,(kind,label) in enumerate([('home','Home'),('bag','Explore'),('chat','Chat'),('shield','Wallet')]):
        icon(im,kind,74+i*138,1080,31,BLUE if i==0 else (132,141,156));text(im,48+i*138,1110,label,17,(113,123,140),False)
    return im

@lru_cache(maxsize=6)
def phone(mode='market'):
    im=Image.new('RGBA',(640,1290));d=ImageDraw.Draw(im)
    for pad,fill in [(0,(104,113,130)),(3,(28,32,42)),(8,(62,69,84)),(13,(8,10,15)),(20,(15,18,24))]:
        rr(im,(pad,10+pad,639-pad,1280-pad),82-pad/2,fill)
    d.line((21,135,21,1130),fill=(142,155,179),width=3)
    d.line((617,240,617,1060),fill=(75,93,125),width=2)
    face=screen(mode).resize((570,1190),Image.Resampling.LANCZOS)
    mask=Image.new('L',face.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,569,1189),radius=61,fill=255)
    face.putalpha(mask);im.alpha_composite(face,(35,48))
    rr(im,(242,51,399,83),16,(8,10,14))
    d.ellipse((365,60,379,74),fill=(20,29,46),outline=(45,55,74),width=2)
    rr(im,(249,1219,391,1227),4,(24,26,31))
    return im

def project(im,texture,cx,cy,scale=1,yaw=0,pitch=0,roll=0,depth=0,shadow=True):
    """Project a textured rigid plane using a perspective camera, not a warped redraw."""
    tw,th=texture.size;f=1800
    verts=np.array([[-tw/2,-th/2,0],[tw/2,-th/2,0],[tw/2,th/2,0],[-tw/2,th/2,0]],dtype=float)*scale
    a,b,c=map(math.radians,(yaw,pitch,roll))
    ry=np.array([[math.cos(a),0,math.sin(a)],[0,1,0],[-math.sin(a),0,math.cos(a)]])
    rx=np.array([[1,0,0],[0,math.cos(b),-math.sin(b)],[0,math.sin(b),math.cos(b)]])
    rz=np.array([[math.cos(c),-math.sin(c),0],[math.sin(c),math.cos(c),0],[0,0,1]])
    verts=verts@(rz@rx@ry).T;z=verts[:,2]+f+depth
    pts=np.column_stack((cx+verts[:,0]*f/z,cy+verts[:,1]*f/z))
    source=[(0,0),(tw,0),(tw,th),(0,th)]
    mat=[];rhs=[]
    for (x,y),(u,v) in zip(pts,source):
        mat.append([x,y,1,0,0,0,-u*x,-u*y]);rhs.append(u)
        mat.append([0,0,0,x,y,1,-v*x,-v*y]);rhs.append(v)
    coeff=np.linalg.solve(np.array(mat),np.array(rhs))
    layer=texture.transform((W,H),Image.Transform.PERSPECTIVE,coeff,Image.Resampling.BICUBIC)
    if shadow:
        shade=Image.new('RGBA',(W,H),(0,0,0,0));shade.putalpha(layer.getchannel('A').filter(ImageFilter.GaussianBlur(35)).point(lambda p:int(p*.36)))
        shifted=Image.new('RGBA',(W,H));shifted.alpha_composite(shade,(0,34));im.alpha_composite(shifted)
    im.alpha_composite(layer)

def label(im,dark=True):
    c=(121,137,164) if dark else (137,148,166)
    center(im,1795,'Illustrative UI • Not an app screenshot',20,c,False)

def call_card(kind,title,subtitle,w=500):
    im=Image.new('RGBA',(w,190));rr(im,(0,0,w-1,189),33,(25,33,48),(66,83,112),2)
    rr(im,(26,36,139,149),32,BLUE);icon(im,kind,83,92,59,WHITE)
    text(im,170,42,title,32,WHITE);text(im,170,95,subtitle,21,(160,177,202),False)
    return im

def wave_card():
    im=Image.new('RGBA',(530,140));rr(im,(0,0,529,139),70,BLUE)
    icon(im,'mic',55,70,48,WHITE);d=ImageDraw.Draw(im)
    for i in range(34):
        amp=12+25*abs(math.sin(i*.78));x=115+i*9
        d.line((x,70-amp,x,70+amp),fill=WHITE,width=5)
    text(im,445,55,'0:12',22,WHITE,False);return im

def hook():
    im=stage();logo_at(im,90,138,49,WHITE);text(im,158,142,'konekta',34,WHITE)
    center(im,299,'Your world.',107,WHITE);center(im,425,'Connected.',107,WHITE)
    project(im,phone(),540,1190,.86,-22,9,-9)
    label(im);return im

def market():
    im=stage(False);text(im,91,185,'Buy. Sell.',118);text(im,91,333,'Find more.',99,BLUE)
    project(im,phone(),675,1160,.86,19,6,9)
    project(im,listing('shirt','Local businesses'),222,940,1.04,-12,-7,-7)
    project(im,listing('house','Land & homes'),232,1350,.95,-8,5,-5)
    label(im,False);return im

def calls():
    im=stage();text(im,90,188,'Closer.',132,WHITE);text(im,90,350,'In a tap.',114,WHITE)
    project(im,phone(),835,1155,.89,-22,8,-10)
    for i,(kind,title,sub) in enumerate([('mic','Voice calls','Talk directly'),('video','Video calls','See the connection'),('chat','Private chat','Keep it in Konekta')]):
        project(im,call_card(kind,title,sub),380,768+i*290,.99,6,-3,-3,shadow=True)
    project(im,wave_card(),400,1575,1.10,4,0,-3);label(im);return im

def protection():
    im=stage(False);center(im,230,'Pay in-app.',118);center(im,385,'Stay protected.',91,BLUE)
    badge=Image.new('RGBA',(390,420));rr(badge,(0,0,389,419),88,(255,255,255),(218,225,237),3)
    icon(badge,'shield',195,178,188);center(badge,306,'Konekta Protection',25)
    project(im,badge,570,999,1.43,-12,-5,-7)
    token=Image.new('RGBA',(235,135));rr(token,(0,0,234,134),67,BLUE);center(token,32,'NLe',57,WHITE)
    project(im,token,259,1265,1.06,-8,0,-5)
    center(im,1485,'Held in escrow.',48)
    center(im,1574,'Release conditions and dispute terms apply.',25,(121,132,148),False)
    label(im,False);return im

def business():
    im=stage();text(im,90,188,'Your business.',93,WHITE);text(im,90,310,'More connections.',77,(119,163,255))
    project(im,phone(),532,1140,.85,-9,3,-3)
    project(im,listing('shirt','Your catalog','Show what you offer',True),232,975,1.09,13,-3,-10)
    project(im,listing('sofa','New possibilities','Connect with customers',True),828,1280,1.02,-13,7,9)
    project(im,call_card('chat','Customer chat','Start a conversation',530),540,1555,1,-6,0,-3)
    label(im);return im

def more():
    im=stage(False);text(im,91,198,'One app.',129);text(im,91,353,'More possibility.',82,BLUE)
    ticket=Image.new('RGBA',(660,310));rr(ticket,(0,0,659,309),39,BLUE);d=ImageDraw.Draw(ticket)
    for y in range(25,285,24):d.line((474,y,474,y+10),fill=(150,188,255),width=3)
    for y in [0,310]:d.ellipse((450,y-24,498,y+24),fill=WHITE)
    text(ticket,38,42,'EVENT TICKETS',24,WHITE,False);text(ticket,38,110,'Be there.',69,WHITE)
    text(ticket,505,66,'K',86,WHITE)
    project(im,ticket,559,915,1.17,-9,-6,-6)
    ai=Image.new('RGBA',(790,270));rr(ai,(0,0,789,269),52,(255,255,255),(216,225,239),2)
    icon(ai,'spark',81,79,52);text(ai,134,47,'Konekta AI',41)
    rr(ai,(36,134,753,232),49,(237,242,250));text(ai,69,165,'Ask. Explore. Connect.',32,(93,107,128),False)
    project(im,ai,541,1329,.98,5,4,4)
    for i,(kind,lab) in enumerate([('home','Homes'),('bag','Products'),('service','Services')]):
        icon(im,kind,218+i*326,1620,48);text(im,165+i*326,1673,lab,27,(100,114,136),False)
    label(im,False);return im

def ending():
    im=stage(False);logo_at(im,457,265,166)
    center(im,589,'Connect',132);center(im,755,'with Konekta.',111)
    rr(im,(148,1150,931,1300),75,BLUE);center(im,1194,'Get it on Google Play',43,WHITE,False)
    center(im,1408,'konekta.website',43,(92,109,133),False)
    center(im,1638,'Made for Sierra Leone.',28,(126,139,157),False)
    return im

SCENES=[hook,market,calls,protection,business,more,ending]
CAPTIONS=['01  PRODUCT REVEAL','02  MARKETPLACE','03  CALLS + CHAT','04  PROTECTION','05  BUSINESS','06  TICKETS + AI','07  CONNECT']

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    strip=Image.new('RGB',(7*288,635),(244,246,250));d=ImageDraw.Draw(strip)
    for i,(scene,caption) in enumerate(zip(SCENES,CAPTIONS)):
        im=scene().convert('RGB');im.save(OUT/f'styleframe-{i+1}.png')
        strip.paste(im.resize((288,512),Image.Resampling.LANCZOS),(288*i,0))
        d.text((288*i+18,540),caption,font=font(15),fill=INK)
    d.text((18,590),'KONEKTA / PRODUCT-MOTION REMAKE / ILLUSTRATIVE INTERFACES / 30s VERTICAL',font=font(16,False),fill=(100,112,129))
    strip.save(OUT/'motion-storyboard.png')

if __name__=='__main__':main()