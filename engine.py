#!/usr/bin/env python3
"""Tech-dev cartoon explainer engine.

Usage:
  python3 engine.py episodes/ep01.py out/ep01            # full render
  python3 engine.py episodes/ep01.py out/ep01 --stills 5,40,90   # preview frames only
Outputs in out dir: video.mp4, thumbnail.png, upload.txt, upload.json, script.txt
"""
import os, sys, re, math, json, subprocess, random, wave, importlib.util, shutil
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
BG = (10, 15, 31); CYAN = (56, 189, 248); AMBER = (251, 191, 36); VIOLET = (167, 139, 250)
GREEN = (52, 211, 153); RED = (239, 68, 68); WHITE = (241, 245, 249); MUTED = (148, 163, 184)
PANEL = (17, 24, 45); PANEL2 = (25, 34, 62); LINE = (44, 56, 92); PINK = (244, 114, 182)
BRANCH_COLORS = [CYAN, AMBER, VIOLET, GREEN, PINK]

FD = '/usr/share/fonts/'
F_POP = FD + 'truetype/google-fonts/Poppins-Bold.ttf'
F_POPM = FD + 'truetype/google-fonts/Poppins-Medium.ttf'
F_INTER = FD + 'opentype/inter/Inter-Medium.otf'
F_INTERSB = FD + 'opentype/inter/Inter-SemiBold.otf'
F_MONO = FD + 'truetype/dejavu/DejaVuSansMono.ttf'
F_MONOB = FD + 'truetype/dejavu/DejaVuSansMono-Bold.ttf'
F_EMOJI = FD + 'truetype/noto/NotoColorEmoji.ttf'


@lru_cache(None)
def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(F_MONO, size)


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(p):
    p = clamp(p); return 1 - (1 - p) ** 3


def ease_io(p):
    p = clamp(p); return p * p * (3 - 2 * p)


def ease_back(p):
    p = clamp(p); c = 1.9
    return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2


def lerp(a, b, p):
    return a + (b - a) * p


def lerpc(c1, c2, p):
    return tuple(int(lerp(a, b, p)) for a, b in zip(c1, c2))


def read_time(cap):
    if not cap:
        return 0.0
    n = len(re.sub(r'\*', '', cap).split())
    return clamp(n / 2.55 + 0.9, 2.4, 9.0)


