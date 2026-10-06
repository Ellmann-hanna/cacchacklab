"""Turn the generated four-panel artwork into a captioned, gently moving short."""
import sys, pathlib, math, wave, struct, subprocess, textwrap, array
sys.path.insert(0, '/private/tmp/moon-video-libs')
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'dist'
art = Image.open(sys.argv[1]).convert('RGB')
w,h = art.size
scenes = [art.crop((x*w//2,y*h//2,(x+1)*w//2,(y+1)*h//2)) for y in range(2) for x in range(2)]
captions = [
  ('One quiet night, a little monkey peered into a well.', '“Oh no! The moon has fallen into the well!”'),
  ('The other monkeys hurried over. “We must save it!”', 'One held a branch. The others held on to one another.'),
  ('Down, down went the chain. The smallest reached for the moon.', 'But every touch made ripples. The shining circle slipped away.'),
  ('Then an older monkey looked up. “The moon is still in the sky!”', 'They laughed. It was only a reflection. Look carefully before you act.')
]
chinese = [
 ('一个宁静的夜晚，小猴子往井里一看。', '“不好啦！月亮掉到井里了！”'),
 ('猴子们赶来，喊道：“我们要救月亮！”', '一只抓住树枝，其他猴子一个接一个拉住。'),
 ('猴子们连成一串，小猴子伸手去捞月亮。', '水面泛起涟漪，圆圆的月亮散开了。'),
 ('老猴子抬头一看：“月亮还在天上呢！”', '原来只是倒影！做事之前，要仔细观察。')
]
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
zhfont = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',28)
small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
ff = imageio_ffmpeg.get_ffmpeg_exe()
cmd=[ff,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','960x540','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p',str(ROOT/'silent.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
for i in range(48*24):
    scene = i//(12*24)
    t = (i%(12*24))/(12*24)
    scale=1+.06*t
    base=ImageOps.fit(scenes[scene],(int(960*scale),int(540*scale)),method=Image.Resampling.LANCZOS)
    dx=(base.width-960)//2;dy=(base.height-540)//2
    frame=base.crop((dx,dy,dx+960,dy+540))
    overlay=Image.new('RGBA',frame.size)
    d=ImageDraw.Draw(overlay)
    d.rectangle((0,394,960,540),fill=(3,13,24,220))
    d.text((28,407),f'{scene+1:02d} / 04',font=small,fill=(234,198,122,255))
    d.text((480,449),chinese[scene][int(t>=.5)],font=zhfont,anchor='mm',fill=(234,198,122,255))
    lines=textwrap.wrap(captions[scene][int(t>=.5)],width=76)
    for j,line in enumerate(lines):
        d.text((480,484+j*28),line,font=font,anchor='mm',fill=(250,245,231,255))
    frame=Image.alpha_composite(frame.convert('RGBA'),overlay).convert('RGB')
    if i==0: frame.save(OUT/'poster.jpg',quality=92)
    p.stdin.write(frame.tobytes())
p.stdin.close()
assert p.wait()==0
# Original playful score: pentatonic plucks, sparkling bells, and a soft pulse.
rate=22050
duration=48
mix=array.array('d',[0.0])*(rate*duration)
beat=60/110
def tone(start,midi,length,gain,kind):
    freq=440*2**((midi-69)/12)
    offset=int(start*rate)
    for n in range(min(int(length*rate),len(mix)-offset)):
        t=n/rate
        if kind=='pluck':
            envelope=min(t/.008,1)*math.exp(-t/0.24)
            signal=math.sin(2*math.pi*freq*t)+.32*math.sin(2*math.pi*freq*2*t)+.14*math.sin(2*math.pi*freq*3*t)
        elif kind=='bell':
            envelope=min(t/.006,1)*math.exp(-t/.6)
            signal=math.sin(2*math.pi*freq*t)+.18*math.sin(2*math.pi*freq*2.76*t)
        else:
            envelope=min(t/.025,1)*math.exp(-t/.18)
            signal=math.sin(2*math.pi*freq*t)
        mix[offset+n]+=gain*envelope*signal
# Rising questions and falling answers. Four phrases follow the story scenes.
phrases=[
 [72,76,79,81,79,76,74,79,76,72,74,76,79,81,84,79],
 [72,76,79,76,74,79,81,79,76,79,84,81,79,76,74,72],
 [76,79,81,84,81,79,76,79,81,84,86,84,81,79,76,74],
 [84,81,79,76,79,76,74,72,76,79,81,79,76,74,72,72]]
for k in range(int(duration/beat)):
    t=k*beat
    scene=min(3,int(t//12))
    midi=phrases[scene][k%16]
    tone(t,midi,.9,.13,'pluck')
    if k%4==2: tone(t+beat/2,midi+12,1.5,.035,'bell')
    if k%2==0: tone(t,48 if k%4==0 else 55,.6,.08,'bass')
    # Light offbeat answering notes make the melody bounce.
    if k%4==1: tone(t+beat/2,midi+7,.6,.045,'pluck')
tone(46.6,72,1.4,.10,'bell');tone(46.6,76,1.4,.06,'bell');tone(46.6,79,1.4,.05,'bell')
with wave.open(str(ROOT/'music.wav'),'wb') as f:
    f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
    buf=bytearray()
    for n,v in enumerate(mix):
        t=n/rate
        v*=max(0,min(t/.5,1,(48-t)/1.5))
        buf.extend(struct.pack('<h',int(math.tanh(v)*32767)))
    f.writeframes(buf)
subprocess.run([ff,'-y','-i',str(ROOT/'silent.mp4'),'-i',str(ROOT/'music.wav'),'-c:v','copy','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',str(OUT/'monkeys-and-the-moon.mp4')],check=True,stderr=subprocess.DEVNULL)
print('Created 48-second captioned MP4 with original music:',OUT/'monkeys-and-the-moon.mp4')
