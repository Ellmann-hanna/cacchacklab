"""Nine-scene original retelling of the well fable, using reference-style artwork."""
import animate_reference as art
from PIL import Image,ImageDraw,ImageChops,ImageOps
import math,random,sys,subprocess,textwrap
ROOT,OUT,W,H,FPS=art.ROOT,art.OUT,art.W,art.H,art.FPS
DURATION=90
# Independently written classroom narration; no dialogue transcribed from the reference.
chinese=[
 ('夜深了，小猴子蹦蹦跳跳地来到井边。','它跳上井沿，探头看见井里的圆月！'),
 ('小猴子吓了一跳，转身去叫大猴子。','大猴子赶来，弯下身子往井里瞧。'),
 ('老猴子也来看，急得抓耳挠腮。','猴子们听见叫声，纷纷跑到井边。'),
 ('大家你一言，我一语，想起了办法。','井旁有棵大树，树枝正好伸到井口上方。'),
 ('老猴子先爬上树，倒挂在树枝上。','大猴子抓住它，小猴子也接着挂了下去。'),
 ('一只接着一只，猴子链慢慢伸进井里。','最小的猴子在下面，把双手伸向水中的月亮。'),
 ('它捧了一次又一次，手里却只有水。','水波散开，月亮碎了；水一静，月亮又圆了。'),
 ('老猴子抬头喘口气，忽然发现了天上的月亮。','大家顺着它的目光一看，全都愣住了。'),
 ('月亮一直在天上，井里只是它的倒影。','猴子们爬回树上，跳到井边，笑成了一团。')]
captions=[
 ('A little monkey skipped to a well in the moonlit forest.','It hopped onto the stone rim and looked down at the moon.'),
 ('Startled, it hurried away to call a bigger monkey.','The bigger monkey came running and peered into the well.'),
 ('An old monkey looked too, scratching its head in alarm.','More monkeys heard the commotion and rushed over.'),
 ('They chattered and argued until they thought of a plan.','A sturdy branch stretched over the mouth of the well.'),
 ('The oldest climbed up and hung upside down.','The others joined, holding on tightly, one after another.'),
 ('Their long chain reached farther and farther into the well.','At the bottom, the smallest monkey stretched out both hands.'),
 ('It scooped again and again, but caught only water.','The moon broke into ripples, then became round again.'),
 ('The oldest looked up for a breath and spotted the moon above.','The others followed its gaze and stared in surprise.'),
 ('The moon had stayed in the sky. The well held its reflection.','They climbed back, hopped down, and laughed together.')]
# Ground and masonry are drawn into the watercolor landscape. Water is confined to the well.
background=art.background.copy()
d=ImageDraw.Draw(background)
d.polygon([(0,330),(180,318),(350,333),(530,347),(750,325),(960,315),(960,394),(0,394)],fill=(43,81,78,255))
rng=random.Random(14)
for i in range(850):
 x=rng.randrange(W);y=rng.randrange(342,394)
 d.line((x,y,x+rng.randrange(2,10),y-1),fill=rng.choice([(50,89,82),(37,72,72),(61,94,83)]),width=1)
for x in [18,68,128,830,884,934]:
 for j in range(5):d.line((x,386,x+(j-2)*8,360+rng.randrange(12)),fill=(26,62,57),width=2)
# Stone body and rim, with ink contours and varied watercolor blocks.
d.rounded_rectangle((419,304,641,395),radius=15,fill=(94,113,113),outline=(23,43,52),width=3)
for row in range(4):
 y=324+row*20
 for col in range(5):
  x=418+col*49-(24 if row%2 else 0)
  d.rectangle((max(421,x),y,min(638,x+46),min(394,y+18)),fill=rng.choice([(100,120,116),(85,106,107),(111,124,117),(91,112,112)]),outline=(50,73,76),width=1)
d.ellipse((413,281,647,343),fill=(134,149,140),outline=(24,43,49),width=3)
d.ellipse((431,292,629,329),fill=(27,56,80),outline=(48,70,78),width=3)
for x in range(430,635,28):d.line((x,285,x+3,294),fill=(64,87,89),width=2)
# Foreground lip occludes objects below the interior waterline.
lip=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(lip)
ld.arc((413,281,647,343),0,180,fill=(30,49,54),width=4)
ld.arc((421,289,639,336),5,175,fill=(151,157,140),width=8)

