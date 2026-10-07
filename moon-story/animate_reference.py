"""Reference-inspired ink-and-watercolor animation with articulated hanging poses."""
import sys, pathlib, math, subprocess, textwrap
from collections import deque
sys.path.insert(0,'/private/tmp/moon-video-libs')
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'dist'
ASSETS=ROOT/'animation-assets'
W,H,FPS=960,540,24
background=Image.open(ASSETS/'pond-background.png').convert('RGBA').resize((960,394),Image.Resampling.LANCZOS)
atlas=Image.open(ASSETS/'comic-monkeys.png').convert('RGBA')
old=Image.open(ASSETS/'puppet.png').convert('RGBA')
moon=old.crop((old.width*2//3,old.height//2,old.width,old.height))
moon=moon.crop(moon.getchannel('A').getbbox())
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
zhfont=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',28)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
captions=[
 ('One moonlit night, a little monkey saw a moon in the pond.', '“Look! The moon has fallen into the water!”'),
 ('The monkeys gathered on the branch to make a plan.', '“Let’s hold on to one another and scoop it up!”'),
 ('They hung in a chain, holding hands and feet.', 'The smallest reached down. Ripples scattered the reflection.'),
 ('“Wait! Look up—the real moon is still in the sky!”', 'The monkeys smiled. The moon in the pond was only a reflection.')
]
chinese=[
 ('一个月夜，小猴子看见池塘里有个月亮。', '“快看！月亮掉进水里了！”'),
 ('猴子们坐在树枝上，一起商量办法。', '“一个接一个，我们把月亮捞上来吧！”'),
 ('猴子们手拉着脚，倒挂着连成一串。', '小猴子伸手一捞，水里的月亮散开了。'),
 ('“快抬头看！月亮还好好地挂在天上呢！”', '大家笑了：原来水里的月亮只是倒影。')
]
def cell(column,row):
    xs=[0,380,758,1124,1448]
    ys=[0,316,766,1086]
    part=atlas.crop((xs[column],ys[row],xs[column+1],ys[row+1]))
    # Select the complete monkey, excluding atlas edge noise and neighboring tips.
    mask=bytearray(1 if v>80 else 0 for v in part.getchannel('A').getdata())
    width,height=part.size;best_count=0;box=None
    for i in range(len(mask)):
        if not mask[i]:continue
        pending=deque([i]);mask[i]=0;count=0;left=width;right=0;top=height;bottom=0
        while pending:
            p=pending.popleft();x=p%width;y=p//width;count+=1
            left=min(left,x);right=max(right,x);top=min(top,y);bottom=max(bottom,y)
            for q in (p-width,p+width,p-1 if x else -1,p+1 if x<width-1 else -1):
                if 0<=q<len(mask) and mask[q]:mask[q]=0;pending.append(q)
        if count>best_count:best_count=count;box=(left,top,right+1,bottom+1)
    return part.crop(box) if box else part
poses=[[cell(c,r) for c in range(4)] for r in range(3)]
def contact_x(part,top):
    alpha=part.getchannel('A')
    rows=range(0,max(1,round(part.height*.07))) if top else range(round(part.height*.93),part.height)
    points=[(x,alpha.getpixel((x,y))) for y in rows for x in range(part.width) if alpha.getpixel((x,y))>80]
    return sum(x*weight for x,weight in points)/sum(weight for _,weight in points)/part.width
feet_contacts=[(contact_x(part,True),.01) for part in poses[1]]
hand_contacts=[(contact_x(part,False),.99) for part in poses[1]]
def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def sprite(frame,character,pose,x,y,height,angle=0,anchor=(.45,.97),end=(.5,1)):
    source=poses[pose][character]
    part=source.resize((round(source.width*height/source.height),round(height)),Image.Resampling.LANCZOS)
    width,high=part.size
    radians=math.radians(angle);cs,sn=math.cos(radians),math.sin(radians)
    ax=(anchor[0]-.5)*width;ay=(anchor[1]-.5)*high
    rotated=part.rotate(-angle,Image.Resampling.BICUBIC,expand=True)
    ox=x-rotated.width/2-(ax*cs-ay*sn)
    oy=y-rotated.height/2-(ax*sn+ay*cs)
    frame.alpha_composite(rotated,(round(ox),round(oy)))
    # Return the lower hands' contact point for the next monkey's feet.
    hx=(end[0]-.5)*width;hy=(end[1]-.5)*high
    return x+(hx-ax)*cs-(hy-ay)*sn,y+(hx-ax)*sn+(hy-ay)*cs
def water(frame,t,disturbed):
    layer=Image.new('RGBA',(240,70))
    disk=moon.resize((65,23),Image.Resampling.LANCZOS)
    if disturbed:
        for y in range(0,23,2):
            layer.alpha_composite(disk.crop((0,y,65,min(y+2,23))),(87+round(10*math.sin(t*7+y*.5)),23+y))
    else:layer.alpha_composite(disk,(87,23))
    d=ImageDraw.Draw(layer)
    for k in range(4 if disturbed else 2):
        u=(t*(.6 if disturbed else .15)+k*.25)%1
        rx=20+88*u;ry=3+17*u
        d.ellipse((120-rx,35-ry,120+rx,35+ry),outline=(242,231,185,round((1-u)*170)),width=2)
    frame.alpha_composite(layer,(410,300))
def bank(frame,character,x,t,point=True):
    baseline=353;height=[90,106,95,102][character]
    shadow=Image.new('RGBA',(W,H));d=ImageDraw.Draw(shadow)
    d.ellipse((x-35,baseline-4,x+35,baseline+5),fill=(7,22,34,80));frame.alpha_composite(shadow)
    sprite(frame,character,2 if point else 0,x,baseline,height,2*math.sin(t*2+character),anchor=(.5,.98))
def chain(frame,t,lower=True):
    # Each child's feet follow the parent's hand position, including sway.
    progress=ease(t/3) if lower else 1
    x=530;y=95-30*(1-progress)
    for k,character in enumerate([1,2,0]):
        angle=5*math.sin(t*1.7+k*.35)
        x,y=sprite(frame,character,1,x,y,[78,78,84][k],angle,anchor=feet_contacts[character],end=hand_contacts[character])
    return x,y
def render(t):
    scene=min(3,int(t//12));u=t%12
    frame=Image.new('RGBA',(W,H),(7,18,31,255));frame.alpha_composite(background)
    water(frame,t,scene==2 and u>4)
    if scene==0:
        sprite(frame,1,0,260,95,90,2*math.sin(u*1.3))
        sprite(frame,2,0,360,100,92,3*math.sin(u*1.8+1))
        x=430+65*ease(u/4)
        sprite(frame,0,0,x,105,95,4+4*math.sin(u*2))
    elif scene==1:
        for k,(x,y,height) in enumerate([(225,91,88),(330,96,90),(430,101,93),(515,108,99)]):
            sprite(frame,k,0,x,y,height,3*math.sin(u*1.8+k))
    elif scene==2:
        chain(frame,u)
        bank(frame,3,825,u,point=False)
    else:
        for k,x in enumerate([155,255,805,885]):bank(frame,k,x,u)
        glow=Image.new('RGBA',(W,H));d=ImageDraw.Draw(glow)
        r=36+4*math.sin(u*2)
        d.ellipse((797-r,55-r,797+r,55+r),outline=(244,234,180,80),width=2)
        frame.alpha_composite(glow)
    panel=Image.new('RGBA',(W,H));d=ImageDraw.Draw(panel)
    d.rectangle((0,394,W,H),fill=(3,13,24,255))
    d.text((28,407),f'{scene+1:02d} / 04',font=small,fill=(234,198,122,255))
    d.text((480,449),chinese[scene][int(u>=6)],font=zhfont,anchor='mm',fill=(234,198,122,255))
    for j,line in enumerate(textwrap.wrap(captions[scene][int(u>=6)],width=76)):
        d.text((480,484+j*28),line,font=font,anchor='mm',fill=(250,245,231,255))
    return Image.alpha_composite(frame,panel).convert('RGB')
if __name__=='__main__':
    if '--preview' in sys.argv:
        contact=Image.new('RGB',(W*2,H*4))
        for i,t in enumerate([3,9,16,21,28,33,39,45]):contact.paste(render(t),(i%2*W,i//2*H))
        contact.save('/private/tmp/moon-reference-preview.jpg');print('/private/tmp/moon-reference-preview.jpg');sys.exit()
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    p=subprocess.Popen([ff,'-y','-f','rawvideo','-pix_fmt','rgb24','-s','960x540','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(ROOT/'silent.mp4')],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    for i in range(48*FPS):
        f=render(i/FPS)
        if i==20*FPS:f.save(OUT/'comic-poster.jpg',quality=93)
        p.stdin.write(f.tobytes())
    p.stdin.close();assert p.wait()==0
    if not (ROOT/'music.wav').exists():
        import wave,struct,array
        source=(ROOT/'generate_video.py').read_text();start=source.index('# Original playful score:');end=source.index('subprocess.run(',start);exec(source[start:end])
    target=OUT/'monkeys-comic.mp4'
    subprocess.run([ff,'-y','-i',str(ROOT/'silent.mp4'),'-i',str(ROOT/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(target)],check=True,stderr=subprocess.DEVNULL)
    subprocess.run([ff,'-y','-i',str(target),'-c:v','libvpx-vp9','-b:v','0','-crf','34','-cpu-used','4','-row-mt','1','-c:a','libopus',str(OUT/'monkeys-comic.webm')],check=True,stderr=subprocess.DEVNULL)
    print('Rendered reference-inspired cartoon in WebM and MP4.')
