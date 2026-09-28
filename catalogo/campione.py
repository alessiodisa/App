#!/usr/bin/env python3
"""
Pagine campione — direzione "design + progettazione tecnica".
Genera campione.html (7 pagine: copertina + 3 doppie pagine).

    python3 campione.py
"""
from math import cos, sin, radians
from pathlib import Path

ROOT = Path(__file__).parent
W, H, M = 230, 300, 15
ACC = "#FF4F1F"          # arancio segnale: annotazioni tecniche
INK = "#1B1B1A"
AZ = "[Nome Azienda]"


# --------------------------------------------------------------------------
# primitive SVG (unità = mm)
# --------------------------------------------------------------------------
def svg(body, x=0, y=0, w=W, h=H, cls="draw"):
    return (f'<svg class="{cls}" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm" '
            f'viewBox="0 0 {w} {h}">{body}</svg>')


def line(x1, y1, x2, y2, c="currentColor", sw=.25, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{sw}"{d}/>'


def text(x, y, s, size=2.1, anchor="start", c="currentColor", rot=None, cls="t-mono"):
    r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
    return f'<text class="{cls}" x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{r}>{s}</text>'


def tick(x, y, c):
    return line(x - 1.1, y + 1.1, x + 1.1, y - 1.1, c, .3)


def dim_h(x1, x2, y, label, c=ACC, ext_from=None):
    out = line(x1, y, x2, y, c) + tick(x1, y, c) + tick(x2, y, c)
    if ext_from is not None:
        out += line(x1, ext_from, x1, y + (1.5 if y > ext_from else -1.5), c, .18)
        out += line(x2, ext_from, x2, y + (1.5 if y > ext_from else -1.5), c, .18)
    return out + text((x1 + x2) / 2, y - 1.2, label, 2, "middle", c)


def dim_v(x, y1, y2, label, c=ACC, ext_from=None):
    out = line(x, y1, x, y2, c) + tick(x, y1, c) + tick(x, y2, c)
    if ext_from is not None:
        out += line(ext_from, y1, x + (1.5 if x > ext_from else -1.5), y1, c, .18)
        out += line(ext_from, y2, x + (1.5 if x > ext_from else -1.5), y2, c, .18)
    return out + text(x - 1.2, (y1 + y2) / 2, label, 2, "middle", c, rot=-90)


def callout(n, px, py, lx, ly, c=ACC):
    return (line(px, py, lx, ly, c, .25) + f'<circle cx="{px}" cy="{py}" r=".8" fill="{c}"/>'
            f'<circle cx="{lx}" cy="{ly}" r="3" fill="{c}"/>' + text(lx, ly + .8, f"{n:02d}", 2.1, "middle", "#fff"))


def crop_marks(x, y, w, h, c=ACC, o=2.5, l=4):
    out = ""
    for cx, sx in ((x, -1), (x + w, 1)):
        for cy, sy in ((y, -1), (y + h, 1)):
            out += line(cx + sx * o, cy, cx + sx * (o + l), cy, c, .25)
            out += line(cx, cy + sy * o, cx, cy + sy * (o + l), c, .25)
    return out


# ---------- assonometria isometrica: facce riempite, ordine pittore ----------
C30, S30 = cos(radians(30)), sin(radians(30))


def iso(x, y, z, ox, oy, k):
    return ox + (x - y) * C30 * k, oy + (x + y) * S30 * k - z * k


def box(x, y, z, dx, dy, dz, ox, oy, k, fill, stroke, sw=.3):
    P = lambda a, b, c: iso(a, b, c, ox, oy, k)
    faces = [  # facce visibili: sinistra (y+), destra (x+), sopra
        [P(x, y + dy, z), P(x + dx, y + dy, z), P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)],
        [P(x + dx, y, z), P(x + dx, y + dy, z), P(x + dx, y + dy, z + dz), P(x + dx, y, z + dz)],
        [P(x, y, z + dz), P(x + dx, y, z + dz), P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)],
    ]
    return "".join(
        f'<polygon points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in f)}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linejoin="round"/>' for f in faces)