def reflection(frame,t,disturbed=False):
 layer=Image.new('RGBA',(190,38));disk=art.moon.resize((46,17),Image.Resampling.LANCZOS)
 for y in range(0,17,2):
  offset=round(9*math.sin(t*8+y*.6)) if disturbed else 0
  layer.alpha_composite(disk.crop((0,y,46,min(17,y+2))),(72+offset,9+y))
 dd=ImageDraw.Draw(layer)
 for k in range(3):
  u=(t*(.7 if disturbed else .14)+k/3)%1;rx=15+65*u;ry=2+12*u
  dd.ellipse((95-rx,18-ry,95+rx,18+ry),outline=(217,226,194,round(160*(1-u))),width=1)
 frame.alpha_composite(layer,(435,293))

def actor(frame,c,x,t,pose=0,base=371,h=None,hop=0,lean=0):
 h=h or [79,96,85,93][c]
 dd=ImageDraw.Draw(frame);dd.ellipse((x-24,base-3,x+24,base+4),fill=(24,52,57))
 art.sprite(frame,c,pose,x,base-hop,h,lean,anchor=(.5,.98))

def point_into_well(frame,c,x,t,base=371,h=None,hop=0):
 """Face the reflection and aim the illustrated arm from a stable foot contact."""
 h=h or [79,96,85,93][c]
 source=art.poses[0][c]
 part=source.resize((round(source.width*h/source.height),round(h)),Image.Resampling.LANCZOS)
 width,height=part.size
 # Isolate the extended arm, preserving the existing ink-and-watercolor drawing.
 mask=Image.new('L',part.size);md=ImageDraw.Draw(mask)
 polygon=[(.56,.49),(.68,.52),(.91,.69),(1,.78),(1,1),(.79,.90),(.64,.71),(.51,.59)]
 md.polygon([(round(a*width),round(b*height)) for a,b in polygon],fill=255)
 arm=part.copy();arm.putalpha(ImageChops.multiply(part.getchannel('A'),mask))
 body=part.copy();body.putalpha(ImageChops.subtract(part.getchannel('A'),mask))
 shoulder=(.57*width,.54*height)
 tip=(.96*width,.89*height)
 flip=x>530
 # Mirroring keeps monkeys on both sides facing the well.
 if flip:
  body=ImageOps.mirror(body);arm=ImageOps.mirror(arm)
  shoulder=(width-shoulder[0],shoulder[1]);tip=(width-tip[0],tip[1])
 # Anchor the visible supporting paws, rather than the full sprite (which includes a tail).
 alpha=body.getchannel('A')
 points=[(xx,alpha.getpixel((xx,yy))) for yy in range(round(height*.95),height) for xx in range(width) if alpha.getpixel((xx,yy))>80]
 foot_x=sum(xx*weight for xx,weight in points)/sum(weight for _,weight in points)
 ox=x-foot_x;oy=base-hop-height*.98
 sx,sy=ox+shoulder[0],oy+shoulder[1]
 target=(530,311)
 original=math.atan2(tip[1]-shoulder[1],tip[0]-shoulder[0])
 aimed=math.atan2(target[1]-sy,target[0]-sx)
 angle=math.degrees(original-aimed)
 radius=max(width,height)*2
 pivot=Image.new('RGBA',(radius*2,radius*2))
 pivot.alpha_composite(arm,(round(radius-shoulder[0]),round(radius-shoulder[1])))
 pivot=pivot.rotate(angle,Image.Resampling.BICUBIC)
 dd=ImageDraw.Draw(frame);dd.ellipse((x-13,base-2,x+13,base+2),fill=(50,68,67))
 frame.alpha_composite(body,(round(ox),round(oy)))
 frame.alpha_composite(pivot,(round(sx-radius),round(sy-radius)))


# Midpoints of four solid stone-rim segments, leaving the water open in the center.
RIM=[(461,331),(428,304),(632,304),(599,331)]
def rim_actor(frame,c,t):
 x,base=RIM[c]
 point_into_well(frame,c,x,t,base=base)

def approach_rim(frame,c,start,u,delay=0):
 elapsed=u-delay
 side=380 if c in (0,1) else 690
 if elapsed<2.3:
  run(frame,c,start,side,elapsed*3.5/2.3)
 else:
  p=art.ease((elapsed-2.3)/1.2)
  x,base=RIM[c]
  # Hop onto the masonry. Contact settles on the rim, never on the water.
  point_into_well(frame,c,side+(x-side)*p,u,base=371+(base-371)*p,hop=16*math.sin(math.pi*p))


