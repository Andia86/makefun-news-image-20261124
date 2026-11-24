#!/usr/bin/env python3
"""Renderer for 'THE DAY IN WORLD NEWS' — Tuesday 24 November 2026.

Draws a flat broadsheet front page at 2048x2048 with PIL and downscales it
to 1024x1024, writing entry.png next to this file. All artwork is original:
flat shapes drawn here, no external images. Story data lives in LEADS and
BRIEFS below and matches NEWS_SOURCES.md number for number.

Pass 2 layout: tighter vertical budget so headlines never touch summaries,
briefs fit above the footer, and the timeline clears the date-check box.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = 2048
H = 2048

CREAM = (247, 241, 227)
PAPER = (253, 250, 240)
NAVY = (16, 42, 84)
RED = (178, 34, 44)
INK = (28, 28, 30)
GREY = (96, 96, 100)
GOLD = (198, 148, 42)
TEAL = (24, 110, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, start_size, max_w, max_lines, min_size=20):
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 2
    fnt = font(path, min_size)
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def one_line(draw, text, path, start_size, max_w, min_size=18):
    """Fit text on one line, shrinking then ellipsising if needed."""
    size = start_size
    while size > min_size:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt, text
        size -= 1
    fnt = font(path, min_size)
    while text and draw.textlength(text + "…", font=fnt) > max_w:
        text = text.rsplit(" ", 1)[0] if " " in text else text[:-1]
    return fnt, text + "…"


# ---------------------------------------------------------------- stories
# (num, region, field, headline, one-line summary, source, icon)
LEADS = [
    (1, "AMERICAS", "ECONOMY", "Nvidia reinstates Huang as CEO; markets soar",
     "Shares jump 30%+; Nasdaq +6.51%", "Reuters", "chart"),
    (2, "ASIA", "POLITICS", "14 nations back ICJ genocide ruling on Myanmar",
     "Ministers call the Rohingya judgment binding", "UN News", "gavel"),
    (3, "AFRICA", "CONFLICT", "Libya demands Kyiv explain strike on Russian ships",
     "Tripoli seeks answers; UN urges a probe", "AFP", "ship"),
    (4, "OCEANIA", "CLIMATE", "COP31 talks end with no deal in Antalya",
     "Pacific leaders say islands are left exposed", "PINA", "globe"),
    (5, "EUROPE", "CONFLICT", "Kyiv region strikes kill at least 14, Ukraine says",
     "Ukraine reports the toll near the capital", "AFP", "burst"),
    (6, "GLOBAL", "SCIENCE / TECH", "UN chief seeks AI risk framework within a year",
     "Guterres asks states to agree AI guardrails", "AP", "robot"),
    (7, "ASIA", "ECONOMY", "Japan cuts view on consumer spending",
     "First downgrade since 2024, on prices", "Reuters", "cart"),
    (8, "AMERICAS", "CONFLICT", "Car bomb hits government HQ in Villavicencio",
     "Dozens hurt in Colombia, officials say", "The Hindu", "bomb"),
    (9, "ASIA", "DISASTER", "Magnitude 5.6 quake strikes Nepal",
     "Tremor in Koshi province, near China border", "EMSC", "wave"),
    (10, "OCEANIA", "CLIMATE", "Fiji closes all schools as drought deepens",
     "Five-day closure from 30 Nov, El Nino crisis", "PINA", "sun"),
    (11, "AFRICA", "SPORT", "Sports court rules on Senegal's AFCON title today",
     "CAS verdict due on the stripped 2025 title", "CAS / BBC", "trophy"),
    (12, "AMERICAS", "SCIENCE / TECH", "US states sue Musk firms over Grok images",
     "Suit alleges sexualised AI images, AP says", "AP", "phone"),
]

# (num, short headline, region tag, source)
BRIEFS = [
    (13, "360,000+ displaced in Yemen since Aug — UN", "MID EAST", "UN"),
    (14, "Merz: Europe ready to negotiate with Russia", "EUROPE", "Anadolu"),
    (15, "NATO chief: defence pledge covers space", "EUROPE", "Anadolu"),
    (16, "Türkiye builds safe Black Sea shipping plan", "MID EAST", "Anadolu"),
    (17, "UN: Black Sea attacks drive food insecurity", "EUROPE", "UN"),
    (18, "EU lists The Base founder on terror sanctions", "EUROPE", "EU Council"),
    (19, "Finland summons Russian ambassador", "EUROPE", "Anadolu"),
    (20, "Iraq, Egypt agree to boost economic ties", "MID EAST", "Anadolu"),
    (21, "S. Korea jets scramble as Russian planes enter zone", "ASIA", "Japan Times"),
    (22, "Seoul: N. Korean aircraft breach near Ulleung", "ASIA", "TOI Live"),
    (23, "N. Korea threatens to close Swiss office", "ASIA", "AFP"),
    (24, "Indonesia charges ex-police chief with treason", "ASIA", "Japan Times"),
    (25, "Prabowo names Indonesia VP picks", "ASIA", "Japan Times"),
    (26, "Hasina seeks return to Bangladesh on 16 Dec", "ASIA", "Reuters"),
    (27, "China sentences official to death for spying", "ASIA", "AP"),
    (28, "US blacklists Megaspeed after Nvidia case", "ASIA", "Japan Times"),
    (29, "India invokes 1943 Bengal famine at the UN", "ASIA", "TOI Live"),
    (30, "India gives $1.62bn package to flood-hit Nepal", "ASIA", "Reuters"),
    (31, "Magnitude 4.1 earthquake strikes Pakistan", "ASIA", "NCS / TOI"),
    (32, "Trump pauses Iowa explosives detonation", "AMERICAS", "AP"),
    (33, "Trump orders federal executions expedited", "AMERICAS", "AFP"),
    (34, "Rep. Gomez resigns after ethics findings", "AMERICAS", "AP"),
    (35, "US drone aided Sinaloa capture, AP reports", "AMERICAS", "AP"),
    (36, "Storms, glitches threaten Thanksgiving travel", "AMERICAS", "AP"),
    (37, "Honda recalls 810,592 US vehicles — airbags", "AMERICAS", "TOI Live"),
    (38, "IDB eyes up to $6bn in loans for Venezuela", "AMERICAS", "TOI Live"),
    (39, "2031 Women's World Cup: US, Mexico, Costa Rica, Jamaica", "AMERICAS", "FIFA"),
    (40, "Commanders rally past Bengals at the death", "AMERICAS", "Japan Times"),
    (41, "Zaporizhzhia hit again in night attacks", "EUROPE", "AFP"),
    (42, "Drones hit homes, UN building in Khartoum", "AFRICA", "AFP"),
    (43, "Gaza strikes kill 3 incl. UNRWA worker — reports", "MID EAST", "Al Jazeera"),
    (44, "Oxfam calls Gaza a 'toxic land' in report", "MID EAST", "Oxfam"),
    (45, "Iran: singer Ahmadi sentenced to 74 lashes", "MID EAST", "Reports"),
    (46, "US envoy unsure Israel aid ends this year", "MID EAST", "Reuters"),
    (47, "Moscow: Estonia acts 'on verge of open war'", "EUROPE", "Reuters"),
    (48, "Solomons drop China deal for Australia treaty", "OCEANIA", "ABC Aust."),
    (49, "Australia coalition opposes Vanuatu deal", "OCEANIA", "PINA"),
    (50, "Greece reopens oldest Acropolis museum", "EUROPE", "AP"),
    (51, "Pope Francis's private diary published", "EUROPE", "AP"),
    (52, "Japan factory PMI rises to 53.7 in November", "ASIA", "Reuters"),
]

# pin positions for leads on the map panel, panel-relative 0..1000 x 0..560
PINS = {
    1: (105, 205), 2: (720, 285), 3: (505, 215), 4: (925, 390),
    5: (540, 125), 6: (215, 155), 7: (805, 180), 8: (175, 335),
    9: (665, 225), 10: (962, 435), 11: (450, 270), 12: (190, 228),
}


def draw_icon(d, kind, x, y, s):
    """Simple flat icons drawn with PIL shapes inside box (x, y, s, s)."""
    cx, cy = x + s // 2, y + s // 2
    if kind == "chart":
        d.line([(x + 6, y + s - 10), (x + s - 6, y + s - 10)], fill=NAVY, width=5)
        for i, hgt in enumerate((0.3, 0.55, 0.85)):
            bx = x + 10 + i * (s // 3)
            d.rectangle([bx, y + s - 10 - int(s * hgt), bx + s // 5, y + s - 10], fill=TEAL)
        d.line([(x + 8, y + s - 22), (x + s // 2, y + s // 3), (x + s - 9, y + 8)], fill=RED, width=6)
    elif kind == "gavel":
        d.rectangle([x + 10, y + 12, x + s - 14, y + 28], fill=GOLD, outline=NAVY, width=4)
        d.line([(x + s // 2, y + 24), (x + s - 14, y + s - 18)], fill=NAVY, width=8)
        d.line([(x + 8, y + s - 8), (x + s - 8, y + s - 8)], fill=RED, width=7)
    elif kind == "ship":
        d.polygon([(x + 8, y + s - 24), (x + s - 8, y + s - 24), (x + s - 20, y + s - 6), (x + 20, y + s - 6)], fill=NAVY)
        d.rectangle([x + s // 2 - 5, y + 10, x + s // 2 + 5, y + s - 24], fill=RED)
        d.polygon([(x + s // 2 + 5, y + 12), (x + s - 12, y + s - 26), (x + s // 2 + 5, y + s - 26)], fill=GOLD)
    elif kind == "globe":
        d.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=TEAL, width=6)
        d.line([(x + 6, cy), (x + s - 6, cy)], fill=TEAL, width=4)
        d.ellipse([cx - s // 5, y + 6, cx + s // 5, y + s - 6], outline=TEAL, width=4)
        d.polygon([(cx - 5, y), (cx + 13, y + 20), (cx - 13, y + 20)], fill=RED)
    elif kind == "burst":
        pts = []
        for i in range(16):
            r = s * 0.48 if i % 2 == 0 else s * 0.22
            a = math.pi * i / 8
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=RED)
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=GOLD)
    elif kind == "robot":
        d.rounded_rectangle([x + 12, y + 18, x + s - 12, y + s - 10], 9, fill=NAVY)
        d.line([(cx, y + 18), (cx, y + 4)], fill=NAVY, width=6)
        d.ellipse([cx - 5, y, cx + 5, y + 10], fill=RED)
        d.ellipse([x + 24, cy - 3, x + 36, cy + 9], fill=CREAM)
        d.ellipse([x + s - 36, cy - 3, x + s - 24, cy + 9], fill=CREAM)
    elif kind == "cart":
        d.polygon([(x + 8, y + 16), (x + 20, y + 16), (x + 27, y + s - 22), (x + s - 12, y + s - 22), (x + s - 6, y + 27), (x + 23, y + 27)], outline=NAVY, width=6)
        d.ellipse([x + 25, y + s - 18, x + 39, y + s - 4], fill=RED)
        d.ellipse([x + s - 36, y + s - 18, x + s - 22, y + s - 4], fill=RED)
        d.line([(x + 33, y + s // 2), (x + s - 20, y + s // 2)], fill=TEAL, width=5)
    elif kind == "bomb":
        d.ellipse([x + 14, y + 19, x + s - 14, y + s - 7], fill=INK)
        d.rectangle([cx - 7, y + 8, cx + 7, y + 22], fill=GREY)
        d.arc([cx - 3, y - 5, cx + 28, y + 18], start=270, end=360, fill=RED, width=5)
        d.polygon([(cx + 25, y - 3), (cx + 32, y + 7), (cx + 21, y + 8)], fill=GOLD)
    elif kind == "wave":
        for i in range(3):
            yy = y + 17 + i * (s // 4)
            d.arc([x + 4, yy - 11, x + s // 2, yy + 11], 180, 360, fill=TEAL, width=6)
            d.arc([x + s // 2 - 4, yy - 11, x + s - 4, yy + 11], 0, 180, fill=TEAL, width=6)
        d.line([(x + 6, y + s - 7), (x + s - 6, y + s - 7)], fill=RED, width=5)
    elif kind == "sun":
        d.ellipse([cx - s // 4, cy - s // 4, cx + s // 4, cy + s // 4], fill=GOLD)
        for i in range(8):
            a = math.pi * i / 4
            d.line([(cx + (s // 4 + 3) * math.cos(a), cy + (s // 4 + 3) * math.sin(a)),
                    (cx + (s // 2 - 3) * math.cos(a), cy + (s // 2 - 3) * math.sin(a))], fill=RED, width=6)
    elif kind == "trophy":
        d.polygon([(x + 19, y + 8), (x + s - 19, y + 8), (x + s - 24, y + s // 2), (x + 24, y + s // 2)], fill=GOLD, outline=NAVY, width=4)
        d.arc([x + 2, y + 6, x + 24, y + 36], 90, 270, fill=NAVY, width=5)
        d.arc([x + s - 24, y + 6, x + s - 2, y + 36], 270, 90, fill=NAVY, width=5)
        d.rectangle([cx - 5, y + s // 2, cx + 5, y + s - 16], fill=NAVY)
        d.rectangle([x + 19, y + s - 14, x + s - 19, y + s - 6], fill=RED)
    elif kind == "phone":
        d.rounded_rectangle([cx - s // 4, y + 6, cx + s // 4, y + s - 6], 9, outline=NAVY, width=6)
        d.rectangle([cx - s // 4 + 7, y + 18, cx + s // 4 - 7, y + s - 21], fill=TEAL)
        d.ellipse([cx - 4, y + s - 18, cx + 4, y + s - 10], fill=RED)


def draw_map(d, x, y, w, h):
    """Simplified world map: flat continent polygons + numbered pins."""
    d.rounded_rectangle([x, y, x + w, y + h], 12, fill=(226, 233, 240), outline=NAVY, width=3)
    land = (150, 175, 150)

    def P(pts):
        return [(x + px * w / 1000, y + py * h / 560) for px, py in pts]

    d.polygon(P([(60, 120), (300, 90), (330, 170), (260, 230), (230, 300), (150, 290), (90, 210)]), fill=land)
    d.polygon(P([(215, 320), (300, 310), (330, 420), (280, 520), (235, 470), (205, 380)]), fill=land)
    d.polygon(P([(455, 110), (560, 95), (585, 160), (540, 200), (480, 185), (450, 150)]), fill=land)
    d.polygon(P([(450, 215), (580, 205), (610, 330), (560, 470), (490, 480), (445, 330)]), fill=land)
    d.polygon(P([(590, 110), (880, 100), (905, 210), (820, 260), (700, 300), (610, 220), (585, 160)]), fill=land)
    d.polygon(P([(770, 330), (905, 320), (920, 420), (830, 460), (765, 410)]), fill=land)
    d.polygon(P([(930, 430), (975, 425), (980, 470), (940, 475)]), fill=land)
    for num, (px, py) in PINS.items():
        cx, cy = x + px * w / 1000, y + py * h / 560
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=RED, outline=PAPER, width=3)
        t = str(num)
        fnt = font(SANS_B, 25 if len(t) == 1 else 21)
        tw = d.textlength(t, font=fnt)
        d.text((cx - tw / 2, cy - 13), t, font=fnt, fill=(255, 255, 255))
    # title plate
    t = "WHERE IT HAPPENED — LEADS 1–12"
    fnt = font(SANS_B, 27)
    tw = d.textlength(t, font=fnt)
    d.rectangle([x + 10, y + 8, x + 22 + tw, y + 46], fill=(226, 233, 240))
    d.text((x + 16, y + 12), t, font=fnt, fill=NAVY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 36

    # ---- masthead
    d.rectangle([0, 0, W, 128], fill=NAVY)
    f = font(SERIF_B, 84)
    t = "THE DAY IN WORLD NEWS"
    d.text(((W - d.textlength(t, font=f)) / 2, 18), t, font=f, fill=(255, 255, 255))
    d.rectangle([0, 128, W, 140], fill=RED)

    # ---- date + count
    f = font(SERIF_B, 94)
    t = "Tuesday 24 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 150), t, font=f, fill=NAVY)
    d.rectangle([M, 262, W - M, 318], fill=RED)
    f = font(SANS_B, 41)
    t = "52 STORIES  ·  7 REGIONS  ·  ONE PAGE  ·  EVERY STORY SOURCED"
    d.text(((W - d.textlength(t, font=f)) / 2, 269), t, font=f, fill=(255, 255, 255))

    # ---- date check strip
    y0 = 332
    d.rounded_rectangle([M, y0, W - M, y0 + 80], 8, outline=NAVY, width=3)
    f = font(SANS_B, 30)
    d.text((M + 22, y0 + 7), "DATE CHECK ✓  Every story happened or was first reported on Tuesday 24 November 2026,", font=f, fill=NAVY)
    d.text((M + 22, y0 + 43), "checked against Reuters, AP, AFP and regional wires carrying 24 Nov datelines and timestamps.", font=f, fill=INK)

    # ---- UTC timeline
    d.text((M, 426), "THE DAY IN UTC", font=font(SANS_B, 29), fill=RED)
    events = [
        ("00:23", "Gold edges up\nReuters GMT stamp"),
        ("00:35", "Japan flash PMI 53.7\npublished, Reuters"),
        ("DAY", "UN: 360,000 displaced\nin Yemen since August"),
        ("PM GMT", "CAS verdict due on\nSenegal AFCON title"),
        ("CLOSE", "S&P +4.73% · Nasdaq\n+6.51% · Nikkei +3.91%"),
    ]
    tx0, tx1, ty = M + 320, W - M - 130, 478
    d.line([(tx0, ty), (tx1, ty)], fill=NAVY, width=5)
    step = (tx1 - tx0) / (len(events) - 1)
    for i, (hh, label) in enumerate(events):
        cx = tx0 + i * step
        d.ellipse([cx - 11, ty - 11, cx + 11, ty + 11], fill=RED)
        fh = font(SANS_B, 26)
        tw = d.textlength(hh, font=fh)
        d.text((cx - tw / 2, ty - 44), hh, font=fh, fill=NAVY)
        fl = font(SANS, 22)
        for j, ln in enumerate(label.split("\n")):
            tw = d.textlength(ln, font=fl)
            d.text((cx - tw / 2, ty + 15 + j * 26), ln, font=fl, fill=INK)

    # ---- lead cards: 3 x 4, each 140 tall
    gy = 548
    cols = 3
    gap = 14
    cw = (W - 2 * M - (cols - 1) * gap) // cols
    ch = 140
    for idx, (num, region, field, head, summ, src, icon) in enumerate(LEADS):
        r, c = divmod(idx, cols)
        x = M + c * (cw + gap)
        y = gy + r * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], 10, fill=PAPER, outline=NAVY, width=3)
        d.ellipse([x + 11, y + 10, x + 51, y + 50], fill=RED)
        fnt = font(SANS_B, 27 if num < 10 else 23)
        tw = d.textlength(str(num), font=fnt)
        d.text((x + 31 - tw / 2, y + 15), str(num), font=fnt, fill=(255, 255, 255))
        d.text((x + 62, y + 11), f"{region} · {field}", font=font(SANS_B, 23), fill=TEAL)
        d.text((x + 62, y + 35), f"via {src}", font=font(SANS, 20), fill=GREY)
        draw_icon(d, icon, x + 11, y + 58, 74)
        hx = x + 97
        maxw = x + cw - 12 - hx
        fh, lines = fit_lines(d, head, SANS_B, 29, maxw, 2, min_size=22)
        yy = y + 50
        for ln in lines:
            d.text((hx, yy), ln, font=fh, fill=INK)
            yy += fh.size + 3
        fs, stext = one_line(d, summ, SANS, 21, maxw)
        d.text((hx, y + ch - 25), stext, font=fs, fill=GREY)

    # ---- map band + markets box
    my = gy + 4 * ch + 3 * gap + 14
    mh = 156
    draw_map(d, M, my, 1230, mh)
    bx = M + 1250
    d.rounded_rectangle([bx, my, W - M, my + mh], 12, fill=NAVY)
    d.text((bx + 20, my + 9), "MARKETS · 24 NOV CLOSE", font=font(SANS_B, 26), fill=GOLD)
    rows_m = [("Nasdaq", "+6.51%"), ("S&P 500", "+4.73%"), ("Nikkei 225", "+3.91%"),
              ("FTSE 100", "+1.30%"), ("Brent crude", "$86.7 −3.0%"), ("US nat. gas", "$3.57 +12%")]
    yy = my + 44
    for name, val in rows_m:
        d.text((bx + 20, yy), name, font=font(SANS, 21), fill=(255, 255, 255))
        fv = font(SANS_B, 21)
        d.text((W - M - 20 - d.textlength(val, font=fv), yy), val, font=fv, fill=(255, 255, 255))
        yy += 18

    # ---- briefs
    by = my + mh + 14
    d.rectangle([M, by, W - M, by + 44], fill=NAVY)
    f = font(SANS_B, 31)
    t = "ALSO TODAY — 40 MORE STORIES, NUMBERED TO MATCH THE SOURCE LIST"
    d.text(((W - d.textlength(t, font=f)) / 2, by + 5), t, font=f, fill=(255, 255, 255))
    by += 56
    col_w = (W - 2 * M - 2 * gap) // 3
    per_col = [BRIEFS[:14], BRIEFS[14:27], BRIEFS[27:]]
    row_h = 42
    for ci, col in enumerate(per_col):
        x = M + ci * (col_w + gap)
        for ri, (num, head, region, src) in enumerate(col):
            y = by + ri * row_h
            d.text((x, y), f"{num}", font=font(SANS_B, 26), fill=RED)
            fh, htext = one_line(d, head, SANS_B, 24, col_w - 56, min_size=19)
            d.text((x + 52, y), htext, font=fh, fill=INK)
            d.text((x + 52, y + 25), f"{region} · {src}", font=font(SANS, 18), fill=GREY)
            if ri < len(col) - 1:
                d.line([(x, y + row_h - 4), (x + col_w - 6, y + row_h - 4)], fill=(210, 202, 180), width=2)

    # ---- footer
    fy = H - 46
    d.line([(M, fy - 8), (W - M, fy - 8)], fill=NAVY, width=3)
    t = ("Every story was reported on Tuesday 24 November 2026; disputed claims are attributed to their source. "
         "Sources: Reuters, AP, AFP, UN News, PINA, Japan Times, Al Jazeera, ABC Australia, The Hindu. Original drawings.")
    f, t = one_line(d, t, SANS, 22, W - 2 * M, min_size=15)
    d.text(((W - d.textlength(t, font=f)) / 2, fy), t, font=f, fill=INK)

    out = img.resize((1024, 1024), Image.LANCZOS)
    here = os.path.dirname(os.path.abspath(__file__))
    out.save(os.path.join(here, "entry.png"), optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
