"""Official Google Play screens and listing-photo crops, with no invented app UI."""
from functools import lru_cache
from PIL import Image, ImageDraw, ImageOps
import styleframes as s

@lru_cache(maxsize=4)
def screenshot(index):
    return Image.open(s.ASSETS/'official'/f'play-screen-{index}.png').convert('RGBA')

@lru_cache(maxsize=4)
def phone(index=2):
    im=Image.new('RGBA',(640,1290));d=ImageDraw.Draw(im)
    for pad,c in [(0,(105,116,135)),(3,(26,31,42)),(8,(62,72,88)),(13,(8,10,15)),(20,(15,18,24))]:
        s.rr(im,(pad,10+pad,639-pad,1280-pad),82-pad/2,c)
    face=ImageOps.contain(screenshot(index),(570,1190),Image.Resampling.LANCZOS)
    mask=Image.new('L',face.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,face.width-1,face.height-1),radius=48,fill=255)
    face.putalpha(mask);im.alpha_composite(face,((640-face.width)//2,(1290-face.height)//2))
    d.line((19,165,19,1120),fill=(133,158,197),width=3)
    d.line((620,250,620,1000),fill=(62,86,124),width=3)
    return im

@lru_cache(maxsize=12)
def photo_card(kind='laptop',dark=False):
    # Coordinates reference the 540×1170 official marketplace screenshot.
    crop={'laptop':(293,448,526,624),'home':(16,816,268,1005),'service':(57,404,225,653),'tester':(291,792,529,1031)}[kind]
    img=screenshot(2).crop(crop)
    im=Image.new('RGBA',(300,310));s.rr(im,(0,0,299,309),26,(26,33,46) if dark else (255,255,255),(64,78,100) if dark else (212,220,234),2)
    photo=ImageOps.fit(img,(268,208),Image.Resampling.LANCZOS)
    mask=Image.new('L',photo.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,267,207),radius=15,fill=255)
    photo.putalpha(mask);im.alpha_composite(photo,(16,16))
    title={'laptop':'Dell laptop','home':'Land & homes','service':'Local services','tester':'Shop products'}[kind]
    s.text(im,18,242,title,25,s.WHITE if dark else s.INK)
    return im

def footer(im,dark=False,features=False):
    c=(129,148,177) if dark else (116,132,154)
    s.center(im,1795,'Feature graphics' if features else 'Konekta • Official app screens',20,c,False)