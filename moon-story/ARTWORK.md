# Story artwork

Built-in imagegen produced `storyboard.png`, used to create `dist/poster.jpg` and `dist/monkeys-and-the-moon.mp4`.

Prompt: One borderless 2×2 storyboard for the Chinese fable The Monkeys Try to Scoop Up the Moon (猴子捞月), consistent adorable brown monkeys, textured Chinese children’s-book illustration, midnight blue, jade foliage, golden moon. Four scenes: little monkey discovers moon reflected in stone well; troop gathers to rescue it; monkeys form a chain from tree into well and reach at rippling reflection; monkeys look joyfully up at real moon. No text or gutters.

Video: 48 seconds, subtle camera movement, Chinese and English captions, original playful pentatonic melody with plucked notes, bell tones, rising question phrases, and a gentle bass pulse.

## Animated edition

The site now plays a 48-second 2D puppet animation with independent limb rotation, walking and bouncing movements, a descending swinging chain, reaching hands, and rippling reflected moonlight. Exported as `dist/monkeys-animated.webm` and `dist/monkeys-animated.mp4`, using the existing playful music and bilingual captions. Renderer: `animate_story.py`.

Two new assets were made with built-in imagegen and saved as `animation-assets/background.png` and `animation-assets/puppet.png`.

Background prompt: Landscape storybook background for 猴子捞月, textured navy-blue and jade watercolor paper-cut garden at night, thick tree trunk left with branch reaching toward upper center, full golden moon upper right, large stone well lower center with visible dark oval water surface near 60% x and 72% y, foreground ground, no monkeys or text.

Puppet prompt: Transparent 3×2 rig sheet with six isolated parts in equal cells: cute brown monkey head and torso with tan face and belly and tail, no arms or legs; a furry arm with shoulder left and tan hand right; mirrored arm; paired short legs and tan feet; elderly monkey head and torso with white brows and tuft, no limbs; a round golden full moon. Matching flat textured 2D storybook style, blank cell margins, no labels or gutters.

## Distinct, softer characters

The updated film uses four unique monkey rigs saved in `animation-assets/puppet-variety.png`, generated with built-in imagegen using `storyboard.png` as the appearance reference and the previous rig only as a layout reference. The original files are preserved.

Prompt: Transparent square atlas with four columns and four rows. Each column is a distinct, adorable natural fluffy monkey: tiny honey-gold baby with oversized ears, round curious dark eyes and small closed smile; plump chestnut mother with cream heart-shaped face, rosy cheeks and gentle smile; slimmer reddish youngster with tousled tuft, mischievous grin and narrower eyes; warm gray-brown elder with white eyebrows, rounded cheeks and gentle squinting smile. Match the softness and cuteness of the original storybook reference. Different silhouettes, faces and proportions, no clothes or ornamental markings. Rows contain head/torso/tail without limbs, isolated right arm, mirrored left arm, and paired legs/feet. Equal cells with transparent margins, no overlap, text or gutters.

Exports: `dist/monkeys-variety.webm`, `dist/monkeys-variety.mp4`, and `dist/animated-poster-variety.jpg`.

## Ground placement correction

Standing monkeys now gather on dry ground to the left and right of the well, with feet aligned to the ground and contact shadows. The baby approaches from the side without climbing onto the rim. During the hanging sequence, the bodies stay above the water; only the lowest monkey's reaching hand descends into the water. Ripple motion stays within the water surface. Current exports: `dist/monkeys-ground.webm`, `dist/monkeys-ground.mp4`, and `dist/animated-poster-ground.jpg`.

## User reference: Chinese ink-and-watercolor comic

The user supplied a four-panel 猴子捞月 comic and requested that design for the animation. The new edition uses slender brown monkeys with long tails, hand-drawn dark ink outlines, blue watercolor mountains, pine branches and a pond. It preserves distinct identities, Chinese/English captions and the original music. Non-hanging monkeys sit on branches or the dry pond banks. The written story now follows the pond variant shown in the reference.

Built-in imagegen created `animation-assets/pond-background.png` and `animation-assets/comic-monkeys.png` using the attached screenshot as a reference. Original artwork and previous films are preserved. Renderer: `animate_reference.py`. Exports: `dist/monkeys-comic.webm`, `dist/monkeys-comic.mp4` and `dist/comic-poster.jpg`.

Background prompt: A single wide 2.4:1 landscape matching the reference's traditional Chinese children's-comic ink-and-watercolor style. Pine trunk far left, strong horizontal branch across the upper quarter, empty space below for a monkey chain, blue pond lower center, dry grassy banks on either side, blue mountain silhouettes, green shrubs, pale full moon upper right. No characters, text, bubbles or panel borders; animated reflection added separately.

Character prompt: A transparent four-column by three-row full-body sprite atlas, ink outlines and flat watercolor matching the screenshot. Four distinct slender natural monkeys: small golden-brown child, broad medium-brown adult, lean reddish youngster, gray-brown elder. Rows: crouching on a branch facing right and reaching down; upside-down hanging with feet at top, head below hips and long arms reaching below head, hands at bottom; seated on the bank looking and pointing up. Complete tails and limbs, no plush/chibi treatment, costumes, overlap, text or cell borders.


