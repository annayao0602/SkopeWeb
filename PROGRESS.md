# Progress

## 2026-10-19: Scenic first screen, swipe carousel, section snapping and reveal animations

### First section (`.intro`)

- **Fits on one screen.** The nav now floats over the first section (`.nav` is `position:absolute`), and `.intro` is exactly one screen tall (`min-height:100svh`). The pillar's height scales with the screen: `clamp(200px, 100svh − 380px, 430px)` on desktop and `clamp(170px, 100svh − 400px, 460px)` at ≤650px. It sits at the bottom of the section and fades out into the mist.
- **Mountains, clouds and moon.** `dist/assets/hero-scene.svg` (6 KB) fills the section behind the text:
  - two hazy layers of jagged mountain peaks, taller at the sides so they stay clear of the headline;
  - soft blurred cloud bands;
  - two rows of rounded mist hills;
  - a fade at the bottom into the page color, so the first section blends into How it works with no edge.

  The moon is a CSS circle with a soft glow (`.moon`). It sits right of the headline on desktop and beside the pillar on phones. The SVG is made by `tools/make-hero-scene.py`: edit the peak lists or colors there, then run `python3 tools/make-hero-scene.py dist/assets/hero-scene.svg`. Its random seed is fixed, so the same settings always produce the same image.
- **Pillar** is slightly brighter (`filter: brightness(1.2)`).
- **Subtitle** is now 24px (21px on phones), the same size as the main body text (the "Why we founded Skope" paragraph), and max 490px wide.
- **Contrast fix.** On the lighter background, the old accent color for "today?" and the subtitle was too faint (about 2.5:1). Both now use a lighter lavender, `#cfd6f5`, for about 3:1. This applies only in the first section; `--accent` is unchanged elsewhere.
- **Removed the divider line** under the pillar (`.how` no longer has a top border).

### Background

- Lighter, duller purple, still a top-to-bottom gradient: `#7a7693` at the top → `#64607e` halfway down the first screen → `--bg` (`#2a2840`, was `#1a1a3a`) at the bottom of the first screen, then solid.

### How it works (`.how`)

- **Heading lines up with "Meet the creators" and "FAQ":** same 46px size (35px on phones), the same 85px/36px padding (60px/5px on phones), left-aligned at the top of the section. The step text and carousel sit in a row below it (stacked at ≤750px).
- **Step text** is 24px (21px on phones), matching the main body text.
- The section is at least one screen tall. The carousel shrinks on shorter screens so it fits.
- **Swipe animation:** the images slide instead of crossfading (0.6s).
  - "Next" moves the current image out to the left while the next one slides in from the right, including when wrapping from step 3 back to step 1.
  - "Previous" slides the other way. Clicking a dot slides in whichever direction leads to that step.
  - The carousel can also be swiped by touch or mouse drag (more than 40px sideways).

### Scroll snapping

- `html{scroll-snap-type:y mandatory}`. The first section, How it works, Meet the creators and FAQ snap to the top of the screen (`scroll-snap-align:start`), and the footer snaps to the bottom.
- Sections taller than the screen (Meet the creators and FAQ on most screens) can still be scrolled freely inside, and snapping takes over near their edges, so long content is never trapped.
- Removed `scroll-padding-top`, so sections snap flush to the top.

### Fade-up animations

- The first section's headline, subtitle and pillar, and every direct child of How it works, Meet the creators and FAQ (heading, content blocks), fade in and slide up 60px over 0.9s as they scroll into view. Elements in the same section are staggered 120ms apart.
- The children animate rather than the sections themselves, so the snap positions don't shift during the animation.
- Still turned off for visitors with "reduce motion" enabled.

### Verified (headless Chrome)

- **First screen fits** at 1280×800 and phone width.
- **Snapping:**
  - Scrolling 150px past or 200px short of How it works settles exactly on its top.
  - Scrolling inside Meet the creators and the FAQ stays where it's put.
