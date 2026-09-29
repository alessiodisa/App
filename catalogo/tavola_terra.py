#!/usr/bin/env python3
"""
Tavola tecnica originale dell'espositore da terra a ripiani (vettoriale, fondo trasparente):
in alto tre viste 3D, in basso gli sviluppi in piano con quote.

    python3 tavola_terra.py   ->  img/disegni/terra-tavola.svg
"""
from math import cos, sin, radians
from pathlib import Path

OUT = Path(__file__).parent / "img" / "disegni" / "terra-tavola.svg"
INK, GRAY = "#1A1A1A", "#8C8C8C"
F_SIDE, F_BACK, F_SHELF, F_LIP, F_HEAD = "#D9DDE1", "#BFCAD4", "#F4F4F3", "#FFFFFF", "#ECECEB"

# misure (mm)
W, D, H = 520, 340, 1580          # larghezza interna, profondità, altezza fianchi
HB = 1540                         # altezza schienale
SLOPE = 170                       # calo del fianco verso il fronte
HEAD_W, HEAD_H = 514, 400         # header
SHELVES = [80, 400, 720, 1040]    # quota dei ripiani
LIP = 70                          # bordo frontale dei ripiani
FULL = 196                        # larghezza della tavola


def model():
    faces = []                    # (punti3d, fill, opacità, tratteggio)
    faces.append(([(0, 0, 0), (W, 0, 0), (W, HB, 0), (0, HB, 0)], F_BACK, 1, False))
    hx = (W - HEAD_W) / 2
    r = 40
    top = HB + HEAD_H - 60
    head = [(hx, HB - 60, -4), (hx + HEAD_W, HB - 60, -4), (hx + HEAD_W, top - r, -4), (hx + HEAD_W - r * .3, top - r * .3, -4),
            (hx + HEAD_W - r, top, -4), (hx + r, top, -4), (hx + r * .3, top - r * .3, -4), (hx, top - r, -4)]
    faces.append((head, F_HEAD, 1, False))
    for y in SHELVES:
        faces.append(([(0, y, 0), (W, y, 0), (W, y, D), (0, y, D)], F_SHELF, .96, False))
        faces.append(([(0, y, D), (W, y, D), (W, y + LIP, D), (0, y + LIP, D)], F_LIP, .96, False))
    for x in (0, W):
        faces.append(([(x, 0, 0), (x, H, 0), (x, H - SLOPE, D), (x, 0, D)], F_SIDE, .62, False))
    return faces


def project(p, yaw, pitch):
    x, y, z = p[0] - W / 2, p[1], p[2] - D / 2
    a, b = radians(yaw), radians(pitch)
    x1 = x * cos(a) + z * sin(a)
    z1 = -x * sin(a) + z * cos(a)
    y2 = y * cos(b) - z1 * sin(b)
    depth = z1 * cos(b) + y * sin(b)
    return x1, -y2, depth


def vista(yaw, pitch, ox, oy, h_target):
    faces = model()
    pts = [project(p, yaw, pitch) for f, *_ in faces for p in f]
    minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
    miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
    k = h_target / (maxy - miny)
    out = []
    for f, fill, op, dash in sorted(faces, key=lambda t: sum(project(p, yaw, pitch)[2] for p in t[0]) / len(t[0])):
        pp = [project(p, yaw, pitch) for p in f]
        d = " ".join(f"{ox + (x - minx) * k:.2f},{oy + (y - miny) * k:.2f}" for x, y, _ in pp)
        out.append(f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}" stroke="{INK}" stroke-width=".32" stroke-linejoin="round"/>')
    return "".join(out), (maxx - minx) * k


# --------------------------------------------------------------------------
# sviluppi in piano
# --------------------------------------------------------------------------
CUT = f'fill="none" stroke="{INK}" stroke-width=".3" stroke-linejoin="round"'
CRE = f'fill="none" stroke="{INK}" stroke-width=".22" stroke-dasharray="1.3 .9"'


def path(pts, attr=CUT, close=True):
    return f'<path d="M{" L".join(f"{x:.2f},{y:.2f}" for x, y in pts)}{" Z" if close else ""}" {attr}/>'


def testo(x, y, s, anchor="middle", rot=None, size=2.3, c=GRAY):
    r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="Inter, Arial, sans-serif" font-size="{size}" font-weight="600" '
            f'fill="{c}" text-anchor="{anchor}"{r}>{s}</text>')


