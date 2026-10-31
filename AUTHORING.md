# How to make the next episode (for the daily 4 PM run)

1. Read `PLAN.md` → pick the episode for today's date. Copy `episodes/ep01.py` as the style reference and write `episodes/epNN.py`.
2. Preview: `python3 engine.py episodes/epNN.py out/epNN --stills 5,30,60,90,120,150` → look at the JPGs (Read tool). Fix overlaps/overflow.
3. Render: `python3 engine.py episodes/epNN.py out/epNN` (~2–3 min on 2 cores). Outputs: video.mp4, thumbnail.jpg, upload.txt/json, script.txt, audio_music_only.wav.
4. Spot-check 2 frames from the final mp4 with ffmpeg, then publish (see RUNBOOK in the scheduled-task prompt).
   Hosting: GitHub Releases are blocked for the automation session, so copy video.mp4 + thumbnail.jpg into `media/epNN/`, commit and push; Metricool pulls them from `https://raw.githubusercontent.com/shivamsv64/tech-dev-git-series/main/media/epNN/video.mp4` (worked for Ep 1).

## Episode file
`EP = {'num', 'title', 'short' (header text), 'scenes': [...], 'thumb': {...}, 'upload': {...}}`
Every scene has `type`, optional `chapter` (YouTube chapter name), and `beats`: a list of dicts. Each beat shows one caption (`cap`, highlight with `*word*`) and triggers that scene's action. Beat duration = max(caption reading time, action time). Optional per beat: `mood` (talk|happy|shock|think|party) and `arms` (down|wave|point|up|shock|think) for the mascot.

| type | scene fields | beat fields |
|---|---|---|
| `title` | `title` (\n allowed), `sub`, `emoji` | `cap` |
| `bubble` | — (big mascot left, speech bubble) | `say` (bubble text), `items` (list of '📄 text'; prefix `!r ` = red warning chip) |
| `cards` | `title`, `emoji` (≤4 cards total) | `card: {emoji, title, text}` |
| `vs` | `title`, `emoji`, `left/right: {emoji,title,sub}`, `rows: [[label, leftval, rightval], ...]` (≤4) | `row: i` reveals row i |
| `terminal` | `cwd` (default ~/my-project) | `cmd`, `out` (lines; prefix `!r !g !y !c !m` colors), `err: True` (red + shocked mascot + buzz), `ok: True` (green + happy), `hl: ['--flag']` boxes tokens, `note` (amber tip chip), `clear: True` |
| `lanes` | `files` (start in Working Dir as untracked) | `cmd` (shown on top), `new`, `modify`, `add` (list or '.'), `unstage`, `restore`, `commit: 'msg'` |
| `graph` | `title`, `emoji`, `branches` (default ['main']), `head` | `ops`: `['commit',br,'C1']`, `['branch',new,from]`, `['checkout',br]`, `['merge',src,dst,'M']`, `['ff',src,dst]`, `['rebase',br,onto]`, `['squash',br,n,'S']`, `['cherry','C2',dst]`, `['tag','C3','v1.0']`, `['reset',br,'C1']` |
| `code` | `file`, `lines` (≤14; conflict markers auto-colored) | `lines` (replace), `hl: [[from,to],[..]]` (1-based), `note` |
| `quiz` | `q`, `opts` (4), `ans` (index) | first beat question, then `{'reveal': True, 'cap': ...}` |
| `recap` | `title`, `emoji`, `items: [[cmd, desc], ...]` (≤7) | `cap` |
| `outro` | `next` (rich text), optional `head`, `sub` | `cap` |

Tips: keep monospace lines ≤ 60 chars; terminal shows 14 lines (older lines scroll); `cards` text ≤ 8 words; one idea per caption; include at least one real-life analogy and one real DevOps example per episode; end each episode with quiz → recap → outro whose `next` names the next episode from PLAN.md (Ep 15 outro: thank viewers, tease the next Tech-dev series).