def esploso_terra(ox, oy, k, fill, stroke, acc):
    """Espositore da terra esploso: header e schienale (dietro), poi zoccolo e ripiani dal basso."""
    out, labels = "", []
    for (px, py) in ((0, 40), (60, 40), (60, 0)):
        a, b = iso(px, py, 0, ox, oy, k), iso(px, py, 110, ox, oy, k)
        out += line(*a, *b, acc, .25, "1.2 1")
    parts = [(0, -34, 132, 60, 3, 32, "Header"), (0, -26, 0, 60, 3, 118, "Schienale"),
             (0, 0, 0, 60, 40, 8, "Zoccolo"), (0, 0, 28, 60, 40, 10, "Ripiano 1"),
             (0, 0, 56, 60, 40, 10, "Ripiano 2"), (0, 0, 84, 60, 40, 10, "Ripiano 3")]
    for x, y, z, dx, dy, dz, n in parts:
        out += box(x, y, z, dx, dy, dz, ox, oy, k, fill, stroke)
        labels.append((n, iso(x + dx, y + dy / 2, z + dz / 2, ox, oy, k)))
    return out, labels


def esploso_banco(ox, oy, k, fill, stroke, acc):
    out = ""
    for (px, py) in ((0, 30), (40, 30), (40, 0)):
        a, b = iso(px, py, 0, ox, oy, k), iso(px, py, 70, ox, oy, k)
        out += line(*a, *b, acc, .25, "1.2 1")
    out += box(0, -12, 40, 40, 2, 34, ox, oy, k, fill, stroke)      # header (dietro)
    out += box(0, 0, 0, 40, 30, 4, ox, oy, k, fill, stroke)         # base
    out += box(0, 0, 16, 40, 30, 12, ox, oy, k, fill, stroke)       # vasca
    return out


# ---------- fustella (sviluppo in piano) di un espositore da banco ----------
def fustella(ox, oy, s=1.0):
    P = lambda x, y: f"{ox + x * s:.2f},{oy + y * s:.2f}"
    cut = ("M" + " L".join(P(*p) for p in [
        (45, 22), (45, 0), (115, 0), (115, 22), (160, 22), (160, 30), (172, 34), (172, 76), (160, 80), (160, 102),
        (115, 102), (115, 128), (45, 128), (45, 102), (0, 102), (0, 80), (-12, 76), (-12, 34), (0, 30), (0, 22)]) + " Z")
    cut_hdr = f"M{P(45, 0)} Q{P(80, -26)} {P(115, 0)}"
    window = f'<rect x="{ox + 62 * s:.2f}" y="{oy + 4 * s:.2f}" width="{36 * s:.2f}" height="{12 * s:.2f}" rx="{2 * s:.2f}" fill="none" stroke="{INK}" stroke-width=".35"/>'
    crease = " ".join(f"M{P(a, b)} L{P(c, d)}" for a, b, c, d in [
        (45, 22, 115, 22), (45, 80, 115, 80), (45, 102, 115, 102), (45, 22, 45, 102), (115, 22, 115, 102),
        (0, 30, 0, 80), (160, 30, 160, 80), (0, 22, 45, 22), (115, 22, 160, 22)])
    glue = "".join(line(ox + (x) * s, oy + 102 * s, ox + (x + 6) * s, oy + 128 * s, ACC, .18)
                   for x in range(47, 112, 5))
    body = (f'<path d="{cut} " fill="none" stroke="{INK}" stroke-width=".35"/>'
            f'<path d="{cut_hdr}" fill="none" stroke="{INK}" stroke-width=".35"/>{window}'
            f'<path d="{crease}" fill="none" stroke="{ACC}" stroke-width=".35" stroke-dasharray="2 1.2"/>'
            f'<clipPath id="gl"><rect x="{ox + 45 * s}" y="{oy + 102 * s}" width="{70 * s}" height="{26 * s}"/></clipPath>'
            f'<g clip-path="url(#gl)">{glue}</g>')
    lab = lambda x, y, t: text(ox + x * s, oy + y * s, t, 2, "middle", "#77746E")
    body += lab(80, 55, "BASE") + lab(80, 92, "FRONTALE") + lab(22, 58, "FIANCO SX") + lab(138, 58, "FIANCO DX") + \
        lab(80, 118, "") + lab(80, -8, "HEADER")
    body += dim_h(ox + 45 * s, ox + 115 * s, oy + 138 * s, "300", ext_from=oy + 130 * s)
    body += dim_h(ox - 12 * s, ox + 172 * s, oy + 146 * s, "790", ext_from=oy + 130 * s)
    body += dim_v(ox + 184 * s, oy - 18 * s, oy + 128 * s, "620", ext_from=oy + 128 * s)
    return body


