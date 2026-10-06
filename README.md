CACC hacklab course in 2026

## 猴子捞月 — The Monkeys Try to Scoop Up the Moon

The `moon-story` folder contains a simple story website and a 48-second animated film for weekend Chinese school. The film has four distinct monkey characters, Chinese and English captions, and original playful music. The page includes the story in Simplified Chinese.

Hosted website: https://monkeys-and-the-moon.csaus-6971.chatgpt.site (access is currently private).

### View locally

From the repository directory, run:

```sh
python3 -m http.server 8000 --directory moon-story/dist
```

Open http://localhost:8000. The current film is available as `monkeys-ground.webm` and `monkeys-ground.mp4`. Previous film versions are also preserved in `dist`.

### Regenerate the animation

Use Python 3.9 or newer with Pillow and imageio-ffmpeg:

```sh
python3 -m pip install Pillow==11.3.0 imageio-ffmpeg==0.6.0
python3 moon-story/animate_story.py
```

The renderer currently uses macOS system fonts for Chinese and English captions. On another operating system, update the font paths in `animate_story.py` and `generate_video.py` to suitable installed fonts.

See `moon-story/ARTWORK.md` for the generated artwork, prompts, and revision notes. The original music is regenerated automatically when needed.
