#!/usr/bin/env python3
"""
Disegni tecnici vettoriali (SVG) degli espositori, originali:
  img/disegni/banco-iso.svg     espositore da banco a gradini, assonometria
  img/disegni/terra-iso.svg     espositore da terra a ripiani, assonometria
  img/disegni/terra-fustelle.svg sviluppo in piano (fianco, schienale, ripiano) con quote

Le coordinate finali sono in mm di stampa: nella pagina si usano con la loro misura.

    python3 disegni.py
"""
from math import cos, sin, radians, pi
from pathlib import Path

OUT = Path(__file__).parent / "img" / "disegni"
INK, GRAY, LIGHT = "#141414", "#8C8C8C", "#E4E4E2"
C30, S30 = cos(radians(30)), sin(radians(30))


# --------------------------------------------------------------------------
# assonometria isometrica con facce riempite (ordine del pittore)
# --------------------------------------------------------------------------
def iso(x, y, z):
    return (x - z) * C30, (x + z) * S30 - y


class Scene:
    def __init__(self):
        self.polys = []   # (punti3d, fill, dashed)
        self.lines = []   # (p3d, p3d, dashed)

    def poly(self, pts, fill="#fff", dash=False):
        self.polys.append((pts, fill, dash))

    def line(self, a, b, dash=False):
        self.lines.append((a, b, dash))

    def render(self, target_h, pad=6, extra=""):
        pts2 = [iso(*p) for pl, _, _ in self.polys for p in pl]
        xs, ys = [p[0] for p in pts2], [p[1] for p in pts2]
        k = (target_h - 2 * pad) / (max(ys) - min(ys))
        ox, oy = -min(xs) * k + pad, -min(ys) * k + pad
        P = lambda p: (iso(*p)[0] * k + ox, iso(*p)[1] * k + oy)
        body = ""
        for pl, fill, dash in self.polys:
            d = " ".join(f"{a:.2f},{b:.2f}" for a, b in map(P, pl))
            da = ' stroke-dasharray="1.6 1.1"' if dash else ""
            body += f'<polygon points="{d}" fill="{fill}" stroke="{INK}" stroke-width=".32" stroke-linejoin="round"{da}/>'
        for a, b, dash in self.lines:
            (x1, y1), (x2, y2) = P(a), P(b)
            da = ' stroke-dasharray="1.6 1.1"' if dash else ""
            body += f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width=".32"{da}/>'
        w = (max(xs) - min(xs)) * k + 2 * pad
        return w, target_h, body, P


def arc_top(x0, x1, y0, r, z, n=8, left=True, right=True):
    """Contorno superiore di un pannello (piano z costante) con angoli arrotondati."""
    pts = []
    if left:
        for i in range(n + 1):
            a = pi - (pi / 2) * i / n
            pts.append((x0 + r + r * cos(a), y0 - r + r * sin(a), z))
    else:
        pts.append((x0, y0, z))
    if right:
        for i in range(n + 1):
            a = pi / 2 - (pi / 2) * i / n
            pts.append((x1 - r + r * cos(a), y0 - r + r * sin(a), z))
    else:
        pts.append((x1, y0, z))
    return pts


def dim_text(x, y, s, rot=None, anchor="middle"):
    r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="Inter, Arial, sans-serif" font-size="2.6" '
            f'font-weight="600" fill="{GRAY}" text-anchor="{anchor}"{r}>{s}</text>')


def dim(a, b, label, off=(0, 0), text_off=(0, 0), rot=None):
    (x1, y1), (x2, y2) = a, b
    ox, oy = off
    x1, y1, x2, y2 = x1 + ox, y1 + oy, x2 + ox, y2 + oy
    t = (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{GRAY}" stroke-width=".22"/>'
         f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r=".55" fill="{GRAY}"/><circle cx="{x2:.2f}" cy="{y2:.2f}" r=".55" fill="{GRAY}"/>')
    return t + dim_text((x1 + x2) / 2 + text_off[0], (y1 + y2) / 2 + text_off[1], label, rot)


def save(name, w, h, body):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
                            f'width="{w:.2f}mm" height="{h:.2f}mm">{body}</svg>', encoding="utf-8")
    print(name, f"{w:.0f}×{h:.0f} mm")


