#!/usr/bin/env python3
"""
Prova in A4 verticale (210 × 297 mm) del Portfolio Espositori.
Riusa contenuti e componenti di portfolio.py con impaginazioni pensate per la pagina verticale.

    python3 portfolio_a4.py   ->  portfolio-a4.html
"""
import portfolio as P
from portfolio import PROGETTI, DESCR, TBD, bx, cid, photo, svg, ruler, callouts, cartiglio, AZ

W, H, M = 210, 297, 14
TOP, BOT = 22, 280
P.W, P.H, P.M = W, H, M          # i componenti condivisi leggono queste misure
CW = W - 2 * M                    # 182 mm di area utile
BANCO, TERRA = P.BANCO, P.TERRA


def head(sezione, tav=""):
    return (f'<div class="hd" style="{bx(M, 10, CW)}"><span>{AZ} / Portfolio 2026</span>'
            f'<span>{sezione}</span><span>{tav}</span></div>')


def foot(n, tot, sezione=""):
    return f'<div class="ft" style="{bx(M, 285, CW)}"><span>{sezione}</span><span>{n:02d} / {tot:02d}</span></div>'


def testo_progetto(code, x, y, w):
    tt, tip, _ = PROGETTI[code]
    d = DESCR.get(code) or tip + ". " + TBD("[Descrizione del progetto: esigenza, soluzione, risultato.]")
    return f"""
  <div class="mono lbl" style="{bx(x, y)}">Tavola</div>
  <div class="code" style="{bx(x, y + 4)}">{cid(code)}</div>
  <div class="h2" style="{bx(x, y + 26, w)}">{tt}</div>
  <p class="body" style="{bx(x, y + 38, w)}">{d}</p>"""


# --------------------------------------------------------------------------
# schemi di pagina A4
# --------------------------------------------------------------------------
def tav_singola(code):
    fr = (M, TOP + 3, CW, CW)
    return photo(code, fr, s=CW) + svg(ruler(fr)) + testo_progetto(code, M, 212, 80) + cartiglio(code, 104, 212, 92)


def tav_coppia(codes):
    a, b = codes
    fa, fb = (M, TOP + 3, 120, 120), (76, 150, 120, 120)
    out = photo(a, fa) + photo(b, fb) + svg(ruler(fa))
    for c, x, y in ((a, 140, TOP + 3), (b, M, 150)):
        tt, tip, sett = PROGETTI[c]
        out += (f'<div style="{bx(x, y, 56)}"><div class="code sm">{cid(c)}</div><div class="h3">{tt}</div></div>'
                f'<dl class="cart two narrow" style="{bx(x, y + 22, 56)}"><dt>Tipol.</dt><dd>{tip}</dd><dt>Settore</dt><dd>{sett}</dd>'
                f'<dt>Mater.</dt><dd>{TBD("[materiale]")}</dd></dl>')
    return out


def tav_sequenza(codes):
    a, b, c, d = codes
    fa = (M, TOP + 3, 120, 120)
    out = photo(a, fa) + svg(ruler(fa))
    out += photo(b, (138, TOP + 3, 58, 58)) + photo(c, (138, TOP + 65, 58, 58)) + photo(d, (M, 150, 89, 89))
    out += (f'<div class="note" style="{bx(107, 150, 89)}"><div class="mono lbl">Nota</div>'
            f'<p class="body">Quattro soluzioni da banco con lo stesso principio: una base stabile e un fondale che porta la comunicazione. '
            f'Cambiano proporzioni, materiali e finiture.</p></div>')
    rows = "".join(f"<tr><td class='c'>{cid(x)}</td><td>{PROGETTI[x][0]}</td><td>{PROGETTI[x][1]}</td><td>{TBD('[materiale]')}</td></tr>"
                   for x in codes)
    out += f'<table class="dist" style="{bx(M, 246, CW)}"><tr><th>Cod.</th><th>Progetto</th><th>Tipologia</th><th>Materiale</th></tr>{rows}</table>'
    return out


