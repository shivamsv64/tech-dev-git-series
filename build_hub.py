#!/usr/bin/env python3
"""Regenerate hub/index.html (the series tracker artifact) from series.json."""
import json, html, os

rows = json.load(open(os.path.join(os.path.dirname(__file__) or '.', 'series.json')))
LABEL = {'planned': 'Planned', 'ready': 'Rendered', 'scheduled': 'Scheduled 4 PM', 'published': 'Live', 'failed': 'Needs attention'}
done = sum(r['status'] in ('scheduled', 'published') for r in rows)

def esc(s):
    return html.escape(s or '')

items = []
for r in rows:
    links = ''
    if r.get('video_url'):
        links += '<a href="%s" target="_blank" rel="noopener">Video file</a>' % esc(r['video_url'])
    if r.get('youtube'):
        links += '<a href="%s" target="_blank" rel="noopener">Watch on YouTube</a>' % esc(r['youtube'])
    if r.get('planner'):
        links += '<a href="%s" target="_blank" rel="noopener">Metricool post</a>' % esc(r['planner'])
    items.append('''
<li class="ep s-%(st)s">
  <div class="num">EP<b>%(ep)02d</b></div>
  <div class="body">
    <div class="top"><h3>%(title)s</h3><span class="pill">%(lab)s</span></div>
    <p class="date">%(date)s · 4:00 PM IST</p>
    <dl><dt>Analogy</dt><dd>%(an)s</dd><dt>DevOps angle</dt><dd>%(dv)s</dd></dl>
    %(links)s
  </div>
</li>''' % {'st': r['status'], 'ep': r['ep'], 'title': esc(r['title']), 'lab': LABEL.get(r['status'], r['status']), 'date': esc(r['date']),
            'an': esc(r['analogy']), 'dv': esc(r['devops']), 'links': ('<div class="links">%s</div>' % links) if links else ''})

page = '''<title>Git Series Tracker</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: one column "commit log" — episodes as nodes on a vertical branch line, newest work highlighted */
:root{--bg:#0a0f1f;--panel:#111a33;--line:#25325a;--fg:#e8eef8;--muted:#93a1bd;--cyan:#38bdf8;--amber:#fbbf24;--violet:#a78bfa;--green:#34d399;--red:#f87171;
--display:"Poppins",system-ui,sans-serif;--body:"Inter",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--body)}
.wrap{max-width:860px;margin:0 auto;padding-block:40px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.brand{font:500 13px var(--mono);color:var(--green);letter-spacing:.04em}
.brand span{color:var(--fg);font-family:var(--display);font-weight:600;margin-left:6px}
h1{font:700 clamp(28px,5vw,42px)/1.15 var(--display);margin:14px 0 8px;text-wrap:balance}
.tri{display:flex;gap:6px;margin:18px 0 8px}.tri i{height:5px;width:56px;border-radius:3px}
.lede{color:var(--muted);max-width:62ch;margin:0}
.meter{display:flex;align-items:center;gap:14px;margin:26px 0 30px;font:500 13px var(--mono);color:var(--muted)}
.bar{flex:1;height:8px;background:var(--line);border-radius:4px;overflow:hidden}
.bar b{display:block;height:100%;background:linear-gradient(90deg,var(--cyan),var(--amber),var(--violet))}
ol{list-style:none;margin:0;padding:0;position:relative}
ol::before{content:"";position:absolute;left:27px;top:8px;bottom:8px;width:3px;background:var(--line);border-radius:2px}
.ep{display:grid;grid-template-columns:56px 1fr;gap:16px;padding:0 0 18px;position:relative}
.num{width:56px;height:56px;border-radius:50%;background:var(--bg);border:3px solid var(--line);display:grid;place-content:center;text-align:center;font:500 10px/1 var(--mono);color:var(--muted);z-index:1}
.num b{display:block;font:700 18px/1.1 var(--display);color:var(--fg)}
.body{min-width:0;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
.top{display:flex;gap:12px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap}
h3{font:600 17px/1.3 var(--display);margin:0;text-wrap:balance;min-width:0}
.pill{font:500 11px var(--mono);text-transform:uppercase;letter-spacing:.06em;padding:4px 10px;border-radius:99px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.date{margin:4px 0 10px;font:500 12px var(--mono);color:var(--muted)}
dl{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;margin:0;font-size:14px}
dt{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em;padding-top:2px}dd{margin:0;min-width:0}
.links{display:flex;gap:16px;flex-wrap:wrap;margin-top:12px}
.links a{color:var(--cyan);font-weight:600;text-decoration:none}.links a:hover,.links a:focus-visible{text-decoration:underline}
.s-ready .num,.s-scheduled .num{border-color:var(--amber)}.s-ready .pill,.s-scheduled .pill{color:var(--amber);border-color:var(--amber)}
.s-published .num{border-color:var(--green);background:#0f2e27}.s-published .pill{color:var(--green);border-color:var(--green)}
.s-failed .pill{color:var(--red);border-color:var(--red)}
@media (max-width:520px){dl{grid-template-columns:1fr}.ep{grid-template-columns:44px 1fr;gap:12px}.num{width:44px;height:44px}ol::before{left:21px}}
</style>
<div class="wrap">
  <div class="brand">&gt;_<span>Tech-dev</span></div>
  <div class="tri"><i style="background:var(--cyan)"></i><i style="background:var(--amber)"></i><i style="background:var(--violet)"></i></div>
  <h1>Git &amp; GitHub: Beginner to Advanced</h1>
  <p class="lede">15 animated episodes of 2–5 minutes, one published every day at 4:00 PM IST from 31 Oct to 14 Nov 2026. Each one pairs a real-life analogy with a real DevOps example.</p>
  <div class="meter"><span>@@DONE@@ / 15 scheduled or live</span><div class="bar"><b style="width:@@PCT@@%"></b></div></div>
  <ol>@@ITEMS@@
  </ol>
</div>'''.replace('@@DONE@@', str(done)).replace('@@PCT@@', str(round(done / 15 * 100))).replace('@@ITEMS@@', ''.join(items))
os.makedirs('hub', exist_ok=True)
open('hub/index.html', 'w').write(page)
print('hub/index.html written')
