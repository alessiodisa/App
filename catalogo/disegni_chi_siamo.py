#!/usr/bin/env python3
"""
Quattro disegni tecnici "a penna" per la pagina Chi siamo (vettoriali, fondo trasparente):
ufficio tecnico, prototipazione, produzione, logistica.

    python3 disegni_chi_siamo.py   ->  img/disegni/chi-01.svg ... chi-04.svg
"""
from math import cos, sin, radians
from pathlib import Path

OUT = Path(__file__).parent / "img" / "disegni"
INK, GRAY, PAPER = "#1C1C1C", "#8A8A8A", "#FBFBFA"
C, S = cos(radians(30)), sin(radians(30))
W, H = 120, 80                       # mm, formato di ogni tavola


def iso(x, y, z):
    return (x - y) * C, (x + y) * S - z


class Tavola:
    def __init__(self, ox, oy, k=1.0):
        self.ox, self.oy, self.k, self.el, self.n = ox, oy, k, [], 0
        self.bb = [1e9, 1e9, -1e9, -1e9]

    def p(self, x, y, z):
        u, v = iso(x, y, z)
        u, v = self.ox + u * self.k, self.oy + v * self.k
        b = self.bb
        b[0], b[1], b[2], b[3] = min(b[0], u), min(b[1], v), max(b[2], u), max(b[3], v)
        return u, v

    def poly(self, pts, fill=PAPER, sw=.32, hatch=None, dash=None):
        q = [self.p(*a) for a in pts]
        d = "M" + " L".join(f"{u:.2f},{v:.2f}" for u, v in q) + " Z"
        if hatch:
            self.n += 1
            cid = f"h{self.n}"
            xs, ys = [u for u, _ in q], [v for _, v in q]
            lines = "".join(f'<line x1="{x0:.2f}" y1="{max(ys) + 2:.2f}" x2="{x0 + (max(ys) - min(ys) + 4) * .6:.2f}" '
                            f'y2="{min(ys) - 2:.2f}"/>'
                            for x0 in [min(xs) - 40 + i * hatch for i in range(int((max(xs) - min(xs) + 60) / hatch))])
            self.el.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><path d="{d}" fill="{fill}"/>'
                           f'<g clip-path="url(#{cid})" stroke="{INK}" stroke-width=".16" opacity=".55">{lines}</g>'
                           f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>')
        else:
            da = f' stroke-dasharray="{dash}"' if dash else ""
            self.el.append(f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"{da}/>')

    def line(self, a, b, sw=.28, col=INK, dash=None):
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.el.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" stroke-width="{sw}" '
                       f'stroke-linecap="round"{da}/>')

    def box(self, x, y, z, dx, dy, dz, hatch=1.1, fill=PAPER):
        """Parallelepipedo: facce visibili (sopra, sinistra, destra), la destra tratteggiata come ombra."""
        self.poly([(x, y + dy, z), (x + dx, y + dy, z), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)], fill)
        self.poly([(x + dx, y, z), (x + dx, y + dy, z), (x + dx, y + dy, z + dz), (x + dx, y, z + dz)], fill, hatch=hatch)
        self.poly([(x, y, z + dz), (x + dx, y, z + dz), (x + dx, y + dy, z + dz), (x, y + dy, z + dz)], fill)

    def quota(self, a, b, off, label, dirn=(0, 0, 0)):
        """Quota con linee di richiamo e frecce, testo al centro."""
        a2 = tuple(ai + oi for ai, oi in zip(a, off))
        b2 = tuple(bi + oi for bi, oi in zip(b, off))
        self.line(a, a2, .14, GRAY)
        self.line(b, b2, .14, GRAY)
        self.line(a2, b2, .16, GRAY)
        for p0, p1 in ((a2, b2), (b2, a2)):
            (x1, y1), (x2, y2) = self.p(*p0), self.p(*p1)
            dx, dy = x2 - x1, y2 - y1
            l = (dx * dx + dy * dy) ** .5 or 1
            ux, uy = dx / l, dy / l
            self.el.append(f'<path d="M{x1:.2f},{y1:.2f} l{(ux * 1.6 - uy * .5):.2f},{(uy * 1.6 + ux * .5):.2f} '
                           f'M{x1:.2f},{y1:.2f} l{(ux * 1.6 + uy * .5):.2f},{(uy * 1.6 - ux * .5):.2f}" '
                           f'stroke="{GRAY}" stroke-width=".16" fill="none"/>')
        (x1, y1), (x2, y2) = self.p(*a2), self.p(*b2)
        self.testo((x1 + x2) / 2, (y1 + y2) / 2 - 1, label)

    def testo(self, x, y, s, size=2.1, anchor="middle", col=GRAY):
        self.el.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="Inter, Arial, sans-serif" font-size="{size}" '
                       f'font-weight="500" fill="{col}" text-anchor="{anchor}">{s}</text>')

    def svg(self, nome):
        OUT.mkdir(parents=True, exist_ok=True)
        m = 4
        x0, y0, x1, y1 = self.bb[0] - m, self.bb[1] - m, self.bb[2] + m, self.bb[3] + m
        (OUT / nome).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" '
                                f'width="{x1 - x0:.1f}mm" height="{y1 - y0:.1f}mm">'
                                + "".join(self.el) + "</svg>", encoding="utf-8")