def quota_h(x1, x2, y, label):
    return (f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{GRAY}" stroke-width=".2"/>'
            f'<line x1="{x1:.2f}" y1="{y - 1.3:.2f}" x2="{x1:.2f}" y2="{y + 1.3:.2f}" stroke="{GRAY}" stroke-width=".2"/>'
            f'<line x1="{x2:.2f}" y1="{y - 1.3:.2f}" x2="{x2:.2f}" y2="{y + 1.3:.2f}" stroke="{GRAY}" stroke-width=".2"/>'
            + testo((x1 + x2) / 2, y + 3.4, label))


def quota_v(x, y1, y2, label):
    return (f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{GRAY}" stroke-width=".2"/>'
            f'<line x1="{x - 1.3:.2f}" y1="{y1:.2f}" x2="{x + 1.3:.2f}" y2="{y1:.2f}" stroke="{GRAY}" stroke-width=".2"/>'
            f'<line x1="{x - 1.3:.2f}" y1="{y2:.2f}" x2="{x + 1.3:.2f}" y2="{y2:.2f}" stroke="{GRAY}" stroke-width=".2"/>'
            + testo(x + 3.2, (y1 + y2) / 2, label, rot=-90))


def onda(x, y, size=1.9):
    t = size / 1.9
    return (f'<path d="M{x:.2f},{y:.2f} l{2.6 * t:.2f},{-4.4 * t:.2f} l{2.6 * t:.2f},{4.4 * t:.2f} Z" fill="none" stroke="{INK}" stroke-width=".22"/>'
            + testo(x + 6.4 * t, y - .5, 'ONDA "EB"', "start", size=size, c=INK))


def fianco(x, y, k, mirror=False):
    """Fianco con aletta di incollaggio e 4 asole per i ripiani."""
    fw, fl, fh, sl = D * k, 60 * k, H * k, SLOPE * k
    sx = (lambda u: x + fw + fl - u) if mirror else (lambda u: x + u)
    body = path([(sx(0), y + fh), (sx(0), y + sl), (sx(fw * .55), y), (sx(fw), y), (sx(fw + fl), y + 3),
                 (sx(fw + fl), y + fh), ])
    body += path([(sx(fw), y), (sx(fw), y + fh)], CRE, close=False)
    for s in SHELVES:
        yy = y + fh - s * k - 3
        a, b = sx(fw * .08), sx(fw * .42)
        body += f'<rect x="{min(a, b):.2f}" y="{yy:.2f}" width="{abs(b - a):.2f}" height="1" rx=".5" {CUT}/>'
    body += onda((x + fl + 1) if mirror else (x + 1), y + fh - 240 * k + 2, size=1.5)
    body += quota_h(x, x + fw + fl, y + fh + 4, f"{D + 60} mm")
    return body


def schienale(x, y, k):
    bw, bh, c = W * k, HB * k, 5
    body = path([(x, y), (x + bw, y), (x + bw, y + bh - c), (x + bw - c, y + bh), (x + c, y + bh), (x, y + bh - c)])
    body += path([(x, y + bh - c * 1.6), (x + bw, y + bh - c * 1.6)], CRE, close=False)
    body += onda(x + 3, y + bh - 13)
    body += quota_h(x, x + bw, y + bh + 4, f"{W} mm") + quota_v(x + bw + 3, y, y + bh, f"{HB} mm")
    return body


