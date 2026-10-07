"""Create a youthful synthetic Mandarin reading, aligned to the 12 picture captions."""
import ast,json,pathlib,subprocess,sys,wave,array,math
sys.path.insert(0,'/private/tmp/moon-video-libs')
import imageio_ffmpeg
ROOT=pathlib.Path(__file__).parent
OUT=ROOT/'narration';OUT.mkdir(exist_ok=True)
RAW=pathlib.Path('/private/tmp/moon-narration-raw');RAW.mkdir(exist_ok=True)
RATE=24000;SLOT=4;VOICE='Tingting';PITCH=1.20
source=ast.parse((ROOT/'generate_video.py').read_text())
lines=next(ast.literal_eval(n.value) for n in source.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='chinese')
ff=imageio_ffmpeg.get_ffmpeg_exe()
timeline=array.array('h',[0])*(RATE*SLOT*len(lines));records=[]
for j,line in enumerate(lines):
 text=line.replace('“','').replace('”','')
 raw=RAW/f'{j+1:02d}.aiff';pcm=RAW/f'{j+1:02d}.wav';target=OUT/f'{j+1:02d}.wav'
 # The macOS speech service needs access outside the process sandbox.
 subprocess.run(['/usr/bin/say','-v',VOICE,'-r','220','-o',str(raw),text],check=True)
 subprocess.run([ff,'-y','-i',str(raw),'-ar',str(RATE),'-ac','1',str(pcm)],check=True,stderr=subprocess.DEVNULL)
 with wave.open(str(pcm)) as f:
  seconds=f.getnframes()/f.getframerate()
 assert seconds>.5, f'No speech produced for scene {j+1}'
 speed=max(1,seconds/3.7)
 filters=f'asetrate={RATE}*{PITCH},aresample={RATE},atempo={speed/PITCH},highpass=f=100,lowpass=f=9000,loudnorm=I=-17:TP=-2:LRA=7,aresample={RATE},afade=t=in:d=0.025'
 subprocess.run([ff,'-y','-i',str(pcm),'-af',filters,'-ar',str(RATE),'-ac','1','-c:a','pcm_s16le',str(target)],check=True,stderr=subprocess.DEVNULL)
 with wave.open(str(target)) as f:clip=array.array('h',f.readframes(f.getnframes()))
 clip_seconds=len(clip)/RATE
 assert clip_seconds<3.82,(j,clip_seconds)
 start=round((j*SLOT+.12)*RATE)
 timeline[start:start+len(clip)]=clip
 records.append(dict(scene=j+1,text=text,start_seconds=j*SLOT+.12,duration_seconds=round(clip_seconds,3),speed=round(speed,3),file=target.name))
 print(f'Scene {j+1:02d}: {clip_seconds:.2f}s',flush=True)
with wave.open(str(OUT/'mandarin-reading.wav'),'wb') as f:
 f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(timeline.tobytes())
(OUT/'READING.json').write_text(json.dumps(dict(description='Synthetic childlike Mandarin narration; not a recording of a child.',voice=VOICE,pitch_ratio=PITCH,sample_rate=RATE,picture_seconds=SLOT,scenes=records),ensure_ascii=False,indent=2)+'\n')
print('Created 48-second caption-aligned Mandarin narration.')