def tav_verticale_coppia(codes):
    out = ""
    for i, c in enumerate(codes):
        x = M + i * 93
        fr = (x, TOP + 3, 89, 160)
        out += photo(c, fr, s=160) + (svg(ruler(fr)) if i == 0 else "")
        tt, tip, sett = PROGETTI[c]
        out += f'<div class="capt" style="{bx(x, 190, 89)}"><b>{cid(c)}</b> {tt}<span>{tip} · {TBD("[materiale]")}</span></div>'
    a, b = codes
    out += f"""<div class="note" style="{bx(M, 214, CW)}"><div class="mono lbl">Tavole {cid(a)} · {cid(b)}</div>
    <p class="body" style="max-width:120mm">Colonne autoportanti con header: la comunicazione sale sopra il prodotto e si legge da lontano, anche dal fondo della corsia.</p></div>"""
    for i, c in enumerate(codes):
        out += cartiglio(c, M + i * 93, 232, 89)
    return out


def tav_verticale_singola(code):
    fr = (M, TOP + 3, 110, 200)
    return photo(code, fr, s=200) + svg(ruler(fr)) + testo_progetto(code, 132, TOP + 3, 64) + cartiglio(code, 132, 158, 64)


def apertura(num, titolo, testo, codes, pages, hero, pts, legenda):
    fr = (M, 78, CW, 160)
    leg = "".join(f"<li><b>{i + 1:02d}</b>{x}</li>" for i, x in enumerate(legenda))
    idx = "".join(f"<li><b>{cid(c)}</b>{PROGETTI[c][0]}<span>p. {pages[c]:02d}</span></li>" for c in codes)
    return f"""
  <div class="mono lbl" style="{bx(M, TOP + 3)}">Sezione</div>
  <div class="bignum" style="{bx(M - 1, TOP + 6)}">{num}</div>
  <div class="h1" style="{bx(96, TOP + 8, 100)}">{titolo}</div>
  <p class="body" style="{bx(96, TOP + 34, 100)}">{testo}</p>
  {photo(hero, fr, s=CW, tag=False)}
  {svg(ruler(fr) + callouts(fr, CW, pts))}
  <ul class="leg" style="{bx(M, 241, CW)}">{leg}</ul>
  <ul class="idx3" style="{bx(M, 257, CW)}">{idx}</ul>"""


def copertina():
    fr = (M, 104, CW, 150)
    return f"""
  <div class="mono lbl" style="{bx(M, TOP + 3)}">{AZ}</div>
  <div class="cover-t" style="{bx(M - 1, 40)}">Portfolio<br><span>Espositori</span></div>
  <p class="body" style="{bx(M, 84, 110)}">Progettazione, prototipazione e produzione di espositori in cartotecnica e materiali durevoli.</p>
  {photo("B06", fr, s=CW, tag=False)}
  {svg(ruler(fr))}
  <table class="dist" style="{bx(M, 262, CW)}"><tr><th>Sez.</th><th>Contenuto</th><th>Tavole</th></tr>
    <tr><td class="c">01</td><td>Espositori da banco</td><td class="p">17</td></tr>
    <tr><td class="c">02</td><td>Espositori da terra</td><td class="p">8</td></tr></table>"""