def ripiano(x, y, k):
    """Vassoio a croce: fondo, bordo frontale doppio, alette laterali con linguette."""
    sw, sd, lp, fl = W * k, D * k, LIP * k, 50 * k
    x0, y0 = x + fl, y + lp * 2
    body = path([(x0, y), (x0 + sw, y), (x0 + sw, y0), (x0 + sw + fl, y0 + 2), (x0 + sw + fl, y0 + sd - 2),
                 (x0 + sw, y0 + sd), (x0 + sw, y0 + sd + lp), (x0, y0 + sd + lp), (x0, y0 + sd),
                 (x0 - fl, y0 + sd - 2), (x0 - fl, y0 + 2), (x0, y0)])
    for a, b in (((x0, y0), (x0 + sw, y0)), ((x0, y + lp), (x0 + sw, y + lp)), ((x0, y0 + sd), (x0 + sw, y0 + sd)),
                 ((x0, y0), (x0, y0 + sd)), ((x0 + sw, y0), (x0 + sw, y0 + sd))):
        body += path([a, b], CRE, close=False)
    for fx in (x0 + sw * .25, x0 + sw * .75):
        body += f'<rect x="{fx - 3:.2f}" y="{y0 + 2.5:.2f}" width="6" height=".9" rx=".45" {CUT}/>'
        body += f'<rect x="{fx - 3:.2f}" y="{y0 + sd - 3.4:.2f}" width="6" height=".9" rx=".45" {CUT}/>'
    body += onda(x0 + 3, y0 + sd - 5)
    body += quota_h(x0 - fl, x0 + sw + fl, y0 + sd + lp + 4, f"{W + 100} mm")
    body += quota_v(x0 + sw + fl + 3, y, y0 + sd + lp, f"{D + 3 * LIP} mm")
    return body, x0 + sw + fl - x, y0 + sd + lp - y


def header(x, y, k):
    hw, hh, r = HEAD_W * k, HEAD_H * k, 3
    t = 8 * k * 3
    body = (f'<path d="M{x},{y + hh} L{x},{y + r} Q{x},{y} {x + r},{y} L{x + hw - r},{y} Q{x + hw},{y} {x + hw},{y + r} '
            f'L{x + hw},{y + hh} L{x + hw * .7},{y + hh} L{x + hw * .7},{y + hh + t} L{x + hw * .58},{y + hh + t} '
            f'L{x + hw * .58},{y + hh} L{x + hw * .42},{y + hh} L{x + hw * .42},{y + hh + t} L{x + hw * .3},{y + hh + t} '
            f'L{x + hw * .3},{y + hh} Z" {CUT}/>')
    body += onda(x + 3, y + hh - 3)
    body += quota_h(x, x + hw, y + hh + t + 4, f"{HEAD_W} mm") + quota_v(x + hw + 3, y, y + hh, f"{HEAD_H} mm")
    return body


def build():
    body = ""
    # riga 1: tre viste
    _, w1 = vista(-38, 12, 0, 0, 100)
    _, w2 = vista(-12, 6, 0, 0, 94)
    _, w3 = vista(38, 26, 0, 0, 90)
    gap = (FULL - 12 - w1 - w2 - w3) / 2
    v1, _ = vista(-38, 12, 6, 6, 100)
    v2, _ = vista(-12, 6, 6 + w1 + gap, 9, 94)
    v3, _ = vista(38, 26, 6 + w1 + w2 + 2 * gap, 12, 90)
    body += f"<g>{v1}</g><g>{v2}</g><g>{v3}</g>"
    top_w = FULL
    # riga 2: sviluppi in piano, scala 1:20
    k = 1 / 20
    y = 122
    x = 6
    body += fianco(x, y, k)
    x += (D + 60) * k + 10
    body += schienale(x, y, k)
    x += W * k + 16
    body += fianco(x, y, k, mirror=True)
    x += (D + 60) * k + 12
    rb, rw, rh = ripiano(x, y, k)
    body += rb
    body += header(x + 2.5, y + rh + 12, k)
    x += rw + 14
    rb2, rw2, _ = ripiano(x, y, k)
    body += rb2
    width = max(top_w, x + rw2 + 10)
    height = y + H * k + 12
    body += (f'<line x1="6" y1="{height - 3}" x2="14" y2="{height - 3}" stroke="{INK}" stroke-width=".3"/>'
             + testo(16, height - 2.2, "TAGLIO", "start", size=2)
             + f'<line x1="34" y1="{height - 3}" x2="42" y2="{height - 3}" stroke="{INK}" stroke-width=".22" stroke-dasharray="1.3 .9"/>'
             + testo(44, height - 2.2, "CORDONATURA", "start", size=2)
             + testo(width - 6, height - 2.2, "SVILUPPI IN SCALA 1:20 — QUOTE IN MM", "end", size=2))
    OUT.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.1f} {height:.1f}" '
                   f'width="{width:.1f}mm" height="{height:.1f}mm">{body}</svg>', encoding="utf-8")
    print(OUT.name, f"{width:.0f}×{height:.0f} mm")


if __name__ == "__main__":
    build()
