# Generates dist/assets/hero-scene.svg: layered misty mountains + clouds (moon is CSS).
import random, sys
random.seed(7)
W, H = 1440, 900

def smooth(pts):
    """Path through a polyline with every corner rounded (quadratic through segment midpoints)."""
    mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f} L{mid(pts[0], pts[1])[0]:.0f} {mid(pts[0], pts[1])[1]:.0f}"
    for i in range(1, len(pts) - 1):
        m = mid(pts[i], pts[i + 1])
        d += f" Q{pts[i][0]:.0f} {pts[i][1]:.0f} {m[0]:.0f} {m[1]:.0f}"
    return d + f" L{pts[-1][0]:.0f} {pts[-1][1]:.0f}"

def spire(x, top, w, base):
    """One asymmetric peak: concave slopes of different steepness, rocky ledges, a small rounded tip."""
    lw = w * random.uniform(1.0, 1.9); rw = w * random.uniform(1.0, 1.9)
    lean = random.uniform(-0.12, 0.12) * w          # tip leans off-centre
    h = base - top
    def side(width, sign):
        k = random.uniform(1.15, 1.75)                # higher k = flatter foot, sharper spire
        ts = (0.0, 0.22, 0.42, 0.6, 0.75, 0.87)
        out = []
        for t in ts:
            ledge = random.uniform(-0.09, 0.09) * h * t * (1 - t) * 4
            px = x + lean + sign * width * (1 - t) + random.uniform(-0.04, 0.04) * width * (1 - t)
            out.append((px, base - h * t ** k - ledge))
        return out
    left = side(lw, -1); right = side(rw, 1)[::-1]
    pts = [(left[0][0], base + 60)] + left + [(x + lean, top)] + right + [(right[-1][0], base + 60)]
    return smooth(pts) + f" L{right[-1][0]:.0f} {H} L{left[0][0]:.0f} {H} Z"

def spires(peaks, base, satellites=0.65):
    """Each listed peak, plus (often) a lower satellite peak on one shoulder."""
    shapes = []
    for x, top, w in peaks:
        if random.random() < satellites:
            off = random.choice((-1, 1)) * w * random.uniform(0.4, 0.75)
            shapes.append(spire(x + off, top + (base - top) * random.uniform(0.22, 0.45), w * random.uniform(0.45, 0.7), base))
        shapes.append(spire(x, top, w, base))
    return " ".join(shapes)

def scallops(top, valley, wmin, wmax):
    """Row of rounded mist humps."""
    x = -random.randint(20, 120)
    d = f"M{x} {H} L{x} {valley}"
    while x < W + 40:
        w = random.randint(wmin, wmax)
        t = top + random.randint(-38, 30)
        v = valley + random.randint(-12, 12)
        d += f" Q{x + w * random.uniform(0.3, 0.7):.0f} {2*t - v:.0f} {x + w} {v}"
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

# (x, tip y, half-width). Tallest peaks are at the far left and right edges; the sky under
# the moon (upper right, x ~1150-1350) is kept clear of tips above y ~330.
far = spires([(-20,340,120),(130,235,135),(275,350,95),(390,425,120),(505,480,105),(625,535,95),
              (835,540,100),(955,470,115),(1075,345,125),(1205,430,90),(1310,385,110),(1445,280,130)], 660)
mid = spires([(40,430,150),(215,505,115),(390,555,140),(560,615,110),(880,600,120),(1015,535,140),
              (1170,470,125),(1355,445,160)], 720)
# The two near layers are the same kind of peak, but few and broad so they read as close up.
near1 = spires([(-30,490,220),(350,555,200),(1085,515,215),(1470,465,235)], 790, satellites=0.3)
near2 = spires([(130,615,270),(735,680,240),(1305,600,280)], 870, satellites=0)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">
<defs>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#b6b1ca" stop-opacity=".38"/><stop offset="1" stop-color="#b6b1ca" stop-opacity="0"/></radialGradient>
<linearGradient id="fog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a5a1bb" stop-opacity="0"/><stop offset=".5" stop-color="#a5a1bb" stop-opacity=".28"/><stop offset="1" stop-color="#a5a1bb" stop-opacity="0"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2840" stop-opacity="0"/><stop offset=".45" stop-color="#2a2840" stop-opacity=".7"/><stop offset=".82" stop-color="#2a2840"/></linearGradient>
<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="haze" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.2"/></filter>
</defs>
<ellipse cx="720" cy="600" rx="760" ry="300" fill="url(#glow)"/>
<g fill="#d6d2e3" filter="url(#soft)">{clouds(170, 5, .18, avoid=(380, 1060))}{clouds(420, 9, .26)}</g>
<g opacity=".5" filter="url(#haze)"><path d="{far}" fill="#827e9b"/></g>
<g fill="#d6d2e3" filter="url(#soft)">{clouds(540, 8, .24)}</g>
<g opacity=".72" filter="url(#haze)"><path d="{mid}" fill="#676383"/></g>
<rect x="0" y="560" width="{W}" height="220" fill="url(#fog)"/>
<path d="{near1}" fill="#514d6f" opacity=".88"/>
<path d="{near2}" fill="#3e3b5b" opacity=".92"/>
<rect x="0" y="640" width="{W}" height="{H-640}" fill="url(#floor)"/>
</svg>
'''
open(sys.argv[1], "w").write(svg)
print(len(svg), "bytes")
