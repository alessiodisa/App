#!/usr/bin/env python3
"""
Portfolio Espositori — impostazione tecnica, formato orizzontale 297 × 210 mm.

Immagini (in img/):
  sq/CODICE.jpg           foto quadrata originale
  scontornate/CODICE.png  (facoltativo) scontorno fornito dall'azienda: se presente,
                          nelle tavole singole l'espositore esce dal riquadro
  bbox.json               ingombro dell'espositore nella foto (px su 1024)

    python3 portfolio.py      ->  portfolio.html
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
W, H, M = 297, 210, 12
TOP, BOT = 20, 193           # area utile
ACC = "#E8541E"
AZ = '<span class="tbd">[Nome Azienda]</span>'
BB = json.loads((ROOT / "img" / "bbox.json").read_text())

PROGETTI = {  # codice: (titolo, tipologia, settore)
    "B01": ("Oli essenziali", "Espositore a gradini con arco strutturale e header", "Erboristeria"),
    "B02": ("Carte da gioco", "Vassoio inclinato con header", "Giochi"),
    "B03": ("Skincare", "Vassoio con crowner sagomato", "Cosmesi"),
    "B04": ("Outdoor", "Vassoio con fondale fotografico", "Abbigliamento"),
    "B05": ("Oli essenziali", "Vassoio a gradini con header", "Erboristeria"),
    "B06": ("Collagene marino", "Pedana con fondale", "Farmacia"),
    "B07": ("Sistemi di fissaggio", "Colonna da banco con ganci", "Ferramenta"),
    "B08": ("Integratori", "Box espositore con header", "Farmacia"),
    "B09": ("Profumeria artistica", "Libreria a incastro", "Profumeria"),
    "B10": ("Occhiali da sole", "Pedana curva con fondale", "Ottica"),
    "B11": ("Occhiali", "Ripiani a sbalzo con fondale", "Ottica"),
    "B12": ("Occhiali", "Fondale con nicchie", "Ottica"),
    "B13": ("Cosmesi naturale", "Pedana con fondale", "Cosmesi"),
    "B14": ("Fragranze", "Pedana con fondale", "Profumeria"),
    "B15": ("Calzature", "Box con fondale doppio", "Abbigliamento"),
    "B16": ("Vino", "Pedana monobottiglia con fondale", "Beverage"),
    "B17": ("Skincare", "Espositore a gradini con header", "Cosmesi"),
    "T01": ("Pet care", "Colonna con vaschette e header", "Pet"),
    "T02": ("Cerotti", "Colonna con ganci e header", "Farmacia"),
    "T03": ("Tisane", "Colonna con mensole a sbalzo", "Erboristeria"),
    "T04": ("Igiene intima", "Colonna a ripiani colorati", "Farmacia"),
    "T05": ("Sistemi di fissaggio", "Colonna a cinque ripiani con header", "Ferramenta"),
    "T06": ("Integratori", "Colonna a ripiani con crowner", "Farmacia"),
    "T07": ("Eyewear", "Podio con fondale", "Ottica"),
    "T08": ("Occhiali da sole", "Totem a nicchie", "Ottica"),
}
DESCR = {
    "B01": "Il ponte ad arco sostiene il secondo gradino senza rinforzi interni: un solo foglio, piegato.",
    "B02": "Vassoio inclinato a scomparti: il prodotto resta ordinato anche quando l'espositore si svuota.",
    "B06": "Pedana e fondale a incastro: il fondale diventa superficie di comunicazione a tutta altezza.",
    "B07": "Colonna da banco con ganci per blister e vaschetta alla base per i prodotti sfusi.",
    "B09": "Montanti e ripiani a incastro, senza colla né ferramenta: si monta in pochi secondi.",
    "T04": "Ripiani a colori alterni che segmentano la gamma e guidano la scelta a colpo d'occhio.",
    "T05": "Fianchi portanti stampati a tutta altezza, ripiani con fascia frontale per il marchio.",
}


def TBD(s):
    return f'<span class="tbd">{s}</span>'


# --------------------------------------------------------------------------
# helper
# --------------------------------------------------------------------------
def bx(x, y, w=None, h=None):
    s = f"left:{x:.2f}mm;top:{y:.2f}mm"
    if w is not None:
        s += f";width:{w:.2f}mm"
    if h is not None:
        s += f";height:{h:.2f}mm"
    return s


def cid(c):
    return f"{c[0]}.{c[1:]}"


def scontornata(code):
    f = ROOT / "img" / "scontornate" / f"{code}.png"
    return f if f.exists() else None


def photo(code, frame, s=None, ax=.5, ay=.5, img_pos=None, pop=False, tag=True):
    """Foto quadrata vista attraverso un riquadro. s = lato della foto in mm
    (default: copre il riquadro). ax/ay = quale parte tenere quando si ritaglia."""
    fx, fy, fw, fh = frame
    s = s or max(fw, fh)
    ix, iy = img_pos or (fx - (s - fw) * ax, fy - (s - fh) * ay)
    out = (f'<div class="frame" style="{bx(fx, fy, fw, fh)}">'
           f'<img src="img/sq/{code}.jpg" style="{bx(ix - fx, iy - fy, s, s)}" alt=""></div>')
    if pop and scontornata(code):
        out += f'<img class="cut" src="img/scontornate/{code}.png" style="{bx(ix, iy, s, s)}" alt="">'
    if tag:
        out += f'<div class="tag" style="{bx(fx + 2.5, fy + 2.5)}">{cid(code)}</div>'
    return out


def svg(body):
    return f'<svg class="ov" viewBox="0 0 {W} {H}" style="{bx(0, 0, W, H)}">{body}</svg>'


def line(x1, y1, x2, y2, c="#9A9DA1", sw=.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{sw}"{d}/>'


def t(x, y, s, size=1.9, anchor="start", c="#8A8D91", rot=None):
    r = f' transform="rotate({rot} {x:.2f} {y:.2f})"' if rot is not None else ""
    return f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" text-anchor="{anchor}" fill="{c}" class="mono"{r}>{s}</text>'


def ruler(frame, side="left", c="#A4A7AB"):
    """Righello tecnico sul bordo superiore e su un lato del riquadro."""
    fx, fy, fw, fh = frame
    o = ""
    for i in range(0, int(fw) + 1, 5):
        L = 2.2 if i % 50 == 0 else (1.4 if i % 10 == 0 else .8)
        o += line(fx + i, fy - 1.2, fx + i, fy - 1.2 - L, c, .18)
        if i % 50 == 0:
            o += t(fx + i + .6, fy - 3.2, str(i), 1.6, "start", c)
    ex = fx - 1.2 if side == "left" else fx + fw + 1.2
    sg = -1 if side == "left" else 1
    for i in range(0, int(fh) + 1, 5):
        L = 2.2 if i % 50 == 0 else (1.4 if i % 10 == 0 else .8)
        o += line(ex, fy + i, ex + sg * L, fy + i, c, .18)
    return o


def callouts(frame, s, pts, img_pos=None):
    """pts: (n, px, py, lx, ly) in pixel della foto 1024×1024."""
    fx, fy, fw, fh = frame
    ix, iy = img_pos or (fx - (s - fw) / 2, fy - (s - fh) / 2)
    k = s / 1024
    o = ""
    for n, px, py, lx, ly in pts:
        ax, ay, bx_, by = ix + px * k, iy + py * k, ix + lx * k, iy + ly * k
        o += line(ax, ay, bx_, by, ACC, .25) + f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r=".7" fill="{ACC}"/>'
        o += f'<circle cx="{bx_:.2f}" cy="{by:.2f}" r="2.8" fill="{ACC}"/>' + t(bx_, by + .7, f"{n:02d}", 2, "middle", "#fff")
    return o


def cartiglio(code, x, y, w, extra=()):
    tt, tip, sett = PROGETTI[code]
    rows = [("Progetto", tt), ("Codice", cid(code)), ("Tipologia", tip), ("Settore", sett),
            ("Materiale", TBD("[materiale]")), ("Cliente", TBD("[cliente]")), ("Anno", TBD("[anno]")), *extra]
    r = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    return f'<dl class="cart" style="{bx(x, y, w)}">{r}</dl>'


def head(sezione, tav=""):
    return (f'<div class="hd" style="{bx(M, 9, W - 2 * M)}"><span>{AZ} / Portfolio espositori 2026</span>'
            f'<span>{sezione}</span><span>{tav}</span></div>')


def foot(n, tot, sezione=""):
    return f'<div class="ft" style="{bx(M, 199, W - 2 * M)}"><span>{sezione}</span><span>{n:02d} / {tot:02d}</span></div>'


# --------------------------------------------------------------------------
# schemi di pagina
# --------------------------------------------------------------------------
BANCO, TERRA = "Sez. 01 — Espositori da banco", "Sez. 02 — Espositori da terra"


def tav_singola(code, mirror=False):
    """Una foto grande quadrata + colonna tecnica con cartiglio."""
    tt, tip, sett = PROGETTI[code]
    fx = M if not mirror else W - M - 176
    tx = 198 if not mirror else M
    pop = scontornata(code) is not None
    frame = (fx, TOP + 36, 176, BOT - TOP - 36) if pop else (fx, TOP + 3, 176, BOT - TOP - 3)
    img_pos = (fx, TOP + 3) if pop else None
    body = photo(code, frame, s=176, img_pos=img_pos, pop=True)
    body += svg(ruler(frame, "left" if not mirror else "right"))
    body += f"""
  <div class="mono lbl" style="{bx(tx, TOP + 3)}">Tavola</div>
  <div class="code" style="{bx(tx, TOP + 7)}">{cid(code)}</div>
  <div class="h2" style="{bx(tx, TOP + 30, 87)}">{tt}</div>
  <p class="body" style="{bx(tx, TOP + 44, 87)}">{DESCR.get(code) or tip + '. ' + TBD('[Descrizione del progetto: esigenza, soluzione, risultato.]')}</p>
  {cartiglio(code, tx, 122, 87)}"""
    return body


def tav_coppia(codes):
    body = ""
    for i, c in enumerate(codes):
        x = M + i * 139
        fr = (x, TOP + 3, 134, 134)
        body += photo(c, fr) + (svg(ruler(fr)) if i == 0 else "")
        tt, tip, sett = PROGETTI[c]
        body += (f'<dl class="cart two" style="{bx(x, 162, 134)}"><dt>Progetto</dt><dd>{tt}</dd><dt>Tipologia</dt><dd>{tip}</dd>'
                 f'<dt>Settore</dt><dd>{sett}</dd><dt>Materiale</dt><dd>{TBD("[materiale]")}</dd></dl>')
    return body


def tav_sequenza(codes):
    a, b, c, d = codes
    fa = (M, TOP + 3, 120, 120)
    body = photo(a, fa) + svg(ruler(fa))
    body += photo(b, (137, TOP + 3, 72, 72)) + photo(c, (213, TOP + 3, 72, 72)) + photo(d, (137, 100, 72, 72))
    rows = "".join(f"<tr><td class='c'>{cid(x)}</td><td>{PROGETTI[x][0]}</td><td>{PROGETTI[x][1]}</td><td>{TBD('[materiale]')}</td></tr>"
                   for x in codes)
    body += f'<table class="dist" style="{bx(M, 150, 120)}"><tr><th>Cod.</th><th>Progetto</th><th>Tipologia</th><th>Materiale</th></tr>{rows}</table>'
    body += (f'<div style="{bx(213, 100, 72, 72)}" class="note"><div class="mono lbl">Nota</div>'
             f'<p class="body">Quattro soluzioni da banco con lo stesso principio: una base stabile e un fondale che porta la comunicazione. '
             f'Cambiano proporzioni, materiali e finiture.</p></div>')
    return body


def tav_verticale_coppia(codes):
    """Due espositori da terra in formato 2:3."""
    body = ""
    for i, c in enumerate(codes):
        x = M + i * 105
        fr = (x, TOP + 3, 100, 150)
        body += photo(c, fr, s=150) + (svg(ruler(fr)) if i == 0 else "")
        tt, tip, sett = PROGETTI[c]
        body += f'<div class="capt" style="{bx(x, 176, 100)}"><b>{cid(c)}</b> {tt}<span>{tip} · {TBD("[materiale]")}</span></div>'
    a, b = codes
    body += f"""<div style="{bx(225, TOP + 3, 60)}">
    <div class="mono lbl">Tavole</div><div class="code sm">{cid(a)} · {cid(b)}</div>
    <p class="body" style="margin-top:4mm">Colonne autoportanti con header: la comunicazione sale sopra il prodotto e si legge da lontano, anche dal fondo della corsia.</p></div>"""
    return body


def tav_verticale_singola(code):
    tt, tip, sett = PROGETTI[code]
    fr = (M, TOP + 3, 116, 170)
    body = photo(code, fr, s=170) + svg(ruler(fr))
    body += f"""
  <div class="mono lbl" style="{bx(140, TOP + 3)}">Tavola</div>
  <div class="code" style="{bx(140, TOP + 7)}">{cid(code)}</div>
  <div class="h2" style="{bx(140, TOP + 30, 90)}">{tt}</div>
  <p class="body" style="{bx(140, TOP + 44, 90)}">{DESCR.get(code) or tip + '.'}</p>
  {cartiglio(code, 140, 122, 145)}"""
    return body


def apertura(num, titolo, testo, sezione_codes, pages, hero, pts, legenda):
    idx = "".join(f"<tr><td class='c'>{cid(c)}</td><td>{PROGETTI[c][0]}</td><td class='p'>p. {pages[c]:02d}</td></tr>"
                  for c in sezione_codes)
    fr = (137, TOP + 3, 148, 148)
    leg = "".join(f"<li><b>{i + 1:02d}</b>{x}</li>" for i, x in enumerate(legenda))
    return f"""
  <div class="mono lbl light" style="{bx(M, TOP + 3)}">Sezione</div>
  <div class="bignum" style="{bx(M - 1, TOP + 5)}">{num}</div>
  <div class="h1" style="{bx(M, 70, 115)}">{titolo}</div>
  <p class="body light" style="{bx(M, 92, 110)}">{testo}</p>
  <table class="dist dark dense" style="{bx(M, 112, 115)}"><tr><th>Cod.</th><th>Progetto</th><th>Pag.</th></tr>{idx}</table>
  {photo(hero, fr, s=148, tag=False)}
  {svg(ruler(fr, "right", "#6B6E73") + callouts(fr, 148, pts))}
  <div class="mono lbl light" style="{bx(137, 175)}">Tav. {cid(hero)} — {PROGETTI[hero][0]}</div>
  <ul class="leg" style="{bx(137, 180, 148)}">{leg}</ul>"""


def copertina():
    fr = (125, TOP + 3, 160, 160)
    return f"""
  <div class="mono lbl light" style="{bx(M, TOP + 3)}">{AZ}</div>
  <div class="cover-t" style="{bx(M - 1, 62)}">Portfolio<br><span>Espositori</span></div>
  <p class="body light" style="{bx(M, 112, 95)}">Progettazione, prototipazione e produzione di espositori in cartotecnica e materiali durevoli.</p>
  <table class="dist dark" style="{bx(M, 150, 95)}"><tr><th>Sez.</th><th>Contenuto</th><th>Tavole</th></tr>
    <tr><td class="c">01</td><td>Espositori da banco</td><td class="p">17</td></tr>
    <tr><td class="c">02</td><td>Espositori da terra</td><td class="p">8</td></tr></table>
  {photo("B06", fr, s=160, tag=False)}
  {svg(ruler(fr, "right", "#6B6E73"))}
  <div class="mono lbl light" style="{bx(125, 187)}">Ed. 2026 — Rev. 00</div>"""


def chi_siamo():
    thumbs = "".join(photo(c, (M + i * 69, 136, 64, 57), s=64) for i, c in enumerate(["B03", "B11", "T02", "B16"]))
    return f"""
  <div class="mono lbl" style="{bx(M, TOP + 3)}">00 — Chi siamo</div>
  <div class="h1 ink" style="{bx(M, TOP + 9, 110)}">Dal disegno<br>al bancale.</div>
  <p class="body" style="{bx(128, TOP + 3, 75)}">Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. Seguiamo ogni progetto internamente: ufficio tecnico, campionatura, stampa, fustellatura, incollaggio e confezionamento.</p>
  <p class="body" style="{bx(128, 62, 75)}">Ogni espositore parte da una domanda semplice: dove verrà visto, da chi, per quanto tempo. Da lì scegliamo struttura, materiale e finiture, prototipiamo, testiamo e solo allora produciamo.</p>
  <dl class="cart" style="{bx(210, TOP + 3, 75)}"><dt>Esperienza</dt><dd>{TBD('35+ anni')}</dd><dt>Progetti</dt><dd>{TBD('400 l’anno')}</dd>
    <dt>Stabilimento</dt><dd>{TBD('6.000 m²')}</dd><dt>Reparti</dt><dd>Ufficio tecnico, stampa, fustellatura, confezionamento</dd>
    <dt>Settori</dt><dd>Cosmesi, farmacia, ottica, ferramenta, beverage, pet</dd></dl>
  {thumbs}"""


def contatti():
    fr = (150, TOP + 3, 135, 135)
    return f"""
  <div class="mono lbl light" style="{bx(M, TOP + 3)}">Contatti</div>
  <div class="h1" style="{bx(M, TOP + 9, 120)}">Il prossimo progetto<br>parte da un brief.</div>
  <dl class="cart dark" style="{bx(M, 90, 120)}"><dt>Email</dt><dd>{TBD('info@azienda.it')}</dd><dt>Telefono</dt><dd>{TBD('+39 000 000 0000')}</dd>
    <dt>Sede</dt><dd>{TBD('Via Esempio 1, Città')}</dd><dt>Web</dt><dd>{TBD('www.azienda.it')}</dd></dl>
  {photo("B17", fr, s=135, tag=False)}
  {svg(ruler(fr, "right", "#6B6E73"))}"""


# --------------------------------------------------------------------------
# sequenza delle pagine
# --------------------------------------------------------------------------
def piano():
    """(tipo, funzione, argomenti, codici, classe pagina, sezione)"""
    return [
        ("copertina", None, (), [], "dark", ""),
        ("chi", None, (), [], "", ""),
        ("ap_banco", None, (), ["B01"], "dark", BANCO),
        ("p", tav_singola, ("B02",), ["B02"], "", BANCO),
        ("p", tav_coppia, (["B03", "B04"],), ["B03", "B04"], "", BANCO),
        ("p", tav_singola, ("B06", True), ["B06"], "", BANCO),
        ("p", tav_sequenza, (["B05", "B08", "B13", "B17"],), ["B05", "B08", "B13", "B17"], "", BANCO),
        ("p", tav_singola, ("B09",), ["B09"], "", BANCO),
        ("p", tav_coppia, (["B10", "B11"],), ["B10", "B11"], "", BANCO),
        ("p", tav_singola, ("B07", True), ["B07"], "", BANCO),
        ("p", tav_sequenza, (["B12", "B14", "B15", "B16"],), ["B12", "B14", "B15", "B16"], "", BANCO),
        ("ap_terra", None, (), ["T05"], "dark", TERRA),
        ("p", tav_verticale_coppia, (["T01", "T02"],), ["T01", "T02"], "", TERRA),
        ("p", tav_verticale_singola, ("T04",), ["T04"], "", TERRA),
        ("p", tav_verticale_coppia, (["T03", "T06"],), ["T03", "T06"], "", TERRA),
        ("p", tav_verticale_coppia, (["T07", "T08"],), ["T07", "T08"], "", TERRA),
        ("contatti", None, (), [], "dark", ""),
    ]


def build():
    pl = piano()
    tot = len(pl)
    pages = {}
    for i, (_, _, _, codes, _, _) in enumerate(pl, start=1):
        for c in codes:
            pages[c] = i
    out = []
    for i, (kind, fn, args, codes, cls, sez) in enumerate(pl, start=1):
        if kind == "copertina":
            body = copertina()
        elif kind == "chi":
            body = head("Chi siamo") + chi_siamo() + foot(i, tot)
        elif kind == "ap_banco":
            body = head(BANCO) + apertura(
                "01", "Espositori<br>da banco",
                "Il punto più vicino alla scelta. Strutture compatte che si montano in pochi gesti e portano il prodotto all'altezza dello sguardo, accanto alla cassa.",
                [c for c in PROGETTI if c[0] == "B"], pages, "B01",
                [(1, 640, 300, 330, 150), (2, 705, 548, 930, 440), (3, 712, 615, 930, 720), (4, 452, 706, 250, 880)],
                ["Header con grafica a vivo", "Gradino portaprodotto", "Arco strutturale", "Fori per tester"]) + foot(i, tot, BANCO)
        elif kind == "ap_terra":
            body = head(TERRA) + apertura(
                "02", "Espositori<br>da terra",
                "Strutture autoportanti a più ripiani, pensate per reggere il carico e farsi vedere da lontano. Spedite piatte, montate in pochi minuti.",
                [c for c in PROGETTI if c[0] == "T"], pages, "T05",
                [(1, 555, 215, 780, 150), (2, 465, 470, 250, 420), (3, 578, 640, 800, 600), (4, 518, 858, 300, 900)],
                ["Header sagomato", "Ripiano con fascia", "Fianco portante", "Piedini a incastro"]) + foot(i, tot, TERRA)
        elif kind == "contatti":
            body = contatti() + foot(i, tot)
        else:
            tav = "Tav. " + " · ".join(cid(c) for c in codes)
            body = head(sez, tav) + fn(*args) + foot(i, tot, sez)
        out.append(f'<section class="page {cls}">{body}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio.css">
</head><body><main class="book">
{chr(10).join(out)}
</main></body></html>
"""
    (ROOT / "portfolio.html").write_text(doc, encoding="utf-8")
    print("portfolio.html:", tot, "pagine")


if __name__ == "__main__":
    build()
