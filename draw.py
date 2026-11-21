#!/usr/bin/env python3
"""Render THE SATURDAY GLOBE — a 1024x1024 broadsheet poster summing up
Saturday 21 November 2026 in 35 dated stories (13 pictured cards + 22 briefs).
Deterministic: fixed seed, no network, no time dependence.
Run: python3 draw.py  -> writes poster.png next to this file.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
OUT = "poster.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# chips: CONFIRMED = verified by officials/data; REPORTED = as reported today;
#        CLAIM = one side's claim, not independently verified.
LEADS = [
    dict(n=1, region="Europe", place="ANTALYA, TURKIYE", cat="CLIMATE",
         art="climate",
         head="COP31 runs into overtime as fossil fuels vanish from draft",
         body="Negotiators work an extra day after the summit misses its Friday close; a third draft is due Saturday morning.",
         src="AP", chip="CONFIRMED"),
    dict(n=2, region="Middle East", place="RIYADH", cat="CONFLICT",
         art="missile",
         head="Three Houthi missiles fired at Riyadh are intercepted",
         body="Saudi defences destroy three ballistic missiles over the capital early Saturday; no casualties reported.",
         src="Reuters", chip="REPORTED"),
    dict(n=3, region="Europe", place="KRYVYI RIH, UKRAINE", cat="WAR",
         art="strike",
         head="Strike on Zelenskyy's hometown kills a boy of 7 and a paramedic",
         body="Two killed and 60 hurt as missiles and 148 drones hit overnight; rescuers are struck again as they work.",
         src="AP", chip="CONFIRMED"),
]

FEATURES = [
    dict(n=4, region="Latin America", place="JUNIN, PERU", cat="QUAKE",
         art="quake",
         head="6.7 quake shakes Peru's Andes; no deaths",
         body="Felt in Lima, 300 km away; homes damaged in Junin, power cut in places.",
         src="USGS / AFP", chip="CONFIRMED"),
    dict(n=5, region="Asia", place="MERCURY, VIA DARMSTADT", cat="SPACE",
         art="space",
         head="BepiColombo slips into orbit around Mercury",
         body="After eight years and 10 billion km, the twin orbiters are captured today.",
         src="ESA / Sky & Telescope", chip="REPORTED"),
    dict(n=6, region="Europe", place="WARSAW, POLAND", cat="NATO",
         art="nato",
         head="NATO chief heads to Warsaw after missiles land in Poland",
         body="Rutte calls the breach a grave violation; Poland seeks more air defences.",
         src="AP", chip="CONFIRMED"),
    dict(n=7, region="Asia", place="DAVAO, PHILIPPINES", cat="AVIATION",
         art="plane",
         head="Air Niugini jet lands in emergency; all 146 safe",
         body="A possible engine-fire warning diverts PX19 to Davao; all leave by slides.",
         src="AP / CAAP", chip="CONFIRMED"),
    dict(n=8, region="Oceania", place="WELLINGTON, NZ", cat="CRICKET",
         art="cricket",
         head="Rahul's 136 puts India on top in Wellington",
         body="The 13th Test hundred completes a set in every SENA country; India lead.",
         src="ESPNcricinfo", chip="CONFIRMED"),
    dict(n=9, region="North America", place="LAS VEGAS, USA", cat="MOTOR RACING",
         art="f1",
         head="Antonelli fastest, but Verstappen takes Vegas pole",
         body="Quickest by 0.258s, then drops five places for a power-unit change.",
         src="Formula1.com", chip="CONFIRMED"),
    dict(n=10, region="Middle East", place="TEHRAN", cat="DIPLOMACY",
         art="uranium",
         head="Iran-US talks deadlocked over uranium stockpile",
         body="Mediators warn of renewed conflict as Washington demands the uranium go.",
         src="Al Arabiya", chip="REPORTED"),
    dict(n=11, region="Middle East", place="STRAIT OF HORMUZ", cat="CONFLICT",
         art="drone",
         head="Iran claims its 58th US MQ-9 drone downed",
         body="The IRGC says a new system downed the Reaper; the US has not confirmed it.",
         src="IRIB / Press TV", chip="CLAIM"),
    dict(n=12, region="North America", place="WASHINGTON, USA", cat="TECH POLICY",
         art="tax",
         head="Trump threatens 'tremendous tax' on data centres abroad",
         body="Firms building AI data centres abroad face a huge levy, the president says.",
         src="AP / CNBC", chip="REPORTED"),
    dict(n=13, region="Middle East", place="STRAIT OF HORMUZ", cat="SHIPPING",
         art="tanker",
         head="Tanker hit by projectile in the Strait of Hormuz",
         body="UK monitors report a strike on the stern near Oman; no casualties confirmed.",
         src="UKMTO", chip="REPORTED"),
]

BRIEFS = [
    dict(n=14, region="North America", place="NEW YORK",
         head="US stocks slide into correction as AI sell-off deepens",
         src="Reuters"),
    dict(n=15, region="North America", place="CRYPTO MARKETS",
         head="Bitcoin sinks below $56,000 as $2.4bn of bets are liquidated",
         src="CoinGecko"),
    dict(n=16, region="Oceania", place="MELBOURNE",
         head="North Melbourne reach a fourth straight AFLW grand final",
         src="ABC"),
    dict(n=17, region="Oceania", place="SYDNEY",
         head="Cricket Australia backs Cummins amid ball-tampering row",
         src="SBS"),
    dict(n=18, region="Oceania", place="SYDNEY",
         head="Three arrested after Sydney terror raids; one charged",
         src="ABC"),
    dict(n=19, region="Oceania", place="AUSTRALIA",
         head="GTA VI launch sends one in four workers calling in sick",
         src="9News"),
    dict(n=20, region="Europe", place="LONDON",
         head="Cancer pill daraxonrasib doubles survival in pancreatic trial",
         src="J. Hematol. Oncol."),
    dict(n=21, region="Middle East", place="GAZA",
         head="Israeli strikes kill Palestinians in Gaza; West Bank violence goes on",
         src="Al Jazeera"),
    dict(n=22, region="Latin America", place="PORT-AU-PRINCE, HAITI",
         head="Salvadoran troops in Haiti lose soldiers to explosives",
         src="AP"),
    dict(n=23, region="Asia", place="INDIA",
         head="Eleven die and 180 are hospitalised after adulterated alcohol",
         src="The Straits Times"),
    dict(n=24, region="Africa", place="NIGERIA",
         head="Funeral boat capsizes in Nigeria; four dead, two of them children",
         src="Al Jazeera"),
    dict(n=25, region="Asia", place="AFGHANISTAN",
         head="Old mortar shell explodes and kills four students",
         src="The Straits Times"),
    dict(n=26, region="Middle East", place="BASRA, IRAQ",
         head="Fire at a power plant in Basra kills at least four",
         src="Reuters"),
    dict(n=27, region="Asia", place="INDONESIA",
         head="Indonesia hit by massive forest fires",
         src="AP"),
    dict(n=28, region="North America", place="WASHINGTON",
         head="FBI and US agriculture department hit by cyberattacks",
         src="Reuters"),
    dict(n=29, region="North America", place="UNITED STATES",
         head="Judge approves Bayer's $7.25bn deal to settle Roundup claims",
         src="ABC News"),
    dict(n=30, region="Europe", place="MADRID",
         head="Spain heads to a 29 November election as conservatives gain",
         src="El Pais"),
    dict(n=31, region="Europe", place="BERLIN",
         head="Gen Z protests spread across 25 European countries",
         src="One Turn"),
    dict(n=32, region="Europe", place="KYIV",
         head="Zelenskyy calls Putin a 'killer' after Trump calls him a friend",
         src="BBC"),
    dict(n=33, region="Europe", place="BRUSSELS",
         head="Trump tells Europe to stop funding Ukraine after Putin summit",
         src="The Telegraph"),
    dict(n=34, region="Middle East", place="WASHINGTON",
         head="Trump weighs new strikes on Iran as Israel presses for action",
         src="NYT"),
    dict(n=35, region="North America", place="WASHINGTON",
         head="NASA halts Perseverance and Mars Odyssey science amid hardware trouble",
         src="NASA"),
]

REGIONS = [("Middle East", 7), ("Europe", 8), ("North America", 7),
           ("Asia", 5), ("Oceania", 5), ("Africa", 1), ("Latin America", 2)]
REGION_COLOURS = {"Middle East": (178, 58, 44), "Europe": (38, 84, 150),
                  "North America": (26, 110, 88), "Asia": (176, 118, 20),
                  "Oceania": (20, 120, 140), "Africa": (150, 84, 20),
                  "Latin America": (110, 60, 140)}

NUMBERS = [
    ("3", "missiles fired at Riyadh,\nall intercepted"),
    ("6.7", "magnitude of the\nPeru earthquake"),
    ("146", "people safe after the\nDavao emergency landing"),
    ("136", "runs by KL Rahul\nin Wellington"),
    ("58", "US MQ-9 drones Iran\nclaims to have downed"),
    ("$2.4bn", "crypto bets liquidated\nas Bitcoin slides"),
]

DATECHECK = [
    ("PIF Tower, Riyadh, hit by a Houthi strike", "Thu 19 Nov"),
    ("US AI-chip licences for China disclosed", "Thu 19 Nov"),
    ("Russian missiles crash in Poland", "Fri 20 Nov"),
    ("Kyiv bridges hit; three killed", "Fri 20 Nov"),
    ("UK and EU sign three post-Brexit deals", "Fri 20 Nov"),
    ("Palisades fire arson verdict in Los Angeles", "Fri 20 Nov"),
]

# world-map pins for the 13 pictured stories: (lon, lat)
PINS = {1: (36.9, 30.7), 2: (46.7, 24.7), 3: (33.4, 47.9), 4: (-76.0, -11.0),
        5: (8.65, 49.87), 6: (21.0, 52.2), 7: (125.6, 7.1), 8: (174.8, -41.3),
        9: (-115.1, 36.2), 10: (51.4, 35.7), 11: (56.3, 26.6),
        12: (-77.0, 38.9), 13: (56.2, 26.2)}
# display offsets (px) so clustered pins don't overlap; a leader line joins
# the pin to its true spot
PIN_OFF = {1: (-20, 8), 2: (22, 0), 3: (0, -18), 5: (-20, 0), 6: (18, 4),
           10: (18, -14), 11: (0, 20), 13: (22, 10)}

# sanity: region counts must sum to the story total, and every story counted once
ALL = LEADS + FEATURES + BRIEFS
assert len(ALL) == 35, len(ALL)
assert [s["n"] for s in ALL] == list(range(1, 36))
assert sum(c for _, c in REGIONS) == 35
for name, c in REGIONS:
    assert sum(1 for s in ALL if s["region"] == name) == c, name
assert len(NUMBERS) == 6
assert 5 <= len(DATECHECK) <= 7


# ---------------------------------------------------------------- helpers
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(d, box, c1, c2):
    x0, y0, x1, y1 = box
    h = max(1, y1 - y0)
    for y in range(y0, y1):
        d.line([(x0, y), (x1, y)], fill=lerp(c1, c2, (y - y0) / h))


def halftone(d, box, rng, col, n, rmax=2):
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rng.randint(x0, x1)
        y = rng.randint(y0, y1)
        r = rng.randint(1, rmax)
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def grain(img, mask_boxes, seed=7, alpha=0.14):
    """Deterministic newsprint grain: per-channel noise in 4x4 blocks, blended
    only over the rich illustration bands (mask_boxes), so flat text areas stay
    crisp and the PNG stays small. Lifts unique colours far above 40k."""
    rng = random.Random(seed)
    small = Image.frombytes("RGB", (W // 4, H // 4), rng.randbytes(W * H * 3 // 16))
    noise = small.resize((W, H), Image.NEAREST)
    blended = Image.blend(img, noise, alpha)
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    for box in mask_boxes:
        md.rectangle(box, fill=255)
    return Image.composite(blended, img, mask)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def badge(d, x, y, n, size=20):
    d.ellipse([x, y, x + size, y + size], fill=(20, 20, 24),
              outline=(255, 255, 255), width=1)
    text(d, (x + size / 2, y + size / 2 - 1), str(n), F(SANS_B, 12),
         (255, 255, 255), anchor="mm")


def chip(d, x, y, label):
    col = {"CONFIRMED": (26, 110, 88), "REPORTED": (176, 118, 20),
           "CLAIM": (178, 58, 44)}[label]
    f = F(SANS_B, 8)
    w = d.textlength(label, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=col)
    text(d, (x + 5, y + 1), label, f, (255, 255, 255))
    return w


def source_tag(d, x, y, src):
    f = F(SANS, 9)
    text(d, (x, y), "SOURCE: " + src, f, (90, 90, 90))


def fit_one_line(d, text, font, maxw):
    """Truncate text with an ellipsis so it fits on a single line."""
    if d.textlength(text, font=font) <= maxw:
        return text
    words = text.split()
    while words and d.textlength(" ".join(words) + " …", font=font) > maxw:
        words.pop()
    return " ".join(words) + " …"


# ---------------------------------------------------------------- art scenes
def art(img, kind, box, rng):
    """Draw a scene clipped to box: art is rendered on a transparent layer and
    pasted, so nothing spills into the text below the picture."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if kind == "climate":
        vgrad(d, box, (250, 190, 90), (70, 130, 90))
        d.ellipse([x1 - 52, y0 + 8, x1 - 12, y0 + 48], fill=(255, 240, 170))
        for i in range(5):
            bx = x0 + i * (w // 5)
            bh = rng.randint(18, 42)
            d.rectangle([bx + 4, y1 - bh, bx + w // 5 - 4, y1], fill=(30, 70, 45))
        d.polygon([(x0, y1), (x0 + w * 0.3, y1 - 34), (x0 + w * 0.6, y1)],
                  fill=(40, 90, 55))
        halftone(d, box, rng, (255, 255, 255), 40)
    elif kind == "missile":
        vgrad(d, box, (16, 20, 48), (70, 60, 110))
        for _ in range(26):
            sx, sy = rng.randint(x0, x1), rng.randint(y0, y1)
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 220))
        for i in range(3):
            sx = x0 + 20 + i * (w // 3)
            d.arc([sx, y0 + 6, sx + 70, y0 + 70], 200, 340, fill=(255, 180, 60),
                  width=3)
            d.ellipse([sx + 62, y0 + 8, sx + 70, y0 + 16], fill=(255, 220, 120))
        for i in range(6):
            bx = x0 + i * (w // 6)
            bh = rng.randint(22, 48)
            d.rectangle([bx + 3, y1 - bh, bx + w // 6 - 3, y1], fill=(10, 12, 30))
            d.rectangle([bx + w // 12 - 2, y1 - bh - 10, bx + w // 12 + 2, y1 - bh],
                        fill=(10, 12, 30))
        halftone(d, box, rng, (255, 200, 100), 30)
    elif kind == "strike":
        vgrad(d, box, (120, 60, 50), (40, 30, 40))
        for i in range(5):
            bx = x0 + i * (w // 5)
            bh = rng.randint(26, 55)
            d.rectangle([bx + 4, y1 - bh, bx + w // 5 - 4, y1], fill=(25, 18, 22))
        d.ellipse([cx - 26, y0 + 8, cx + 26, y0 + 60], fill=(220, 140, 60))
        d.polygon([(cx - 40, y0 + 20), (cx, y0 + 44), (cx + 40, y0 + 20),
                   (cx + 18, y0 + 60), (cx - 18, y0 + 60)], fill=(90, 70, 70))
        d.rectangle([x0 + 8, y1 - 16, x0 + 44, y1 - 6], fill=(200, 60, 50))
        text(d, (x0 + 26, y1 - 11), "+", F(SANS_B, 12), (255, 255, 255),
             anchor="mm")
        halftone(d, box, rng, (255, 220, 180), 30)
    elif kind == "quake":
        vgrad(d, box, (90, 70, 60), (200, 170, 120))
        d.polygon([(x0, y1), (x0 + w * 0.25, y0 + 30), (x0 + w * 0.5, y1)],
                  fill=(70, 55, 45))
        d.polygon([(x0 + w * 0.4, y1), (x0 + w * 0.7, y0 + 18),
                   (x0 + w, y1)], fill=(55, 45, 38))
        d.polygon([(x0 + w * 0.2, y0 + 34), (x0 + w * 0.28, y0 + 26),
                   (x0 + w * 0.34, y0 + 36)], fill=(240, 240, 230))
        pts = []
        for i in range(30):
            pts.append((x0 + 8 + i * (w - 16) / 29,
                        cy + 8 + (rng.choice([-1, 1]) * rng.randint(2, 16)
                                  if i % 3 == 0 else 0)))
        d.line(pts, fill=(178, 40, 30), width=2)
        halftone(d, box, rng, (60, 40, 30), 40)
    elif kind == "space":
        vgrad(d, box, (8, 8, 26), (40, 30, 70))
        for _ in range(40):
            sx, sy = rng.randint(x0, x1), rng.randint(y0, y1)
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
        d.ellipse([x1 - 66, y0 + 10, x1 - 6, y0 + 70], fill=(200, 170, 140))
        d.ellipse([x1 - 60, y0 + 16, x1 - 16, y0 + 64], fill=(170, 140, 115))
        for i in range(5):
            d.ellipse([x1 - 58 + i * 8, y0 + 30 + (i % 2) * 12,
                       x1 - 52 + i * 8, y0 + 36 + (i % 2) * 12],
                      fill=(140, 110, 90))
        d.rectangle([x0 + 14, cy - 8, x0 + 62, cy + 8], fill=(220, 220, 230))
        d.polygon([(x0 + 62, cy - 14), (x0 + 86, cy), (x0 + 62, cy + 14)],
                  fill=(180, 180, 200))
        d.line([(x0 + 14, cy - 14), (x0 + 30, cy - 34)], fill=(255, 200, 80),
               width=2)
        halftone(d, box, rng, (160, 180, 255), 30)
    elif kind == "nato":
        vgrad(d, box, (200, 220, 240), (60, 90, 140))
        for i in range(4):
            bx = x0 + i * (w // 4)
            bh = rng.randint(24, 50)
            d.rectangle([bx + 5, y1 - bh, bx + w // 4 - 5, y1], fill=(30, 45, 70))
        d.ellipse([cx - 24, y0 + 8, cx + 24, y0 + 56], fill=(20, 40, 90))
        for a in range(12):
            ang = a * math.pi / 6
            d.ellipse([cx + 16 * math.cos(ang) - 2, y0 + 32 + 16 * math.sin(ang) - 2,
                       cx + 16 * math.cos(ang) + 2, y0 + 32 + 16 * math.sin(ang) + 2],
                      fill=(255, 220, 60))
        halftone(d, box, rng, (255, 255, 255), 30)
    elif kind == "plane":
        vgrad(d, box, (140, 190, 230), (240, 220, 180))
        d.ellipse([x1 - 50, y0 + 6, x1 - 14, y0 + 42], fill=(255, 245, 200))
        d.polygon([(x0 + 12, cy - 6), (x0 + 70, cy - 6), (x0 + 86, cy),
                   (x0 + 70, cy + 6), (x0 + 12, cy + 6)], fill=(240, 240, 245))
        d.polygon([(x0 + 30, cy - 6), (x0 + 44, cy - 26), (x0 + 52, cy - 6)],
                  fill=(200, 200, 210))
        d.polygon([(x0 + 30, cy + 6), (x0 + 44, cy + 22), (x0 + 52, cy + 6)],
                  fill=(200, 200, 210))
        d.rectangle([x0, y1 - 14, x1, y1 - 8], fill=(60, 60, 70))
        for i in range(6):
            d.line([(x0 + i * (w // 6) + 6, y1 - 11), (x0 + i * (w // 6) + 22,
                    y1 - 11)], fill=(255, 255, 255), width=2)
        halftone(d, box, rng, (255, 255, 255), 30)
    elif kind == "cricket":
        vgrad(d, box, (120, 190, 110), (40, 110, 50))
        d.ellipse([x0 + 10, y0 + 8, x1 - 10, y0 + 30], fill=(230, 220, 170))
        d.rectangle([x0 + 14, y1 - 34, x1 - 14, y1 - 6], fill=(190, 160, 110))
        d.rectangle([x0 + w // 2 - 16, y1 - 52, x0 + w // 2 - 12, y1 - 34],
                    fill=(240, 220, 160))
        d.rectangle([x0 + w // 2 + 12, y1 - 52, x0 + w // 2 + 16, y1 - 34],
                    fill=(240, 220, 160))
        d.ellipse([x0 + w // 2 - 4, y1 - 56, x0 + w // 2 + 4, y1 - 48],
                  fill=(200, 40, 30))
        d.polygon([(x0 + 18, y0 + 40), (x0 + 30, y0 + 40), (x0 + 44, y1 - 40),
                   (x0 + 32, y1 - 40)], fill=(150, 100, 50))
        halftone(d, box, rng, (255, 255, 255), 36)
    elif kind == "f1":
        vgrad(d, box, (30, 30, 60), (120, 40, 90))
        d.arc([x0 - 30, y0 + 10, x1 + 10, y1 + 60], 300, 90, fill=(220, 220, 220),
              width=10)
        d.arc([x0 - 30, y0 + 10, x1 + 10, y1 + 60], 300, 90, fill=(200, 30, 40),
              width=2)
        d.rectangle([x0 + 16, cy - 8, x0 + 76, cy + 8], fill=(200, 30, 40))
        d.ellipse([x0 + 20, cy - 12, x0 + 32, cy], fill=(20, 20, 20))
        d.ellipse([x0 + 60, cy - 12, x0 + 72, cy], fill=(20, 20, 20))
        for i in range(4):
            for j in range(2):
                d.rectangle([x1 - 34 + i * 8, y0 + 8 + j * 8, x1 - 26 + i * 8,
                             y0 + 16 + j * 8],
                            fill=(0, 0, 0) if (i + j) % 2 == 0 else (255, 255, 255))
        halftone(d, box, rng, (255, 220, 60), 30)
    elif kind == "uranium":
        vgrad(d, box, (40, 60, 80), (140, 170, 190))
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 200, 60))
        for a, col in [(0, (220, 80, 60)), (60, (60, 160, 220)),
                       (120, (90, 200, 120))]:
            rx, ry = 46, 18
            pts = []
            for t in range(0, 361, 10):
                r = math.radians(t + a)
                pts.append((cx + rx * math.cos(r), cy + ry * math.sin(r)))
            d.line(pts, fill=col, width=2)
        d.rectangle([x0 + 10, y1 - 22, x0 + 46, y1 - 6], fill=(70, 80, 90))
        d.ellipse([x0 + 14, y1 - 34, x0 + 42, y1 - 18], fill=(110, 120, 130))
        halftone(d, box, rng, (255, 255, 255), 30)
    elif kind == "drone":
        vgrad(d, box, (200, 120, 60), (60, 80, 120))
        d.rectangle([x0, y1 - 26, x1, y1], fill=(30, 90, 130))
        for i in range(3):
            d.arc([x0 + 10 + i * 30, y1 - 22, x0 + 40 + i * 30, y1 - 2],
                  180, 360, fill=(255, 255, 255), width=2)
        d.rectangle([cx - 22, cy - 22, cx + 22, cy - 10], fill=(40, 40, 50))
        d.ellipse([cx - 34, cy - 30, cx - 14, cy - 10], fill=(30, 30, 40))
        d.ellipse([cx + 14, cy - 30, cx + 34, cy - 10], fill=(30, 30, 40))
        d.line([(cx - 24, cy - 20), (cx - 44, cy - 20)], fill=(30, 30, 40), width=2)
        d.line([(cx + 24, cy - 20), (cx + 44, cy - 20)], fill=(30, 30, 40), width=2)
        d.line([(cx, cy - 10), (cx, cy + 14)], fill=(30, 30, 40), width=2)
        d.polygon([(cx - 4, cy + 14), (cx + 4, cy + 14), (cx, cy + 26)],
                  fill=(200, 60, 40))
        halftone(d, box, rng, (255, 220, 150), 30)
    elif kind == "tax":
        vgrad(d, box, (230, 210, 160), (90, 110, 140))
        d.polygon([(cx - 40, y1 - 30), (cx, y0 + 16), (cx + 40, y1 - 30)],
                  fill=(240, 240, 235))
        d.rectangle([x0 + 16, y1 - 30, x1 - 16, y1 - 22], fill=(200, 200, 190))
        for i in range(4):
            d.rectangle([x0 + 22 + i * 20, y1 - 52, x0 + 30 + i * 20, y1 - 30],
                        fill=(220, 220, 210))
        d.ellipse([x1 - 44, y0 + 10, x1 - 12, y0 + 42], fill=(255, 215, 90),
                  outline=(180, 140, 20), width=2)
        text(d, (x1 - 28, y0 + 26), "$", F(SANS_B, 16), (140, 100, 10),
             anchor="mm")
        halftone(d, box, rng, (255, 255, 255), 30)
    elif kind == "tanker":
        vgrad(d, box, (240, 180, 110), (120, 90, 70))
        d.rectangle([x0, y1 - 34, x1, y1], fill=(25, 70, 110))
        for i in range(4):
            d.arc([x0 + 8 + i * 34, y1 - 30, x0 + 42 + i * 34, y1 - 8],
                  180, 360, fill=(200, 230, 250), width=2)
        d.rectangle([x0 + 18, cy - 4, x0 + w - 18, cy + 16], fill=(140, 40, 30))
        d.rectangle([x0 + 30, cy - 22, x0 + 58, cy - 4], fill=(200, 200, 200))
        d.rectangle([x0 + 62, cy - 30, x0 + 70, cy - 4], fill=(180, 60, 40))
        d.line([(x1 - 20, y0 + 6), (x0 + w - 40, cy - 6)], fill=(255, 240, 160),
               width=3)
        d.ellipse([x0 + w - 44, cy - 10, x0 + w - 36, cy - 2],
                  fill=(255, 200, 60))
        halftone(d, box, rng, (255, 240, 200), 30)
    # clip to the box: paste only the cropped layer, honouring its alpha
    crop = layer.crop(box)
    img.paste(crop, (box[0], box[1]), crop)


# ---------------------------------------------------------------- layout
def draw_map(d, box, rng):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 235), outline=(20, 20, 24), width=2)
    # graticule
    for gx in range(x0 + 60, x1, 60):
        d.line([(gx, y0), (gx, y1)], fill=(190, 205, 215), width=1)
    for gy in range(y0 + 30, y1, 30):
        d.line([(x0, gy), (x1, gy)], fill=(190, 205, 215), width=1)
    # very simplified continents (equirectangular lon -180..180, lat 75..-55)
    def P(lon, lat):
        return (x0 + (lon + 180) / 360 * (x1 - x0),
                y0 + (75 - lat) / 130 * (y1 - y0))
    land = (150, 175, 140)
    sea = (214, 228, 235)
    continents = [
        [(-168, 66), (-140, 70), (-120, 71), (-100, 69), (-85, 66), (-80, 62),
         (-75, 45), (-70, 42), (-75, 32), (-80, 26), (-85, 30), (-90, 21),
         (-95, 19), (-100, 23), (-105, 20), (-110, 24), (-115, 30),
         (-122, 37), (-125, 48), (-135, 58), (-150, 60), (-165, 60)],
        [(-70, 10), (-60, 8), (-52, 5), (-44, -3), (-35, -8), (-40, -20),
         (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-73, -40),
         (-72, -20), (-78, -5), (-80, 5), (-77, 8)],
        [(-18, 64), (-10, 66), (0, 60), (5, 58), (10, 57), (18, 56),
         (21, 55), (28, 60), (30, 70), (40, 68), (50, 69), (60, 69),
         (68, 66), (60, 60), (50, 52), (45, 44), (40, 42), (35, 36),
         (30, 36), (22, 37), (19, 42), (12, 44), (8, 44), (3, 43),
         (-2, 48), (-5, 48), (-10, 54), (-18, 58)],
        [(60, 70), (70, 72), (90, 75), (110, 73), (130, 72), (150, 70),
         (170, 67), (178, 65), (170, 60), (160, 60), (150, 59), (140, 50),
         (135, 43), (127, 40), (122, 38), (120, 32), (110, 20), (108, 12),
         (105, 8), (100, 6), (95, 15), (90, 22), (85, 20), (80, 15),
         (77, 8), (73, 20), (68, 23), (62, 25), (57, 26), (52, 28),
         (48, 30), (43, 12), (40, 15), (35, 28), (32, 30)],
        [(113, -22), (114, -30), (115, -35), (120, -34), (125, -33),
         (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
         (153, -27), (150, -22), (146, -19), (142, -11), (136, -12),
         (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)],
        [(113, -43), (120, -43), (125, -41), (130, -42), (135, -43),
         (140, -43), (145, -41), (147, -39), (140, -38), (130, -40),
         (122, -42), (115, -43)],
        [(166, -34), (168, -35), (170, -37), (172, -40), (174, -41),
         (176, -38), (178, -38), (176, -35), (173, -34), (167, -35)],
    ]
    for poly in continents:
        d.polygon([P(lon, lat) for lon, lat in poly], fill=land,
                  outline=(110, 135, 105))
    # pins (offset where clustered, with a leader line to the true spot)
    for n, (lon, lat) in PINS.items():
        px, py = P(lon, lat)
        ox, oy = PIN_OFF.get(n, (0, 0))
        qx, qy = px + ox, py + oy
        if (ox, oy) != (0, 0):
            d.line([(px, py), (qx, qy)], fill=(178, 40, 30), width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(178, 40, 30))
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=(178, 40, 30),
                  outline=(255, 255, 255), width=1)
        text(d, (qx, qy - 1), str(n), F(SANS_B, 9), (255, 255, 255), anchor="mm")
    text(d, (x0 + 8, y0 + 4), "WHERE IT HAPPENED — the 13 pictured stories",
         F(SANS_B, 11), (20, 20, 24))


def render():
    rng = random.Random(20261121)
    img = Image.new("RGB", (W, H), (248, 244, 230))
    d = ImageDraw.Draw(img)
    ink = (20, 20, 24)
    rule = (20, 20, 24)
    ART_BOXES = []

    # ---- masthead
    d.rectangle([0, 0, W, 88], fill=(24, 24, 30))
    vgrad(d, [0, 0, W, 88], (30, 30, 38), (18, 18, 24))
    text(d, (W / 2, 10), "THE SATURDAY GLOBE", F(SERIF, 40), (250, 240, 210),
         anchor="ma")
    text(d, (W / 2, 56),
         "35 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
         F(SANS_B, 14), (255, 210, 90), anchor="ma")
    text(d, (W / 2, 74),
         "COP31 in overtime  ·  Missiles over Riyadh  ·  A boy and a paramedic die in Kryvyi Rih",
         F(SANS, 11), (220, 220, 215), anchor="ma")

    # ---- region strip
    y = 92
    d.rectangle([12, y, 1012, y + 26], fill=(255, 255, 255), outline=rule, width=1)
    x = 22
    seg = (1012 - 12 - 20) / 7
    for i, (name, c) in enumerate(REGIONS):
        col = REGION_COLOURS[name]
        d.rectangle([x, y + 4, x + 14, y + 22], fill=col)
        text(d, (x + 19, y + 5), f"{name} {c}", F(SANS_B, 12), ink)
        x += seg
    d.line([(12, y + 26), (1012, y + 26)], fill=rule, width=1)

    # ---- lead cards
    ly, lh, lw = 124, 202, 328
    for i, s in enumerate(LEADS):
        x0 = 12 + i * (lw + 8)
        x1 = x0 + lw
        d.rectangle([x0, ly, x1, ly + lh], fill=(255, 255, 255), outline=rule,
                    width=2)
        art(img, s["art"], (x0 + 2, ly + 2, x1 - 2, ly + 96), rng)
        ART_BOXES.append((x0 + 2, ly + 2, x1 - 2, ly + 96))
        badge(d, x0 + 8, ly + 8, s["n"], 24)
        tx = x0 + 10
        ty = ly + 104
        text(d, (tx, ty), f"{s['place']}  ·  {s['cat']}", F(SANS_B, 10),
             REGION_COLOURS[s["region"]])
        ty += 15
        for ln in wrap(d, s["head"], F(SERIF, 17), lw - 20)[:2]:
            text(d, (tx, ty), ln, F(SERIF, 17), ink)
            ty += 19
        ty += 2
        for ln in wrap(d, s["body"], F(SANS, 11), lw - 20)[:2]:
            text(d, (tx, ty), ln, F(SANS, 11), (50, 50, 55))
            ty += 13
        source_tag(d, tx, ly + lh - 14, s["src"])
        chip(d, x1 - 78, ly + lh - 15, s["chip"])

    # ---- feature cards (2 rows x 5)
    fy, fh, fw, gap = 330, 121, 198, 6
    for i, s in enumerate(FEATURES):
        r, c = divmod(i, 5)
        x0 = 12 + c * (fw + gap)
        x1 = x0 + fw
        y0 = fy + r * (fh + 4)
        d.rectangle([x0, y0, x1, y0 + fh], fill=(255, 255, 255), outline=rule,
                    width=1)
        art(img, s["art"], (x0 + 1, y0 + 1, x1 - 1, y0 + 34), rng)
        ART_BOXES.append((x0 + 1, y0 + 1, x1 - 1, y0 + 34))
        badge(d, x0 + 5, y0 + 5, s["n"], 18)
        tx = x0 + 7
        ty = y0 + 38
        text(d, (tx, ty), f"{s['place']} · {s['cat']}", F(SANS_B, 8),
             REGION_COLOURS[s["region"]])
        ty += 11
        for ln in wrap(d, s["head"], F(SERIF, 12), fw - 14)[:2]:
            text(d, (tx, ty), ln, F(SERIF, 12), ink)
            ty += 13
        for ln in wrap(d, s["body"], F(SANS, 9), fw - 14)[:2]:
            text(d, (tx, ty), ln, F(SANS, 9), (55, 55, 60))
            ty += 11
        source_tag(d, tx, y0 + fh - 13, s["src"])
        chip(d, x1 - 62, y0 + fh - 14, s["chip"])

    # ---- numbers strip
    ny = 580
    d.rectangle([12, ny, 1012, ny + 44], fill=(24, 24, 30))
    text(d, (22, ny + 4), "THE DAY\nIN NUMBERS", F(SANS_B, 10), (255, 210, 90))
    seg = (1012 - 130) / 6
    for i, (big, small) in enumerate(NUMBERS):
        cx = 140 + i * seg + seg / 2
        text(d, (cx, ny + 2), big, F(SERIF, 22), (255, 255, 255), anchor="ma")
        for j, ln in enumerate(small.split("\n")):
            text(d, (cx, ny + 25 + j * 9), ln, F(SANS, 8), (200, 200, 195),
                 anchor="ma")

    # ---- map + date check
    my = 628
    draw_map(d, (12, my, 640, my + 132), rng)
    dx0, dx1 = 650, 1012
    d.rectangle([dx0, my, dx1, my + 132], fill=(255, 250, 220), outline=rule,
                width=2)
    text(d, (dx0 + 10, my + 6), "DATE CHECK — left out on purpose",
         F(SANS_B, 12), (178, 58, 44))
    text(d, (dx0 + 10, my + 23),
         "These stories are real, but they are NOT from 21 November.",
         F(SANS, 10), (60, 55, 45))
    yy = my + 40
    for name, when in DATECHECK:
        d.ellipse([dx0 + 12, yy + 2, dx0 + 20, yy + 10], fill=(178, 58, 44))
        text(d, (dx0 + 26, yy), name, F(SANS, 11), ink)
        text(d, (dx1 - 10, yy), when, F(SANS_B, 11), (178, 58, 44), anchor="ra")
        yy += 14
    text(d, (dx0 + 10, my + 124),
         "Checked against the day's wires before printing.",
         F(SANS, 9), (90, 85, 75))

    # ---- briefs
    by = 766
    text(d, (12, by), "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES",
         F(SANS_B, 13), ink)
    d.line([(12, by + 18), (1012, by + 18)], fill=rule, width=2)
    yy = by + 24
    for i, s in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        x0 = 12 + col * 502
        y0 = yy + row * 18
        text(d, (x0, y0), f"{s['n']}.", F(SANS_B, 11), (178, 58, 44))
        srcw = d.textlength(f"({s['src']})", font=F(SANS, 9)) + 6
        maxw = 502 - 30 - srcw
        head = s["head"]
        while d.textlength(head, font=F(SANS, 11)) > maxw and len(head) > 10:
            head = head[:-2] + "…"
        text(d, (x0 + 26, y0), head, F(SANS, 11), ink)
        text(d, (x0 + 502 - 6, y0), f"({s['src']})", F(SANS, 9), (90, 90, 90),
             anchor="ra")

    # ---- footer
    fy2 = 992
    d.line([(12, fy2), (1012, fy2)], fill=rule, width=2)
    text(d, (12, fy2 + 5),
         "Every story here happened, or was first reported, on Saturday 21 November 2026.",
         F(SANS_B, 11), ink)
    text(d, (12, fy2 + 20),
         "Sources: AP · Reuters · AFP · USGS · ESA · Formula1.com · Al Arabiya · UKMTO · ESPNcricinfo · ABC · BBC · NYT · Al Jazeera — Original drawings.",
         F(SANS, 9), (80, 80, 85))
    text(d, (1012, fy2 + 5), "REPORTED = as reported today  ·  CONFIRMED = verified  ·  CLAIM = unverified claim",
         F(SANS, 8), (90, 90, 90), anchor="ra")

    img = grain(img, [(0, 0, W, 88), (12, 580, 1012, 624), (12, 628, 640, 760)]
                + ART_BOXES)
    img.save(OUT, optimize=True, compress_level=9)
    return img


if __name__ == "__main__":
    im = render()
    from PIL import Image as _I
    im2 = _I.open(OUT)
    print("size:", im2.size, "bytes:", __import__("os").path.getsize(OUT),
          "colours:", len(im2.getcolors(maxcolors=1 << 24) or []))
