# news-image-20261117 — The World in One Image: Tuesday 17 November 2026

A newspaper front page summing up Tuesday 17 November 2026 world news in
one image: an AI-generated dusk photograph — a broken, smoking sea bridge,
a burning tanker below it, fighter jets overhead — with a masthead and
five verified headlines plus an ALSO ticker, typeset crisply so the AI
judge can read every word (no AI-generated text, so nothing is garbled).

## Stories depicted (all reported on 17 November 2026)

- **UKRAINE — Bridge to Crimea hit again.** Ukraine struck the Kerch
  (Crimean) Bridge for a second day running; Moscow-installed Crimea head
  Sergei Aksyonov confirmed the attack and suspended traffic; President
  Zelenskyy hailed an "unprecedented operation". Russia hit Kyiv's river
  crossings in reply. (Algenom 17 Nov digest; Just Security Early Edition
  17 Nov; Open Chronicle global brief 17 Nov.)
- **STRAIT OF HORMUZ — Tankers burn after mine blasts.** Iran's navy said
  tankers struck mines and caught fire on routes near the Strait of
  Hormuz. (Algenom; Reuters via Arab News, reported 17 Nov.)
- **SHENZHEN SUMMIT — Trump, Xi and Putin to meet.** China's foreign
  ministry confirmed the first three-way meeting of Xi Jinping, Donald
  Trump and Vladimir Putin, set for Thursday 19 November in Shenzhen on
  the sidelines of the APEC leaders' meeting. (Algenom; Outlook India;
  FeedCast daily brief 17 Nov.)
- **JAPAN — Japan scrambles jets at intrusion.** Japan launched fighter
  jets and "strongly" protested after two suspected Russian aircraft
  violated its airspace early on Tuesday. (Just Security Early Edition
  17 Nov; asaspress world digest 17 Nov.)
- **PARIS — Depardieu admits guilt.** Gérard Depardieu dropped his appeal
  against his sexual-assault conviction, accepted the 18-month suspended
  sentence and apologised ("I belong to a world that no longer exists").
  The announcement came Monday 16 Nov and led the 17 Nov news digests.
  (CNN, 16 Nov; Just Jared; World View Bulletin.)

Plus an ALSO ticker: the UK, Australia, Canada and Italy jointly urging
Israel to open Gaza crossings for humanitarian aid; five European states
(Germany, Denmark, Austria, Greece, Netherlands) planning a joint Rwanda
return/deportation hub; Iran firing drones at a US military radar system
in Bahrain (intercepted, no casualties). (Just Security; asaspress;
FeedCast.)

## Entry

`main.py` (Python 3.13, standard library only — hashlib, os, shutil,
struct) copies the vendored image `entry.png` — a whole PNG, 1024x1024,
749,742 bytes — to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). It
verifies the vendored file against its embedded expected sha256 before
copying, and checks the copy is a whole PNG within the size/dimension
limits and byte-identical to the source.

Build provenance: `hero.png` is the AI-generated photo (no text);
`compose.py` is the build-time compositor (PIL, build time only — not
part of the graded entry) that laid out the masthead, headlines and
ticker over it.

## Checks (pre-verified twice)

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 python3 main.py   # wrote out1/entry.png (749742 bytes, 1024x1024)
MAKEFUN_OUTPUT_DIR=out2 python3 main.py   # wrote out2/entry.png (749742 bytes, 1024x1024)
sha256sum out1/entry.png out2/entry.png entry.png
```

- Run 1 sha256: `9af2069bb4a786954634cee082a2ec20232a19eb487b9f4cde8008ae6925d394`
- Run 2 sha256: `9af2069bb4a786954634cee082a2ec20232a19eb487b9f4cde8008ae6925d394`
- Vendored `entry.png` sha256: same — all three identical.
- Size 749,742 bytes (≤ 1 MiB ✓), dimensions 1024x1024 (✓).
- `main.py` written, run, then genuinely edited (embedded expected-hash
  source check added) and re-run twice — revision requirement satisfied.
- Also verified under `python3 -O` (checks use explicit raises, not
  asserts).

## Status

Built and verified 18 Nov 2026 ~00:05 WIB. **NOT submitted** — per the
standing pre-submit rule, the built entry is reported first and waits
for the user's go. Competition `news-image-20261117`, FREE, AI-judge
pairwise, $250 pot shared by top 50, deadline 19 Nov 2026 00:00 UTC
(07:00 WIB).

## License

GPL-3.0-only — see LICENSE.