def run(frame,c,start,end,u,delay=0):
 p=art.ease((u-delay)/3.5);x=start+(end-start)*p
 moving=0<p<1;hop=abs(math.sin((u-delay)*7))*13 if moving else 0
 if p>=.5 and abs(end-530)<330:point_into_well(frame,c,x,u,hop=hop)
 else:actor(frame,c,x,u,hop=hop,lean=8*math.sin(u*7) if moving else 2*math.sin(u*2))

def hanging(frame,u,count=4,lower=1,lookup=False,scoop=False):
 # Four feet-to-hand contacts follow the same articulated chain as it sways.
 x=530;y=95
 order=[3,1,2,0]
 for k,c in enumerate(order[:count]):
  height=[52,52,52,61][k]*lower
  angle=(3 if k<3 else 7)*math.sin(u*1.7+k*.2)
  if lookup and k==0:angle=-10+3*math.sin(u)
  if scoop and k==3:height+=4*math.sin(u*3)
  original=art.poses[1][c]
  if scoop and k==3:
   changed=Image.new('RGBA',original.size)
   pivot=round(original.height*.74)
   changed.alpha_composite(original.crop((0,0,original.width,pivot)),(0,0))
   for row in range(pivot,original.height):
    delta=round(7*math.sin(u*3)*(row-pivot)/(original.height-pivot))
    changed.alpha_composite(original.crop((0,row,original.width,row+1)),(delta,row))
   art.poses[1][c]=changed
  x,y=art.sprite(frame,c,1,x,y,height,angle,anchor=art.feet_contacts[c],end=art.hand_contacts[c])
  art.poses[1][c]=original
 if scoop:
  dd=ImageDraw.Draw(frame)
  # Droplets leave the dipping hands and fall back into the well.
  for j in range(5):
   p=(u*.9+j*.2)%1
   dx=x+(j-2)*5+math.sin(u*3)*4;dy=313-23*math.sin(math.pi*p)
   dd.ellipse((dx,dy,dx+2,dy+4),fill=(172,214,222))
 return x,y