# ---------------------------------------------------------------- emoji & text
@lru_cache(None)
def emoji(ch, size):
    f = ImageFont.truetype(F_EMOJI, 109)
    im = Image.new('RGBA', (300, 160), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
    bb = im.getbbox()
    if not bb:
        return Image.new('RGBA', (size, size))
    im = im.crop(bb)
    r = size / im.height
    return im.resize((max(1, int(im.width * r)), size), Image.LANCZOS)


def split_emoji(s):
    """'📄 file.txt' -> ('📄', 'file.txt')"""
    if s and ord(s[0]) > 0x2000:
        parts = s.split(' ', 1)
        return parts[0], (parts[1] if len(parts) > 1 else '')
    return None, s


def parse_rich(text):
    segs = []
    for p in re.split(r'(\*[^*]+\*)', text or ''):
        if len(p) > 2 and p.startswith('*') and p.endswith('*'):
            segs.append((p[1:-1], True))
        elif p:
            segs.append((p, False))
    toks = []; prev_space = True
    for seg, hl in segs:
        words = seg.split(' ')
        for j, w in enumerate(words):
            if not w:
                continue
            glue = (j == 0 and not prev_space and bool(toks))
            toks.append((w, hl, glue))
        prev_space = seg.endswith(' ')
    return toks


def wrap_rich(text, fnt, maxw):
    toks = parse_rich(text); sp = fnt.getlength(' ')
    lines = [[]]; cw = 0
    for w, hl, glue in toks:
        ww = fnt.getlength(w); add = ww + (0 if glue or not lines[-1] else sp)
        if lines[-1] and cw + add > maxw and not glue:
            lines.append([]); cw = 0; add = ww
        lines[-1].append((w, hl, glue)); cw += add
    out = []
    for ln in lines:
        x = 0; items = []
        for i, (w, hl, glue) in enumerate(ln):
            if i and not glue:
                x += sp
            items.append((x, w, hl)); x += fnt.getlength(w)
        out.append((x, items))
    return out


def draw_rich(d, x, y, text, fnt, col=WHITE, hl=CYAN, maxw=1400, align='center', lh=None, alpha=255):
    lines = wrap_rich(text, fnt, maxw)
    lh = lh or int(fnt.size * 1.32)
    for i, (lw, items) in enumerate(lines):
        x0 = x - lw / 2 if align == 'center' else x
        for dx, w, h in items:
            c = hl if h else col
            d.text((x0 + dx, y + i * lh), w, font=fnt, fill=c + (alpha,) if len(c) == 3 else c)
    return len(lines) * lh


def text_h(text, fnt, maxw, lh=None):
    return len(wrap_rich(text, fnt, maxw)) * (lh or int(fnt.size * 1.32))


# ---------------------------------------------------------------- mascot "Bit"
@lru_cache(maxsize=512)
def bot_sprite(scale, expr, mouth, arms, blink):
    S = 2; s = scale * S
    w, h = int(s * 2.0), int(s * 2.15)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = w / 2; ht = s * 0.32; hh = s * 0.78; hw = s * 1.0
    bt = ht + hh + s * 0.03; bw = s * 0.66; bh = s * 0.5
    metal = (30, 41, 59); dark = (8, 12, 24); ey = (125, 211, 252)
    # antenna
    d.line([(cx, ht + 4), (cx, ht - s * 0.2)], fill=(100, 116, 139), width=int(s * 0.04))
    r = s * 0.075; d.ellipse([cx - r, ht - s * 0.2 - r, cx + r, ht - s * 0.2 + r], fill=AMBER)
    # legs
    for sx in (-1, 1):
        lx = cx + sx * s * 0.16
        d.rounded_rectangle([lx - s * .075, bt + bh - s * .06, lx + s * .075, bt + bh + s * .17], radius=s * .05, fill=(51, 65, 85))
    # arms
    ang = {'down': (18, 18), 'wave_a': (18, 158), 'wave_b': (18, 118), 'point': (100, 18),
           'up': (150, 150), 'shock': (128, 128), 'think': (18, 150)}[arms]
    for side, a in zip((-1, 1), ang):
        shx, shy = cx + side * (bw / 2 - s * 0.02), bt + s * 0.13
        rad = math.radians(a); L = s * 0.42
        ex, eyy = shx + side * math.sin(rad) * L, shy + math.cos(rad) * L
        d.line([(shx, shy), (ex, eyy)], fill=(71, 85, 105), width=int(s * 0.085))
        hr = s * 0.075; d.ellipse([ex - hr, eyy - hr, ex + hr, eyy + hr], fill=CYAN)
    # body
    d.rounded_rectangle([cx - bw / 2, bt, cx + bw / 2, bt + bh], radius=s * .14, fill=metal, outline=VIOLET, width=int(s * .03))
    d.rounded_rectangle([cx - s * .19, bt + s * .1, cx + s * .19, bt + s * .3], radius=s * .05, fill=dark)
    d.text((cx, bt + s * .2), '>_', font=font(F_MONOB, int(s * .14)), fill=GREEN, anchor='mm')
    # head
    for sx in (-1, 1):
        ex0 = cx + sx * hw / 2
        d.rounded_rectangle([ex0 - s * .06, ht + hh * .32, ex0 + s * .06, ht + hh * .68], radius=s * .03, fill=(71, 85, 105))
    d.rounded_rectangle([cx - hw / 2, ht, cx + hw / 2, ht + hh], radius=s * .24, fill=metal, outline=CYAN, width=int(s * .035))
    vi = s * .1
    d.rounded_rectangle([cx - hw / 2 + vi, ht + vi, cx + hw / 2 - vi, ht + hh - vi], radius=s * .16, fill=dark)
    # eyes
    eyy = ht + hh * .44; ex = s * .19; lw = int(s * .045)
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.line([(x - s * .07, eyy), (x + s * .07, eyy)], fill=ey, width=lw)
        elif expr in ('happy', 'party'):
            d.arc([x - s * .08, eyy - s * .06, x + s * .08, eyy + s * .1], 200, 340, fill=ey, width=lw)
        elif expr == 'shock':
            d.ellipse([x - s * .085, eyy - s * .1, x + s * .085, eyy + s * .1], fill=ey)
            d.ellipse([x - s * .03, eyy - s * .03, x + s * .03, eyy + s * .03], fill=dark)
        elif expr == 'think':
            d.rounded_rectangle([x - s * .055 + s * .03, eyy - s * .12, x + s * .055 + s * .03, eyy + s * .04], radius=s * .05, fill=ey)
        else:
            d.rounded_rectangle([x - s * .06, eyy - s * .085, x + s * .06, eyy + s * .085], radius=s * .055, fill=ey)
    # cheeks
    for sx in (-1, 1):
        x = cx + sx * s * .3
        d.ellipse([x - s * .05, eyy + s * .1, x + s * .05, eyy + s * .14], fill=(120, 60, 110))
    # mouth
    my = ht + hh * .72
    if expr == 'shock':
        d.ellipse([cx - s * .05, my - s * .05, cx + s * .05, my + s * .06], outline=ey, width=lw)
    elif expr == 'think':
        d.line([(cx - s * .02, my), (cx + s * .09, my - s * .02)], fill=ey, width=lw)
    elif mouth == 1:
        d.ellipse([cx - s * .075, my - s * .045, cx + s * .075, my + s * .055], fill=PINK)
    elif expr in ('happy', 'party'):
        d.chord([cx - s * .11, my - s * .09, cx + s * .11, my + s * .07], 10, 170, fill=PINK)
    else:
        d.arc([cx - s * .08, my - s * .07, cx + s * .08, my + s * .03], 20, 160, fill=ey, width=lw)
    return im.resize((w // S, h // S), Image.LANCZOS)


def draw_bot(img, cx, bottom, scale, t, expr='talk', arms='down', talking=False, seed=0):
    blink = (t * 0.9 + seed * 0.37) % 3.3 < 0.12
    mouth = 0
    if talking:
        ph = t * 7.5 + math.sin(t * 3.1) * 1.3
        mouth = 1 if (ph % 2) < 1 else 0
    if arms in ('wave', 'wave_a'):
        arms = 'wave_a' if (t * 3) % 2 < 1 else 'wave_b'
    e = expr if expr in ('happy', 'party', 'shock', 'think') else 'talk'
    spr = bot_sprite(int(scale), e, mouth, arms, blink)
    bob = math.sin(t * 2 * math.pi * 0.7 + seed) * scale * 0.035
    x = int(cx - spr.width / 2); y = int(bottom - spr.height + bob)
    img.alpha_composite(spr, (x, y)) if img.mode == 'RGBA' else img.paste(spr, (x, y), spr)
    if expr == 'shock':
        sp = emoji('💦', int(scale * .32)); img.paste(sp, (x + int(spr.width * .78), y + int(scale * .2)), sp)
    elif expr == 'think':
        sp = emoji('❓', int(scale * .35)); img.paste(sp, (x + int(spr.width * .74), y), sp)
    elif expr == 'party':
        for i, ch in enumerate(('🎉', '✨')):
            sp = emoji(ch, int(scale * .34))
            img.paste(sp, (x + (int(-scale * .1) if i == 0 else int(spr.width * .82)), y + int(scale * .1 + math.sin(t * 4 + i) * 8)), sp)


# ---------------------------------------------------------------- background
def make_bg():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    img = np.zeros((H, W, 3), np.float32) + np.array(BG, np.float32)
    for (gx, gy, rad, col, k) in [(300, 120, 700, (37, 99, 235), .32), (1700, 950, 800, (124, 58, 237), .28), (1600, 120, 500, (14, 165, 233), .12)]:
        dd = np.exp(-(((xx - gx) ** 2 + (yy - gy) ** 2) / (rad ** 2)))
        img += dd[..., None] * np.array(col, np.float32) * k
    grid = ((xx % 64 < 1.2) | (yy % 64 < 1.2)).astype(np.float32) * 9
    img += grid[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def pill(d, x, y, text, fnt, fg, bg, padx=18, pady=8, anchor='l', outline=None):
    tw = fnt.getlength(text); hh = fnt.size + pady * 2
    if anchor == 'r':
        x -= tw + padx * 2
    elif anchor == 'c':
        x -= (tw + padx * 2) / 2
    d.rounded_rectangle([x, y, x + tw + padx * 2, y + hh], radius=hh / 2, fill=bg, outline=outline, width=2 if outline else 0)
    d.text((x + padx, y + pady + fnt.size * 0.02), text, font=fnt, fill=fg)
    return tw + padx * 2


def panel(d, box, fill=PANEL, outline=LINE, r=26, w=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=w)


# ---------------------------------------------------------------- scenes
class Scene:
    mascot = 'corner'   # corner | none | custom
    lead = 0.6
    tail = 0.7

    def __init__(self, spec, ep):
        self.spec = spec; self.ep = ep
        self.beats = spec.get('beats', [])
        self.events = []
        self.starts = []; t = self.lead
        for b in self.beats:
            self.starts.append(t)
            t += max(read_time(b.get('cap', '')), self.beat_min(b))
        self.dur = max(t + self.tail, spec.get('min_dur', 0))
        self.events.append((0.0, 'whoosh'))
        self.setup()

    def beat_min(self, b):
        return 0

    def setup(self):
        pass

    def beat_at(self, t):
        k = -1
        for i, s in enumerate(self.starts):
            if t >= s:
                k = i
        return k

    def mood(self, t):
        k = self.beat_at(t)
        if k < 0:
            return 'happy', 'down'
        b = self.beats[k]
        return b.get('mood', 'talk'), b.get('arms', 'down')

    def talking(self, t):
        k = self.beat_at(t)
        if k < 0:
            return False
        lt = t - self.starts[k]
        return 0.2 < lt < read_time(self.beats[k].get('cap', '')) - 0.6

    def draw(self, img, d, t):
        pass

    def title(self, d, t, text, emo=None, y=128):
        a = ease_out(t / 0.5)
        f = font(F_POP, 54)
        x = 120
        if emo:
            sp = emoji(emo, 58); img = d._image
            img.paste(sp, (x, int(y + 6 + (1 - a) * 20)), sp); x += 76
        d.text((x, y + (1 - a) * 20), text, font=f, fill=WHITE)


class TitleScene(Scene):
    mascot = 'none'; lead = 0.4

    def setup(self):
        self.events.append((0.5, 'pop')); self.events.append((0.9, 'pop'))

    def draw(self, img, d, t):
        sp = self.spec; ep = self.ep
        # floating code glyphs
        rnd = random.Random(7)
        for i in range(18):
            gx = rnd.uniform(80, 1840); gy0 = rnd.uniform(0, H); spd = rnd.uniform(12, 30)
            gy = (gy0 - t * spd) % (H + 100) - 50
            g = rnd.choice(['git', '{ }', '</>', '#', 'main', 'HEAD', '+1', 'diff', '>_'])
            d.text((gx, gy), g, font=font(F_MONO, rnd.randint(22, 34)), fill=(40, 54, 92))
        a = ease_back((t - 0.4) / 0.6)
        pill(d, 140, 250 - (1 - clamp(a)) * 40, 'EPISODE %02d' % ep['num'], font(F_POP, 34), (17, 24, 39), AMBER, padx=24, pady=10)
        ft = font(F_POP, 104)
        y = 330
        for i, line in enumerate(sp['title'].split('\n')):
            p = ease_out((t - 0.6 - i * 0.15) / 0.6)
            d.text((140 - (1 - p) * 60, y), line, font=ft, fill=WHITE + (int(255 * p),))
            y += 128
        p = ease_out((t - 1.0) / 0.6)
        draw_rich(d, 142, y + 14, sp.get('sub', ''), font(F_INTER, 44), MUTED, CYAN, maxw=1100, align='left')
        # tri bar
        bw = 360 * ease_out((t - 0.9) / 0.8)
        for i, c in enumerate((CYAN, AMBER, VIOLET)):
            if bw > 24:
                d.rectangle([140 + i * bw / 3, 236 - 14, 140 + (i + 1) * bw / 3 - 6, 236 - 8], fill=c)
        if sp.get('emoji'):
            s = int(180 * ease_back((t - 0.8) / 0.6))
            if s > 4:
                e = emoji(sp['emoji'], s); img.paste(e, (1200 - s // 2, 300 - s // 2), e)
        draw_bot(img, 1560, 860, 280, t, 'happy', 'wave', talking=self.talking(t))


class BubbleScene(Scene):
    mascot = 'none'

    def setup(self):
        self.items = []
        for i, b in enumerate(self.beats):
            for j, it in enumerate(b.get('items', [])):
                tt = self.starts[i] + 0.5 + j * 0.45
                self.items.append((tt, it)); self.events.append((tt, 'pop'))

    def beat_min(self, b):
        return 1.2 + 0.45 * len(b.get('items', []))

    def draw(self, img, d, t):
        k = self.beat_at(t)
        mood, arms = self.mood(t)
        draw_bot(img, 360, 850, 300, t, mood, arms if arms != 'down' else ('think' if mood == 'think' else 'down'), talking=self.talking(t), seed=1)
        if k >= 0:
            b = self.beats[k]; say = b.get('say', '')
            p = ease_back((t - self.starts[k]) / 0.45)
            if say and p > 0.02:
                f = font(F_POP, 50)
                th = text_h(say, f, 1000, 64)
                bx0, by0 = 640, 150; bx1 = 1780; by1 = by0 + th + 60
                sc = clamp(p, 0, 1.2)
                cxb, cyb = (bx0 + bx1) / 2, (by0 + by1) / 2
                box = [cxb - (cxb - bx0) * sc, cyb - (cyb - by0) * sc, cxb + (bx1 - cxb) * sc, cyb + (by1 - cyb) * sc]
                d.rounded_rectangle(box, radius=34, fill=(248, 250, 252))
                d.polygon([(box[0] + 40, box[3] - 30), (box[0] - 70 * sc, box[3] + 60 * sc), (box[0] + 120, box[3] - 4)], fill=(248, 250, 252))
                if p > 0.6:
                    draw_rich(d, cxb, by0 + 30, say, f, (15, 23, 42), (2, 132, 199), maxw=1000, lh=64)
        shown = [it for it in self.items if it[0] <= t]
        y = 470 if k < 0 or not self.beats[max(k, 0)].get('say') else 470
        n = len(shown); cols = 2 if n > 4 else 1
        for i, (tt, it) in enumerate(shown):
            p = ease_back((t - tt) / 0.45)
            col = i % cols if cols == 2 else 0; row = i // cols if cols == 2 else i
            cw = 540 if cols == 2 else 1000
            x = 680 + col * (cw + 40); yy = y + row * 92 + (1 - clamp(p)) * 30
            red = it.startswith('!r ')
            txt = it[3:] if red else it
            em, label = split_emoji(txt)
            panel(d, [x, yy, x + cw, yy + 76], fill=(60, 20, 30) if red else PANEL2, outline=RED if red else LINE, r=20)
            tx = x + 24
            if em:
                e = emoji(em, 44); img.paste(e, (int(tx), int(yy + 16)), e); tx += 62
            d.text((tx, yy + 38), label, font=font(F_MONOB if '.' in label or '_' in label else F_INTERSB, 34), fill=WHITE, anchor='lm')


class CardsScene(Scene):
    def setup(self):
        for i, s in enumerate(self.starts):
            if self.beats[i].get('card'):
                self.events.append((s + 0.2, 'pop'))

    def mood(self, t):
        k = self.beat_at(t)
        if k >= 0 and t - self.starts[k] < 1.0 and 'mood' not in self.beats[k]:
            return 'happy', 'point'
        return super().mood(t)

    def draw(self, img, d, t):
        self.title(d, t, self.spec.get('title', ''), self.spec.get('emoji'))
        cards = [(i, b['card']) for i, b in enumerate(self.beats) if b.get('card')]
        n = max(1, len(cards)); gap = 40; total = 1440
        cw = (total - gap * (n - 1)) / n; ch = 470
        k = self.beat_at(t)
        for j, (i, c) in enumerate(cards):
            st = self.starts[i] + 0.15
            p = ease_back((t - st) / 0.55)
            if t < st:
                continue
            x = 120 + j * (cw + gap); y = 300 + (1 - clamp(p)) * 60
            active = (i == k)
            col = c.get('color', [CYAN, AMBER, VIOLET, GREEN][j % 4])
            col = tuple(col)
            panel(d, [x, y, x + cw, y + ch], fill=PANEL2 if active else PANEL, outline=col if active else LINE, r=30, w=4 if active else 2)
            d.rectangle([x + 30, y + 22, x + 110, y + 28], fill=col)
            es = 130 if n <= 3 else 104
            e = emoji(c.get('emoji', '💡'), es); img.paste(e, (int(x + cw / 2 - e.width / 2), int(y + 60)), e)
            fs_ = 44 if n <= 3 else 38
            while fs_ > 24 and font(F_POP, fs_).getlength(c.get('title', '')) > cw - 40:
                fs_ -= 2
            ft = font(F_POP, fs_)
            d.text((x + cw / 2, y + 60 + es + 44), c.get('title', ''), font=ft, fill=col, anchor='mm')
            draw_rich(d, x + cw / 2, y + 60 + es + 92, c.get('text', ''), font(F_INTER, 32 if n <= 3 else 29), (203, 213, 225), CYAN, maxw=cw - 60, lh=44)


class VsScene(Scene):
    def setup(self):
        for i, b in enumerate(self.beats):
            if 'row' in b:
                self.events.append((self.starts[i] + 0.2, 'pop'))

    def draw(self, img, d, t):
        sp = self.spec
        self.title(d, t, sp.get('title', ''), sp.get('emoji'))
        cols = [(sp['left'], CYAN, 690), (sp['right'], VIOLET, 1310)]
        for j, (c, col, cx) in enumerate(cols):
            p = ease_back((t - 0.3 - j * 0.25) / 0.5)
            if p <= 0:
                continue
            y = 230 + (1 - clamp(p)) * 40
            panel(d, [cx - 220, y, cx + 220, y + 150], fill=PANEL2, outline=col, r=26, w=3)
            e = emoji(c.get('emoji', '💡'), 64); img.paste(e, (int(cx - 196), int(y + 43)), e)
            d.text((cx - 112 + 12, y + 50), c['title'], font=font(F_POP, 46), fill=col, anchor='lm')
            d.text((cx - 100, y + 104), c.get('sub', ''), font=font(F_INTER, 28), fill=MUTED, anchor='lm')
        vp = ease_back((t - 0.6) / 0.4)
        if vp > 0:
            d.ellipse([1000 - 38 * vp, 305 - 38 * vp, 1000 + 38 * vp, 305 + 38 * vp], fill=AMBER)
            d.text((1000, 305), 'VS', font=font(F_POP, int(30 * clamp(vp, .1, 1.2))), fill=(17, 24, 39), anchor='mm')
        rows = sp.get('rows', [])
        for i, b in enumerate(self.beats):
            if 'row' not in b or t < self.starts[i] + 0.1:
                continue
            r = b['row']; lab, lv, rv = rows[r]
            p = ease_out((t - self.starts[i] - 0.1) / 0.45)
            y = 420 + r * 102; act = self.beat_at(t) == i
            panel(d, [120, y, 1520, y + 88], fill=PANEL2 if act else PANEL, outline=AMBER if act else LINE, r=20, w=3 if act else 2)
            a = int(255 * p)
            d.text((150, y + 44), lab, font=font(F_POPM, 32), fill=AMBER + (a,), anchor='lm')
            for val, cx, col in ((lv, 760, CYAN), (rv, 1260, VIOLET)):
                em, txt = split_emoji(val)
                fx = font(F_INTERSB, 32)
                tw = fx.getlength(txt) + (50 if em else 0)
                x0 = cx - tw / 2 + (1 - p) * 30
                if em:
                    e = emoji(em, 38); img.paste(e, (int(x0), int(y + 25)), e); x0 += 50
                d.text((x0, y + 44), txt, font=fx, fill=WHITE + (a,), anchor='lm')


def _out_color(line):
    for k, c in (('!r ', RED), ('!g ', GREEN), ('!y ', AMBER), ('!c ', CYAN), ('!m ', MUTED)):
        if line.startswith(k):
            return line[3:], c
    return line, (203, 213, 225)


class TermScene(Scene):
    CPS = 20.0

    def beat_min(self, b):
        return 0.4 + len(b.get('cmd', '')) / self.CPS + 0.35 + 0.09 * len(b.get('out', [])) + 1.6

    def setup(self):
        self.tl = []  # per beat: (t_type_start, t_type_end, t_out_start)
        for i, b in enumerate(self.beats):
            s = self.starts[i] + 0.4; cmd = b.get('cmd', '')
            te = s + len(cmd) / self.CPS; to = te + 0.35
            self.tl.append((s, te, to))
            for c in range(len(cmd)):
                if cmd[c] != ' ':
                    self.events.append((s + c / self.CPS, 'type'))
            if b.get('out'):
                self.events.append((to, 'buzz' if b.get('err') else ('ding' if b.get('ok') else 'tick')))

    def mood(self, t):
        k = self.beat_at(t)
        if k >= 0:
            b = self.beats[k]
            if 'mood' in b:
                return b['mood'], b.get('arms', 'down')
            if t > self.tl[k][2]:
                if b.get('err'):
                    return 'shock', 'shock'
                if b.get('ok'):
                    return 'happy', 'up'
        return 'talk', 'down'

    def draw(self, img, d, t):
        sp = self.spec
        x0, y0, x1, y1 = 110, 120, 1580, 868
        panel(d, [x0, y0, x1, y1], fill=(9, 13, 26), outline=LINE, r=22)
        d.rounded_rectangle([x0, y0, x1, y0 + 56], radius=22, fill=(22, 30, 54))
        d.rectangle([x0, y0 + 30, x1, y0 + 56], fill=(22, 30, 54))
        for i, c in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
            d.ellipse([x0 + 26 + i * 34, y0 + 18, x0 + 46 + i * 34, y0 + 38], fill=c)
        cwd = sp.get('cwd', '~/my-project')
        d.text(((x0 + x1) / 2, y0 + 28), 'bash — ' + cwd, font=font(F_INTER, 26), fill=MUTED, anchor='mm')
        fm = font(F_MONO, 33); fb = font(F_MONOB, 33); lh = 47
        prompt_u = sp.get('user', 'shivam@tech-dev');
        lines = []  # list of list of (text, color, font)
        cursor = None; hl_tokens = []
        for i, b in enumerate(self.beats):
            ts, te, to = self.tl[i]
            if t < self.starts[i]:
                break
            cmd = b.get('cmd', '')
            if b.get('clear'):
                lines = []
            if cmd or b.get('prompt', True):
                n = int(clamp((t - ts) * self.CPS, 0, len(cmd))) if t >= ts else 0
                typed = cmd[:n]
                pr = [(prompt_u, GREEN, fb), (':', WHITE, fm), (cwd, CYAN, fb), ('$ ', WHITE, fm)]
                if b.get('comment') and t < ts:
                    pass
                lines.append(pr + [(typed, WHITE, fm)])
                if i == self.beat_at(t) and n < len(cmd) or (i == self.beat_at(t) and not b.get('out') and t >= te):
                    cursor = len(lines) - 1
                if b.get('hl') and t >= te + 0.2 and i == self.beat_at(t):
                    hl_tokens.append((len(lines) - 1, b['hl'], t - te - 0.2))
            if t >= to:
                outs = b.get('out', [])
                m = int(clamp((t - to) / 0.09 + 1, 0, len(outs)))
                for ln in outs[:m]:
                    txt, c = _out_color(ln)
                    if b.get('err') and not ln.startswith('!'):
                        c = RED
                    elif b.get('ok') and not ln.startswith('!'):
                        c = GREEN
                    lines.append([(txt, c, fm)])
        maxl = 14
        off = max(0, len(lines) - maxl)
        vis = lines[off:]
        for li, segs in enumerate(vis):
            x = x0 + 34; y = y0 + 84 + li * lh
            for txt, c, f in segs:
                d.text((x, y), txt, font=f, fill=c); x += f.getlength(txt)
            if cursor is not None and li + off == cursor and (t * 2.2) % 2 < 1.4:
                d.rectangle([x + 2, y + 2, x + 20, y + 38], fill=WHITE)
        for (li, toks, dt) in hl_tokens:
            if li < off:
                continue
            segs = lines[li]; full = ''.join(s[0] for s in segs)
            y = y0 + 84 + (li - off) * lh
            for tok in toks:
                idx = full.rfind(tok)
                if idx < 0:
                    continue
                pre = full[:idx]
                xs = x0 + 34 + sum(font(F_MONOB if j < 3 and j != 1 else F_MONO, 33).getlength(s[0]) for j, s in enumerate(segs) if sum(len(q[0]) for q in segs[:j]) + len(s[0]) <= idx)
                # simpler precise: measure char by char
                xs = x0 + 34; acc = 0
                for s_txt, _, f in segs:
                    if acc + len(s_txt) <= idx:
                        xs += f.getlength(s_txt); acc += len(s_txt)
                    else:
                        xs += f.getlength(s_txt[:idx - acc]); break
                wtok = fm.getlength(tok)
                p = ease_back(dt / 0.4)
                pad = 8 * clamp(p)
                d.rounded_rectangle([xs - pad, y - 4 - pad / 2, xs + wtok + pad, y + 42 + pad / 2], radius=10, outline=AMBER, width=4)
        k = self.beat_at(t)
        if k >= 0:
            b = self.beats[k]; note = b.get('note')
            ts, te, to = self.tl[k]
            if note and t > te + 0.3:
                p = ease_back((t - te - 0.3) / 0.45)
                f = font(F_INTERSB, 32)
                tw = f.getlength(note) + 110
                bx = x1 - 30 - tw; by = y1 - 96 + (1 - clamp(p)) * 30
                d.rounded_rectangle([bx, by, x1 - 30, by + 70], radius=35, fill=(66, 46, 6), outline=AMBER, width=3)
                e = emoji('💡', 40); img.paste(e, (int(bx + 22), int(by + 15)), e)
                d.text((bx + 80, by + 35), note, font=f, fill=(254, 243, 199), anchor='lm')


class LanesScene(Scene):
    LANES = [('wd', 'Working Directory', '📁', CYAN), ('stage', 'Staging Area', '📦', AMBER), ('repo', 'Repository', '🗄️', VIOLET)]
    MOVE_AT = 0.9; MOVE_D = 0.8

    def beat_min(self, b):
        return 2.6

    def setup(self):
        files = {}; order = []; commits = []
        self.states = []  # (before, after) each: files dict, commits list
        def snap():
            return ({k: dict(v) for k, v in files.items()}, list(order), list(commits))
        for f in self.spec.get('files', []):
            files[f] = {'lane': 'wd', 'st': 'U'}; order.append(f)
        for i, b in enumerate(self.beats):
            before = snap()
            for f in b.get('new', []):
                files[f] = {'lane': 'wd', 'st': 'U'}; order.append(f)
            for f in b.get('modify', []):
                files[f] = {'lane': 'wd', 'st': 'M'}
                if f in order: order.remove(f)
                order.append(f)
            add = b.get('add', [])
            if add == '.' or add == ['.']:
                add = [f for f in order if files.get(f, {}).get('lane') == 'wd']
            for f in add:
                if f in files:
                    files[f] = {'lane': 'stage', 'st': 'A' if files[f]['st'] == 'U' else 'M'}
            for f in b.get('unstage', []):
                if f in files:
                    files[f] = {'lane': 'wd', 'st': 'U' if files[f]['st'] == 'A' else 'M'}
            for f in b.get('restore', []):
                files.pop(f, None)
                if f in order: order.remove(f)
            if b.get('commit'):
                staged = [f for f in order if files[f]['lane'] == 'stage']
                commits.append({'msg': b['commit'], 'files': staged, 'id': 'C%d' % (len(commits) + 1)})
                for f in staged:
                    files[f] = {'lane': 'gone', 'st': '', 'into': len(commits) - 1}
                    order.remove(f)
            self.states.append((before, snap()))
            self.events.append((self.starts[i] + self.MOVE_AT, 'pop'))
            if b.get('commit'):
                self.events.append((self.starts[i] + self.MOVE_AT + self.MOVE_D, 'ding'))

    def lane_x(self, lane):
        return {'wd': 120, 'stage': 610, 'repo': 1100}[lane]

    def positions(self, state):
        files, order, commits = state; pos = {}; cnt = {'wd': 0, 'stage': 0}
        for f in order:
            ln = files[f]['lane']
            if ln in cnt:
                pos[f] = (self.lane_x(ln) + 24, 330 + cnt[ln] * 78); cnt[ln] += 1
        return pos

    def commit_pos(self, j, ncommits):
        return (self.lane_x('repo') + 24, 330 + (ncommits - 1 - j) * 96)

    def chip(self, img, d, x, y, name, st, alpha=1.0):
        col = {'U': RED, 'M': AMBER, 'A': GREEN}.get(st, MUTED)
        panel(d, [x, y, x + 392, y + 64], fill=PANEL2, outline=col, r=16, w=2)
        e = emoji('📄', 34); img.paste(e, (int(x + 16), int(y + 15)), e)
        d.text((x + 64, y + 32), name, font=font(F_MONOB, 30), fill=WHITE, anchor='lm')
        if st:
            d.rounded_rectangle([x + 336, y + 14, x + 376, y + 50], radius=8, fill=col)
            d.text((x + 356, y + 32), st, font=font(F_MONOB, 26), fill=(15, 23, 42), anchor='mm')

    def draw(self, img, d, t):
        for j, (key, name, em, col) in enumerate(self.LANES):
            p = ease_out((t - j * 0.15) / 0.5)
            x = self.lane_x(key); y = 230 + (1 - p) * 40
            panel(d, [x, y, x + 440, 860], fill=PANEL, outline=col, r=26, w=2)
            e = emoji(em, 46); img.paste(e, (x + 22, int(y + 16)), e)
            d.text((x + 82, y + 40), name, font=font(F_POP, 32), fill=col, anchor='lm')
            if j < 2:
                ax = x + 452; d.polygon([(ax, 540), (ax + 26, 560), (ax, 580)], fill=LINE)
        k = self.beat_at(t)
        if k < 0:
            state = self.states[0][0] if self.states else ({}, [], []); mv = 0; before = after = state
        else:
            before, after = self.states[k]
            lt = t - self.starts[k]
            mv = ease_io((lt - self.MOVE_AT) / self.MOVE_D)
            b = self.beats[k]
            cmd = b.get('cmd')
            if cmd:
                pa = ease_back(lt / 0.4)
                f = font(F_MONOB, 36)
                tw = f.getlength('$ ' + cmd) + 60
                bx = 120; by = 132 + (1 - clamp(pa)) * -20
                d.rounded_rectangle([bx, by, bx + tw, by + 70], radius=18, fill=(9, 13, 26), outline=GREEN, width=3)
                d.text((bx + 30, by + 35), '$ ', font=f, fill=GREEN, anchor='lm')
                d.text((bx + 30 + f.getlength('$ '), by + 35), cmd, font=f, fill=WHITE, anchor='lm')
        pb = self.positions(before); pa_ = self.positions(after)
        fb, ob, cb = before; fa, oa, ca = after
        # commits
        for j, c in enumerate(ca):
            new = j >= len(cb)
            if new and mv < 0.85:
                continue
            x, y = self.commit_pos(j, len(ca) if (not new or mv >= .85) else len(cb))
            if not new:
                ox, oy = self.commit_pos(j, len(cb)); x = lerp(ox, x, mv); y = lerp(oy, y, mv)
            p = ease_back((mv - 0.85) / 0.15) if new else 1
            panel(d, [x, y, x + 392, y + 82], fill=(36, 28, 70), outline=VIOLET, r=18, w=3)
            r_ = 22 * clamp(p, 0.3, 1.2)
            d.ellipse([x + 40 - r_, y + 41 - r_, x + 40 + r_, y + 41 + r_], fill=VIOLET)
            d.text((x + 40, y + 41), c['id'][1:], font=font(F_MONOB, 22), fill=(15, 23, 42), anchor='mm')
            d.text((x + 76, y + 26), c['id'] + '  "' + c['msg'] + '"', font=font(F_MONOB, 24), fill=WHITE, anchor='lm')
            d.text((x + 76, y + 58), ', '.join(c['files'])[:30], font=font(F_MONO, 20), fill=MUTED, anchor='lm')
        names = list(dict.fromkeys(ob + oa + [f for f in fa if fa[f]['lane'] == 'gone' and f in fb and fb[f]['lane'] != 'gone']))
        for f in names:
            if f in pb and f in pa_:
                x = lerp(pb[f][0], pa_[f][0], mv); y = lerp(pb[f][1], pa_[f][1], mv) - math.sin(mv * math.pi) * 60
                st = fa[f]['st'] if mv > .5 else fb[f]['st']
                self.chip(img, d, x, y, f, st)
            elif f in pa_ and f not in pb:
                if mv <= 0:
                    continue
                p = ease_back(mv / 0.6)
                x, y = pa_[f]; self.chip(img, d, x, y + (1 - clamp(p)) * 30, f, fa[f]['st'])
            elif f in pb and f not in pa_:
                if fa.get(f, {}).get('lane') == 'gone':
                    j = fa[f]['into']; tx, ty = self.commit_pos(j, len(ca))
                    if mv < 0.85:
                        x = lerp(pb[f][0], tx, mv / .85); y = lerp(pb[f][1], ty, mv / .85) - math.sin(mv / .85 * math.pi) * 70
                        self.chip(img, d, x, y, f, fb[f]['st'])
                elif mv < 1:
                    self.chip(img, d, pb[f][0] - mv * 40, pb[f][1], f, fb[f]['st'])


class GraphScene(Scene):
    OP_D = 0.65

    def beat_min(self, b):
        return 0.6 + self.OP_D * len(b.get('ops', [])) + 1.4

    def setup(self):
        self.nodes = []; self.br = {}; self.head = []; self.tags = []
        bi = 0; xi = 0
        def tip(b, tt):
            h = [n for (ti, n) in self.br[b]['tips'] if ti <= tt]
            return h[-1] if h else None
        def anc(nid):
            s = set(); st = [nid]
            while st:
                c = st.pop()
                if c is None or c in s: continue
                s.add(c); st.extend(self.nodes[c]['par'])
            return s
        for f in self.spec.get('branches', ['main']):
            self.br[f] = {'row': bi, 'col': BRANCH_COLORS[bi % 5], 'tips': [(0, None)], 'born': 0}; bi += 1
        self.head.append((0, self.spec.get('head', 'main')))
        def add_node(b, label, par, tt, ghost_of=None):
            nonlocal xi
            self.nodes.append({'label': label, 'row': self.br[b]['row'], 'col': self.br[b]['col'], 'x': xi, 'par': par, 'born': tt, 'ghost': None})
            xi += 1; self.events.append((tt, 'pop'))
            return len(self.nodes) - 1
        for i, b in enumerate(self.beats):
            for j, op in enumerate(b.get('ops', [])):
                tt = self.starts[i] + 0.5 + j * self.OP_D
                o = op[0]
                if o == 'commit':
                    br = op[1]; p = tip(br, tt)
                    n = add_node(br, op[2], [p] if p is not None else [], tt)
                    self.br[br]['tips'].append((tt, n))
                elif o == 'branch':
                    self.br[op[1]] = {'row': bi, 'col': BRANCH_COLORS[bi % 5], 'tips': [(tt, tip(op[2], tt))], 'born': tt}; bi += 1
                    self.events.append((tt, 'pop'))
                elif o == 'checkout':
                    self.head.append((tt, op[1])); self.events.append((tt, 'tick'))
                elif o == 'merge':
                    src, dst = op[1], op[2]
                    n = add_node(dst, op[3] if len(op) > 3 else 'M', [tip(dst, tt), tip(src, tt)], tt)
                    self.br[dst]['tips'].append((tt, n)); self.events.append((tt + 0.1, 'ding'))
                elif o == 'ff':
                    src, dst = op[1], op[2]; self.br[dst]['tips'].append((tt, tip(src, tt))); self.events.append((tt, 'ding'))
                elif o in ('rebase', 'squash'):
                    src = op[1]
                    if o == 'rebase':
                        base = anc(tip(op[2], tt)); chain = []; c = tip(src, tt)
                        while c is not None and c not in base:
                            chain.append(c); c = self.nodes[c]['par'][0] if self.nodes[c]['par'] else None
                        chain.reverse(); par = tip(op[2], tt)
                        for c in chain:
                            self.nodes[c]['ghost'] = tt
                        for q, c in enumerate(chain):
                            par = add_node(src, self.nodes[c]['label'] + "'", [par], tt + 0.25 + q * 0.2)
                        self.br[src]['tips'].append((tt, par))
                    else:
                        nsq = op[2]; chain = []; c = tip(src, tt)
                        for _ in range(nsq):
                            chain.append(c); c = self.nodes[c]['par'][0] if self.nodes[c]['par'] else None
                        for c2 in chain:
                            self.nodes[c2]['ghost'] = tt
                        n = add_node(src, op[3] if len(op) > 3 else 'S', [c] if c is not None else [], tt + 0.3)
                        self.br[src]['tips'].append((tt, n))
                elif o == 'cherry':
                    lab, dst = op[1], op[2]
                    p = tip(dst, tt); n = add_node(dst, lab + "'", [p] if p is not None else [], tt)
                    self.br[dst]['tips'].append((tt, n))
                elif o == 'tag':
                    nid = [q for q, nn in enumerate(self.nodes) if nn['label'] == op[1]][-1]
                    self.tags.append((tt, nid, op[2])); self.events.append((tt, 'pop'))
                elif o == 'reset':
                    br = op[1]; nid = [q for q, nn in enumerate(self.nodes) if nn['label'] == op[2]][-1]
                    old = tip(br, tt); c = old
                    while c is not None and c != nid:
                        self.nodes[c]['ghost'] = tt; c = self.nodes[c]['par'][0] if self.nodes[c]['par'] else None
                    self.br[br]['tips'].append((tt, nid)); self.events.append((tt, 'whoosh'))
        self.nbr = bi; self.ncols = max(1, xi)
        self.step = min(210, 1050 / max(1, self.ncols - 1)) if self.ncols > 1 else 210
        self.rowh = min(190, 460 / max(1, self.nbr - 1)) if self.nbr > 1 else 0
        self.y0 = 540 - (self.nbr - 1) * self.rowh / 2 + 20
        self.x0 = 360 + (1150 - (self.ncols - 1) * self.step) / 2
        self._tip = tip

    def npos(self, n):
        return self.x0 + n['x'] * self.step, self.y0 + n['row'] * self.rowh

    def draw(self, img, d, t):
        self.title(d, t, self.spec.get('title', ''), self.spec.get('emoji'))
        rowh = self.rowh
        for name, b in self.br.items():
            if t < b['born']:
                continue
            p = ease_out((t - b['born']) / 0.5)
            y = self.y0 + b['row'] * rowh
            d.line([(330, y), (330 + (1250 * p), y)], fill=tuple(int(c * .25 + 10) for c in b['col']), width=3)
            pill(d, 120, y - 24, name, font(F_MONOB, 28), (15, 23, 42), b['col'], padx=16, pady=7)
        # edges
        for q, n in enumerate(self.nodes):
            if t < n['born']:
                continue
            x, y = self.npos(n); p = ease_out((t - n['born']) / 0.35)
            for pid in n['par']:
                if pid is None:
                    continue
                px, py = self.npos(self.nodes[pid])
                gh = n['ghost'] is not None and t > n['ghost']
                col = (60, 70, 100) if gh else n['col']
                pts = []
                for s in range(21):
                    u = s / 20 * p
                    if py == y:
                        pts.append((lerp(px, x, u), y))
                    else:
                        bx = (1 - u) ** 3 * px + 3 * (1 - u) ** 2 * u * (px + (x - px) * .6) + 3 * (1 - u) * u * u * (px + (x - px) * .4) + u ** 3 * x
                        by = (1 - u) ** 3 * py + 3 * (1 - u) ** 2 * u * py + 3 * (1 - u) * u * u * y + u ** 3 * y
                        pts.append((bx, by))
                d.line(pts, fill=col, width=6, joint='curve')
        for q, n in enumerate(self.nodes):
            if t < n['born']:
                continue
            x, y = self.npos(n); p = ease_back((t - n['born']) / 0.45)
            r = 38 * clamp(p, 0, 1.3)
            gh = n['ghost'] is not None and t > n['ghost']
            ga = clamp((t - n['ghost']) / 0.5) if gh else 0
            col = lerpc(n['col'], (45, 55, 85), ga)
            d.ellipse([x - r - 6, y - r - 6, x + r + 6, y + r + 6], fill=BG)
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
            if p > 0.5:
                fs = 28 if len(n['label']) <= 3 else 22
                d.text((x, y), n['label'], font=font(F_MONOB, fs), fill=(15, 23, 42) if not gh else (110, 120, 150), anchor='mm')
        # branch pointers
        for name, b in self.br.items():
            if t < b['born']:
                continue
            tp = self._tip(name, t)
            if tp is None:
                continue
            x, y = self.npos(self.nodes[tp])
            # stack labels if multiple branches point to same node
            same = [nm for nm, bb in self.br.items() if t >= bb['born'] and self._tip(nm, t) == tp]
            k = same.index(name)
            ly = y - 100 - k * 46
            f = font(F_MONOB, 24)
            pill(d, x, ly, name, f, (15, 23, 42), b['col'], padx=12, pady=6, anchor='c')
            hb = [h for (ti, h) in self.head if ti <= t][-1]
            if hb == name:
                pill(d, x + f.getlength(name) / 2 + 24, ly, 'HEAD', font(F_MONOB, 22), WHITE, (190, 40, 70), padx=10, pady=7)
        for (tt, nid, tg) in self.tags:
            if t < tt:
                continue
            x, y = self.npos(self.nodes[nid]); p = ease_back((t - tt) / .4)
            e = emoji('🏷️', 34); img.paste(e, (int(x - 60), int(y + 46)), e)
            d.text((x - 20, y + 64), tg, font=font(F_MONOB, 24), fill=AMBER, anchor='lm')


class CodeScene(Scene):
    def draw(self, img, d, t):
        sp = self.spec; k = self.beat_at(t)
        lines = sp.get('lines', [])
        hl = []
        for i in range(0, k + 1):
            b = self.beats[i]
            if 'lines' in b:
                lines = b['lines']
            hl = b.get('hl', [])
        x0, y0, x1, y1 = 110, 120, 1580, 868
        panel(d, [x0, y0, x1, y1], fill=(13, 17, 32), outline=LINE, r=22)
        d.rounded_rectangle([x0, y0, x1, y0 + 60], radius=22, fill=(22, 30, 54)); d.rectangle([x0, y0 + 30, x1, y0 + 60], fill=(22, 30, 54))
        d.rounded_rectangle([x0 + 24, y0 + 10, x0 + 60 + font(F_INTERSB, 26).getlength(sp.get('file', 'file.txt')) + 30, y0 + 60], radius=10, fill=(13, 17, 32))
        d.text((x0 + 50, y0 + 36), sp.get('file', 'file.txt'), font=font(F_INTERSB, 26), fill=WHITE, anchor='lm')
        fm = font(F_MONO, 32); lh = 48; mode = None
        for i, ln in enumerate(lines[:14]):
            y = y0 + 90 + i * lh
            c = (203, 213, 225)
            if ln.startswith('<<<<<<<'):
                c = RED; mode = 'ours'; d.rectangle([x0 + 2, y - 6, x1 - 2, y + lh - 6], fill=(60, 22, 34))
            elif ln.startswith('======='):
                c = MUTED; mode = 'theirs'
            elif ln.startswith('>>>>>>>'):
                c = RED; mode = None; d.rectangle([x0 + 2, y - 6, x1 - 2, y + lh - 6], fill=(60, 22, 34))
            elif mode == 'ours':
                c = CYAN; d.rectangle([x0 + 2, y - 6, x1 - 2, y + lh - 6], fill=(14, 40, 64))
            elif mode == 'theirs':
                c = VIOLET; d.rectangle([x0 + 2, y - 6, x1 - 2, y + lh - 6], fill=(40, 30, 72))
            for (a, bb, *col) in hl:
                if a <= i + 1 <= bb:
                    cc = tuple(col[0]) if col else AMBER
                    d.rectangle([x0 + 2, y - 6, x0 + 10, y + lh - 6], fill=cc)
            d.text((x0 + 30, y), '%2d' % (i + 1), font=fm, fill=(71, 85, 105))
            d.text((x0 + 110, y), ln, font=fm, fill=c)
        if k >= 0 and self.beats[k].get('note'):
            note = self.beats[k]['note']; p = ease_back((t - self.starts[k] - .4) / .45)
            if p > 0:
                f = font(F_INTERSB, 32); tw = f.getlength(note) + 110
                bx = x1 - 30 - tw; by = y1 - 96 + (1 - clamp(p)) * 30
                d.rounded_rectangle([bx, by, x1 - 30, by + 70], radius=35, fill=(66, 46, 6), outline=AMBER, width=3)
                e = emoji('💡', 40); img.paste(e, (int(bx + 22), int(by + 15)), e)
                d.text((bx + 80, by + 35), note, font=f, fill=(254, 243, 199), anchor='lm')


class RecapScene(Scene):
    STEP = 0.55

    def beat_min(self, b):
        return 0

    def setup(self):
        n = len(self.spec.get('items', []))
        self.dur = max(self.dur, self.lead + 0.6 + n * self.STEP + 2.0)
        for i in range(n):
            self.events.append((self.lead + 0.6 + i * self.STEP, 'pop'))

    def draw(self, img, d, t):
        self.title(d, t, self.spec.get('title', 'Cheat sheet'), self.spec.get('emoji', '📝'))
        items = self.spec.get('items', [])
        fm = font(F_MONOB, 32); fi = font(F_INTER, 32)
        cw = max([fm.getlength(c) for c, _ in items] + [200]) + 56
        rh = min(92, 600 / max(1, len(items)))
        for i, (c, desc) in enumerate(items):
            tt = self.lead + 0.6 + i * self.STEP
            if t < tt:
                continue
            p = ease_back((t - tt) / .45); y = 250 + i * rh
            x = 120 + (1 - clamp(p)) * -40
            panel(d, [x, y, 1540, y + rh - 16], fill=PANEL, outline=LINE, r=18)
            d.rounded_rectangle([x + 14, y + 12, x + 14 + cw, y + rh - 28], radius=12, fill=(9, 13, 26), outline=CYAN, width=2)
            d.text((x + 14 + 28, y + (rh - 16) / 2), c, font=fm, fill=CYAN, anchor='lm')
            d.text((x + cw + 50, y + (rh - 16) / 2), desc, font=fi, fill=WHITE, anchor='lm')
            e = emoji('✅', 34); img.paste(e, (1480, int(y + (rh - 16) / 2 - 17)), e)


class QuizScene(Scene):
    def setup(self):
        for i, b in enumerate(self.beats):
            if b.get('reveal'):
                self.events.append((self.starts[i] + 0.15, 'tada'))
            self.rev_t = next((self.starts[i] for i, b in enumerate(self.beats) if b.get('reveal')), 1e9)

    def beat_min(self, b):
        return 4.0 if not b.get('reveal') else 2.5

    def mood(self, t):
        if t >= self.rev_t:
            return 'party', 'up'
        return 'think', 'think'

    def draw(self, img, d, t):
        sp = self.spec
        pill(d, 120, 130, 'QUICK QUIZ', font(F_POP, 30), (17, 24, 39), AMBER, padx=22, pady=9)
        e = emoji('🧠', 52); img.paste(e, (380, 124), e)
        draw_rich(d, 120, 210, sp['q'], font(F_POP, 54), WHITE, CYAN, maxw=1400, align='left', lh=70)
        opts = sp['opts']; rev = t >= self.rev_t
        for i, o in enumerate(opts):
            p = ease_back((t - 0.5 - i * 0.18) / 0.45)
            if p <= 0:
                continue
            cx = i % 2; cy = i // 2
            x = 120 + cx * 720; y = 420 + cy * 170 + (1 - clamp(p)) * 30
            good = i == sp['ans']
            col = GREEN if (rev and good) else LINE
            fill = (16, 60, 48) if (rev and good) else PANEL
            a = 0.35 if (rev and not good) else 1
            panel(d, [x, y, x + 680, y + 140], fill=fill, outline=col, r=24, w=4 if rev and good else 2)
            d.ellipse([x + 26, y + 38, x + 90, y + 102], fill=lerpc(BG, CYAN if not rev or good else MUTED, a))
            d.text((x + 58, y + 70), 'ABCD'[i], font=font(F_POP, 34), fill=(15, 23, 42), anchor='mm')
            d.text((x + 116, y + 70), o, font=font(F_INTERSB, 38), fill=lerpc(BG, WHITE, a), anchor='lm')
            if rev and good:
                e = emoji('✅', 56); img.paste(e, (x + 600, int(y + 42)), e)
        if not rev and self.beats:
            # countdown ring in last 3s before reveal
            rem = self.rev_t - t
            if rem < 3.2:
                p = clamp(rem / 3.2)
                d.arc([1380, 120, 1500, 240], -90, -90 + 360 * p, fill=AMBER, width=10)
                d.text((1440, 180), str(int(math.ceil(rem))), font=font(F_POP, 48), fill=WHITE, anchor='mm')


class OutroScene(Scene):
    mascot = 'none'

    def setup(self):
        self.dur = max(self.dur, 16.0); self.events.append((0.8, 'pop'))

    def draw(self, img, d, t):
        sp = self.spec; ep = self.ep
        p = ease_out(t / 0.6)
        d.text((120, 190 + (1 - p) * 30), sp.get('head', 'Thanks for watching!'), font=font(F_POP, 76), fill=WHITE)
        draw_rich(d, 122, 300, sp.get('sub', 'New Git episode *every day at 4 PM*. Follow the full playlist!'), font(F_INTER, 38), MUTED, AMBER, maxw=780, align='left')
        pb = ease_back((t - 0.8) / 0.5); pulse = 1 + 0.04 * math.sin(t * 5)
        if pb > 0:
            s = clamp(pb, 0, 1.2) * pulse; bx, by = 340, 520
            w2, h2 = 220 * s, 52 * s
            d.rounded_rectangle([bx - w2, by - h2, bx + w2, by + h2], radius=h2, fill=RED)
            d.text((bx + 20 * s, by), 'SUBSCRIBE', font=font(F_POP, max(8, int(44 * s))), fill=WHITE, anchor='mm')
            e = emoji('🔔', max(8, int(54 * s))); img.paste(e, (int(bx - w2 + 30 * s), int(by - 27 * s)), e)
        nx = sp.get('next')
        if nx:
            pn = ease_out((t - 1.4) / 0.6)
            d.text((120, 660), 'UP NEXT', font=font(F_POP, 28), fill=AMBER + (int(255 * pn),))
            draw_rich(d, 120, 700, nx, font(F_POP, 40), WHITE, CYAN, maxw=780, align='left', lh=52)
        # end-screen safe area (right half) — subtle frames
        for (bx0, by0, bx1, by1) in ((1020, 160, 1820, 590), ):
            d.rounded_rectangle([bx0, by0, bx1, by1], radius=26, outline=(38, 50, 86), width=2)
        d.text((1420, 375), 'Watch next', font=font(F_POP, 40), fill=(52, 66, 104), anchor='mm')
        draw_bot(img, 1700, 880, 140, t, 'happy', 'wave', talking=self.talking(t), seed=2)


SCENES = {'title': TitleScene, 'bubble': BubbleScene, 'cards': CardsScene, 'vs': VsScene, 'terminal': TermScene,
          'lanes': LanesScene, 'graph': GraphScene, 'code': CodeScene, 'recap': RecapScene, 'quiz': QuizScene, 'outro': OutroScene}


# ---------------------------------------------------------------- episode
class Episode:
    def __init__(self, ep):
        self.ep = ep
        self.scenes = [SCENES[s['type']](s, ep) for s in ep['scenes']]
        self.offsets = []; t = 0
        for s in self.scenes:
            self.offsets.append(t); t += s.dur
        self.total = t
        self.bg = make_bg()
        self.base = self.bg.copy(); d = ImageDraw.Draw(self.base)
        d.rectangle([0, 0, W, 86], fill=(10, 14, 30))
        d.rounded_rectangle([36, 20, 236, 66], radius=12, fill=(17, 24, 45), outline=LINE, width=2)
        d.text((54, 43), '>_', font=font(F_MONOB, 28), fill=GREEN, anchor='lm')
        d.text((98, 43), 'Tech-dev', font=font(F_POP, 26), fill=WHITE, anchor='lm')
        d.text((262, 43), ep.get('series', 'Git & GitHub · Beginner → Advanced'), font=font(F_INTER, 26), fill=MUTED, anchor='lm')
        f = font(F_INTERSB, 26)
        right = ep.get('short', '')
        rx = W - 40 - f.getlength(right)
        d.text((rx, 43), right, font=f, fill=WHITE, anchor='lm')
        pill(d, rx - 20, 24, 'EP %02d' % ep['num'], font(F_POP, 22), (17, 24, 39), AMBER, padx=14, pady=6, anchor='r')

    def frame(self, si, t):
        sc = self.scenes[si]
        img = self.base.copy(); d = ImageDraw.Draw(img, 'RGBA')
        g = (self.offsets[si] + t) / self.total
        d.rectangle([0, 86, W, 90], fill=(28, 36, 62))
        gw = W * g
        for i, c in enumerate((CYAN, AMBER, VIOLET)):
            a, b = W * i / 3, W * (i + 1) / 3
            if gw > a:
                d.rectangle([a, 86, min(gw, b), 90], fill=c)
        sc.draw(img, d, t)
        if sc.mascot == 'corner':
            mood, arms = sc.mood(t)
            draw_bot(img, 1745, 870, 150, t, mood, arms, talking=sc.talking(t), seed=si)
        # caption
        k = sc.beat_at(t)
        if k >= 0 and sc.beats[k].get('cap'):
            cap = sc.beats[k]['cap']; lt = t - sc.starts[k]
            p = ease_out(lt / 0.3)
            f = font(F_INTERSB, 42)
            lines = wrap_rich(cap, f, 1500)
            hh = len(lines) * 56 + 34
            y0 = 1052 - hh + (1 - p) * 14
            wmax = max(l[0] for l in lines) + 70
            d.rounded_rectangle([W / 2 - wmax / 2, y0, W / 2 + wmax / 2, y0 + hh], radius=22, fill=(8, 12, 26, int(235 * p)), outline=(44, 56, 92, int(255 * p)), width=2)
            draw_rich(d, W / 2, y0 + 16, cap, f, WHITE, AMBER, maxw=1500, lh=56, alpha=int(255 * p))
        fa = 0.32
        if t < fa or t > sc.dur - fa:
            a = clamp(t / fa) if t < fa else clamp((sc.dur - t) / fa)
            img = Image.blend(self.bg, img, ease_io(a))
        return img

    def chapters(self):
        out = []; last = -99
        for s, off in zip(self.scenes, self.offsets):
            ch = s.spec.get('chapter')
            if not ch:
                continue
            if not out:
                out.append((0, ch)); last = 0
            elif off - last >= 10:
                out.append((off, ch)); last = off
            elif len(out) == 1:
                out[0] = (0, ch)
        return out


_EPI = None


def render_scene(args):
    si, path = args; epi = _EPI
    sc = epi.scenes[si]; n = int(round(sc.dur * FPS))
    tmp = path + '.part.mp4'
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (W, H), '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(epi.frame(si, i / FPS).convert('RGB').tobytes())
    p.stdin.close(); rc = p.wait()
    if rc != 0:
        raise RuntimeError('ffmpeg failed on scene %d' % si)
    os.replace(tmp, path)
    return si


# ---------------------------------------------------------------- audio
SR = 44100


def synth_audio(epi, path):
    T = epi.total + 0.5; N = int(T * SR); tt = np.arange(N) / SR
    mus = np.zeros(N)
    bpm = 78; beat = 60 / bpm; bar = beat * 4
    chords = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 64]]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    nb = int(T / bar) + 1
    for bi in range(nb):
        ch = chords[bi % 4]; s0 = int(bi * bar * SR); s1 = min(N, int((bi + 1) * bar * SR) + int(.4 * SR))
        if s0 >= N: break
        loc = tt[s0:s1] - bi * bar
        env = np.minimum(1, loc / 0.35) * np.exp(-loc * 0.35)
        for m in ch:
            f = hz(m)
            mus[s0:s1] += 0.045 * env * (np.sin(2 * np.pi * f * loc) + 0.35 * np.sin(2 * np.pi * 2 * f * loc) * np.exp(-loc * 1.5) + 0.25 * np.sin(2 * np.pi * f * 1.003 * loc))
        fb = hz(ch[0] - 12)
        mus[s0:s1] += 0.06 * np.exp(-loc * 1.2) * np.sin(2 * np.pi * fb * loc)
    rng = np.random.default_rng(3); noise = rng.standard_normal(N)
    nbeats = int(T / beat)
    for k in range(nbeats):
        s0 = int(k * beat * SR)
        if s0 >= N: break
        if k % 4 in (0, 2) or k % 8 == 7:  # kick
            L = min(int(.35 * SR), N - s0); lt = np.arange(L) / SR
            f = 50 + 70 * np.exp(-lt * 25)
            mus[s0:s0 + L] += 0.16 * np.exp(-lt * 9) * np.sin(2 * np.pi * np.cumsum(f) / SR)
        if k % 4 in (1, 3):  # snare (soft)
            L = min(int(.22 * SR), N - s0); lt = np.arange(L) / SR
            mus[s0:s0 + L] += 0.05 * np.exp(-lt * 18) * noise[s0:s0 + L]
        for half in (0, 0.5):  # hats
            h0 = int((k + half) * beat * SR)
            if h0 >= N: continue
            L = min(int(.05 * SR), N - h0); lt = np.arange(L) / SR
            hn = np.diff(noise[h0:h0 + L + 1])
            mus[h0:h0 + L] += 0.018 * np.exp(-lt * 60) * hn
    # crude lowpass for warmth
    k = np.ones(6) / 6; mus = np.convolve(mus, k, mode='same')
    fx = np.zeros(N)
    def put(t0, sig):
        s0 = int(t0 * SR)
        if s0 >= N or s0 < 0: return
        L = min(len(sig), N - s0); fx[s0:s0 + L] += sig[:L]
    def env(L, dec):
        lt = np.arange(L) / SR; return lt, np.exp(-lt * dec)
    for off, sc in zip(epi.offsets, epi.scenes):
        for (et, kind) in sc.events:
            t0 = off + et
            if kind == 'whoosh':
                L = int(.6 * SR); lt = np.arange(L) / SR; n = rng.standard_normal(L)
                n = np.convolve(n, np.ones(30) / 30, 'same'); e = np.sin(np.pi * lt / .6) ** 2
                put(t0 - 0.1, 0.10 * e * n)
            elif kind == 'pop':
                L = int(.12 * SR); lt, e = env(L, 35)
                put(t0, 0.09 * e * np.sin(2 * np.pi * (500 + 900 * lt / .12) * lt))
            elif kind == 'type':
                L = int(.018 * SR); lt, e = env(L, 300)
                put(t0, 0.05 * e * rng.standard_normal(L))
            elif kind == 'tick':
                L = int(.05 * SR); lt, e = env(L, 80)
                put(t0, 0.06 * e * np.sin(2 * np.pi * 1200 * lt))
            elif kind == 'ding':
                L = int(.9 * SR); lt, e = env(L, 5)
                put(t0, 0.07 * e * (np.sin(2 * np.pi * 1318.5 * lt) + .5 * np.sin(2 * np.pi * 1975.5 * lt)))
            elif kind == 'tada':
                for q, f in enumerate((523.25, 659.25, 783.99, 1046.5)):
                    L = int(.8 * SR); lt, e = env(L, 4)
                    put(t0 + q * .08, 0.06 * e * np.sin(2 * np.pi * f * lt))
            elif kind == 'buzz':
                L = int(.3 * SR); lt, e = env(L, 6)
                put(t0, 0.06 * e * np.sign(np.sin(2 * np.pi * 110 * lt)))
    # fade music in/out
    fade = np.ones(N); fi = int(1.5 * SR); fo = int(3 * SR)
    fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
    mix = mus * fade * 0.8 + fx
    mix /= max(1e-6, np.abs(mix).max()) / 0.85
    st = np.stack([mix, mix], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    # music-only stem for voiceover editing
    m = mus * fade; m /= max(1e-6, np.abs(m).max()) / 0.7
    with wave.open(path.replace('.wav', '_music_only.wav'), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.stack([m, m], 1) * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- thumbnail
def thumbnail(ep, path):
    th = ep.get('thumb', {}); TW, TH = 1280, 720
    bg = make_bg().resize((TW, TH)).convert('RGBA'); d = ImageDraw.Draw(bg)
    for i, c in enumerate((CYAN, AMBER, VIOLET)):
        d.rectangle([i * TW / 3, TH - 14, (i + 1) * TW / 3, TH], fill=c)
    words = th.get('words', ['GIT'])
    cols = [tuple(c) for c in th.get('colors', [WHITE, CYAN, AMBER])]
    y = 150 if len(words) > 2 else 190
    for i, w in enumerate(words):
        fs = 128 if len(w) <= 9 else (104 if len(w) <= 12 else 86)
        f = font(F_POP, fs)
        d.text((60, y), w, font=f, fill=cols[i % len(cols)], stroke_width=8, stroke_fill=(5, 8, 18))
        y += int(fs * 1.08)
    pill(d, 60, 64, 'GIT & GITHUB · EP %02d' % ep['num'], font(F_POP, 34), (17, 24, 39), AMBER, padx=22, pady=8)
    d.rounded_rectangle([TW - 250, 30, TW - 30, 84], radius=14, fill=(17, 24, 45), outline=LINE, width=2)
    d.text((TW - 230, 57), '>_', font=font(F_MONOB, 30), fill=GREEN, anchor='lm')
    d.text((TW - 180, 57), 'Tech-dev', font=font(F_POP, 30), fill=WHITE, anchor='lm')
    spr = bot_sprite(250, th.get('mood', 'happy') if th.get('mood') in ('happy', 'shock', 'think', 'party') else 'happy', 0, th.get('arms', 'point'), False)
    bg.alpha_composite(spr, (TW - spr.width - 10, TH - spr.height - 10))
    if th.get('emoji'):
        e = emoji(th['emoji'], 140); bg.alpha_composite(e, (TW - spr.width - 60, 120))
    if th.get('badge'):
        f = font(F_POP, 40); tw = f.getlength(th['badge'])
        bx, by = 60, y + 20
        d.rounded_rectangle([bx, by, bx + tw + 60, by + 74], radius=37, fill=AMBER)
        d.text((bx + 30 + tw / 2, by + 37), th['badge'], font=f, fill=(17, 24, 39), anchor='mm')
    bg.convert('RGB').save(path, quality=92)


# ---------------------------------------------------------------- upload text
def fmt_ts(s):
    s = int(s); return '%d:%02d' % (s // 60, s % 60)


def upload_kit(epi, outdir):
    ep = epi.ep; up = ep.get('upload', {})
    chs = epi.chapters()
    lines = [up.get('hook', ''), '',
             "I'm Shivam Singh Verma, a DevOps & SRE engineer with 5 years of experience building CI/CD pipelines, running cloud infrastructure on AWS & GCP, and managing projects.", '']
    if up.get('learn'):
        lines += ['🔑 In this video:'] + ['• ' + x for x in up['learn']] + ['']
    lines += ['⏱️ Chapters'] + ['%s %s' % (fmt_ts(t), n) for t, n in chs] + ['']
    if up.get('commands'):
        lines += ['💻 Commands used'] + ['  ' + c for c in up['commands']] + ['']
    lines += ['📚 Full playlist: Git & GitHub — Beginner to Advanced (new episode daily at 4 PM IST)',
              '🔔 Subscribe to Tech-dev for practical DevOps, SRE, Cloud, Security & AI videos.', '',
              '💬 ' + up.get('question', 'Which Git command confuses you the most? Tell me in the comments!'), '',
              ' '.join(up.get('hashtags', ['#Git', '#GitHub', '#DevOps', '#LearnGit', '#TechDev']))]
    desc = '\n'.join(lines)
    data = {'title': up.get('title', ep['title']), 'description': desc, 'tags': up.get('tags', []), 'chapters': chs,
            'duration_s': round(epi.total, 1)}
    json.dump(data, open(os.path.join(outdir, 'upload.json'), 'w'), indent=2, ensure_ascii=False)
    with open(os.path.join(outdir, 'upload.txt'), 'w') as f:
        f.write('TITLE\n' + data['title'] + '\n\nDESCRIPTION\n' + desc + '\n\nTAGS\n' + ', '.join(data['tags']) + '\n')
    # timed voiceover script
    with open(os.path.join(outdir, 'script.txt'), 'w') as f:
        f.write('VOICEOVER SCRIPT — EP %02d: %s\n(read each line when its caption appears; times are mm:ss)\n\n' % (ep['num'], ep['title']))
        for off, sc in zip(epi.offsets, epi.scenes):
            for st, b in zip(sc.starts, sc.beats):
                if b.get('cap'):
                    f.write('[%s] %s\n' % (fmt_ts(off + st), b['cap'].replace('*', '')))
    return data


# ---------------------------------------------------------------- main
def load_ep(path):
    spec = importlib.util.spec_from_file_location('ep', path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m.EP


def main():
    epf, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    epi = Episode(load_ep(epf))
    print('total %.1fs, scenes: %s' % (epi.total, ', '.join('%s %.1f' % (s.spec['type'], s.dur) for s in epi.scenes)))
    if '--stills' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--stills') + 1].split(',')]
        for tg in ts:
            si = max(i for i, o in enumerate(epi.offsets) if o <= tg)
            epi.frame(si, tg - epi.offsets[si]).convert('RGB').save(os.path.join(outdir, 'still_%05.1f.jpg' % tg), quality=90)
        thumbnail(epi.ep, os.path.join(outdir, 'thumbnail.jpg'))
        return
    sd = os.path.join(outdir, 'scenes'); os.makedirs(sd, exist_ok=True)
    global _EPI; _EPI = epi
    jobs = [(i, os.path.join(sd, 's%02d.mp4' % i)) for i in range(len(epi.scenes))]
    import multiprocessing as mp
    order = sorted(range(len(jobs)), key=lambda i: -epi.scenes[i].dur)
    with mp.get_context('fork').Pool(max(1, os.cpu_count() or 1)) as pool:
        for si in pool.imap_unordered(render_scene, [jobs[i] for i in order]):
            print('scene', si, 'done', flush=True)
    with open(os.path.join(sd, 'list.txt'), 'w') as f:
        for i, pth in jobs:
            f.write("file '%s'\n" % os.path.abspath(pth))
    synth_audio(epi, os.path.join(outdir, 'audio.wav'))
    silent = os.path.join(outdir, 'silent.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(sd, 'list.txt'), '-c', 'copy', silent], check=True)
    fin = os.path.join(outdir, 'video.part.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', silent, '-i', os.path.join(outdir, 'audio.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', fin], check=True)
    os.replace(fin, os.path.join(outdir, 'video.mp4'))
    thumbnail(epi.ep, os.path.join(outdir, 'thumbnail.jpg'))
    upload_kit(epi, outdir)
    print('DONE', os.path.join(outdir, 'video.mp4'))


if __name__ == '__main__':
    main()
