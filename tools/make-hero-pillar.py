# Generates dist/assets/hero-pillar.webp: the intro pillar (bottom cropped) with the celebrating
# character from characters.PNG standing on its top face, plus a soft contact shadow.
# Usage: python3 tools/make-hero-pillar.py   (needs Pillow)
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ASSETS = Path(__file__).resolve().parent.parent / "dist" / "assets"
PILLAR_KEEP = 600        # px of pillar.webp kept from the top (of 859); the rest is cropped
CHAR_HEIGHT = 1.45       # character height (incl. excitement marks) as a multiple of pillar width
FACE_CENTER = 0.25       # centre of the pillar's top face, as a fraction of pillar width from the top
FEET_DROP = 0.02         # feet sit slightly below the face centre so they look planted
CHAR_BRIGHTNESS = 1.18   # the sheet's lavender is a little dim against the dark scene

pillar = Image.open(ASSETS / "pillar.webp").convert("RGBA")
pillar = pillar.crop((0, 0, pillar.width, PILLAR_KEEP))
rgb = ImageEnhance.Brightness(pillar.convert("RGB")).enhance(1.2)   # was CSS brightness(1.2)
rgb.putalpha(pillar.split()[3]); pillar = rgb
W = pillar.width

sheet = Image.open(ASSETS / "characters.PNG").convert("RGBA")
char = sheet.crop((1150, 780, 1380, 1450))
char = char.crop(char.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox())
# Centre on the legs (the arms aren't symmetric): mean x of opaque pixels in the bottom 15%.
a = char.split()[3]; rows = range(int(char.height * 0.85), char.height)
xs = [x for y in rows for x in range(char.width) if a.getpixel((x, y)) > 128]
legs_x = sum(xs) / len(xs)
scale = CHAR_HEIGHT * W / char.height
char = char.resize((round(char.width * scale), round(char.height * scale)), Image.LANCZOS)
lit = ImageEnhance.Brightness(char.convert("RGB")).enhance(CHAR_BRIGHTNESS)
lit.putalpha(char.split()[3]); char = lit
legs_x *= scale

feet_y = W * (FACE_CENTER + FEET_DROP)
top = round(char.height - feet_y)                 # canvas space above the pillar
canvas = Image.new("RGBA", (W, top + pillar.height), (0, 0, 0, 0))
canvas.alpha_composite(pillar, (0, top))

shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
cx, cy, rx, ry = W / 2, top + W * FACE_CENTER + 2, W * 0.24, W * 0.065
ImageDraw.Draw(shadow).ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(8, 6, 26, 150))
canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(W * 0.025)))

canvas.alpha_composite(char, (round(W / 2 - legs_x), 0))
out = ASSETS / "hero-pillar.webp"
canvas.save(out, "WEBP", quality=90, method=6)
print(out.name, canvas.size, out.stat().st_size, "bytes")
