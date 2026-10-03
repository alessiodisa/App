#!/usr/bin/env python3
"""
Ricalco vettoriale fedele della tavola dell'espositore da terra (img/fonti/terra-tavola-originale.jpg):
campiture e linee separate per livelli, filigrana rimossa, quote e scritte rifatte come testo.

    python3 tavola_terra_ricalco.py   ->  img/disegni/terra-tavola.svg
"""
from pathlib import Path

import cv2
import numpy as np
import potrace

ROOT = Path(__file__).parent
SRC = ROOT / "img" / "fonti" / "terra-tavola-originale.jpg"
OUT = ROOT / "img" / "disegni" / "terra-tavola.svg"
U = 3                                   # sovracampionamento per il ricalco
MM = 0.2                                # mm per pixel dell'originale (1199 px -> ~240 mm)

# campiture: (nome, colore, condizione sul grigio g e sulla saturazione s)
FILLS = [
    ("chiaro", "#DCDCDC", lambda g, s: (g >= 198) & (g < 234) & (s <= 12)),
    ("pannello", "#BEBEBE", lambda g, s: (g >= 168) & (g < 198) & (s <= 12)),
    ("medio", "#9E9E9E", lambda g, s: (g >= 125) & (g < 168) & (s <= 12)),
    ("scuro", "#6C6C6C", lambda g, s: (g >= 85) & (g < 125) & (s <= 12)),
    ("azzurro", "#B4C3CE", lambda g, s: (s > 12) & (g > 150)),
    ("ardesia", "#7F8993", lambda g, s: (s > 12) & (g <= 150) & (g > 90)),
]

# testi rifatti: (x, y, testo, rotazione, allineamento, dimensione px) in pixel dell'originale
FLUTE = 'FLUTE TYPE: "EB"'
TESTI = [(156, 1090, FLUTE, 0, "start", 9), (337, 1090, FLUTE, 0, "start", 9), (514, 1090, FLUTE, 0, "start", 9),
         (782, 793, FLUTE, 0, "start", 9), (998, 793, FLUTE, 0, "start", 9), (783, 1073, FLUTE, 0, "start", 9),
         (146, 1132, "827mm", 0, "middle", 7), (368, 1132, "570mm", 0, "middle", 7), (590, 1132, "827mm", 0, "middle", 7),
         (813, 1009, "760mm", 0, "middle", 7), (1023, 1009, "760mm", 0, "middle", 7), (812, 1133, "514mm", 0, "middle", 7),
         (263, 930, "1587mm", -90, "middle", 7), (459, 947, "1560mm", -90, "middle", 7), (708, 930, "1587mm", -90, "middle", 7),
         (919, 869, "1076mm", -90, "middle", 7), (1141, 869, "1076mm", -90, "middle", 7), (893, 1060, "400mm", -90, "middle", 7)]
# zone da ripulire prima del ricalco (vecchie scritte): x1, y1, x2, y2
CANC = [(150, 1080, 236, 1094), (331, 1080, 416, 1094), (508, 1080, 593, 1094),
        (776, 783, 856, 797), (992, 783, 1078, 797), (777, 1063, 863, 1077),
        (128, 1124, 166, 1136), (350, 1124, 388, 1136), (572, 1124, 610, 1136),
        (795, 1001, 832, 1013), (1005, 1001, 1042, 1013), (794, 1125, 832, 1137),
        (257, 908, 268, 952), (453, 925, 464, 970), (702, 908, 713, 952),
        (913, 845, 924, 893), (1135, 845, 1146, 893), (887, 1040, 898, 1080)]


# tratti di contorno interrotti dalla filigrana: (x1, y1, x2, y2, grigio)
RIPARA = [(860, 826, 860, 842, 100), (896, 895, 896, 914, 100), (982, 750, 982, 763, 100), (982, 751, 987, 751, 100), (916, 778, 916, 808, 205)]


def path_d(bitmap, scale, turd=6, alpha=1.0):
    """Ricalca un bitmap booleano e restituisce il 'd' di un path SVG (coordinate in mm)."""
    plist = potrace.Bitmap(~np.asarray(bitmap, bool)).trace(turdsize=turd, alphamax=alpha, opticurve=True, opttolerance=.3)
    f = lambda p: f"{p.x * scale:.2f},{p.y * scale:.2f}"
    out = []
    for curve in plist:
        out.append("M" + f(curve.start_point))
        for s in curve.segments:
            if s.is_corner:
                out.append("L" + f(s.c) + "L" + f(s.end_point))
            else:
                out.append("C" + f(s.c1) + " " + f(s.c2) + " " + f(s.end_point))
        out.append("Z")
    return "".join(out)