# --------------------------------------------------------------------------
# 1. espositore da banco a gradini (mm reali: L 300, P 220, H 450)
# --------------------------------------------------------------------------
def banco():
    W, D, H, HB, HF = 300, 220, 450, 250, 80
    s = Scene()
    # schienale con header arrotondato (piano z = 0)
    s.poly([(0, 0, 0), (W, 0, 0)] + list(reversed(arc_top(0, W, H, 40, 0))), fill=LIGHT)
    # fianco sinistro (nascosto, tratteggiato)
    s.poly([(0, 0, 0), (0, HB, 0), (0, HF, D), (0, 0, D)], fill="none", dash=True)
    # gradini: (y piano, z inizio, z fine)
    steps = [(200, 0, 70), (120, 70, 145), (20, 145, D)]
    for y, z0, z1 in steps:
        s.poly([(0, y, z0), (W, y, z0), (W, y, z1), (0, y, z1)])
        if z1 < D:
            s.poly([(0, 0, z1), (W, 0, z1), (W, y, z1), (0, y, z1)])
    # labbro frontale
    s.poly([(0, 0, D), (W, 0, D), (W, HF, D), (0, HF, D)])
    # fianco destro (visibile)
    s.poly([(W, 0, 0), (W, HB, 0), (W, HF, D), (W, 0, D)])
    # prodotti tratteggiati sui gradini
    for y, z0, z1 in steps[:2]:
        for i in range(4):
            x0 = 20 + i * 70
            s.poly([(x0, y, z0 + 12), (x0 + 50, y, z0 + 12), (x0 + 50, y + 70, z0 + 12), (x0, y + 70, z0 + 12)],
                   fill="none", dash=True)
    w, h, body, P = s.render(150, pad=10)
    body += dim(P((W, 0, 0)), P((W, H, 0)), "H 450 mm", off=(7, 0), text_off=(2.8, 0), rot=-90)
    body += dim(P((0, 0, D)), P((W, 0, D)), "L 300 mm", off=(0, 5), text_off=(-3, 4.5))
    body += dim(P((W, 0, 0)), P((W, 0, D)), "P 220 mm", off=(4, 3), text_off=(5, 3))
    save("banco-iso.svg", w, h, body)


# --------------------------------------------------------------------------
# 2. espositore da terra a ripiani (mm reali: L 400, P 300, H 1600)
# --------------------------------------------------------------------------
def terra():
    W, D, H, HS, LIP = 400, 300, 1600, 1450, 60
    s = Scene()
    s.poly([(0, 0, 0), (W, 0, 0)] + list(reversed(arc_top(0, W, H, 60, 0))), fill=LIGHT)
    s.poly([(0, 0, 0), (0, HS, 0), (0, HS - 120, D), (0, 0, D)], fill="none", dash=True)
    shelves = [250, 550, 850, 1150]
    for y in shelves:
        s.poly([(0, y, 0), (W, y, 0), (W, y, D), (0, y, D)])
        s.poly([(0, y, D), (W, y, D), (W, y + LIP, D), (0, y + LIP, D)])
    s.poly([(0, 0, D), (W, 0, D), (W, 230, D), (0, 230, D)], fill=LIGHT)      # zoccolo frontale
    s.poly([(W, 0, 0), (W, HS, 0), (W, HS - 120, D), (W, 0, D)])
    for y in shelves:                                                      # incastri sul fianco
        s.line((W, y + 20, D - 90), (W, y + 20, D - 20), dash=True)
    w, h, body, P = s.render(175, pad=10)
    body += dim(P((W, 0, 0)), P((W, H, 0)), "H 1600 mm", off=(7, 0), text_off=(2.8, 0), rot=-90)
    body += dim(P((0, 0, D)), P((W, 0, D)), "L 400 mm", off=(0, 5), text_off=(-3, 4.5))
    body += dim(P((W, 0, 0)), P((W, 0, D)), "P 300 mm", off=(4, 3), text_off=(5, 3))
    save("terra-iso.svg", w, h, body)


