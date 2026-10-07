"""Place synthetic Mandarin narration in front of a quiet, ducked music bed."""
import pathlib,subprocess,sys
sys.path.insert(0,'/private/tmp/moon-video-libs')
import imageio_ffmpeg
ROOT=pathlib.Path(__file__).parent

def mix_film(video):
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 voice=ROOT/'narration/mandarin-reading.wav'
 assert voice.exists(),'Generate the Mandarin narration first.'
 target=ROOT/'dist/monkeys-narrated.mp4'
 # Music begins 17 dB lower, and ducks further whenever the voice is active.
 filters='[1:a]volume=0.14,aresample=24000[bed];[2:a]asplit=2[voice][detector];[bed][detector]sidechaincompress=threshold=0.015:ratio=4:attack=15:release=250:makeup=1[ducked];[voice][ducked]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.9:level=false[mix]'
 subprocess.run([ff,'-y','-i',str(video),'-i',str(ROOT/'music.wav'),'-i',str(voice),'-filter_complex',filters,'-map','0:v:0','-map','[mix]','-c:v','copy','-c:a','aac','-b:a','128k','-shortest','-movflags','+faststart',str(target)],check=True,stderr=subprocess.DEVNULL)
 subprocess.run([ff,'-y','-i',str(target),'-c:v','libvpx-vp9','-b:v','0','-crf','34','-cpu-used','4','-row-mt','1','-c:a','libopus',str(ROOT/'dist/monkeys-narrated.webm')],check=True,stderr=subprocess.DEVNULL)
 print('Rendered narration with soft, ducked background music.')
if __name__=='__main__':mix_film(pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'dist/monkeys-and-the-moon.mp4')
