#!/usr/bin/env python3
"""Draw the news-image-20261122 poster: a newspaper front page, 1024x1024 PNG.

Everything is drawn with PIL text and shapes - no photos, no scraped images.
Four verified stories from Sunday 22 November 2026 (Reuters / AP):
  lead  COP31 climate talks in Antalya - revised draft tabled early Sunday,
        president says a deal is close; text still omits fossil fuels.
  col 1 Australia vs US CBO over AUKUS submarines (Reuters, Sydney, Nov 22).
  col 2 FBI investigating apparent hack of its NCIC crime database (AP).
  col 3 Mexico captures FBI most-wanted cartel boss "El Chapo Isidro" (AP).
Run:  python3 draw_poster.py   -> writes poster.png beside this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
NAVY = (26, 35, 64)
GOLD = (217, 164, 65)
RED = (179, 32, 42)
INK = (26, 26, 26)
GREY = (102, 102, 102)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    draw_centered(d, W // 2, 34, "THE WORLD IN ONE DAY",
                  font(SERIF, 62), (255, 255, 255))
    draw_centered(d, W // 2, 104, "SUNDAY, 22 NOVEMBER 2026",
                  font(SANS_B, 27), GOLD)
    d.rectangle([0, 148, W, 152], fill=GOLD)

    # ---- lead story: COP31 ---------------------------------------------
    d.text((48, 176), "CLIMATE  —  ANTALYA", font=font(SANS_B, 22), fill=RED)
    d.text((48, 204), "COP31 NEARS DEAL", font=font(SERIF, 54), fill=INK)
    d.text((48, 264), "AFTER OVERTIME", font=font(SERIF, 54), fill=INK)
    lead_body = (
        "UN climate talks in Antalya ran into overtime and a revised draft "
        "was tabled early Sunday. The president said a deal was close "
        "\u2014 but the text still omits fossil fuels."
    )
    y = 340
    for line in wrap(d, lead_body, font(SANS, 23), 600):
        d.text((48, y), line, font=font(SANS, 23), fill=INK)
        y += 30

    # lead graphic: globe in a framed box
    d.rectangle([700, 176, 976, 452], outline=NAVY, width=3)
    cx, cy, r = 838, 300, 82
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    d.ellipse([cx - 34, cy - r, cx + 34, cy + r], outline=NAVY, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=3)
    d.arc([cx - r, cy - 44, cx + r, cy + 44], 20, 160, fill=NAVY, width=3)
    d.arc([cx - r, cy - 44, cx + r, cy + 44], 200, 340, fill=NAVY, width=3)
    d.text((716, 408), "COP31", font=font(SANS_B, 24), fill=NAVY)

    # ---- rule -----------------------------------------------------------
    d.line([48, 492, 976, 492], fill=NAVY, width=2)

    # ---- three columns ---------------------------------------------------
    cols = [
        dict(
            x=48, kicker="DEFENCE  —  SYDNEY",
            headline=["CANBERRA", "REBUKES US", "SUB REPORT"],
            body=("Australia's defence minister criticised the US budget "
                  "office after it said AUKUS would leave the US Navy short "
                  "of attack submarines."),
            icon="sub",
        ),
        dict(
            x=364, kicker="CYBER  —  WASHINGTON",
            headline=["FBI CRIME", "DATABASE", "HACKED"],
            body=("The FBI is investigating a hack of the National Crime "
                  "Information Center, the database behind fugitive and "
                  "warrant checks. Trump: \u2018not good\u2019."),
            icon="lock",
        ),
        dict(
            x=680, kicker="CARTELS  —  SINALOA",
            headline=["EL CHAPO", "ISIDRO", "CAPTURED"],
            body=("Mexican forces captured FBI most-wanted cartel boss "
                  "Fausto Isidro Meza Flores in Guasave. Eleven people died "
                  "in the battle."),
            icon="shield",
        ),
    ]
    for c in cols:
        x = c["x"]
        # icon, centred in the 296px column
        icx = x + 148
        if c["icon"] == "sub":
            # submarine silhouette: tower joined to the hull, short periscope
            d.rounded_rectangle([icx - 78, 544, icx + 78, 578], radius=17,
                                outline=NAVY, width=4)
            d.rectangle([icx - 16, 522, icx + 16, 546], outline=NAVY, width=4)
            d.line([icx + 6, 522, icx + 6, 508], fill=NAVY, width=4)
            for px in (-48, 0, 48):
                d.ellipse([icx + px - 6, 555, icx + px + 6, 567],
                          outline=NAVY, width=3)
        elif c["icon"] == "lock":
            # padlock with a crack
            d.rounded_rectangle([icx - 42, 540, icx + 42, 596], radius=8,
                                outline=NAVY, width=4)
            d.arc([icx - 30, 506, icx + 30, 566], 180, 360, fill=NAVY, width=4)
            d.ellipse([icx - 7, 556, icx + 7, 570], fill=NAVY)
            d.line([icx, 570, icx, 584], fill=NAVY, width=5)
            d.line([icx - 42, 540, icx + 10, 596], fill=RED, width=4)
        else:
            # shield with star
            d.polygon([(icx, 500), (icx + 52, 516), (icx + 52, 556),
                       (icx, 596), (icx - 52, 556), (icx - 52, 516)],
                      outline=NAVY, width=4)
            d.text((icx, 528), "\u2605", font=font(SANS_B, 40), fill=NAVY,
                   anchor="ma")
        d.text((x, 612), c["kicker"], font=font(SANS_B, 20), fill=RED)
        y = 640
        for line in c["headline"]:
            d.text((x, y), line, font=font(SERIF, 37), fill=INK)
            y += 44
        y = 782
        for line in wrap(d, c["body"], font(SANS, 21), 296):
            d.text((x, y), line, font=font(SANS, 21), fill=INK)
            y += 29

    # ---- footer ----------------------------------------------------------
    d.line([48, 950, 976, 950], fill=NAVY, width=2)
    draw_centered(d, W // 2, 964, "Reporting: Reuters  \u00b7  Associated Press",
                  font(SANS, 19), GREY)

    img.save("poster.png", optimize=True)
    print("wrote poster.png", img.size)


if __name__ == "__main__":
    main()
