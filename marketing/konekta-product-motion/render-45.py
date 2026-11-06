"""45-second approved extension: kinetic feature list, real-photo mosaic, convergence."""
from pathlib import Path
import argparse, importlib.util, math, subprocess, json
import numpy as np
from scipy.io import wavfile
from PIL import Image, ImageDraw
import styleframes as s
import real_assets as real

ROOT=Path(__file__).resolve().parent;OUT=ROOT/'output'
spec=importlib.util.spec_from_file_location('full',ROOT/'render-final.py')
full=importlib.util.module_from_spec(spec);spec.loader.exec_module(full)
smooth,out,mix,alpha,type_line=full.smooth,full.out,full.mix,full.alpha,full.type_line
FPS,LENGTH=30,45

def features(t):
    im=s.stage(False)
    type_line(im,'More ways',90,208,111,s.INK,t,.02)
    type_line(im,'to Konekta.',90,351,102,s.BLUE,t,.2)
    labels=['Products','Services','Land & homes','Businesses','Private chat','Protection']
    progress=min(5,t*1.23);focus=min(5,int(progress));frac=smooth(progress-focus)
    offset=95*(focus+frac)
    layer=Image.new('RGBA',(s.W,s.H))
    for i,lab in enumerate(labels):
        y=930+i*95-offset
        distance=abs(y-930)
        opacity=max(0,1-distance/385)
        col=s.BLUE if i==focus else (154,165,184)
        row=Image.new('RGBA',(s.W,s.H));s.text(row,106,y,lab,55,col)
        if i==focus:ImageDraw.Draw(row).ellipse((74,y+28,86,y+40),fill=s.BLUE)
        layer.alpha_composite(alpha(row,opacity))
    im.alpha_composite(layer)
    kind=['laptop','service','home','tester','laptop','home'][focus]
    if focus<4:
        card=real.photo_card(kind)
        s.project(im,card,803,1000+13*math.sin(t*2),.94,-10+4*math.sin(t),4,5)
    else:s.project(im,real.phone(3 if focus==4 else 4),825,1130,.43,-12,5,6)
    type_line(im,'One place. Local possibilities.',92,1580,35,(91,110,137),t,.8)
    real.footer(im);return im

def mosaic_layout():
    return [(185,660,-9),(540,647,3),(895,688,10),(170,1057,6),(540,1050,-4),(902,1080,-8),(202,1450,-7),(554,1455,6),(907,1477,-5)]