def ufficio_tecnico():
    t = Tavola(56, 22, .72)
    # foglio sul tavolo
    t.poly([(0, 0, 0), (80, 0, 0), (80, 56, 0), (0, 56, 0)])
    # sviluppo di un astuccio (fustella) disegnato sul foglio
    X, Y = 12, 10
    pannelli = [(X, Y + 12, 14, 20), (X + 14, Y + 12, 20, 20), (X + 34, Y + 12, 14, 20), (X + 48, Y + 12, 20, 20),
                (X + 14, Y, 20, 12), (X + 14, Y + 32, 20, 12), (X + 48, Y, 20, 12), (X + 48, Y + 32, 20, 12)]
    for x, y, dx, dy in pannelli:
        t.poly([(x, y, 0), (x + dx, y, 0), (x + dx, y + dy, 0), (x, y + dy, 0)], "none", .24)
    for x in (X + 14, X + 34, X + 48):
        t.line((x, Y + 12, 0), (x, Y + 32, 0), .2, INK, "1.2 .8")
    t.poly([(X + 68, Y + 12, 0), (X + 72, Y + 14, 0), (X + 72, Y + 30, 0), (X + 68, Y + 32, 0)], "none", .24)
    t.quota((X, Y, 0), (X + 14, Y, 0), (0, -5, 0), "90")
    t.quota((X + 72, Y + 12, 0), (X + 72, Y + 32, 0), (4, 0, 0), "120")
    # squadra
    t.poly([(56, 2, .4), (78, 2, .4), (78, 22, .4)], PAPER, .3)
    t.poly([(66, 6, .4), (75, 6, .4), (75, 14, .4)], "none", .2)
    # matita
    t.box(30, 49, 0, 34, 2.2, 2.2, .9)
    t.poly([(64, 49, 0), (69, 50.1, 1.1), (64, 51.2, 2.2)], PAPER, .28)
    t.svg("chi-01.svg")


def prototipazione():
    t = Tavola(60, 16, .8)
    # espositore da banco a gradini, campione bianco
    t.box(0, 0, 0, 44, 30, 8)
    t.box(0, 0, 8, 44, 18, 10)
    t.box(0, 0, 18, 44, 8, 10)
    t.box(0, 0, 28, 44, 2.4, 26)                 # fondale
    t.line((6, 0, 50), (38, 0, 50), .2, INK, "1.2 .8")
    t.quota((0, 30, 0), (44, 30, 0), (0, 8, 0), "300")
    t.quota((44, 30, 0), (44, 0, 0), (8, 0, 0), "210")
    t.quota((0, 30, 0), (0, 30, 8), (0, 6, 0), "60")
    t.quota((44, 0, 0), (44, 0, 54), (8, 0, 0), "380")
    # cutter
    t.box(10, 46, 0, 20, 3, 2.4, .8)
    t.poly([(30, 46, 0), (36, 47.5, 1.2), (30, 49, 2.4)], PAPER, .26)
    t.svg("chi-02.svg")


def produzione():
    t = Tavola(58, 14, .78)
    # pila di fogli stampati
    for i in range(6):
        t.box(0, 0, i * 1.6, 60, 42, 1.2, 1.4)
    # fustella (tavola di legno con filetti) sospesa sopra la pila
    z = 22
    t.box(-2, -2, z, 64, 46, 3, 1.0)
    for x, y, dx, dy in [(8, 8, 18, 12), (26, 8, 18, 12), (8, 20, 18, 12), (26, 20, 18, 12)]:
        t.poly([(x, y, z + 3), (x + dx, y, z + 3), (x + dx, y + dy, z + 3), (x, y + dy, z + 3)], "none", .24)
    for x in (14, 46):
        t.line((x, 44, z + 16), (x, 44, z + 5), .24)
        t.line((x - 1.5, 44, z + 7), (x, 44, z + 5), .24)
        t.line((x + 1.5, 44, z + 7), (x, 44, z + 5), .24)
    t.quota((0, 42, 0), (60, 42, 0), (0, 8, 0), "1000")
    t.quota((60, 42, 0), (60, 0, 0), (8, 0, 0), "700")
    t.svg("chi-03.svg")


def logistica():
    t = Tavola(58, 12, .72)
    # bancale
    for y in (0, 21, 42):
        t.box(0, y, 0, 64, 6, 5, 1.2)
    for x in range(0, 64, 8):
        t.box(x, 0, 5, 6, 48, 1.4, 1.2)
    # colli piatti impilati
    for zi in range(3):
        for xi in range(2):
            t.box(xi * 32, 0, 6.4 + zi * 10, 32, 48, 10, 1.3)
    # reggette
    for x in (16, 48):
        t.line((x, 48, 6.4), (x, 48, 36.4), .34)
        t.line((x, 48, 36.4), (x, 0, 36.4), .34)
    for y in (12, 36):
        t.line((64, y, 6.4), (64, y, 36.4), .34)
        t.line((64, y, 36.4), (0, y, 36.4), .34)
    t.quota((64, 48, 0), (64, 0, 0), (8, 0, 0), "800")
    t.quota((0, 48, 0), (0, 48, 36.4), (0, 8, 0), "1200")
    t.svg("chi-04.svg")


if __name__ == "__main__":
    ufficio_tecnico(), prototipazione(), produzione(), logistica()
    print("chi-01..04.svg")