def profilo_onda(x, y, w, kind):
    """Sezioni dei materiali in sezione."""
    out = ""
    if kind in ("E", "B"):
        h = 2.2 if kind == "E" else 4
        per = 3.2 if kind == "E" else 6
        out += line(x, y, x + w, y, INK, .3) + line(x, y + h, x + w, y + h, INK, .3)
        d = f"M{x},{y + h}"
        n = int(w / per)
        for i in range(n):
            xa = x + i * per
            d += f" Q{xa + per / 4:.2f},{y - h * .1:.2f} {xa + per / 2:.2f},{y:.2f} Q{xa + per * .75:.2f},{y + h * 1.1:.2f} {xa + per:.2f},{y + h:.2f}"
        out += f'<path d="{d}" fill="none" stroke="{ACC}" stroke-width=".3"/>'
    elif kind == "BC":
        out += profilo_onda(x, y, w, "B") + profilo_onda(x, y + 4, w, "E").replace(f'stroke="{INK}"', f'stroke="{INK}"')
    elif kind == "HC":
        out += line(x, y, x + w, y, INK, .3) + line(x, y + 7, x + w, y + 7, INK, .3)
        for i in range(int(w / 4)):
            xa = x + i * 4
            out += f'<path d="M{xa},{y + 7} L{xa + 1},{y} M{xa + 2},{y} L{xa + 3},{y + 7}" stroke="{ACC}" stroke-width=".3" fill="none"/>'
    elif kind == "SOLID":
        out += f'<rect x="{x}" y="{y}" width="{w}" height="3" fill="none" stroke="{INK}" stroke-width=".3"/>'
        for i in range(int(w / 1.5)):
            out += line(x + i * 1.5, y + 3, x + i * 1.5 + 1.5, y, ACC, .15)
    elif kind == "PMMA":
        out += f'<rect x="{x}" y="{y}" width="{w}" height="5" fill="rgba(255,79,31,.08)" stroke="{INK}" stroke-width=".3"/>'
        out += line(x + 3, y + 1.5, x + 12, y + 1.5, ACC, .3)
    return out


# --------------------------------------------------------------------------
# helper HTML
# --------------------------------------------------------------------------
def ph(code, what, x, y, w, h, dark=False):
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = ROOT / "img" / f"{code}.{ext}"
        if f.exists():
            return f'<div class="ph" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm"><img src="img/{f.name}" alt=""></div>'
    return (f'<div class="ph{" d" if dark else ""}" style="left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm">'
            f'<span class="code">{code}</span><span class="what">{what}</span></div>')


def at(x, y, w=None):
    return f"left:{x}mm;top:{y}mm" + (f";width:{w}mm" if w else "")


def head(l, r):
    return f'<div class="hd"><span>{l}</span><span>{r}</span></div>'


def foot(n, t):
    return f'<div class="ft"><span>{n:02d}</span><span>{t}</span></div>'