def mosaic(t,collapse=False):
    im=s.stage(False)
    if not collapse:
        type_line(im,'Find your',90,169,113,s.INK,t,.02)
        type_line(im,'next connection.',90,314,83,s.BLUE,t,.2)
    kinds=['laptop','home','tester','service','laptop','home','tester','service','laptop']
    for i,((x,y,roll),kind) in enumerate(zip(mosaic_layout(),kinds)):
        if collapse:
            q=smooth((t-i*.08)/2.7)
            cx=mix(x,540,q);cy=mix(y,920,q);scale=mix(.89,.07,q)
            tex=alpha(real.photo_card(kind),1-out((t-2.15)/1.1))
            s.project(im,tex,cx,cy,scale,mix(-9,0,q),4,mix(roll,0,q))
        else:
            q=out((t-i*.065)/.7)
            if q<=0:continue
            cx=mix(540,x,q);cy=mix(1020,y,q)+5*math.sin(t*.8+i)
            s.project(im,alpha(real.photo_card(kind),q),cx,cy,mix(.25,.88,q),mix(20,-9,q),4,mix(0,roll,q))
    if collapse:
        q=out((t-2.35)/.8)
        if q>0:
            n=round(mix(65,174,q));layer=Image.new('RGBA',(s.W,s.H));s.logo_at(layer,540-n//2,830,n)
            im.alpha_composite(alpha(layer,q))
            type_line(im,'All connected.',0,1140,83,s.INK,t,2.7,True)
    else:
        # Catalog cards stay conceptually sourced, without pretending live availability.
        real.footer(im)
    return im

def extension(t):
    if t<5:return features(t)
    if t<11:
        im=mosaic(t-5)
        if t<5.25:im=Image.blend(features(4.99),im,smooth((t-5)/.25))
        return im
    im=mosaic(t-11,True)
    if t<11.25:im=Image.blend(mosaic(5.99),im,smooth((t-11)/.25))
    return im

def frame(t):
    if t<26:return full.frame(t)
    if t<41:
        im=extension(t-26)
        if t<26.25:im=Image.blend(full.frame(25.999).convert('RGBA'),im,smooth((t-26)/.25))
        return im.convert('RGB')
    im=full.ending(t-41)
    if t<41.25:im=Image.blend(extension(14.999),im,smooth((t-41)/.25))
    return im.convert('RGB')

def master_audio():
    # Read the approved mix and existing instrumental; no voice regeneration/time-stretch.
    source=OUT/'approved-decoded.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(ROOT/'audio/approved-soundtrack.m4a'),'-c:a','pcm_s16le',str(source)],check=True)
    sr,original=wavfile.read(source);sr2,music=wavfile.read(ROOT/'audio/instrumental.wav')
    assert sr==sr2==48000
    original=original.astype(float)/32768;music=music.astype(float)/32768
    original=original[:30*sr]
    bridge=music[12*sr:27*sr].copy()
    assert len(bridge)==15*sr
    bridge*=.052/max(np.sqrt(np.mean(bridge**2)),1e-9)
    audio=np.concatenate((original[:26*sr],bridge,original[26*sr:30*sr]))
    # Smooth only the music joins, inside the silence before the closing CTA.
    fade=int(sr*.05)
    for boundary in [26*sr,41*sr]:
        left=audio[boundary-fade:boundary].copy();right=audio[boundary:boundary+fade].copy()
        level=np.mean(np.concatenate((left,right)),axis=0)
        ramp=np.linspace(0,1,fade)[:,None]
        audio[boundary-fade:boundary]=left*(1-ramp)+level*ramp
        audio[boundary:boundary+fade]=level*(1-ramp)+right*ramp
    assert len(audio)==sr*45
    assert np.max(abs(audio))<.99
    wavfile.write(OUT/'soundtrack-45.wav',sr,(audio*32767).astype(np.int16))
    (OUT/'audio-45-edit.json').write_text(json.dumps({'insert_at':26,'music_bridge_seconds':15,'closing_cta_starts':41.3,'voices':'approved mix, no regeneration or time-stretch','join_ms':50,'peak_dbfs':float(20*np.log10(np.max(abs(audio))))},indent=2))

def render(stills=False):
    OUT.mkdir(parents=True,exist_ok=True)
    times=[6,15.6,24.5,27.1,29.6,33.2,36,39.8,43.5]
    for i,t in enumerate(times):
        im=frame(t);im.save(OUT/f'45-scene-{i+1}.jpg',quality=94)
    # Compact thumbnails for QA without altering delivered full-size frame samples.
    sheet=Image.new('RGB',(1080,1620),(237,241,246))
    for i,t in enumerate(times):
        im=frame(t);sheet.paste(im.resize((270,480),Image.Resampling.LANCZOS),((i%4)*270,(i//4)*540));s.text(sheet,(i%4)*270+15,(i//4)*540+495,f'{t:.1f}s',22)
    sheet.save(OUT/'45-contact-sheet.jpg',quality=94)
    full.ending(3).convert('RGB').save(OUT/'konekta-45-cover.png')
    if stills:return
    master_audio()
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{s.W}x{s.H}','-r',str(FPS),'-i','-','-i',str(OUT/'soundtrack-45.wav'),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(LENGTH),'-movflags','+faststart',str(OUT/'konekta-product-motion-45sec.mp4')]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for k in range(FPS*LENGTH):
            proc.stdin.write(frame(k/FPS).tobytes())
            if k%150==0:print(f'{k}/{FPS*LENGTH}',flush=True)
    finally:proc.stdin.close()
    assert proc.wait()==0

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--stills',action='store_true')
    render(parser.parse_args().stills)