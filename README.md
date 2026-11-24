# The Day in World News — Tuesday 24 November 2026

[![Bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/Andia86/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261124/Andia86/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One page that sums up the world's news of **Tuesday 24 November 2026**:
52 stories (12 illustrated leads + 40 briefs), 7 regions, every story sourced.

## What the image shows

A flat broadsheet front page, "THE DAY IN WORLD NEWS", built to be read
the way a picture editor reads a front page:

- **Masthead and date line** — the day is named in full: Tuesday
  24 November 2026, with the count line "52 STORIES · 7 REGIONS · ONE PAGE".
- **Date check strip** — every story happened or was first reported on
  Tuesday 24 November 2026, checked against Reuters, AP, AFP and regional
  wires carrying 24 Nov datelines and timestamps.
- **UTC timeline** — five anchor moments of the day, from Reuters' 00:23 GMT
  gold report and the 00:35 GMT Japan flash PMI to the closing market
  figures (S&P 500 +4.73%, Nasdaq +6.51%, Nikkei 225 +3.91%).
- **12 illustrated lead cards** — number chip, region · field tag, source
  tag, a bold headline, one line of summary, and an original flat icon
  drawn in code.
- **"Where it happened" map** — a simplified world map with numbered pins
  matching the 12 lead cards, beside a markets panel for the day.
- **40 numbered briefs** — the rest of the day in a dense three-column
  list, each with region and source tags.
- **Footer** — the attribution rule: disputed claims are attributed to
  their source, and the outlets used are named.

## Method and sources

Stories were gathered on 24 November 2026 from major wire and world
outlets — Reuters, AP and AFP wire copy, UN News, PINA (Pacific),
The Japan Times, Al Jazeera, ABC Australia, The Hindu, Anadolu reporting
and same-day live blogs — and every story had to carry a verifiable
24 November 2026 date basis (a dateline, a publication timestamp, or a
same-day live report). Anything that could not be dated to 24 November
was discarded, however prominent. The full numbered list, with each
story's source and date basis, is in [NEWS_SOURCES.md](NEWS_SOURCES.md);
the numbers there match the numbers printed in the image.

The image was drawn with PIL at 2048×2048 and downscaled to 1024×1024
by [render.py](render.py). All artwork is original flat shapes drawn in
code — no photographs and no external images.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only, no network) copies the
committed `entry.png` into `$MAKEFUN_OUTPUT_DIR`, byte for byte, so two
runs always produce identical bytes. The image is a 1024×1024 PNG under
1 MiB.

---

Built for [make.fun](https://make.fun)'s "Sum up 24 November's world news in one image" bounty.
