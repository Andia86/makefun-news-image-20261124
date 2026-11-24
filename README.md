# The Day in World News — Tuesday 24 November 2026

[![bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Andia86/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Andia86/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

One page, 52 sourced stories, all of them Tuesday's. Entry for the
[news-image-20261124](https://make.fun/bounty/news-image-20261124)
bounty on [make.fun](https://make.fun).

## What the page does differently

- **Count first, honestly.** 12 illustrated cards plus 40 numbered
  briefs = 52 distinct stories. No duplicates, no padding.
- **A DATE CHECK strip on the page itself.** The biggest stories of
  Monday 23 November — Nvidia reinstating Jensen Huang and the US
  market surge, the Grok-image lawsuits, FIFA's 2031/2035 host votes,
  the Merz–Rutte pledges — are named and left out on purpose. They are
  Monday's news, not Tuesday's.
- **Every card carries a status tag** (CONFIRMED / REPORTED /
  OFFICIAL) and every story is dated in `NEWS_SOURCES.md` against the
  wire reporting itself — "on Tuesday", a 24 Nov dateline or a 24 Nov
  timestamp — never against an index page's date.
- **Markets are split by session and labelled by day**: Asia's Tuesday
  close (Nikkei +3.91%, Kospi +6.3%, Taiex +9%) is not dressed up as
  America's; the US panel is printed as what it is, Monday's close.
- **A UTC timeline with real timestamps** (00:35 Japan flash PMI,
  01:32 the Koshi quake, 06:00 the Nikkei close, 12:03 the UK Houthi
  designation, 13:43 the CAS ruling in Lausanne) and a map whose
  numbered pins match the twelve cards.
- **Rebuilt the same evening after review.** A first draft of this
  page was caught by an independent fact-check carrying Monday
  stories under a Tuesday banner, and was scrapped. This version was
  re-sourced item by item against Tuesday's own reporting, then
  re-checked by a second reviewer before submission.

## Files

- `main.py` — entry point; writes the page to the output directory.
- `render.py` — the deterministic renderer (pure PIL, no clock, no
  network, no randomness; two runs give identical bytes).
- `entry.png` — the rendered page, 1024×1024.
- `NEWS_SOURCES.md` — the per-story source and date ledger, including
  the drop list of Monday stories that were excluded.

## Run

```sh
python3 render.py   # regenerates entry.png in place
```
