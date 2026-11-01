# Tech-dev · Git & GitHub: Beginner → Advanced

Animated explainer series for the **Tech-dev** YouTube channel by Shivam Singh Verma (DevOps & SRE).
One 5–10 minute episode (Ep 1–2 were ~3 min) goes live every day at **4:00 PM IST** (31 Oct → 14 Nov 2026).

- `engine.py` — renders an episode spec into a 1080p video with the mascot **Bit**, captions, lofi music and sound effects, plus thumbnail, upload text and a timed voiceover script.
- `episodes/epNN.py` — one spec per episode. `AUTHORING.md` documents the scene types.
- `PLAN.md` — the 15-episode plan with real-life analogies and DevOps examples.
- `series.json` + `build_hub.py` — status tracker page.
- Rendered videos are attached to GitHub Releases (`ep01`, `ep02`, …).

```bash
python3 engine.py episodes/ep01.py out/ep01 --stills 5,30,60   # preview frames
python3 engine.py episodes/ep01.py out/ep01                     # full render (~2–3 min)
```
Requires Python 3 with Pillow + NumPy, ffmpeg, and the Poppins / Inter / DejaVu Sans Mono / Noto Color Emoji fonts.