# --------------------------------------------------------------------------
# pagine
# --------------------------------------------------------------------------
def p_copertina():
    draw, labels = esploso_terra(96, 150, 0.62, INK, "#F2F1ED", ACC)
    leg = ""
    labels.sort(key=lambda t: t[1][1])
    for i, (n, (x, y)) in enumerate(labels):
        lx = 186
        ly = 52 + i * 22
        leg += line(x, y, lx - 4, ly, "#8A877F", .2) + f'<circle cx="{x:.2f}" cy="{y:.2f}" r=".7" fill="{ACC}"/>'
        leg += text(lx - 2.5, ly + .7, f"{i + 1:02d}", 2, "start", ACC) + text(lx + 3, ly + .7, n.upper(), 2, "start", "#CFCCC6")
    return ("dark grid", f"""
  {head(AZ + " — Portfolio Vol. 01", "Rif. PF-2026 · Scala 1:20")}
  {svg(draw + leg)}
  <div class="abs" style="{at(M, 214, 200)}">
    <div class="mono acc">Progettazione · Design · Produzione</div>
    <div class="t-xxl" style="margin-top:4mm">Portfolio<br><span class="thin">Espositori</span></div>
  </div>
  <div class="ft"><span>Cartotecnica &amp; materiali durevoli</span><span>2026</span></div>""")


def p_sezione_sx():
    # prospetti quotati di un espositore da banco
    ox, oy = M + 8, 150
    front = (f'<path d="M{ox},{oy + 62} L{ox},{oy + 30} L{ox + 70},{oy + 30} L{ox + 70},{oy + 62} Z" fill="none" stroke="{INK}" stroke-width=".35"/>'
             f'<path d="M{ox + 4},{oy + 30} L{ox + 4},{oy + 6} Q{ox + 35},{oy - 8} {ox + 66},{oy + 6} L{ox + 66},{oy + 30}" fill="none" stroke="{INK}" stroke-width=".35"/>'
             f'<rect x="{ox + 22}" y="{oy + 8}" width="26" height="10" rx="1.5" fill="none" stroke="{INK}" stroke-width=".3"/>')
    for i in range(4):
        front += f'<rect x="{ox + 7 + i * 15}" y="{oy + 20}" width="11" height="34" fill="none" stroke="#8A877F" stroke-width=".25" stroke-dasharray="1 .8"/>'
    front += line(ox, oy + 50, ox + 70, oy + 50, INK, .3)
    front += dim_h(ox, ox + 70, oy + 72, "300", ext_from=oy + 62)
    front += dim_v(ox - 8, oy - 1.5, oy + 62, "450", ext_from=ox)
    sx = ox + 100
    side = (f'<path d="M{sx},{oy + 62} L{sx},{oy + 1} L{sx + 5},{oy + 1} L{sx + 5},{oy + 30} L{sx + 48},{oy + 44} L{sx + 48},{oy + 62} Z" '
            f'fill="none" stroke="{INK}" stroke-width=".35"/>' + line(sx + 5, oy + 50, sx + 48, oy + 50, INK, .3))
    side += dim_h(sx, sx + 48, oy + 72, "200", ext_from=oy + 62)
    side += dim_v(sx + 58, oy + 44, oy + 62, "80", ext_from=sx + 48)
    labels = text(ox, oy - 16, "PROSPETTO FRONTALE", 2, "start", "#77746E") + text(sx, oy - 16, "PROSPETTO LATERALE", 2, "start", "#77746E")
    tip = "".join(
        f'<div class="row"><span class="acc">B.{i + 1:02d}</span><span>{t}</span></div>'
        for i, t in enumerate(["A gradini con header", "Con vano tester", "Girevole", "Porta-leaflet", "Espositore cassa", "Edizione limitata"]))
    return ("paper grid", f"""
  {head("Sezione 01 / 12", "Espositori da banco")}
  <div class="abs outline-num" style="{at(M - 2, 22)}">01</div>
  <div class="abs" style="{at(M, 92, 200)}"><div class="t-xl">Espositori<br>da banco</div></div>
  {svg(front + side + labels)}
  <div class="abs" style="{at(M, 250, 200)}"><div class="mono dim" style="margin-bottom:2mm">Indice progetti</div><div class="idx">{tip}</div></div>
  {foot(10, "Espositori da banco")}""")


