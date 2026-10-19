# Generates dist/assets/hero-scene.svg: layered misty mountains + clouds (moon is CSS).
import random, sys
random.seed(7)
W, H = 1440, 900

def spires(peaks, base):
    """Each peak is its own polygon: concave, slightly rocky slopes rising to a small notched tip."""
    shapes = []
    for x, top, w in peaks:
        lw = w * random.uniform(0.85, 1.15); rw = w * random.uniform(0.85, 1.15)
        pts = [(x - lw, base + 40)]
        for t in (0.0, 0.25, 0.45, 0.62, 0.78, 0.9):
            px = x - lw * (1 - t)
            py = top + (base - top) * (1 - t) ** 1.45 + random.uniform(-7, 7) * (1 - t)
            pts.append((px, py))
        pts += [(x - 4, top), (x + 3, top + 6), (x + 9, top + 2)]
        for t in (0.9, 0.78, 0.62, 0.45, 0.25, 0.0):
            px = x + 9 + rw * (1 - t)
            py = top + 2 + (base - top) * (1 - t) ** 1.45 + random.uniform(-7, 7) * (1 - t)
            pts.append((px, py))
        pts.append((x + 9 + rw, base + 40))
        shapes.append("M" + " L".join(f"{a:.0f} {b:.0f}" for a, b in pts) + f" L{x + rw:.0f} {H} L{x - lw:.0f} {H} Z")
    return " ".join(shapes)

def scallops(top, valley, wmin, wmax):
    """Row of rounded mist humps."""
    x = -random.randint(20, 120)
    d = f"M{x} {H} L{x} {valley}"
    while x < W + 40:
        w = random.randint(wmin, wmax)
        t = top + random.randint(-18, 18)
        d += f" Q{x + w/2:.0f} {2*t - valley:.0f} {x + w} {valley}"
        x += w
    return d + f" L{x} {H} Z"

def clouds(y, n, opacity, spread=(0, W), avoid=None):
    out = []
    for _ in range(n):
        cx = random.randint(*spread)
        if avoid and avoid[0] < cx < avoid[1]:
            continue
        rx = random.randint(90, 220); ry = random.randint(10, 22)
        out.append(f'<ellipse cx="{cx}" cy="{y + random.randint(-25, 25)}" rx="{rx}" ry="{ry}" opacity="{opacity}"/>')
    return "".join(out)

far = spires([(40,380,150),(190,300,190),(330,410,120),(470,470,150),(985,465,150),(1110,400,130),(1250,290,200),(1420,370,160)], 660)
mid = spires([(110,470,190),(300,520,170),(520,585,190),(905,580,190),(1120,510,180),(1330,460,200)], 720)
near1 = scallops(690, 770, 170, 260)
near2 = scallops(780, 850, 200, 300)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">
<defs>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#c3bddb" stop-opacity=".38"/><stop offset="1" stop-color="#c3bddb" stop-opacity="0"/></radialGradient>
<linearGradient id="fog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b3adcc" stop-opacity="0"/><stop offset=".5" stop-color="#b3adcc" stop-opacity=".32"/><stop offset="1" stop-color="#b3adcc" stop-opacity="0"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2840" stop-opacity="0"/><stop offset=".45" stop-color="#2a2840" stop-opacity=".7"/><stop offset=".82" stop-color="#2a2840"/></linearGradient>
<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="haze" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.2"/></filter>
</defs>
<ellipse cx="720" cy="600" rx="760" ry="300" fill="url(#glow)"/>
<g fill="#e4dff0" filter="url(#soft)">{clouds(170, 5, .18, avoid=(380, 1060))}{clouds(420, 9, .26)}</g>
<g opacity=".5" filter="url(#haze)"><path d="{far}" fill="#8f8aad"/></g>
<g fill="#e4dff0" filter="url(#soft)">{clouds(540, 8, .24)}</g>
<g opacity=".72" filter="url(#haze)"><path d="{mid}" fill="#726d93"/></g>
<rect x="0" y="560" width="{W}" height="220" fill="url(#fog)"/>
<path d="{near1}" fill="#5b5680" opacity=".88"/>
<path d="{near2}" fill="#46426a" opacity=".92"/>
<rect x="0" y="640" width="{W}" height="{H-640}" fill="url(#floor)"/>
</svg>
'''
open(sys.argv[1], "w").write(svg)
print(len(svg), "bytes")
