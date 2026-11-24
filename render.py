#!/usr/bin/env python3
"""Render the Tuesday 24 November 2026 world-news front page (1024x1024).

Every story in this file was reported on Tuesday 24 November 2026 and is
date-checked in NEWS_SOURCES.md. Monday's news is named and excluded in
the DATE CHECK strip. Deterministic: pure PIL drawing, no clock, no
network, no randomness — two runs produce identical bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
CARD_BG = (255, 253, 246)
NAVY = (20, 38, 76)
RED = (179, 49, 42)
INK = (26, 26, 26)
MUTE = (90, 83, 72)
LINE = (201, 191, 168)
LAND = (214, 203, 172)
SEA = (233, 228, 210)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


CARDS = [
    # n, region tag, headline, summary, status, (lon, lat)
    (1, "ASIA · MARKETS", "Asia markets roar back",
     "Nikkei +3.91%, Kospi +6.3%, Taiex +9% as AI shares rally across the region.",
     "CONFIRMED", (139.7, 35.7)),
    (2, "ASIA · POLITICS", "China probes Politburo member Chen Jining",
     "Shanghai's party chief is the fourth top leader investigated since 2025.",
     "OFFICIAL", (121.5, 31.2)),
    (3, "EUROPE · WAR", "Russian strike kills 2 in Zaporizhzhia",
     "Overnight attack on flats wounds 22, incl. 2 children, officials say.",
     "REPORTED", (35.2, 47.8)),
    (4, "MIDDLE EAST · WAR", "Israel kills Hamas security chief in Gaza",
     "Airstrike kills Naeem Abu Nahel in Gaza City; medics count at least 6 dead.",
     "REPORTED", (34.3, 31.4)),
    (5, "ASIA · ECONOMY", "Japan cuts view of consumer spending",
     "First downgrade since Feb 2024, in Tuesday's monthly assessment.",
     "OFFICIAL", (133.5, 33.9)),
    (6, "ASIA · DISASTER", "M5.6 quake strikes Koshi, Nepal",
     "07:17 local, Taplejung area. Nepal centre 5.6; EMSC reads 5.3.",
     "CONFIRMED", (87.7, 27.4)),
    (7, "AFRICA · SPORT", "Senegal restored as Africa Cup champions",
     "CAS upholds Senegal's appeal; the 1-0 final win over Morocco stands.",
     "OFFICIAL", (-17.4, 14.7)),
    (8, "AMERICAS · ECONOMY", "Venezuela puts its debt at $237.5bn",
     "First full economic framework in years could anchor a giant restructuring.",
     "OFFICIAL", (-66.9, 10.5)),
    (9, "MIDDLE EAST · POLITICS", "Iraq orders takeover of Kurd crossings",
     "Baghdad to run all border crossings and Kurdish-held oilfields.",
     "OFFICIAL", (44.4, 33.3)),
    (10, "ASIA · SECURITY", "Korea jets scramble as Russian planes enter zone",
     "No breach of airspace; Ulleung alert was an error, lifted in minutes.",
     "OFFICIAL", (126.8, 37.9)),
    (11, "OCEANIA · DIPLOMACY", "Solomons to swap China pact for Australia treaty",
     "Honiara moves to replace its Beijing security deal, Reuters reports.",
     "REPORTED", (159.9, -9.6)),
    (12, "EUROPE · SANCTIONS", "UK designates the Houthis, sanctions four chiefs",
     "Britain acts under its Yemen regime over torture and abuse claims.",
     "OFFICIAL", (-0.1, 51.5)),
]

BRIEFS = [
    "Japan flash PMI 53.7, factories growing",
    "Hasina seeks return, aide tells Reuters",
    "Pope Francis's private diary published",
    "Wang Yi urges UK to back free trade",
    "China extends gallium suspension to Jan 27",
    "Berlin 'shocked' by Trump's Nvidia move",
    "Hungary's Magyar meets Zelenskiy",
    "UK warns Ukraine suppliers of sabotage",
    "Kyiv: Libya strike was self-defence — FM",
    "N. Korea threatens to close Swiss office",
    "Russia downed nearly 700 Ukraine drones",
    "Gavi: 1.5m Bundibugyo doses for Congo",
    "Norway in dialogue with Ukraine — minister",
    "UN: five women killed hourly by kin",
    "Malaysia seeks homes for Rohingya",
    "Japan speeds ICC support — Takaichi",
    "Anwar: China easier than US on tech",
    "Hanoi blast kills 6, injures a dozen",
    "Indonesia fire toll rises to 26 — police",
    "Serbia school shooting: two staff hurt",
    "US bird flu: 3 cases in Washington, 1 dead",
    "China names Shenzhou-24 crew for launch",
    "UN: HIV infections may rise from lows",
    "William pays first visit to No 10",
    "Trump set to pardon turkeys Freedom, Feathers",
    "Sooryavanshi, 15, hits 204 off 53 balls",
    "Sanofi to buy Insmed in $41bn deal",
    "Kingfisher lifts profit outlook on UK sales",
    "Best Buy beats forecasts, raises outlook",
    "Germany's Ifo index rises to 90.6",
    "Pound climbs off 19-month low",
    "Oil slips to near three-month low",
    "Gold slips as Fed hike bets build",
    "Bitcoin falls back below $60,000",
    "Wall St futures dip as chip rally cools",
    "Bayer to pull kidney drug Kerendia in Germany",
    "Anthropic stock drops below IPO price",
    "US bill aims to ease addiction-drug access",
    "EU votes to expand carbon reserve",
    "EU backs digital product manuals, 622-2",
]

TIMELINE = [
    ("00:35", "Japan flash PMI prints 53.7"),
    ("01:32", "M5.6 quake in Koshi, Nepal (07:17 local)"),
    ("06:00", "Nikkei closes +3.91% in Tokyo"),
    ("07:52 KST", "Ulleung alert an error (22:52 GMT Mon)"),
    ("12:03", "UK designates the Houthis"),
    ("13:43", "CAS restores Senegal's title, Lausanne"),
]

# Rough equirectangular continent outlines as (lon, lat) polygons.
EURASIA = [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50),
           (5, 53), (8, 55), (8, 57), (13, 55), (18, 56), (21, 59),
           (24, 59), (28, 60), (30, 65), (35, 68), (50, 68), (70, 70),
           (90, 72), (110, 72), (130, 72), (150, 71), (170, 70),
           (178, 65), (178, 62), (162, 60), (155, 58), (142, 54),
           (141, 50), (135, 44), (129, 41), (126, 40), (122, 38),
           (121, 35), (122, 31), (120, 27), (114, 22), (108, 17),
           (106, 9), (104, 3), (100, 7), (98, 13), (94, 16), (91, 22),
           (88, 21), (85, 19), (80, 15), (77, 8), (75, 13), (72, 20),
           (68, 23), (66, 25), (61, 25), (57, 26), (54, 26), (51, 28),
           (48, 30), (50, 27), (52, 25), (55, 24), (58, 23), (59, 22),
           (55, 17), (52, 15), (48, 14), (44, 13), (43, 12), (40, 15),
           (38, 20), (36, 24), (34, 28), (36, 31), (36, 36), (33, 36),
           (30, 36), (27, 37), (23, 36), (19, 40), (15, 38), (12, 39),
           (10, 37), (8, 37), (3, 37)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 55), (-8, 56), (-6, 58), (-3, 58),
           (-1, 54), (-2, 51)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40),
         (142, 44), (143, 43), (141, 39), (140, 35), (136, 33),
         (132, 32)]
NAMERICA = [(-165, 68), (-140, 70), (-120, 71), (-105, 68), (-92, 66),
            (-82, 62), (-79, 57), (-86, 51), (-92, 47), (-88, 43),
            (-83, 41), (-76, 37), (-71, 41), (-68, 44), (-61, 46),
            (-66, 50), (-72, 55), (-82, 59), (-95, 62), (-110, 64),
            (-125, 66), (-150, 64), (-165, 60)]
SAMERICA = [(-79, 9), (-72, 12), (-62, 10), (-50, 4), (-44, -3),
            (-35, -8), (-39, -20), (-52, -27), (-60, -36), (-65, -41),
            (-72, -50), (-74, -52), (-73, -44), (-72, -30), (-70, -18),
            (-77, -12), (-81, -4), (-77, 4)]
AFRICA = [(-6, 35), (10, 37), (20, 32), (30, 31), (35, 28), (38, 22),
          (40, 15), (43, 12), (48, 11), (51, 12), (48, 5), (42, -2),
          (40, -10), (38, -18), (36, -26), (32, -29), (26, -34),
          (20, -35), (17, -32), (15, -27), (13, -18), (12, -10),
          (13, -2), (9, 4), (4, 6), (-3, 5), (-8, 5), (-13, 8),
          (-17, 12), (-17, 15), (-16, 20), (-15, 25), (-13, 28),
          (-10, 31)]
NEWGUINEA = [(131, -1), (138, -2), (145, -4), (150, -8), (146, -9),
             (138, -7), (132, -4)]
AUSTRALIA = [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32),
             (132, -32), (135, -35), (138, -36), (140, -38), (145, -38),
             (150, -37), (153, -30), (153, -25), (150, -22), (146, -19),
             (142, -15), (142, -11), (137, -12), (136, -15), (135, -12),
             (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)]


def draw_map(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SEA, outline=LINE)
    sx = (x1 - x0) / 360.0
    sy = (y1 - y0) / 140.0

    def px(lon, lat):
        return (x0 + (lon + 180) * sx, y0 + (82 - lat) * sy)

    for poly in (EURASIA, BRITAIN, JAPAN, NAMERICA, SAMERICA, AFRICA,
                 NEWGUINEA, AUSTRALIA):
        d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=MUTE)
    # Island dots for SE Asia / Oceania texture.
    for lon, lat in ((100, 0), (107, -6), (113, -2), (120, -2),
                     (125, -1), (168, -46), (173, -41), (160, -10)):
        cx, cy = px(lon, lat)
        d.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=LAND, outline=MUTE)
    fnum = F(SANS_B, 9)
    for n, _tag, _h, _s, _st, (lon, lat) in CARDS:
        cx, cy = px(lon, lat)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=fnum)
        d.text((cx - tw / 2, cy - 5), t, font=fnum, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 58], fill=NAVY)
    d.text((16, 12), "THE DAY IN WORLD NEWS", font=F(SERIF_B, 30),
           fill=(247, 241, 227))
    right = "52 STORIES · 6 CONTINENTS · ONE DAY"
    fr = F(SANS_B, 15)
    d.text((W - 16 - d.textlength(right, font=fr), 22), right, font=fr,
           fill=(232, 205, 130))

    # Date line
    d.text((16, 64), "TUESDAY 24 NOVEMBER 2026", font=F(SERIF_B, 38),
           fill=NAVY)
    sub = "One page · every story dated & checked"
    fs = F(SANS, 13)
    d.text((W - 16 - d.textlength(sub, font=fs), 84), sub, font=fs,
           fill=MUTE)
    d.line([16, 106, W - 16, 106], fill=NAVY, width=2)

    # DATE CHECK strip
    d.rectangle([16, 112, W - 16, 156], outline=RED, width=2)
    fdc = F(SANS, 12)
    dc = ("DATE CHECK — Left out on purpose: Nvidia reinstates Huang and "
          "the US market surge, the Grok-image lawsuits, FIFA's 2031/2035 "
          "host votes and the Merz–Rutte pledges — all Monday 23 November "
          "news, not Tuesday's.")
    lines = wrap(d, dc, fdc, W - 48)
    for i, ln in enumerate(lines[:2]):
        d.text((24, 118 + i * 17), ln, font=fdc, fill=RED if i == 0 else INK)

    # Cards: 4 cols x 3 rows
    cx0, cy0, cw, chh, gx, gy = 16, 164, 242, 118, 8, 6
    ftag = F(SANS_B, 10)
    fhead = F(SERIF_B, 15)
    fsum = F(SANS, 11)
    fchip = F(SANS_B, 11)
    fstat = F(SANS_B, 9)
    for idx, (n, tag, head, summ, stat, _ll) in enumerate(CARDS):
        cx = cx0 + (idx % 4) * (cw + gx)
        cy = cy0 + (idx // 4) * (chh + gy)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD_BG, outline=LINE)
        d.rectangle([cx, cy, cx + 24, cy + 24], fill=NAVY)
        t = str(n)
        d.text((cx + 12 - d.textlength(t, font=fchip) / 2, cy + 5), t,
               font=fchip, fill=(255, 255, 255))
        d.text((cx + 32, cy + 7), tag, font=ftag, fill=RED)
        yy = cy + 30
        for ln in wrap(d, head, fhead, cw - 16)[:2]:
            d.text((cx + 8, yy), ln, font=fhead, fill=INK)
            yy += 19
        yy += 2
        for ln in wrap(d, summ, fsum, cw - 16)[:3]:
            d.text((cx + 8, yy), ln, font=fsum, fill=(52, 48, 42))
            yy += 14
        d.text((cx + 8, cy + chh - 15), stat, font=fstat, fill=MUTE)

    # Mid band: map left, timeline + markets right
    my0 = 534
    d.text((16, my0), "WHERE IT HAPPENED — pins match the cards",
           font=F(SANS_B, 12), fill=NAVY)
    draw_map(d, 16, my0 + 20, 590, my0 + 158)
    rx = 602
    d.text((rx, my0), "TUESDAY IN UTC", font=F(SANS_B, 12), fill=NAVY)
    ftl = F(SANS, 11)
    ftlb = F(SANS_B, 11)
    yy = my0 + 20
    for tstamp, txt in TIMELINE:
        d.text((rx, yy), tstamp, font=ftlb, fill=RED)
        d.text((rx + 74, yy), txt, font=ftl, fill=INK)
        yy += 14
    myy = yy + 4
    d.rectangle([rx, myy, W - 16, myy + 52], outline=LINE)
    d.text((rx + 8, myy + 4), "MARKETS", font=F(SANS_B, 11), fill=NAVY)
    fm = F(SANS, 10)
    d.text((rx + 8, myy + 21),
           "ASIA CLOSE TUE — Nikkei +3.91% · Kospi +6.3% · Taiex +9%",
           font=fm, fill=INK)
    d.text((rx + 8, myy + 36),
           "US & LONDON CLOSE MON — Nasdaq +6.51% · S&P 500 +4.73% · FTSE +1.30%",
           font=fm, fill=MUTE)

    # Briefs: 3 columns, numbers 13..52
    by0 = 706
    d.line([16, by0 - 6, W - 16, by0 - 6], fill=NAVY, width=2)
    d.text((16, by0), "THE REST OF TUESDAY — FORTY MORE, EVERY ONE DATED",
           font=F(SANS_B, 12), fill=NAVY)
    fb = F(SANS, 12)
    fnb = F(SANS_B, 12)
    numbered = [(13 + i, b) for i, b in enumerate(BRIEFS)]
    cols = [numbered[:14], numbered[14:27], numbered[27:]]
    colw = (W - 32 - 20) // 3
    for ci, col in enumerate(cols):
        xx = 16 + ci * (colw + 10)
        yy = by0 + 24
        for n, b in col:
            ns = str(n) + " "
            d.text((xx, yy), ns, font=fnb, fill=RED)
            off = d.textlength(ns, font=fnb)
            budget = colw - off - 2
            use = fb if d.textlength(b, font=fb) <= budget else F(SANS, 10)
            d.text((xx + off, yy), b, font=use, fill=INK)
            yy += 17

    # Footer
    d.line([16, 972, W - 16, 972], fill=NAVY, width=2)
    ff = F(SANS, 10)
    l1 = ("Every story was reported on Tuesday 24 November 2026; disputed "
          "claims are attributed. An independent re-check removed 21 "
          "Monday items before publication.")
    l2 = ("Sources: Reuters, AP, AFP, Xinhua, Al Jazeera, Yonhap, UN News, "
          "SCMP, Japan Times, PA, ESPNcricinfo, CoinDesk. Original drawings.")
    for i, ln in enumerate((l1, l2)):
        tw = d.textlength(ln, font=ff)
        d.text(((W - tw) / 2, 978 + i * 14), ln, font=ff, fill=MUTE)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    return out


# Aliases so any thin entry wrapper can reach the renderer.
render = main
build = main
generate = main

if __name__ == "__main__":
    main()
