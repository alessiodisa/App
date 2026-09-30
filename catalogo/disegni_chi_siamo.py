#!/usr/bin/env python3
"""
Quattro bozze "a matita" per la pagina Chi siamo (vettoriali, tratto irregolare e ripassato, fondo bianco
da usare con mix-blend-mode multiply):
ufficio tecnico, prototipazione, produzione, logistica.

    python3 disegni_chi_siamo.py   ->  img/disegni/chi-01.svg ... chi-04.svg
"""
import random
from math import cos, sin, radians
from pathlib import Path

OUT = Path(__file__).parent / "img" / "disegni"
INK, GRAY, PAPER = "#2E2E2E", "#8A8A8A", "#FFFFFF"
RNG = random.Random(7)


def tratto(p1, p2, sw=.26, col=INK, op=.8, passate=2, over=.9, dash=None):
    """Linea a matita: due passate leggermente curve e sfalsate, che sforano un po' agli estremi."""
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = x2 - x1, y2 - y1
    l = (dx * dx + dy * dy) ** .5 or 1
    ux, uy = dx / l, dy / l
    out = ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    for k in range(passate):
        o1, o2 = RNG.uniform(-.2, over), RNG.uniform(-.2, over)
        j = lambda: RNG.uniform(-.18, .18)
        a = (x1 - ux * o1 + j(), y1 - uy * o1 + j())
        b = (x2 + ux * o2 + j(), y2 + uy * o2 + j())
        bend = RNG.uniform(-.35, .35) * min(1, l / 20)
        m = ((a[0] + b[0]) / 2 - uy * bend, (a[1] + b[1]) / 2 + ux * bend)
        w = sw * (1 if k == 0 else .6)
        out += (f'<path d="M{a[0]:.2f},{a[1]:.2f} Q{m[0]:.2f},{m[1]:.2f} {b[0]:.2f},{b[1]:.2f}" fill="none" '
                f'stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round" opacity="{op * (1 if k == 0 else .6):.2f}"{da}/>')
    return out
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

    def poly(self, pts, fill=PAPER, sw=.3, hatch=None, dash=None):
        q = [self.p(*a) for a in pts]
        d = "M" + " L".join(f"{u:.2f},{v:.2f}" for u, v in q) + " Z"
        if fill != "none":
            self.el.append(f'<path d="{d}" fill="{fill}"/>')
        if hatch:
            # tratteggio a matita: linee inclinate irregolari, ritagliate sulla faccia
            self.n += 1
            cid = f"h{self.n}"
            xs, ys = [u for u, _ in q], [v for _, v in q]
            lines, x0 = "", min(xs) - (max(ys) - min(ys))
            while x0 < max(xs):
                x0 += hatch * RNG.uniform(.8, 1.3)
                lines += tratto((x0, max(ys) + 1), (x0 + (max(ys) - min(ys) + 2) * .7, min(ys) - 1), .14, INK, .45, 1, .3)
            self.el.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">{lines}</g>')
        for i in range(len(q)):
            self.el.append(tratto(q[i], q[(i + 1) % len(q)], sw, INK, .85, 2, .9, dash))

    def line(self, a, b, sw=.26, col=INK, dash=None):
        self.el.append(tratto(self.p(*a), self.p(*b), sw, col, .8 if col == INK else .9, 2 if col == INK else 1,
                              .7 if col == INK else .2, dash))

    def box(self, x, y, z, dx, dy, dz, hatch=1.4, fill=PAPER):
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
                       f'font-weight="400" font-style="italic" fill="{col}" text-anchor="{anchor}">{s}</text>')

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
    """Linea di produzione: nastro con fogli stampati che passano sotto la fustellatrice, pila di pezzi finiti."""
    t = Tavola(40, 10, .7)
    # montante posteriore del portale (dietro al nastro)
    t.box(34, -7, 0, 6, 5, 49, 1.2)
    # gambe e nastro trasportatore
    for x in (2, 84):
        for y in (1, 23):
            t.box(x, y, 0, 3, 3, 12, 1.2)
    t.box(0, 0, 12, 90, 27, 3, 1.1)
    for x in range(10, 90, 12):                    # rulli visti dal fianco
        t.line((x, 27, 12.5), (x, 27, 14.5), .18)
    # fogli stampati in ingresso
    t.box(4, 4, 15, 20, 19, .6, 1.4)
    for x, y, dx, dy in [(8, 8, 5, 11), (13, 8, 6, 11), (19, 8, 2, 11)]:
        t.poly([(x, y, 15.6), (x + dx, y, 15.6), (x + dx, y + dy, 15.6), (x, y + dy, 15.6)], "none", .18)
    # foglio fustellato in uscita, con la sagoma dell'espositore
    t.box(52, 4, 15, 20, 19, .6, 1.4)
    t.poly([(55, 7, 15.6), (63, 7, 15.6), (63, 12, 15.6), (69, 12, 15.6), (69, 20, 15.6), (55, 20, 15.6)], "none", .2)
    t.line((63, 12, 15.6), (63, 20, 15.6), .16, INK, "1 .7")
    # piano di taglio che scende, montante anteriore e traversa
    t.box(33, 2, 26, 8, 23, 4, 1.0)
    for y in (8, 18):
        t.line((37, y, 25), (37, y, 18), .2)
        t.line((35.8, y, 20), (37, y, 18), .2)
        t.line((38.2, y, 20), (37, y, 18), .2)
    t.box(34, 29, 0, 6, 5, 49, 1.2)
    t.box(32, -7, 42, 10, 41, 7, 1.1)
    # pila di pezzi finiti
    for i in range(5):
        t.box(100, 4, i * 1.4, 22, 19, 1.1, 1.6)
    t.quota((90, 27, 0), (90, 0, 0), (8, 0, 0), "800")
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
