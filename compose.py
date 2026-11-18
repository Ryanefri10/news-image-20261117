#!/usr/bin/env python3
"""Compose the news-image-20261117 front page (BUILD-TIME ONLY).

Takes the AI-generated hero photo (hero.png, 1600x1600, no text) and
composes a newspaper front page: masthead strip over the photo, then a
cream panel with five verified 17 Nov 2026 headlines and an ALSO box.
Output: entry.png, 1024x1024, <= 1 MiB. Uses PIL at build time only;
the graded main.py is stdlib-only and just copies entry.png.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERO_H = 640
INK = (17, 24, 39)
PAPER = (245, 239, 224)
RED = (178, 34, 34)
GREY = (74, 74, 74)
AMBER = (245, 185, 66)
FDIR = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

hero = Image.open("hero.png").convert("RGB")
# Crop to 1600x1000 (jets, broken bridge, burning tanker all in frame),
# then scale to the 1024x640 photo slot.
hero = hero.crop((0, 130, 1600, 1130)).resize((W, HERO_H), Image.LANCZOS)

page = Image.new("RGB", (W, H), PAPER)
page.paste(hero, (0, 0))
d = ImageDraw.Draw(page, "RGBA")

# --- masthead strip over the dark sky ---
d.rectangle([0, 0, W, 96], fill=(10, 14, 24, 215))
d.rectangle([0, 96, W, 100], fill=AMBER)
d.text((W // 2, 16), "THE WORLD IN ONE IMAGE", font=SERIF_B(46),
       fill=(255, 255, 255), anchor="ma")
d.text((W // 2, 66), "TUESDAY, 17 NOVEMBER 2026", font=SANS_B(21),
       fill=AMBER, anchor="ma")

# --- headline panel ---
y0 = HERO_H
d.rectangle([0, y0, W, y0 + 4], fill=INK)
d.rectangle([W // 2 - 1, y0 + 14, W // 2 + 1, H - 12], fill=(190, 180, 160))

STORIES_LEFT = [
    ("UKRAINE", "Bridge to Crimea hit again",
     "Kyiv strikes the Kerch span a second day running; Zelenskyy hails an \u201cunprecedented operation\u201d."),
    ("STRAIT OF HORMUZ", "Tankers burn after mine blasts",
     "Iran says ships struck mines near the strait; fires at sea as shipping on edge."),
    ("SHENZHEN SUMMIT", "Trump, Xi and Putin to meet",
     "Trilateral talks set for Thursday at the APEC summit in Shenzhen."),
]
STORIES_RIGHT = [
    ("JAPAN", "Japan scrambles jets at intrusion",
     "Tokyo protests after suspected Russian aircraft enter its airspace."),
    ("PARIS", "Depardieu admits guilt",
     "Actor drops his appeal, accepts his sexual-assault conviction and apologises."),
]

def fit_headline(text, width, size=24):
    """Largest serif-bold size (down to 19) that fits on one line."""
    while size > 19 and d.textlength(text, font=SERIF_B(size)) > width:
        size -= 1
    return SERIF_B(size)


def story_block(x, y, width, kicker, headline, deck):
    d.text((x, y), kicker, font=SANS_B(19), fill=RED)
    y += 26
    d.text((x, y), headline, font=fit_headline(headline, width), fill=INK)
    y += 33
    for line in wrap(d, deck, SANS(18), width):
        d.text((x, y), line, font=SANS(18), fill=GREY)
        y += 23
    return y

col_w = 462
y = y0 + 18
for s in STORIES_LEFT:
    y = story_block(24, y, col_w, *s) + 12

y = y0 + 18
for s in STORIES_RIGHT:
    y = story_block(538, y, col_w, *s) + 12

# --- ALSO box ---
box_y = y + 2
d.rectangle([538, box_y, 1000, H - 12], outline=RED, width=2)
d.text((552, box_y + 8), "ALSO TODAY", font=SANS_B(18), fill=RED)
ay = box_y + 34
also = [
    "Four nations urge Israel: open Gaza crossings.",
    "Five European states plan a Rwanda hub.",
    "Iran drones target a US radar base in Bahrain.",
]
for item in also:
    for line in wrap(d, "\u2022  " + item, SANS(17), col_w - 28):
        d.text((552, ay), line, font=SANS(17), fill=INK)
        ay += 21
    ay += 3

page.save("entry.png", optimize=True)
print("saved entry.png", page.size)
