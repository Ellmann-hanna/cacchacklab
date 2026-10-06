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
