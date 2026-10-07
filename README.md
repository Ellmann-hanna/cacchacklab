CACC hacklab course in 2026

## 猴子捞月 — The Monkeys Try to Scoop Up the Moon

The `moon-story` folder contains a story website for weekend Chinese school. Its current 48-second storybook film has 12 illustrations, changing every four seconds, with synthetic childlike Mandarin narration, soft background music, and compact Chinese and English captions below the pictures. The page includes the story in Simplified Chinese.

[Visit the public website](https://monkeys-and-the-moon.csaus-6971.chatgpt.site). No ChatGPT login is required.

### View locally

From the repository directory, run:

```sh
python3 -m http.server 8000 --directory moon-story/dist
```

Open http://localhost:8000. The current film is `monkeys-narrated.webm`, with `monkeys-narrated.mp4` as a fallback. Previous film versions are preserved in `dist`.

### Regenerate the current film

Use Python 3.9 or newer with Pillow and imageio-ffmpeg:

```sh
python3 -m pip install Pillow==11.3.0 imageio-ffmpeg==0.6.0
python3 moon-story/generate_video.py moon-story/storyboard.png
```

This uses the saved narration clips, generates the original music, renders the illustrations and captions, and mixes the voice over a quiet music bed that becomes softer during speech.

The renderer uses macOS system fonts. On another operating system, update the font paths in `generate_video.py` to suitable installed fonts. To regenerate the synthetic Mandarin voice on macOS, run `python3 moon-story/generate_narration.py` before rendering the film. The narration is generated speech, not a recording of a child.

See `moon-story/ARTWORK.md` for artwork paths, generation prompts, and revision notes; `moon-story/narration/READING.json` records the spoken words and timing. The twelve-picture reading uses the original storybook style; earlier 2D animation scripts are retained for reference.