## Expanded well story (90 seconds, nine scenes)

The uploaded comic is a visual reference only. Its speech bubbles are not used. All Chinese and English captions and the seven-paragraph Chinese reading passage were independently written for this adaptation of the familiar well story.

`animate_expanded.py` reuses the generated watercolor forest and four distinct monkey identities. It adds a stone well and dry ground in code, progressive climbing and chain assembly, forearm dipping, droplets, changing ripples, a closer scooping shot, the discovery of the sky moon, and the return to the ground. The oldest monkey leads the chain; the smallest reaches the well water.

The original pentatonic pluck-and-bell music is extended to 90 seconds with a concluding cadence. Outputs: `dist/monkeys-expanded.webm`, MP4 fallback, and `expanded-poster.jpg`. Re-render with `/usr/bin/python3 animate_expanded.py` after installing the renderer dependencies.


## Pointing correction

The ground-level discovery and planning poses pivot the original illustrated pointing arm toward the well reflection at (530, 311). Monkeys to the right of the well are mirrored to face inward. The arm uses the existing watercolor artwork; the feet remain on dry ground. Approaching monkeys adopt the aimed pose as they arrive.


## Well-rim staging

Discovery and discussion actors now hop onto four stone-rim contact points: (461,331), (428,304), (632,304), (599,331). The supporting paws are anchored using the visible body alpha, rather than the tail-inclusive sprite center. Left and right actors face inward with arms aimed at the reflected moon (530,311). The troop climbs down from the rim before heading into the tree. The poster shows the troop inspecting the well from the rim.


## Restored storybook presentation

At the user's request, the player now uses the original 48-second illustrated storybook film and its original poster, replacing the 2D puppet presentation. Chinese reading content and public access are retained, and the removed English lesson block stays removed. A WebM copy of the original film is provided alongside its MP4 fallback.


## Compact captions

The storybook renderer now preserves the full 960×540 illustration and places captions below it in a separate 66-pixel footer (output 960×606). Chinese type is reduced from 28 to 22 pixels and English from 22 to 16 pixels. The scene counter is removed from the subtitle area. The website player follows the new aspect ratio.


## One picture per caption

The storybook film now has eight distinct pictures, changing every six seconds alongside the eight existing Chinese/English caption pairs. Four original storyboard panels alternate with four new built-in image_gen illustrations saved to:

- `story-images/02-alarm.png`: little monkey gasps and points into the well.
- `story-images/04-chain-plan.png`: troop assembles its hanging rescue chain.
- `story-images/06-failed-scoop.png`: dripping cupped hands and broken moonlight in ripples.
- `story-images/08-realization.png`: monkeys laugh beside the smooth reflection, with the real moon also visible above.

`story-images/PROMPTS.json` contains the exact final prompts and reference information. The original fluffy storybook style, 48-second duration, compact subtitle footer and playful music are preserved.


## Twelve story illustrations

The film is expanded to twelve pictures and twelve matching Chinese/English captions. Each picture stays on screen for six seconds, for a total of 72 seconds; the original playful music is extended with the same four musical phrases and a closing cadence. The compact 66-pixel caption footer remains below the scene.

Four additional illustrations were made with built-in image_gen using `storyboard.png` as the style and character reference, and are saved as:

- `story-images/03-calling-troop.png`: the little monkey calls while the troop approaches.
- `story-images/05-rescue-plan.png`: the elder identifies the branch above the well.
- `story-images/07-lowering-chain.png`: the chain descends toward the reflected moon.
- `story-images/10-elder-discovers-moon.png`: the hanging elder discovers the true moon in the sky.

The exact additional prompts are recorded in `story-images/PROMPTS-12.json`. All eight previous illustrations are retained in the film.


## Faster story pacing

Each of the twelve story illustrations now stays on screen for four seconds, reducing the full film from 72 to 48 seconds. Matching captions switch with each picture. The original musical score follows the shorter duration with its closing cadence and fade. Artwork and the compact caption footer are preserved.


## Mandarin reading with background music

The current player uses `dist/monkeys-narrated.webm` and its MP4 fallback. A synthetic childlike Mandarin voice reads all twelve Chinese captions, one line per four-second illustration. This is generated speech, not a recording of a child. The page identifies it as 合成语音.

`generate_narration.py` creates the reading with macOS Tingting at 220 words/minute, a gentle 1.20 pitch ratio, per-line timing adjustment where needed, and voice loudness normalization. The twelve source clips and the complete 48-second timeline are saved in `narration/`, with exact words, timing, and voice settings recorded in `narration/READING.json`.

`mix_story_audio.py` reduces the original playful music to 14% amplitude and ducks it further during speech, placing the narration in front. The original music-only film is preserved. The twelve illustrations, four-second pacing, and compact subtitles are retained.