# --------------------------------------------------------------------------
# 3. fustelle in piano, scala 1:10 (taglio continuo, cordonatura tratteggiata)
# --------------------------------------------------------------------------
def fustelle():
    k = .1                         # 1:10
    body = ""
    CUT = f'fill="none" stroke="{INK}" stroke-width=".3" stroke-linejoin="round"'
    CRE = f'fill="none" stroke="{INK}" stroke-width=".25" stroke-dasharray="1.4 1"'

    def path(pts, attr=CUT, close=True):
        d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + (" Z" if close else "")
        return f'<path d="{d}" {attr}/>'

    def flute(x, y):
        return (f'<path d="M{x},{y} l3,-5 l3,5 Z" fill="none" stroke="{INK}" stroke-width=".25"/>'
                f'<text x="{x + 8}" y="{y - .6}" font-family="Inter, Arial, sans-serif" font-size="2.2" fill="{INK}">ONDA "EB"</text>')

    top, gap = 12, 14
    # fianco (x 300 + aletta 40, h 1450) con 4 asole
    ox = 12
    fw, fh, fl = 300 * k, 1450 * k, 40 * k
    body += path([(ox, top + 12), (ox + fw * .45, top), (ox + fw, top), (ox + fw + fl, top + 3),
                  (ox + fw + fl, top + fh - 3), (ox + fw, top + fh), (ox, top + fh)])
    body += path([(ox + fw, top), (ox + fw, top + fh)], CRE, close=False)
    for i in range(4):
        y = top + fh - (250 + 300 * i) * k - 4
        body += f'<rect x="{ox + 2}" y="{y:.2f}" width="{fw * .38:.2f}" height="1.1" rx=".55" {CUT}/>'
    body += flute(ox + 2, top + fh - 3)
    body += dim((ox, top + fh + 5), (ox + fw + fl, top + fh + 5), "340")
    body += dim((ox - 4, top), (ox - 4, top + fh), "1450", text_off=(-1.5, 0), rot=-90)
    # schienale con header (400 + alette 2×40, h 1600)
    ox2 = ox + fw + fl + gap
    bw, bh = 400 * k, 1600 * k
    r = 6
    body += (f'<path d="M{ox2 + fl},{top + bh} L{ox2 + fl},{top + r} Q{ox2 + fl},{top} {ox2 + fl + r},{top} '
             f'L{ox2 + fl + bw - r},{top} Q{ox2 + fl + bw},{top} {ox2 + fl + bw},{top + r} L{ox2 + fl + bw},{top + bh} Z" {CUT}/>')
    for sx in (ox2, ox2 + fl + bw):
        body += path([(sx, top + 18), (sx + fl, top + 16), (sx + fl, top + bh), (sx, top + bh - 2)])
    body += path([(ox2 + fl, top + 16), (ox2 + fl, top + bh)], CRE, close=False)
    body += path([(ox2 + fl + bw, top + 16), (ox2 + fl + bw, top + bh)], CRE, close=False)
    body += flute(ox2 + fl + 2, top + bh - 3)
    body += dim((ox2, top + bh + 5), (ox2 + 2 * fl + bw, top + bh + 5), "480")
    body += dim((ox2 + 2 * fl + bw + 4, top), (ox2 + 2 * fl + bw + 4, top + bh), "1600", text_off=(2.8, 0), rot=-90)
    # ripiano a vassoio: fondo 400×300, bordo frontale 60, alette 40
    ox3 = ox2 + 2 * fl + bw + gap + 6
    sw, sd, lp = 400 * k, 300 * k, 60 * k
    y0 = top + 30
    x0 = ox3 + fl
    body += path([(x0, y0 - fl), (x0 + sw, y0 - fl), (x0 + sw, y0), (x0 + sw + fl, y0 + 1), (x0 + sw + fl, y0 + sd - 1),
                  (x0 + sw, y0 + sd), (x0 + sw, y0 + sd + lp * 2), (x0, y0 + sd + lp * 2), (x0, y0 + sd),
                  (x0 - fl, y0 + sd - 1), (x0 - fl, y0 + 1), (x0, y0)])
    for a, b in (((x0, y0), (x0 + sw, y0)), ((x0, y0 + sd), (x0 + sw, y0 + sd)),
                 ((x0, y0 + sd + lp), (x0 + sw, y0 + sd + lp)), ((x0, y0), (x0, y0 + sd)), ((x0 + sw, y0), (x0 + sw, y0 + sd))):
        body += path([a, b], CRE, close=False)
    body += flute(x0 + 3, y0 + sd - 3)
    body += dim((x0 - fl, y0 + sd + lp * 2 + 5), (x0 + sw + fl, y0 + sd + lp * 2 + 5), "480")
    body += dim((x0 + sw + fl + 4, y0 - fl), (x0 + sw + fl + 4, y0 + sd + lp * 2), "460", text_off=(2.8, 0), rot=-90)
    # legenda
    ly = top + bh + 14
    body += (f'<line x1="{ox}" y1="{ly}" x2="{ox + 8}" y2="{ly}" stroke="{INK}" stroke-width=".3"/>'
             + dim_text(ox + 10, ly + .9, "TAGLIO", anchor="start")
             + f'<line x1="{ox + 28}" y1="{ly}" x2="{ox + 36}" y2="{ly}" stroke="{INK}" stroke-width=".25" stroke-dasharray="1.4 1"/>'
             + dim_text(ox + 38, ly + .9, "CORDONATURA", anchor="start")
             + dim_text(ox + 70, ly + .9, "SCALA 1:10 — QUOTE IN MM", anchor="start"))
    save("terra-fustelle.svg", ox3 + 2 * fl + sw + 14, ly + 6, body)


if __name__ == "__main__":
    banco()
    terra()
    fustelle()