- **Carousel transforms:** checked after next/next/next (wrap)/prev (wrap)/dot clicks; the slide directions and text are correct each time.
- **Headings:** "How it works" and "Meet the creators" have the same left edge.

## 2026-10-19: New template for the first two sections and nav

The hero ("Make progress, one step at a time" with the character and waitlist form) and the mission section ("Starting is one thing…") are replaced by the new design: an intro with a pillar, then a How it works carousel. Meet the creators, the FAQ, and the footer are unchanged (markup and styles).

> **Placeholder link:** "join our waitlist" opens `https://docs.google.com/spreadsheets/create` in a new tab, which creates a new blank sheet in the visitor's own Google account. Replace it in `dist/index.html` (the last link in the `<nav>`) with your real sheet or form URL before launch.

### Nav (`dist/index.html` line 4, `dist/style.css`)

- Links: **how it works** (→ `#how`), **about the creators** (was "meet the creators", → `#creators`), **FAQ** (→ `#faq`), **join our waitlist** (new; opens in a new tab with `rel="noopener"`).
- The bordered pill around "how it works" is removed (`.nav-pill` CSS deleted).
- Bigger to match the mockup: brand 50px → 62px, links 17px → 24px with 70px gaps, 47px top padding. At ≤1000px the links are 18px with 32px gaps; at ≤650px the link group can be up to 230px wide (was 200px) so the four links wrap neatly.

### Background

- `--bg` is now `#1a1a3a`. The body background fades from `#696999` at the top of the page to `#1a1a3a` at 860px, then stays solid `#1a1a3a` (colors sampled from the mockup). Previously the gradient stretched over the whole page height.

### Intro section (`.intro`)

- Centered headline "Where do you want to go <span>today?</span>". "today?" is in the accent color. `h1` is now `clamp(44px, 5.15vw, 66px)`, 52px at ≤1000px, `clamp(32px, 8.6vw, 44px)` at ≤650px.
- Subtitle "Meet Skope, the app that turns your goals into a journey." in the accent color, 32px, max 600px wide so it wraps after "into" like the mockup.
- `assets/pillar.webp`: `pillar.png` cropped to the pillar (the empty space above it removed) and halved to 342×859. It shows at 171px wide (120px at ≤650px) and fades out over its bottom ~22% with a CSS mask. It hangs 53px below the divider line (37px on phones) so the line crosses in front of it, as in the mockup.

### How it works section (`.how`, `id="how"`)

- Has the 1px divider line on top. Two columns: the "How it works" heading and step text on the left, the carousel on the right. Stacks on one column at ≤750px, with text centered above the carousel.
- Carousel order and text:
  1. `step-start.webp`: "Make a goal. We'll help you."
  2. `step-goal-created.webp`: "Submit evidence of completing the goal. We'll verify it for you."
  3. `step-celebrate.webp`: "See your progress in real time. We'll celebrate with you."