def chi_siamo():
    fr = (M, 104, 112, 176)
    return f"""
  <div class="mono lbl" style="{bx(M, TOP + 3)}">00 — Chi siamo</div>
  <div class="h1" style="{bx(M, TOP + 9, CW)}">Dal disegno al bancale.</div>
  <p class="body" style="{bx(M, 50, 88)}">Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. Seguiamo ogni progetto internamente: ufficio tecnico, campionatura, stampa, fustellatura, incollaggio e confezionamento.</p>
  <p class="body" style="{bx(108, 50, 88)}">Ogni espositore parte da una domanda semplice: dove verrà visto, da chi, per quanto tempo. Da lì scegliamo struttura, materiale e finiture, prototipiamo, testiamo e solo allora produciamo.</p>
  {photo("B16", fr, s=176)}
  {svg(ruler(fr))}
  <dl class="cart" style="{bx(132, 104, 64)}"><dt>Esperienza</dt><dd>{TBD('35+ anni')}</dd><dt>Progetti</dt><dd>{TBD('400 l’anno')}</dd>
    <dt>Stabilimento</dt><dd>{TBD('6.000 m²')}</dd><dt>Reparti</dt><dd>Ufficio tecnico, stampa, fustellatura, confezionamento</dd>
    <dt>Settori</dt><dd>Cosmesi, farmacia, ottica, ferramenta, beverage, pet</dd></dl>"""


def contatti():
    fr = (M, 118, CW, 160)
    return f"""
  <div class="mono lbl" style="{bx(M, TOP + 3)}">Contatti</div>
  <div class="h1" style="{bx(M, TOP + 9, CW)}">Il prossimo progetto<br>parte da un brief.</div>
  <dl class="cart" style="{bx(M, 62, CW)}"><dt>Email</dt><dd>{TBD('info@azienda.it')}</dd><dt>Telefono</dt><dd>{TBD('+39 000 000 0000')}</dd>
    <dt>Sede</dt><dd>{TBD('Via Esempio 1, Città')}</dd><dt>Web</dt><dd>{TBD('www.azienda.it')}</dd></dl>
  {photo("B17", fr, s=CW, tag=False)}
  {svg(ruler(fr))}"""


def piano():
    return [
        ("copertina", None, (), []), ("chi", None, (), []), ("ap_banco", None, (), ["B01"]),
        ("p", tav_singola, ("B02",), ["B02"]),
        ("p", tav_coppia, (["B03", "B04"],), ["B03", "B04"]),
        ("p", tav_singola, ("B06",), ["B06"]),
        ("p", tav_sequenza, (["B05", "B08", "B13", "B17"],), ["B05", "B08", "B13", "B17"]),
        ("p", tav_singola, ("B09",), ["B09"]),
        ("p", tav_coppia, (["B10", "B11"],), ["B10", "B11"]),
        ("p", tav_singola, ("B07",), ["B07"]),
        ("p", tav_sequenza, (["B12", "B14", "B15", "B16"],), ["B12", "B14", "B15", "B16"]),
        ("ap_terra", None, (), ["T05"]),
        ("p", tav_verticale_coppia, (["T01", "T02"],), ["T01", "T02"]),
        ("p", tav_verticale_singola, ("T04",), ["T04"]),
        ("p", tav_verticale_coppia, (["T03", "T06"],), ["T03", "T06"]),
        ("p", tav_verticale_coppia, (["T07", "T08"],), ["T07", "T08"]),
        ("contatti", None, (), []),
    ]


def build():
    pl = piano()
    tot = len(pl)
    pages = {c: i for i, (_, _, _, cs) in enumerate(pl, start=1) for c in cs}
    out = []
    for i, (kind, fn, args, codes) in enumerate(pl, start=1):
        sez = BANCO if any(c[0] == "B" for c in codes) else TERRA if codes else ""
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
            body = head("Contatti") + contatti() + foot(i, tot)
        else:
            body = head(sez, "Tav. " + " · ".join(cid(c) for c in codes)) + fn(*args) + foot(i, tot, sez)
        out.append(f'<section class="page">{body}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori A4</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio.css">
<link rel="stylesheet" href="portfolio-a4.css">
</head><body><main class="book">
{chr(10).join(out)}
</main></body></html>
"""
    (P.ROOT / "portfolio-a4.html").write_text(doc, encoding="utf-8")
    print("portfolio-a4.html:", tot, "pagine")


if __name__ == "__main__":
    build()
