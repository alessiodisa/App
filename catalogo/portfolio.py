#!/usr/bin/env python3
"""
Portfolio Espositori — formato orizzontale 297 × 210 mm.

Immagini (in img/):
  sq/CODICE.jpg      foto quadrata originale
  cut/CODICE.webp    stesso scatto scontornato (per gli espositori che escono dal riquadro)
  bbox.json          ingombro dell'espositore nella foto (px su 1024)

    python3 portfolio.py      ->  portfolio.html
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
W, H, M = 297, 210, 14
BB = json.loads((ROOT / "img" / "bbox.json").read_text())
AZ = '<span class="tbd">[Nome Azienda]</span>'

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
MAT = '<span class="tbd">[materiale]</span>'
CLI = '<span class="tbd">[cliente]</span>'


# --------------------------------------------------------------------------
# helper
# --------------------------------------------------------------------------
def box(x, y, w=None, h=None):
    s = f"left:{x:.2f}mm;top:{y:.2f}mm"
    if w is not None:
        s += f";width:{w:.2f}mm"
    if h is not None:
        s += f";height:{h:.2f}mm"
    return s


def place(code, cx, bottom, h):
    """Posiziona la foto quadrata in modo che l'espositore sia alto h mm,
    centrato su cx e appoggiato a quota bottom. Ritorna (ix, iy, lato)."""
    x1, y1, x2, y2 = BB[code]
    s = h / ((y2 - y1) / 1024)
    ix = cx - (x1 + x2) / 2 / 1024 * s
    iy = bottom - y2 / 1024 * s
    return ix, iy, s


def obj_w(code, h):
    x1, y1, x2, y2 = BB[code]
    return h * (x2 - x1) / (y2 - y1)


def photo(code, pos, frame, pop=False):
    """Foto vista attraverso un riquadro; con pop=True l'espositore scontornato
    esce dal riquadro."""
    ix, iy, s = pos
    fx, fy, fw, fh = frame
    out = (f'<div class="frame" style="{box(fx, fy, fw, fh)}">'
           f'<img src="img/sq/{code}.jpg" style="{box(ix - fx, iy - fy, s, s)}" alt=""></div>')
    if pop:
        out += f'<img class="cut" src="img/cut/{code}.webp" style="{box(ix, iy, s, s)}" alt="">'
    return out


def cutout(code, pos, shadow=True):
    ix, iy, s = pos
    x1, y1, x2, y2 = BB[code]
    sh = ""
    if shadow:
        cx = ix + (x1 + x2) / 2 / 1024 * s
        w = (x2 - x1) / 1024 * s * 1.1
        by = iy + y2 / 1024 * s
        sh = f'<div class="ground" style="{box(cx - w / 2, by - 3, w, 6)}"></div>'
    return sh + f'<img class="cut free" src="img/cut/{code}.webp" style="{box(ix, iy, s, s)}" alt="">'


def title(t, sub=""):
    return (f'<div class="ptitle" style="{box(M, M)}">{t}</div>'
            + (f'<div class="psub" style="{box(M, M + 7)}">{sub}</div>' if sub else ""))


def pnum(n):
    return f'<div class="pnum">{n:02d}</div>'


def foot(sezione):
    return f'<div class="pfoot"><span>{sezione}</span></div>'


def code_id(c):
    return f"{c[0]}.{c[1:]}"


def data(code, extra=()):
    t, tip, sett = PROGETTI[code]
    rows = [("Tipologia", tip), ("Settore", sett), ("Materiale", MAT), ("Cliente", CLI), *extra]
    return '<dl class="data">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def cap(code, x, y, w, extra=""):
    t, tip, sett = PROGETTI[code]
    return (f'<div class="cap" style="{box(x, y, w)}"><b>{code_id(code)}</b>&ensp;{t}'
            f'<span>{tip}{extra}</span></div>')


def vline(x, y1, y2):
    return f'<div class="vline" style="{box(x, y1, None, y2 - y1)}"></div>'


def text(html, x, y, w, cls="body"):
    return f'<div class="{cls}" style="{box(x, y, w)}">{html}</div>'


# --------------------------------------------------------------------------
# pagine
# --------------------------------------------------------------------------
BANCO, TERRA = "Espositori da banco", "Espositori da terra"


def copertina():
    pos = place("B01", 205, 184, 122)
    return ("", f"""
  <div class="block" style="{box(128, 104, 155, 92)}"></div>
  {cutout("B01", pos, shadow=False)}
  {text("Progettazione, prototipazione e produzione di espositori per il punto vendita.", M + 1, 92, 95, "lead")}
  <ul class="idx one" style="{box(M + 1, 150, 95)}"><li><b>01</b>Espositori da banco</li><li><b>02</b>Espositori da terra</li></ul>
  <div class="cover-t" style="{box(M, 26)}">Portfolio</div>
  <div class="cover-s" style="{box(M + 1, 50)}">Espositori · Cartotecnica · Materiali durevoli</div>
  <div class="cover-az" style="{box(M + 1, 57)}">{AZ}</div>
  <div class="vtext" style="left:{W - 10}mm;top:{24}mm">2026</div>""")


def chi_siamo():
    return ("taupe", f"""
  {title("Chi siamo", "Progettazione · Prototipazione · Produzione")}
  {pnum(1)}
  {vline(104, 40, 190)}{vline(196, 40, 190)}
  {text('Progettiamo e produciamo espositori in cartotecnica e materiali durevoli: dal primo schizzo al bancale pronto a partire.', M, 42, 80, "lead")}
  {photo("B05", place("B05", M + 40, 182, 56), (M, 110, 80, 80))}
  {text('Dal <span class="tbd">[anno]</span> a <span class="tbd">[città]</span> seguiamo ogni progetto internamente: ufficio tecnico, campionatura, stampa, fustellatura e confezionamento.<br><br>Ogni espositore nasce da una domanda semplice: dove verrà visto, da chi, per quanto tempo. Da lì scegliamo struttura, materiale e finiture, prototipiamo, testiamo e solo allora produciamo.', 114, 42, 72)}
  {text('<dl class="data light"><dt>Esperienza</dt><dd><span class="tbd">35+ anni</span></dd><dt>Progetti</dt><dd><span class="tbd">400 l’anno</span></dd><dt>Stabilimento</dt><dd><span class="tbd">6.000 m²</span></dd><dt>Settori</dt><dd>Cosmesi, farmacia, alimentare, ottica, ferramenta, beverage, pet</dd></dl>', 206, 42, 77, "")}
  <div class="vtext light" style="left:{W - 10}mm;top:120mm">Contatti · <span class="tbd">info@azienda.it</span></div>
  {foot("Portfolio 2026")}""")


def apertura_banco():
    pos = place("B06", 102, 192, 150)
    idx = "".join(f'<li><b>{code_id(c)}</b>{PROGETTI[c][0]}</li>' for c in PROGETTI if c[0] == "B")
    return ("", f"""
  {photo("B06", pos, (0, 0, 160, H), pop=True)}
  <div class="bignum" style="{box(198, 12)}">01</div>
  <div class="h1" style="{box(198, 58, 88)}">Espositori<br>da banco</div>
  {text("Il punto più vicino alla scelta. Strutture compatte che si montano in pochi gesti e mettono il prodotto all'altezza dello sguardo, accanto alla cassa.", 198, 82, 86)}
  <ul class="idx" style="{box(198, 112, 86)}">{idx}</ul>
  {foot(BANCO)}""")


def overview(code, n, sez, mirror=False):
    t, tip, sett = PROGETTI[code]
    h = {"B02": 150, "B17": 160}.get(code, 138)
    if not mirror:
        pos = place(code, 202, 186, h)
        frame, bx = (122, 58, 161, 138), M
    else:
        pos = place(code, 95, 186, h)
        frame, bx = (M, 58, 161, 138), 187
    info = f"""<div class="ovbox" style="{box(bx, 58, 96, 138)}">
      <div class="ov-t">{t}</div><div class="ov-s">{code_id(code)} · {sett}</div>
      <div class="ov-h">Il progetto</div><p>{tip}. <span class="tbd">[Obiettivo del cliente, soluzione, risultato: 2–3 righe.]</span></p>
      <div class="ov-h">Dati</div>{data(code)}</div>"""
    return ("", f"""{title("Progetto in evidenza", sez)}{pnum(n)}{photo(code, pos, frame, pop=True)}{info}{foot(sez)}""")


def mosaico(codes, n, sez):
    a, b, c, d, e = codes
    body = (
        photo(a, place(a, 70, 150, 98), (M, 34, 112, 124)) + cap(a, M, 161, 112)
        + photo(b, place(b, 207, 102, 64), (132, 34, 151, 74)) + cap(b, 132, 111, 151)
        + photo(c, place(c, 155, 160, 38), (132, 124, 46, 46)) + cap(c, 132, 173, 46)
        + photo(d, place(d, 207, 160, 38), (184, 124, 46, 46)) + cap(d, 184, 173, 46)
        + photo(e, place(e, 260, 160, 38), (236, 124, 47, 46)) + cap(e, 236, 173, 47)
    )
    return ("", f"""{title("Selezione progetti", sez)}{pnum(n)}{body}{foot(sez)}""")


def laterale(code, n, sez, mirror=False, pos=None):
    """Foto al vivo su un lato, espositore che sconfina verso il testo."""
    t, tip, sett = PROGETTI[code]
    if not mirror:
        frame, tx = (0, 0, 165, H), 180
    else:
        frame, tx = (132, 0, 165, H), M
    return ("", f"""
  {photo(code, pos, frame, pop=True)}
  {pnum(n) if not mirror else ''}
  <div class="ov-s" style="{box(tx, 24)}">{code_id(code)} · {sett}</div>
  <div class="h2" style="{box(tx, 30, 100)}">{t}</div>
  {text(f'{tip}. <span class="tbd">[Descrizione del progetto: esigenza, soluzione strutturale, risultato.]</span>', tx, 50, 92)}
  {text(data(code), tx, 78, 92, "")}
  {foot(sez)}""")


def tavola_scontornati(codes, n, sez, heights, floor=170, taupe=True):
    xs = [M + 30 + i * ((W - 2 * M - 60) / (len(codes) - 1)) for i in range(len(codes))]
    body = f'<div class="floor" style="{box(M, floor, W - 2 * M)}"></div>'
    for c, cx, h in zip(codes, xs, heights):
        body += cutout(c, place(c, cx, floor, h))
        t, tip, sett = PROGETTI[c]
        body += (f'<div class="cap center" style="{box(cx - 30, floor + 4, 60)}"><b>{code_id(c)}</b>&ensp;{t}'
                 f'<span>{tip}</span></div>')
    return ("taupe" if taupe else "", f"""{title("Silhouette", sez)}{pnum(n)}{body}{foot(sez)}""")


def dettagli(codes, n, sez):
    a, b, c = codes
    return ("white", f"""
  {title("Dettagli di progetto", sez)}{pnum(n)}
  {vline(104, 36, 192)}{vline(196, 36, 192)}
  {photo(a, place(a, 55, 118, 68), (M, 36, 82, 92))}
  {text(f'<b>{code_id(a)} — {PROGETTI[a][0]}</b><br>{PROGETTI[a][1]}. Ripiani a sbalzo agganciati al fondale: struttura leggera, lettura pulita del prodotto.', M, 136, 82)}
  {text(f'<b>{code_id(b)} — {PROGETTI[b][0]}</b><br>{PROGETTI[b][1]}. Nicchie ricavate nello spessore del fondale, senza parti aggiunte.', 114, 36, 72)}
  {photo(b, place(b, 150, 180, 84), (114, 66, 72, 126))}
  {photo(c, place(c, 245, 150, 70), (206, 58, 77, 84), pop=True)}
  {text(f'<b>{code_id(c)} — {PROGETTI[c][0]}</b><br>{PROGETTI[c][1]}. Due fondali sfalsati creano profondità e raccontano il prodotto in due scene.', 206, 150, 77)}
  {foot(sez)}""")


def coppia(big, small, n, sez, big_h=120, frame_big=(160, 40, 123, 150), pop_big=True):
    tb, tipb, settb = PROGETTI[big]
    ts, tips, setts = PROGETTI[small]
    fx, fy, fw, fh = frame_big
    pos = place(big, fx + fw / 2 - 6, fy + fh - 12, big_h)
    return ("", f"""
  {title(ts, code_id(small) + " · " + setts)}{pnum(n)}
  {photo(small, place(small, 76, 104, 50), (40, 38, 84, 72))}
  <div class="meta" style="{box(40, 113, 84)}"><span>Settore: {setts}</span><span>Cliente: {CLI}</span></div>
  {text(f'{tips}. <span class="tbd">[Breve descrizione del progetto.]</span>', 40, 124, 84)}
  {vline(140, 40, 190)}
  {photo(big, pos, frame_big, pop=pop_big)}
  <div class="cap" style="{box(fx, fy + fh + 3, fw)}"><b>{code_id(big)}</b>&ensp;{tb}<span>{tipb}</span></div>
  {foot(sez)}""")


def apertura_terra():
    pos = place("T05", 136, 200, 186)
    idx = "".join(f'<li><b>{code_id(c)}</b>{PROGETTI[c][0]}</li>' for c in PROGETTI if c[0] == "T")
    return ("", f"""
  {photo("T05", pos, (0, 0, 150, H), pop=True)}
  <div class="bignum" style="{box(190, 12)}">02</div>
  <div class="h1" style="{box(190, 58, 95)}">Espositori<br>da terra</div>
  {text("Strutture autoportanti a più ripiani, pensate per reggere il carico e farsi vedere da lontano. Spedite piatte, montate in pochi minuti.", 190, 82, 90)}
  <ul class="idx" style="{box(190, 112, 95)}">{idx}</ul>
  {foot(TERRA)}""")


def contatti():
    return ("taupe", f"""
  {title("Contatti", "Parliamo del prossimo progetto")}
  {pnum(99).replace("99", "")}
  {cutout("B01", place("B01", 212, 176, 112))}
  {text('Ogni progetto di questo portfolio è nato da un brief. Il prossimo può essere il tuo.', M, 42, 110, "lead")}
  {text('<dl class="data light"><dt>Email</dt><dd><span class="tbd">info@azienda.it</span></dd><dt>Telefono</dt><dd><span class="tbd">+39 000 000 0000</span></dd><dt>Sede</dt><dd><span class="tbd">Via Esempio 1, Città</span></dd><dt>Web</dt><dd><span class="tbd">www.azienda.it</span></dd></dl>', M, 100, 110, "")}
  <div class="vtext light" style="left:{W - 10}mm;top:150mm">Portfolio 2026</div>""")


def pagine():
    p = [copertina(), chi_siamo(), apertura_banco()]
    p.append(overview("B02", 3, BANCO))
    p.append(mosaico(["B03", "B04", "B05", "B08", "B13"], 4, BANCO))
    p.append(laterale("B09", 5, BANCO, pos=(-30, -4, 232)))
    p.append(tavola_scontornati(["B07", "B10", "B16"], 6, BANCO, [118, 82, 92]))
    p.append(dettagli(["B11", "B12", "B15"], 7, BANCO))
    p.append(coppia("B01", "B14", 8, BANCO))
    p.append(overview("B17", 9, BANCO, mirror=True))
    p.append(apertura_terra())
    p.append(tavola_scontornati(["T01", "T02", "T03", "T06"], 11, TERRA, [120, 138, 112, 146], floor=172))
    p.append(coppia("T04", "T07", 12, TERRA, big_h=160, frame_big=(170, 52, 113, 136)))
    p.append(laterale("T08", 13, TERRA, mirror=True, pos=place("T08", 150, 196, 178)))
    p.append(contatti())
    return p


# --------------------------------------------------------------------------
CSS = f"""
@page {{ size: 297mm 210mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --bg: #F1F0ED; --white: #F8F8F6; --taupe: #BAB0A3; --ink: #1E1D1B; --ink2: #5A554E; --line: #CBC5BC; --tbd: rgba(255,196,0,.4); }}
html, body {{ background: #8C857C; font-family: "Montserrat", sans-serif; color: var(--ink);
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.book {{ display: flex; flex-direction: column; align-items: center; gap: 12mm; padding: 14mm 0; }}
@media screen {{ .book {{ zoom: .75; }} .page {{ box-shadow: 0 3mm 10mm rgba(0,0,0,.28); }} }}
@media print {{ html, body {{ background: none; }} .book {{ display: block; padding: 0; }} .page {{ break-after: page; }} }}
.page {{ position: relative; width: 297mm; height: 210mm; overflow: hidden; background: var(--bg); }}
.page.white {{ background: var(--white); }}
.page.taupe {{ background: var(--taupe); color: #fff; }}
.page > * {{ position: absolute; }}

.frame {{ overflow: hidden; background: #D6D6D4; }}
.frame img {{ position: absolute; max-width: none; }}
.cut {{ position: absolute; pointer-events: none; filter: drop-shadow(0 1.2mm 1.6mm rgba(0,0,0,.16)); }}
.cut.free {{ filter: none; }}
.ground {{ border-radius: 50%; background: radial-gradient(closest-side, rgba(0,0,0,.28), rgba(0,0,0,0)); }}
.block {{ background: var(--taupe); }}
.floor {{ border-top: .25mm solid rgba(255,255,255,.7); }}

.ptitle {{ font-weight: 700; font-size: 12.5pt; text-transform: uppercase; letter-spacing: .01em; line-height: 1; }}
.psub {{ font-weight: 400; font-size: 6.4pt; text-transform: uppercase; letter-spacing: .12em; color: var(--ink2); }}
.taupe .psub {{ color: rgba(255,255,255,.8); }}
.pnum {{ right: 12mm; top: 5mm; font-family: "Cormorant Garamond", serif; font-weight: 300; font-size: 50pt; line-height: 1; color: rgba(0,0,0,.14); }}
.taupe .pnum {{ color: rgba(255,255,255,.75); }}
.pfoot {{ left: {M}mm; bottom: 7mm; font-size: 5.6pt; text-transform: uppercase; letter-spacing: .14em; color: var(--ink2); }}
.taupe .pfoot {{ color: rgba(255,255,255,.75); }}
.vline {{ border-left: .25mm solid var(--line); }}
.taupe .vline {{ border-color: rgba(255,255,255,.55); }}
.vtext {{ transform: rotate(90deg); transform-origin: left top; font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; white-space: nowrap; }}
.vtext.light {{ color: #fff; }}

.body {{ font-weight: 300; font-size: 7.3pt; line-height: 1.6; color: var(--ink2); }}
.body b {{ font-weight: 600; color: var(--ink); }}
.taupe .body {{ color: #fff; }}
.lead {{ font-weight: 400; font-size: 13pt; line-height: 1.35; letter-spacing: -.005em; }}
.h1 {{ font-weight: 700; font-size: 25pt; line-height: 1.02; text-transform: uppercase; letter-spacing: -.005em; }}
.h2 {{ font-weight: 700; font-size: 17pt; line-height: 1.05; text-transform: uppercase; }}
.bignum {{ font-family: "Cormorant Garamond", serif; font-weight: 300; font-size: 96pt; line-height: 1; color: rgba(0,0,0,.16); }}

.cover-t {{ font-weight: 700; font-size: 54pt; text-transform: uppercase; letter-spacing: -.01em; line-height: 1; }}
.cover-s {{ font-weight: 500; font-size: 8pt; text-transform: uppercase; letter-spacing: .2em; }}
.cover-az {{ font-weight: 400; font-size: 8pt; letter-spacing: .06em; color: var(--ink2); }}

.idx {{ list-style: none; column-count: 2; column-gap: 6mm; font-size: 6.8pt; }}
.idx li {{ border-top: .25mm solid var(--line); padding: 1.3mm 0 1.5mm; break-inside: avoid; }}
.idx.one {{ column-count: 1; font-size: 7.5pt; }}
.idx b {{ display: inline-block; width: 11mm; font-weight: 600; color: var(--ink2); }}

.ovbox {{ border: .3mm solid var(--ink); padding: 7mm 6mm; }}
.ov-t {{ font-weight: 700; font-size: 15pt; text-transform: uppercase; line-height: 1.05; }}
.ov-s {{ font-weight: 400; font-size: 6.4pt; text-transform: uppercase; letter-spacing: .12em; color: var(--ink2); margin-top: 1.5mm; }}
.ov-h {{ font-weight: 600; font-size: 8.5pt; text-transform: uppercase; margin-top: 7mm; margin-bottom: 1.5mm; }}
.ovbox p {{ font-weight: 300; font-size: 7.2pt; line-height: 1.6; color: var(--ink2); }}

.data {{ display: grid; grid-template-columns: 22mm 1fr; }}
.data > * {{ border-top: .25mm solid var(--line); padding: 1.4mm 0 1.6mm; font-size: 6.8pt; line-height: 1.4; }}
.data dt {{ font-weight: 600; text-transform: uppercase; font-size: 5.6pt; letter-spacing: .1em; color: var(--ink2); padding-top: 1.8mm; }}
.data dd {{ font-weight: 400; }}
.data.light > * {{ border-color: rgba(255,255,255,.5); color: #fff; }}
.data.light dd {{ font-size: 8pt; }}

.cap {{ font-size: 6.6pt; line-height: 1.35; font-weight: 500; }}
.cap b {{ font-weight: 700; }}
.cap span {{ display: block; font-weight: 300; color: var(--ink2); font-size: 6.2pt; }}
.taupe .cap span {{ color: rgba(255,255,255,.85); }}
.cap.center {{ text-align: center; }}
.meta {{ display: flex; justify-content: space-between; font-size: 6pt; color: var(--ink2); }}
.tbd {{ background: var(--tbd); }}
"""


def build():
    pages = pagine()
    html = "\n".join(f'<section class="page {c}">{b}\n</section>' for c, b in pages)
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori</title>
<link rel="stylesheet" href="fonts/fonts.css">
<style>{CSS}</style></head>
<body><main class="book">
{html}
</main></body></html>
"""
    (ROOT / "portfolio.html").write_text(doc, encoding="utf-8")
    print("portfolio.html:", len(pages), "pagine")


if __name__ == "__main__":
    build()
