"""Render twelve caption-matched storybook images with compact subtitles."""
import sys, pathlib, math, wave, struct, subprocess, textwrap, array
sys.path.insert(0, '/private/tmp/moon-video-libs')
from PIL import Image, ImageDraw, ImageFont, ImageOps
import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / 'dist'
art = Image.open(sys.argv[1]).convert('RGB')
w,h = art.size
original = [art.crop((x*w//2,y*h//2,(x+1)*w//2,(y+1)*h//2)) for y in range(2) for x in range(2)]
new_images=ROOT/'story-images'
def picture(name):return Image.open(new_images/name).convert('RGB')
scenes=[original[0],picture('02-alarm.png'),picture('03-calling-troop.png'),
        original[1],picture('05-rescue-plan.png'),picture('04-chain-plan.png'),
        picture('07-lowering-chain.png'),original[2],picture('06-failed-scoop.png'),
        picture('10-elder-discovers-moon.png'),original[3],picture('08-realization.png')]
SECONDS_PER_PICTURE=4
duration=len(scenes)*SECONDS_PER_PICTURE
captions = [
 'One quiet night, a little monkey peered into a well.',
 '“Oh no! The moon has fallen into the well!”',
 'It called into the forest. The other monkeys hurried over.',
 'They gathered at the well and wanted to rescue the moon.',
 'The elder spotted a sturdy branch stretching over the well.',
 'One held the branch. The others joined, holding on tightly.',
 'Their long chain slowly reached farther down into the well.',
 'At the bottom, the smallest monkey reached for the moon.',
 'It caught only water. Ripples broke the shining reflection.',
 'The elder looked up and suddenly spotted the real moon.',
 'The others followed its gaze. The moon was still in the sky!',
 'They laughed: the moon in the well was only a reflection.'
]
chinese = [
 '一个宁静的夜晚，小猴子往井里一看。',
 '“不好啦！月亮掉到井里了！”',
 '小猴子大声呼喊，其他猴子急忙赶来。',
 '大家围在井沿上，都想把月亮救出来。',
 '老猴子发现，一根树枝正好伸在井口上方。',
 '一只抓住树枝，其他猴子一个接一个拉住。',
 '长长的猴子链，慢慢地向井水伸去。',
 '最下面的小猴子，伸出双手去捞月亮。',
 '手里只有水，水波把月亮的倒影打散了。',
 '老猴子抬头一看，发现月亮还在天上。',
 '大家跟着抬头看，天上的月亮好好的！',
 '猴子们笑了：井里的月亮原来只是倒影。'
]
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
zhfont = ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',22)
small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
ff = imageio_ffmpeg.get_ffmpeg_exe()
def render_frame(i):
    scene = i//(SECONDS_PER_PICTURE*24)
    t = (i%(SECONDS_PER_PICTURE*24))/(SECONDS_PER_PICTURE*24)
    scale=1+.06*t
    base=ImageOps.fit(scenes[scene],(int(960*scale),int(540*scale)),method=Image.Resampling.LANCZOS)
    dx=(base.width-960)//2;dy=(base.height-540)//2
    picture=base.crop((dx,dy,dx+960,dy+540))
    # Keep the entire illustrated scene visible; subtitles occupy their own slim footer.
    frame=Image.new('RGB',(960,606),(3,13,24))
    frame.paste(picture,(0,0))
    d=ImageDraw.Draw(frame)
    d.text((480,562),chinese[scene],font=zhfont,anchor='mm',fill=(234,198,122))
    d.text((480,590),captions[scene],font=font,anchor='mm',fill=(250,245,231))
    return frame

if '--preview' in sys.argv:
    contact=Image.new('RGB',(1920,3636))
    for j,i in enumerate([int((j*SECONDS_PER_PICTURE+2)*24) for j in range(12)]):contact.paste(render_frame(i),(j%2*960,j//2*606))
    contact.save('/private/tmp/compact-captions-preview.jpg')
    print('/private/tmp/compact-captions-preview.jpg')
    sys.exit()
cmd=[ff,'-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s','960x606','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p',str(ROOT/'silent.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
for i in range(duration*24):
    frame=render_frame(i)
    if i==0:frame.save(OUT/'poster.jpg',quality=92)
    p.stdin.write(frame.tobytes())
p.stdin.close()
assert p.wait()==0
# Original playful score: pentatonic plucks, sparkling bells, and a soft pulse.
rate=22050
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
    scene=min(3,int(t//(duration/4)))
    midi=phrases[scene][k%16]
    tone(t,midi,.9,.13,'pluck')
    if k%4==2: tone(t+beat/2,midi+12,1.5,.035,'bell')
    if k%2==0: tone(t,48 if k%4==0 else 55,.6,.08,'bass')
    # Light offbeat answering notes make the melody bounce.
    if k%4==1: tone(t+beat/2,midi+7,.6,.045,'pluck')
tone(duration-1.4,72,1.4,.10,'bell');tone(duration-1.4,76,1.4,.06,'bell');tone(duration-1.4,79,1.4,.05,'bell')
with wave.open(str(ROOT/'music.wav'),'wb') as f:
    f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate)
    buf=bytearray()
    for n,v in enumerate(mix):
        t=n/rate
        v*=max(0,min(t/.5,1,(duration-t)/1.5))
        buf.extend(struct.pack('<h',int(math.tanh(v)*32767)))
    f.writeframes(buf)
from mix_story_audio import mix_film
mix_film(ROOT/'silent.mp4')
print('Created 48-second storybook film with Mandarin narration and 12 illustrations:',OUT/'monkeys-narrated.mp4')
