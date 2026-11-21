# The Saturday Globe — 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/arnesasarizky/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/arnesasarizky/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

One broadsheet image summing up the world's news of **Saturday 21 November 2026**:
**35 stories, 7 regions, every one dated that day** — 13 pictured cards (3 leads +
10 features) and 22 numbered briefs, each with its source.

Leads: COP31 runs into overtime in Antalya as fossil fuels vanish from the draft
deal; Saudi defences intercept three Houthi missiles over Riyadh; a Russian strike
on Kryvyi Rih kills a seven-year-old boy and a paramedic. Also inside: the 6.7
Peru quake, BepiColombo's arrival at Mercury, Rutte in Warsaw, the Davao emergency
landing with all 146 safe, Rahul's 136 in Wellington, and Las Vegas GP qualifying.

The poster carries a region strip whose counts sum exactly to 35, a six-number
"Day in Numbers" strip, a world map with pins for all 13 pictured stories, and a
DATE CHECK box naming real stories left out because they happened on 19–20 November.

## How it is built

`draw.py` (Pillow, run at build time) draws `poster.png` — a 1024×1024 PNG with
gradient illustration scenes and a deterministic grain. `main.py` (standard library
only) copies `poster.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, so both grader runs
write identical bytes.

Run locally:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
