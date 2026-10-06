"""Render a 2D puppet film with independently moving limbs and water ripples."""
import sys, pathlib, math, subprocess, textwrap, ast, wave, struct, array
sys.path.insert(0, '/private/tmp/moon-video-libs')
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent
OUT = ROOT/'dist'
ASSETS = ROOT/'animation-assets'
W,H,FPS = 960,540,24
source=(ROOT/'generate_video.py').read_text()
constants={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(source).body
           if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('captions','chinese')}
captions,chinese=constants['captions'],constants['chinese']
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
zhfont=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',28)
small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
ff=imageio_ffmpeg.get_ffmpeg_exe()
background=Image.open(ASSETS/'background.png').convert('RGBA').resize((960,394),Image.Resampling.LANCZOS)
atlas=Image.open(ASSETS/'puppet.png').convert('RGBA')
def cell(x,y):
    part=atlas.crop((x*atlas.width//3,y*atlas.height//2,(x+1)*atlas.width//3,(y+1)*atlas.height//2))
    box=part.getchannel('A').getbbox()
    return part.crop(box) if box else part
body,arm,arm_left,feet,elder,moon=[cell(x,y) for y in range(2) for x in range(3)]
variety=Image.open(ASSETS/'puppet-variety.png').convert('RGBA')
def character_cell(column,row):
    # Generated bodies need taller cells than the separate limbs.
    xs=[0,315,640,950,1254];ys=[0,460,700,940,1254]
    part=variety.crop((xs[column],ys[row],xs[column+1],ys[row+1]))
    box=part.getchannel('A').point(lambda v:255 if v>64 else 0).getbbox()
    return part.crop(box) if box else part
characters=[tuple(character_cell(column,row) for row in range(4)) for column in range(4)]
# Keep the full backdrop visible; the separate moon retains a circular shape.
background.alpha_composite(moon.resize((104,104),Image.Resampling.LANCZOS),(727,8))
def resized(part,height):
    return part.resize((max(1,round(part.width*height/part.height)),round(height)),Image.Resampling.LANCZOS)
def place(frame,part,x,y):
    frame.alpha_composite(part,(round(x),round(y)))
def limb(frame,x,y,length,angle,left=False,character=0):
    part=characters[character][2 if left else 1]
    part=part.resize((round(length),max(8,round(length*part.height/part.width))),Image.Resampling.LANCZOS)
    radius=round(length+12)
    canvas=Image.new('RGBA',(radius*2,radius*2))
    canvas.alpha_composite(part,(radius-part.width if left else radius,radius-part.height//2))
    canvas=canvas.rotate(-angle,Image.Resampling.BICUBIC)
    place(frame,canvas,x-radius,y-radius)
def puppet(frame,x,y,size=110,right=65,left=-65,sway=0,old=False,walk=0,legs=True,character=0,ground=None,reach=False):
    # y is the torso center. Arms pivot independently around both shoulders.
    if old:character=3
    part=resized(characters[character][0],size)
    if ground is not None:
        shadow=Image.new('RGBA',(W,H));d=ImageDraw.Draw(shadow)
        d.ellipse((x-size*.35,ground-4,x+size*.35,ground+5),fill=(3,11,17,95))
        frame.alpha_composite(shadow)
    if legs:
        shoe=resized(characters[character][3],size*.29)
        shoe=shoe.rotate(walk*8,Image.Resampling.BICUBIC,expand=True)
        place(frame,shoe,x-shoe.width/2,y+size*.31)
    limb(frame,x-size*.19,y+size*.12,size*.54,left,left=True,character=character)
    limb(frame,x+size*.19,y+size*.12,size*(.82 if reach else .54),right,character=character)
    part=part.rotate(sway,Image.Resampling.BICUBIC,expand=True)
    place(frame,part,x-part.width/2,y-part.height/2)
def ease(v):
    v=max(0,min(1,v));return v*v*(3-2*v)
def reflection(frame,t,disturbed=False):
    water=Image.new('RGBA',(210,75))
    disk=moon.resize((60,28),Image.Resampling.LANCZOS)
    if disturbed:
        # Horizontal strips undulate independently when the hand touches water.
        for y in range(0,28,2):
            strip=disk.crop((0,y,60,min(28,y+2)))
            water.alpha_composite(strip,(75+round(9*math.sin(t*7+y*.5)),20+y))
    else: water.alpha_composite(disk,(75,20))
    d=ImageDraw.Draw(water)
    for k in range(4 if disturbed else 2):
        u=(t*(.65 if disturbed else .18)+k*.25)%1
        rx=15+75*u;ry=3+12*u
        d.ellipse((105-rx,34-ry,105+rx,34+ry),outline=(239,203,128,round(150*(1-u))),width=2)
    place(frame,water,470,248)

def render(t):
    scene=min(3,int(t//12));u=t%12
    frame=Image.new('RGBA',(W,H),(7,18,31,255));frame.alpha_composite(background)
    # The water moves independently of the backdrop and camera.
    reflection(frame,t,scene==2 and u>4)
    if scene==0:
        x=180+170*ease(u/4)
        bob=3*math.sin(u*9)*(1-ease((u-3)/2))
        lean=ease((u-4)/2)
        y=335-98*.60
        if u<6:
            puppet(frame,x,y+bob,size=98,right=65-40*lean+12*math.sin(u*2),left=-65,sway=-lean*9,walk=math.sin(u*9),ground=335)
        else:
            # Surprise is acted with both arms rising rather than a camera pan.
            puppet(frame,x,y,size=98,right=-45+18*math.sin(u*4),left=45-18*math.sin(u*4),sway=3*math.sin(u*3),ground=335)
    elif scene==1:
        for k,target in enumerate([250,350,815,895]):
            enter=ease((u-k*.65)/3)
            start=target-220 if k<2 else target+180
            x=start*(1-enter)+target*enter
            bob=4*math.sin(u*8+k)*(1-enter)+2*math.sin(u*2+k)
            size=[98,124,110,118][k]
            puppet(frame,x,335-size*.60+bob*(1-enter),size=size,right=-25+22*math.sin(u*2+k),left=-60+18*math.sin(u*2+k),sway=2*math.sin(u*2+k),walk=math.sin(u*8+k)*(1-enter),character=k,ground=335)
    elif scene==2:
        descend=ease(u/4)
        for k in range(3):
            x=500+12*math.sin(u*1.7+k*.22)
            y=88+k*66-35*(1-descend)
            puppet(frame,x,y,size=72,right=90+12*math.sin(u*2.6) if k==2 else 110,left=110 if k else 150,sway=4*math.sin(u*1.7+k*.22),legs=False,character=[1,2,0][k],reach=k==2)
        # The elder stays on dry ground; only the lowest arm reaches the water.
        puppet(frame,840,335-116*.60,size=116,right=-15+12*math.sin(u*2),left=-55,sway=2*math.sin(u*2),character=3,ground=335)
    else:
        point=ease((u-1)/2)
        for k,x in enumerate([250,350,815,895]):
            bounce=max(0,math.sin((u-5)*4+k))*9 if u>5 else 2*math.sin(u*2+k)
            size=[98,124,110,118][k]
            puppet(frame,x,335-size*.60-bounce,size=size,right=-55*point+60*(1-point)+10*math.sin(u*2+k),left=-65+20*math.sin(u*2+k),sway=3*math.sin(u*2+k),character=k,ground=335)
        # A soft animated ring directs attention to the real moon above.
        if u>1:
            glow=Image.new('RGBA',(W,H));d=ImageDraw.Draw(glow)
            r=43+5*math.sin(u*2)
            d.ellipse((779-r,60-r,779+r,60+r),outline=(255,216,132,round(65+35*math.sin(u*2))),width=2)
            frame.alpha_composite(glow)
    overlay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(overlay)
    d.rectangle((0,394,W,H),fill=(3,13,24,255))
    d.text((28,407),f'{scene+1:02d} / 04',font=small,fill=(234,198,122,255))
    d.text((480,449),chinese[scene][int(u>=6)],font=zhfont,anchor='mm',fill=(234,198,122,255))
    for j,line in enumerate(textwrap.wrap(captions[scene][int(u>=6)],width=76)):
        d.text((480,484+j*28),line,font=font,anchor='mm',fill=(250,245,231,255))
    frame=Image.alpha_composite(frame,overlay).convert('RGB')
    return frame

if __name__=='__main__':
    if '--preview' in sys.argv:
        times=[3,9,16,21,28,33,39,45]
        sheet=Image.new('RGB',(W*2,H*4))
        for i,t in enumerate(times):sheet.paste(render(t),(i%2*W,i//2*H))
        sheet.save('/private/tmp/moon-animation-preview.jpg')
        print('/private/tmp/moon-animation-preview.jpg');sys.exit()
    cmd=[ff,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','960x540','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(ROOT/'silent.mp4')]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    for i in range(48*FPS):
        f=render(i/FPS)
        if i==20*FPS:f.save(OUT/'animated-poster-ground.jpg',quality=93)
        p.stdin.write(f.tobytes())
    p.stdin.close();assert p.wait()==0
    if not (ROOT/'music.wav').exists():
        start=source.index('# Original playful score:');end=source.index('subprocess.run(',start)
        exec(source[start:end])
    target=OUT/'monkeys-ground.mp4'
    subprocess.run([ff,'-y','-i',str(ROOT/'silent.mp4'),'-i',str(ROOT/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(target)],check=True,stderr=subprocess.DEVNULL)
    subprocess.run([ff,'-y','-i',str(target),'-c:v','libvpx-vp9','-b:v','0','-crf','34','-cpu-used','4','-row-mt','1','-c:a','libopus',str(OUT/'monkeys-ground.webm')],check=True,stderr=subprocess.DEVNULL)
    print('Rendered 48-second puppet animation in MP4 and WebM.')