- The left/right chevron buttons move one step, wrapping from the last image back to the first and vice versa. The dots under the image show the current step (a wide pill) and can also be clicked. Images crossfade over 0.45s. The step text lives in each image's `data-caption`, and the text box is `aria-live="polite"`, so screen readers announce it when it changes.
- Images use a 570:534 frame (the mockup's shape), with 19px rounded corners and `object-fit: cover`. The source images have slightly different shapes, so a few pixels are trimmed at the sides.
- Image files: the three PNGs resized to 1140px wide (2× the 570px display width) and saved as WebP (`cwebp -q 94 -m 6 -sharp_yuv -resize 1140 0`), about 30 KB each instead of about 0.9 MB. A lower quality setting (q82) visibly blurred the brush texture, so q94 is used.

### Removed

- The hero waitlist form (markup, styles, and script) and the animated character from the page, including the character sprite and blink styles.
- The old hero, mission, stat, and `.button` CSS, cleaned out by exact selector.
- Removed "main .button" from the scroll-reveal selector, since that button no longer exists.

### Not used on the page (still in `dist/assets/`)

`character-idle.webp` (blinking character sprite sheet), `characters.PNG`, `app-icon.png`, and the original `start.PNG`, `goalcreated.png`, `celebrate.png`, `pillar.png`. They're kept for reference and can be deleted.

### Verified

Checked in headless Chrome at 1280px (side by side with the mockup), 1000px, and phone width. Clicking "next" steps through the images in order and wraps back to the first, with the text and dots updating each time. The creators, FAQ, and footer markup are byte-for-byte unchanged.

## 2026-10-15: Waitlist signup replaces "Coming soon on iOS" (look and behavior only; signups are not saved yet)

> **Before deploying:** the form doesn't send emails anywhere yet. Set `WAITLIST_ENDPOINT` in the script at the bottom of `dist/index.html` to a form endpoint (for example a Formspree URL). Until then, visitors will see "Joined", but their address is not stored.

### What changed

- **`dist/index.html`**:
  - The "Coming soon on iOS" caption is replaced by a `<form class="waitlist" id="waitlist">` to the right of the character. It has a "Join our waitlist!" label, an email field (placeholder `yourname@example.com`), a "Join" button, and an empty `<p class="waitlist-thanks" role="status">` that holds the thank-you message. `role="status"` makes screen readers announce the message when it appears.
  - The inline script at the bottom has the new waitlist logic:
    - The Join button is disabled (greyed) while the field is empty and enables as soon as something is typed.
    - The browser checks the address is a valid email (`type="email" required`) before the form submits.
    - On submit: the field locks, and the button changes to **"Joined"** with a white check mark and stays black. The message "Thanks for joining our waitlist. We are excited to tell you more about Skope soon!" appears under the button.
    - When `WAITLIST_ENDPOINT` is set, the email is POSTed there as form data (`email` field) first. If that fails, the field and button unlock, and "Something went wrong. Please try again." shows instead.
- **`dist/style.css`**:
  - `.hero-art` is now a row: character on the left, form on the right, vertically centered.
  - New `.waitlist` styles:
    - Light input with grey placeholder text.
    - Black pill-shaped button with white text, greyed (`#4a5167` / `#9aa1b5`) when disabled.
    - White 17px thank-you text.
    - Accent-colored focus outlines.
  - At ≤1000px wide: character 120×240, 20px gap, label 21px. At ≤650px: character 110×220.
  - Removed the `.availability` styles (desktop and phone).

### Known behavior

The form is vertically centered next to the character. When the thank-you message appears, the form gets taller, and the label and field move up slightly.

## 2026-10-15: Darker background, bigger hero character and caption

All changes are in `dist/style.css`.

- **Page background** (line 8): every gradient stop is darker; it's still a top-to-bottom linear gradient, darkest at the bottom of the page.
  - Was: `#495673 0% → #36415d 30% → #2a324b 65% → #20273c 100%`
  - Now: `#3e4964 0% → #2d3650 30% → #222941 65% → #181d2e 100%`
  - `--bg` (`#2a324b`) is unchanged; it's still used for the "learn more" button text.
- **Character** (line 4): 110×220px → **150×300px** on desktop, 85×170px → **110×220px** at ≤650px wide. The ground shadow is now 20px tall (was 16px) and sits 5px below the feet (was 4px).
- **"Coming soon on iOS" caption** (`.availability`, line 2): 18px → **24px** on desktop, 16px → **20px** at ≤650px wide. Space above it is 28px (was 24px).

Note: each frame of the sprite sheet is 392px tall, so at 300px on high-resolution (2×) screens the character is slightly upscaled and can look a little soft. Exporting the Procreate frames on a larger canvas (for example 1200×1200) and rebuilding the sheet, with the crop scaled to match, would make it fully sharp.

## 2026-10-15: Hero character animation replaces the app icon

### What changed

- **`dist/index.html`**: the hero's `<img class="app-icon">` is replaced by an animated character:
  `<div class="character" role="img" aria-label="Skope character"><div class="character-sprite"></div></div>`.
- **`dist/style.css`** (line 4): the `.app-icon` styles (rounded tile, box shadow, 220px/170px square) are replaced by:
  - `.hero-art .character`: 110×220px (85×170px at ≤650px wide), no border or background.
  - `.hero-art .character::before`: a soft elliptical ground shadow under the feet (static; does not animate).
  - `.character-sprite`: the sprite sheet as a background, animated by `@keyframes character-blink`.
  - With `prefers-reduced-motion: reduce`, the animation is off and the first frame shows.
- **Added `dist/assets/character-idle.webp`** (80 KB): the sprite sheet.
- **Removed the unused Rive files**: `dist/character.js`, `dist/character.png`, `dist/assets/idle.riv`, `dist/assets/rive/rive.js`, `dist/assets/rive/rive.wasm` (about 2 MB). None of them were referenced by the page.
- **`README.md`**: the file list now describes the sprite sheet instead of the Rive files.

`dist/assets/app-icon.png` is no longer shown on the page but is kept in the repo.

### The sprite sheet

- Source: 10 Procreate animation frames, 600×600 with transparent backgrounds.
- Every frame is cropped to the same 196×392 box at (221, 96), so the character stays aligned between frames. The crop covers the character's bounds across all frames plus about 12px of padding.
- The frames are joined left to right into one 1960×392 strip (frame 1 on the left), then converted to WebP:

```sh
# from the folder holding 1.png … 10.png
ffmpeg -i 1.png -i 2.png -i 3.png -i 4.png -i 5.png -i 6.png -i 7.png -i 8.png -i 9.png -i 10.png \
  -filter_complex "[0]crop=196:392:221:96[c1];[1]crop=196:392:221:96[c2];[2]crop=196:392:221:96[c3];[3]crop=196:392:221:96[c4];[4]crop=196:392:221:96[c5];[5]crop=196:392:221:96[c6];[6]crop=196:392:221:96[c7];[7]crop=196:392:221:96[c8];[8]crop=196:392:221:96[c9];[9]crop=196:392:221:96[c10];[c1][c2][c3][c4][c5][c6][c7][c8][c9][c10]hstack=inputs=10,format=rgba" \
  -frames:v 1 character-idle.png
cwebp -q 90 -alpha_q 100 -exact character-idle.png -o character-idle.webp
```

To update the art, redraw the frames in the same canvas positions, re-run the commands, and replace `dist/assets/character-idle.webp`. If the character moves outside the crop box, widen the crop and change `.character`'s width:height ratio to match (it's 1:2 now).

### Blink timing

The animation uses `step-end` keyframes so each frame holds for its own length of time, instead of `steps()`, which gives every frame the same length. Frame *n* (0–9) sits at `background-position: n/9 × 100%`. The loop is 9 seconds:

| Time | Frames | What happens |
|---|---|---|
| 0–2.4s | 1 | eyes open (hold) |
| 2.4–3.1s | 2, 3, 4, 5, 7, 8, 9, 10 | single blink (frame 6, the second blink, is skipped); closed frames show for about 80ms |
| 3.1–5.6s | 10 | eyes open (hold) |
| 5.6–6.44s | 2–10 | double blink using all frames |
| 6.44–9s | 10 | eyes open (hold), then loop |

To change the pace, change `9s` in `.character-sprite`'s `animation`, or move the keyframe percentages in `@keyframes character-blink` (percentage = seconds ÷ 9 × 100).

### Verified

- Checked in headless Chrome at desktop and phone widths: the character sits centered above "Coming soon on iOS", with the shadow and no tile.
- Screenshots paused at set times show closed eyes at 2.55s, 2.62s and 6.1s and open eyes elsewhere, with no edge of a neighboring frame showing.