def p_sezione_dx():
    x, y, w, h = M, 28, 200, 200
    ann = crop_marks(x, y, w, h) + callout(1, 115, 70, 150, 48) + callout(2, 95, 150, 60, 176) + callout(3, 140, 200, 175, 214)
    leg = [("01", "Header fustellato con finestra logo"), ("02", "Vasca rinforzata in microonda E"), ("03", "Base a incastro, montaggio senza colla")]
    legh = "".join(f'<div class="row"><span class="acc">{n}</span><span>{t}</span></div>' for n, t in leg)
    return ("white", f"""
  {head(AZ, "Fig. 01")}
  {ph("BAN-01", "Foto principale del progetto — quadrata o 4:5, prodotto caricato, fondo neutro", x, y, w, h)}
  {svg(ann)}
  <div class="abs" style="{at(M, 240, 95)}"><div class="mono dim">Fig. 01 — <span class="tbd">[Brand]</span>, 2025</div>
    <p class="body" style="margin-top:2mm">Espositore da banco a tre ripiani per il lancio di una linea skincare. Struttura in un unico pezzo, spedito piatto.</p></div>
  <div class="abs" style="{at(120, 240, 95)}"><div class="idx">{legh}</div></div>
  {foot(11, "Espositori da banco")}""")


def p_progetto_sx():
    spec = [("Progetto", '<span class="tbd">[Brand] — [Linea]</span>'), ("Tipologia", "Espositore da banco a gradini"),
            ("Struttura", "Monopezzo + header a incastro"), ("Materiale", "Microonda E, 1,5 mm"),
            ("Stampa", "Offset 4/0 + UV selettiva"), ("Formato", "300 × 200 × 450 mm"),
            ("Tiratura", '<span class="tbd">1.200 pz</span>'), ("Montaggio", "45 secondi, senza colla")]
    sp = "".join(f'<div><div class="mono dim">{k}</div><div class="v">{v}</div></div>' for k, v in spec)
    return ("white", f"""
  {head("Progetto B.01", "Anatomia di un progetto")}
  <div class="abs" style="{at(M, 26, 200)}"><div class="mono acc">B.01</div><div class="t-l" style="margin-top:2mm"><span class="tbd">[Brand]</span><br><span class="thin">Linea <span class="tbd">[Nome]</span></span></div></div>
  {ph("BAN-02", "Foto orizzontale 3:2 — vista 3/4 del progetto", M, 80, 200, 133)}
  {svg(crop_marks(M, 80, 200, 133))}
  <div class="abs spec" style="{at(M, 222, 200)}">{sp}</div>
  {foot(12, "Espositori da banco")}""")


def p_progetto_dx():
    d = fustella(42, 66, 0.78)
    ex = esploso_banco(52, 258, 0.62, "#F2F1ED", INK, ACC)
    leg = (line(M, 26, M + 8, 26, INK, .35) + text(M + 10, 26.7, "TAGLIO", 2, "start", INK) +
           line(M + 30, 26, M + 38, 26, ACC, .35, "2 1.2") + text(M + 40, 26.7, "CORDONATURA", 2, "start", INK) +
           f'<rect x="{M + 68}" y="24.5" width="6" height="3" fill="none" stroke="{ACC}" stroke-width=".25"/>' +
           text(M + 76, 26.7, "INCOLLAGGIO", 2, "start", INK))
    return ("paper grid", f"""
  {head("Sviluppo in piano", "Scala 1:5")}
  {svg(d + ex + leg + text(M, 200, "ESPLOSO ASSONOMETRICO", 2, "start", "#77746E"))}
  {ph("BAN-03", "Dettaglio 3:2", 122, 200, 93, 62)}
  <div class="abs mono dim" style="{at(122, 265, 93)}">Fig. 02 — Dettaglio incastro header</div>
  {foot(13, "Espositori da banco")}""")