def build():
    im = cv2.imread(str(SRC))
    for x1, y1, x2, y2 in CANC:
        im[y1:y2, x1:x2] = 255
    for x1, y1, x2, y2, v in RIPARA:
        cv2.line(im, (x1, y1), (x2, y2), (v, v, v), 1)
    g0 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    b, _, r = [c.astype(int) for c in cv2.split(im)]
    sat = b - r
    h0, w0 = g0.shape

    # linee: black-hat sul grigio sovracampionato (la filigrana è più chiara del fondo e sparisce)
    gu = cv2.resize(g0, None, fx=U, fy=U, interpolation=cv2.INTER_CUBIC)
    bh = cv2.morphologyEx(gu, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))

    def pulisci(m, area, lato=0):
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        keep = (st[:, 4] >= area) & (np.maximum(st[:, 2], st[:, 3]) >= lato)
        keep[0] = False
        return keep[lab]

    solid = pulisci(bh > 75, 120, 36)          # via anche i segni isolati della filigrana
    near = cv2.dilate(solid.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    # tratteggi: soglie diverse per sviluppi (puliti) e viste 3D (disturbate dalla filigrana)
    yy, xx = np.mgrid[0:bh.shape[0], 0:bh.shape[1]]
    svil = yy >= 735 * U
    v3 = (xx >= 790 * U) & ~svil
    faint = (pulisci((bh > 22) & ~near & svil, 8, 4)
             | pulisci((bh > 35) & ~near & ~svil & ~v3, 40, 12)
             | pulisci((bh > 45) & ~near & v3 & (yy < 300 * U), 60, 14))   # nella vista dall'alto solo in testa

    # campiture: regioni chiuse dalle linee, ciascuna col colore prevalente (la filigrana non conta)
    barr = cv2.dilate((solid | faint).astype(np.uint8), np.ones((5, 5), np.uint8))
    barr = cv2.resize(barr, (w0, h0), interpolation=cv2.INTER_AREA) > 0
    n, lab = cv2.connectedComponents((~barr).astype(np.uint8), connectivity=4)
    cls = np.full((h0, w0), 0, int)                     # 0 = bianco
    for i, (_, _, cond) in enumerate(FILLS):
        cls[cond(g0, sat)] = i + 1
    bordo = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    cnt = np.zeros((n, len(FILLS) + 1), int)
    np.add.at(cnt, (lab.ravel(), cls.ravel()), 1)
    scelta = cnt.argmax(1)
    scelta[0] = -1
    scelta[bordo] = -1
    reg = scelta[lab]
    # i pixel di linea prendono la regione vicina, così le campiture passano sotto le linee
    for _ in range(3):
        d = cv2.dilate((reg + 1).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(int) - 1
        reg = np.where(barr & (reg < 0), d, reg)
    # tutto ciò che sta dentro il contorno di un pezzo è pieno (anche se chiuso solo da tratteggi);
    # l'apertura toglie quote e linee sottili, che restano senza fondo
    base = cv2.morphologyEx(((reg >= 0) | barr).astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ff = np.pad(base * 255, 1)
    cv2.floodFill(ff, np.zeros((h0 + 4, w0 + 4), np.uint8), (0, 0), 128)
    pieno = cv2.morphologyEx((ff[1:-1, 1:-1] != 128).astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
    reg = np.where(pieno & (reg < 0), 0, reg)
    bianco = reg >= 0
    masks = [reg == i + 1 for i in range(len(FILLS))]

    s1 = MM                      # scala per i livelli a risoluzione originale
    su = MM / U                  # scala per i livelli sovracampionati
    def up(m):                   # campitura allargata sotto le linee, sovracampionata e liscia
        m = m.astype(np.uint8)
        m = cv2.resize(m * 255, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        return cv2.GaussianBlur(m, (5, 5), 0) > 127

    body = [f'<path d="{path_d(up(bianco), s1 / 2, 40)}" fill="#FFFFFF"/>']
    for (nome, col, _), m in zip(FILLS, masks):
        body.append(f'<path d="{path_d(up(m), s1 / 2, 40)}" fill="{col}"/>')
    body.append(f'<path d="{path_d(faint, su, 4)}" fill="#8A8A8A"/>')
    body.append(f'<path d="{path_d(solid, su, 4)}" fill="#1E1E1E"/>')
    for x, y, t, rot, anc, size in TESTI:
        x, y = x * MM, y * MM
        tr = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot else ""
        body.append(f'<text x="{x:.2f}" y="{y:.2f}" font-family="Inter, Arial, sans-serif" font-size="{size * MM:.2f}" '
                    f'font-weight="600" fill="#8A8A8A" stroke="#FFFFFF" stroke-width="{.9 * MM:.2f}" paint-order="stroke" text-anchor="{anc}"{tr}>{t}</text>')
    W, H = w0 * MM, h0 * MM
    OUT.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.1f}mm" '
                   f'height="{H:.1f}mm" fill-rule="evenodd">{"".join(body)}</svg>', encoding="utf-8")
    print(OUT.name, f"{W:.0f}×{H:.0f} mm", f"{OUT.stat().st_size // 1024} kB")


if __name__ == "__main__":
    build()