def render(t):
 scene=min(8,int(t//10));u=t%10
 frame=Image.new('RGBA',(W,H),(7,18,31));frame.alpha_composite(background)
 reflection(frame,t,scene==6 and (u%4)<2.8)
 # Tiny drifting fireflies provide forest life independently of the acting.
 dd=ImageDraw.Draw(frame)
 for j in range(9):
  x=90+j*98+8*math.sin(t*.5+j);y=200+30*math.sin(t*.4+j*2)
  dd.ellipse((x,y,x+2,y+2),fill=(194,210,130,140))
 if scene==0:
  approach_rim(frame,0,165,u)
 elif scene==1:
  if u<5:
   p=art.ease(u/1.2);x,base=RIM[0]
   actor(frame,0,x+(120-x)*art.ease(u/3.5),t,base=base+(371-base)*p,hop=10*math.sin(math.pi*p))
  else:
   approach_rim(frame,1,100,u-5)
   approach_rim(frame,0,180,u-5,delay=.5)
 elif scene==2:
  rim_actor(frame,1,t);rim_actor(frame,0,t)
  approach_rim(frame,3,950,u)
  approach_rim(frame,2,1000,u,delay=3)
 elif scene==3:
  # Draw rear rim monkeys before the front pair for clear depth.
  for c in [1,2,0,3]:
   x,base=RIM[c]
   if u<5:rim_actor(frame,c,t)
   else:
    p=art.ease((u-5-c*.3)/3.6)
    if p<.35:
     q=p/.35
     actor(frame,c,x+(130-x)*q,t,base=base+(371-base)*min(1,q*3),hop=8*math.sin(math.pi*min(1,q*3)))
    elif p<.7:
     q=(p-.35)/.35;art.sprite(frame,c,0,130-35*q,371-276*q,85,8*math.sin(u*5))
    else:
     q=(p-.7)/.3;art.sprite(frame,c,0,95+(220+c*80-95)*q,95,85,3*math.sin(u*3))
  if u>5:
   dd=ImageDraw.Draw(frame);dd.arc((460,80,560,160),185,280,fill=(226,205,144),width=2)
 elif scene==4:
  if u<3:
   art.sprite(frame,3,0,460+70*art.ease(u/3),95,85,3*math.sin(u*3))
   for c,x in enumerate([230,330,420]):art.sprite(frame,c,0,x,95,80,3*math.sin(u*2+c))
  else:
   count=min(4,1+int((u-3)//1.8));hanging(frame,u,count,.85)
   for k,c in enumerate([1,2,0]):
    if k>=count-1:
     p=art.ease((u-3-k*1.8)/1.8)
     art.sprite(frame,c,0,250+k*80+(520-250-k*80)*p,95,80,3*math.sin(u*3))
 elif scene==5:
  hanging(frame,u,4,.85+.15*art.ease(u/5))
 elif scene==6:
  hanging(frame,u,4,1,scoop=True)
 elif scene==7:
  hanging(frame,u,4,1,lookup=True)
  dd=ImageDraw.Draw(frame)
  if u>3:
   r=36+3*math.sin(u*2);dd.ellipse((797-r,55-r,797+r,55+r),outline=(229,218,153),width=2)
 elif scene==8:
  if u<4:
   # Lift the chain back, one actor releasing onto the branch at a time.
   count=max(1,4-int(u));hanging(frame,u,count,.9)
   for k,c in enumerate([0,2,1]):
    if u>k+1:art.sprite(frame,c,0,260+k*95,96,72,3*math.sin(u*3))
  else:
   for c,x in enumerate([350,250,785,690]):
    p=art.ease((u-4-c*.25)/2)
    base=100+271*p;hop=12*abs(math.sin(u*3+c)) if p==1 else 0
    actor(frame,c,260+c*90+(x-260-c*90)*p,u,pose=2 if p==1 else 0,base=base,hop=hop,lean=6*math.sin(u*3+c))
 frame.alpha_composite(lip)
 if scene in (5,6):
  close=frame.crop((230,78,830,324)).resize((W,394),Image.Resampling.LANCZOS)
  frame.paste(close,(0,0))
 panel=Image.new('RGBA',(W,H));dd=ImageDraw.Draw(panel)
 dd.rectangle((0,394,W,H),fill=(3,13,24))
 dd.text((28,407),f'{scene+1:02d} / 09',font=art.small,fill=(234,198,122))
 dd.text((480,449),chinese[scene][int(u>=5)],font=art.zhfont,anchor='mm',fill=(234,198,122))
 for j,line in enumerate(textwrap.wrap(captions[scene][int(u>=5)],width=76)):
  dd.text((480,484+j*28),line,font=art.font,anchor='mm',fill=(250,245,231))
 return Image.alpha_composite(frame,panel).convert('RGB')

def music():
 import wave,struct,array
 source=(ROOT/'generate_video.py').read_text();start=source.index('# Original playful score:');end=source.index('subprocess.run(',start)
 score=source[start:end].replace('duration=48','duration=90').replace('duration = 48','duration = 90').replace('min(3,int(t//12))','min(3,int(t//25))').replace('46.6','88.6').replace('(48-t)','(90-t)')
 exec(score,dict(globals(),wave=wave,struct=struct,array=array))

if __name__=='__main__':
 if '--preview' in sys.argv:
  contact=Image.new('RGB',(W*2,H*5))
  for i,t in enumerate([4,8,18,28,38,48,58,68,78,88]):contact.paste(render(t),(i%2*W,i//2*H))
  contact.save('/private/tmp/moon-expanded-preview.jpg');print('/private/tmp/moon-expanded-preview.jpg');sys.exit()
 if '--reuse-music' not in sys.argv:music()
 ff=art.imageio_ffmpeg.get_ffmpeg_exe()
 p=subprocess.Popen([ff,'-y','-f','rawvideo','-pix_fmt','rgb24','-s','960x540','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(ROOT/'silent.mp4')],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
 for i in range(DURATION*FPS):
  f=render(i/FPS)
  if i==28*FPS:f.save(OUT/'expanded-poster.jpg',quality=93)
  p.stdin.write(f.tobytes())
 p.stdin.close();assert p.wait()==0
 target=OUT/'monkeys-expanded.mp4'
 subprocess.run([ff,'-y','-i',str(ROOT/'silent.mp4'),'-i',str(ROOT/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(target)],check=True,stderr=subprocess.DEVNULL)
 subprocess.run([ff,'-y','-i',str(target),'-c:v','libvpx-vp9','-b:v','0','-crf','34','-cpu-used','4','-row-mt','1','-c:a','libopus',str(OUT/'monkeys-expanded.webm')],check=True,stderr=subprocess.DEVNULL)
 print('Rendered nine-scene, 90-second well story.')