def p_materiali_sx():
    rows = [("M.01", "Microonda E", "1,5 mm · stampa diretta, pieghe nette", "E"),
            ("M.02", "Onda B", "3 mm · strutture e ripiani", "B"),
            ("M.03", "Onda BC", "7 mm · pallet display, alte portate", "BC"),
            ("M.04", "Alveolare", "10–50 mm · pannelli portanti leggeri", "HC"),
            ("M.05", "Cartoncino teso", "300–600 g/m² · resa premium", "SOLID"),
            ("M.06", "Plexiglass", "3–10 mm · trasparente, satinato, fumé", "PMMA")]
    body, draw = "", ""
    for i, (c, n, d, k) in enumerate(rows):
        y = 70 + i * 30
        body += (f'<div class="mrow" style="top:{y}mm"><span class="acc mono">{c}</span>'
                 f'<span class="t-m">{n}</span><span class="mono dim2">{d}</span></div>')
        draw += profilo_onda(150, y + 5, 60, k).replace(INK, "#E9E7E2")
    return ("dark grid", f"""
  {head("Materiali", "Sezioni in scala 2:1")}
  <div class="abs" style="{at(M, 26, 200)}"><div class="t-xl" style="color:#fff">Materia<br><span class="thin">prima.</span></div></div>
  {''.join(body)}
  {svg(draw)}
  {foot(14, "Materiali")}""")


def p_materiali_dx():
    tiles = ""
    for i in range(6):
        x, y = M + (i % 2) * 102, 28 + (i // 2) * 82
        tiles += ph(f"MAT-{i + 1:02d}", "Macro materiale 5:4", x, y, 98, 72)
        tiles += f'<div class="abs mono dim" style="{at(x, y + 74)}">M.{i + 1:02d}</div>'
    return ("white", f"""
  {head(AZ, "Campionario")}
  {tiles}
  {foot(15, "Materiali")}""")


# --------------------------------------------------------------------------
CSS = f"""
@page {{ size: 230mm 300mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ background: #CFCDC8; font-family: "Inter", sans-serif; font-size: 8pt; line-height: 1.5; color: {INK};
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.book {{ display: grid; grid-template-columns: repeat(2, 230mm); row-gap: 16mm; justify-content: center; padding: 16mm 0; }}
@media screen {{ .book {{ zoom: .6; }} }}
.book > .page:first-child {{ grid-column: 2; }}
@media print {{ html, body {{ background: none; }} .book {{ display: block; padding: 0; }} .page {{ break-after: page; }} }}
.page {{ position: relative; width: 230mm; height: 300mm; overflow: hidden; background: #fff; }}
.page.paper {{ background: #EEEDE9; }}
.page.dark {{ background: {INK}; color: #F2F1ED; }}
.page.grid {{ background-image: linear-gradient(rgba(0,0,0,.045) .2mm, transparent .2mm), linear-gradient(90deg, rgba(0,0,0,.045) .2mm, transparent .2mm);
  background-size: 10mm 10mm; background-position: 5mm 5mm; }}
.page.dark.grid {{ background-image: linear-gradient(rgba(255,255,255,.05) .2mm, transparent .2mm), linear-gradient(90deg, rgba(255,255,255,.05) .2mm, transparent .2mm); }}
.abs, .draw, .ph {{ position: absolute; }}
.draw {{ overflow: visible; }}
.t-mono, .mono, .hd, .ft {{ font-family: "IBM Plex Mono", monospace; }}
.t-mono {{ letter-spacing: .15px; font-weight: 500; }}
.hd, .ft {{ position: absolute; left: {M}mm; right: {M}mm; display: flex; justify-content: space-between; font-size: 6pt; letter-spacing: .08em; text-transform: uppercase; }}
.hd {{ top: 10mm; }} .ft {{ bottom: 10mm; }}
.page:nth-child(odd) .ft {{ flex-direction: row-reverse; }}
.mono {{ font-size: 6.3pt; letter-spacing: .08em; text-transform: uppercase; line-height: 1.5; }}
.acc {{ color: {ACC}; }}
.dim {{ color: #8A877F; }}
.dim2 {{ color: #9C998F; }}
.t-xxl, .t-xl, .t-l, .t-m {{ font-family: "Inter Tight", sans-serif; font-weight: 600; letter-spacing: -.04em; }}
.t-xxl {{ font-size: 64pt; line-height: .9; }}
.t-xl {{ font-size: 46pt; line-height: .92; }}
.t-l {{ font-size: 30pt; line-height: .98; }}
.t-m {{ font-size: 15pt; line-height: 1; letter-spacing: -.02em; }}
.thin {{ font-weight: 300; }}
.outline-num {{ font-family: "Inter Tight", sans-serif; font-weight: 600; font-size: 170pt; line-height: .8; letter-spacing: -.06em;
  color: transparent; -webkit-text-stroke: .3mm {INK}; }}
.body {{ font-size: 7.8pt; line-height: 1.55; color: #55524D; }}
.idx .row {{ display: grid; grid-template-columns: 12mm 1fr; border-top: .2mm solid rgba(0,0,0,.2); padding: 1.6mm 0 1.8mm; font-size: 7.6pt; }}
.idx .row .acc {{ font-family: "IBM Plex Mono", monospace; font-size: 6.3pt; }}
.idx {{ column-count: 2; column-gap: 8mm; }}
.idx .row {{ break-inside: avoid; }}
.spec {{ display: grid; grid-template-columns: repeat(4, 1fr); column-gap: 5mm; row-gap: 5mm; }}
.spec > div {{ border-top: .2mm solid rgba(0,0,0,.25); padding-top: 2mm; }}
.spec .v {{ font-size: 7.8pt; margin-top: 1mm; }}
.mrow {{ position: absolute; left: {M}mm; width: 200mm; height: 24mm; border-top: .2mm solid rgba(255,255,255,.18); padding-top: 3mm;
  display: grid; grid-template-columns: 16mm 1fr; grid-template-rows: auto 1fr; column-gap: 0; }}
.mrow .t-m {{ color: #fff; }}
.mrow .dim2 {{ grid-column: 2; margin-top: 1.5mm; }}
.tbd {{ background: rgba(255,196,0,.35); }}
.ph {{ background: linear-gradient(155deg, #E2E0DB, #CAC7C0); overflow: hidden; }}
.ph img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.ph .code {{ position: absolute; top: 3mm; left: 3mm; font: 500 6pt/1 "IBM Plex Mono", monospace; background: {INK}; color: #fff; padding: 1.2mm 1.5mm; }}
.ph .what {{ position: absolute; left: 3mm; bottom: 3mm; max-width: 110mm; font: 400 6.3pt/1.35 "Inter", sans-serif; color: rgba(0,0,0,.55);
  background: rgba(255,255,255,.55); padding: 1mm 1.4mm; }}
"""


def build():
    pages = [p_copertina(), p_sezione_sx(), p_sezione_dx(), p_progetto_sx(), p_progetto_dx(), p_materiali_sx(), p_materiali_dx()]
    html = "\n".join(f'<section class="page {c}">{b}\n</section>' for c, b in pages)
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pagine Campione</title>
<link rel="stylesheet" href="fonts/fonts.css">
<style>{CSS}</style></head>
<body><main class="book">
{html}
</main></body></html>
"""
    (ROOT / "campione.html").write_text(doc, encoding="utf-8")
    print("campione.html:", len(pages), "pagine")


if __name__ == "__main__":
    build()
