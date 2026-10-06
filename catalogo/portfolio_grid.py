#!/usr/bin/env python3
"""
Portfolio Espositori — formato orizzontale A4 (297 × 210 mm) a doppia pagina,
su griglia a vista (7 × 5 moduli per pagina), sul modello "Architecture Portfolio".

Immagini: img/sq/CODICE.jpg (foto) e img/scontornate/CODICE.png (scontornate fornite).

    python3 portfolio_grid.py   ->  portfolio-grid.html
"""
import json
from portfolio import PROGETTI as _P, DESCR, BB, ROOT

PROGETTI = dict(_P)
PROGETTI.update({
    "B18": ("Confezioni regalo", "Fondale sagomato con vetrina in plexiglas", "Regalo"),
    "B19": ("Calzature sportive", "Pedana con fondali sfalsati", "Sport"),
    "B20": ("Serramenti", "Espositore campionario con fondale ambientato", "Edilizia"),
})
CB = json.loads((ROOT / "img" / "cbbox.json").read_text())   # ingombro nelle scontornate

W, H = 297, 210
C, R = W / 7, H / 5            # modulo di griglia: 42,43 × 42 mm
AZ = "Onprint"
LOGO = "img/logo-onprint.png"


def logo(x, y, w, right=False):
    """Logo aziendale (fondo bianco reso trasparente con multiply)."""
    pos = f"right:{x:.1f}mm" if right else f"left:{x:.1f}mm"
    return f'<img class="logo" src="{LOGO}" style="{pos};top:{y:.1f}mm;width:{w:.1f}mm" alt="Onprint">'


def TBD(s):
    return f'<span class="tbd">{s}</span>'


def bx(x, y, w=None, h=None):
    s = f"left:{x:.2f}mm;top:{y:.2f}mm"
    if w is not None:
        s += f";width:{w:.2f}mm"
    if h is not None:
        s += f";height:{h:.2f}mm"
    return s


MARG = 15   # margine uguale su tutti i lati (mm)


def g(col, row):
    """Coordinate di impaginazione -> mm dentro l'area utile con margini di 15 mm
    (colonne .5–6.5 e righe .45–4.55 corrispondono ai bordi dell'area)."""
    return MARG + (col - .5) * (W - 2 * MARG) / 6, MARG + (row - .45) * (H - 2 * MARG) / 4.1


def cid(c):
    return f"{c[0]}.{c[1:]}"


def cut_file(code):
    f = ROOT / "img" / "scontornate" / f"{code}.png"
    return f"img/scontornate/{code}.png" if f.exists() else None


def photo(code, c0, r0, c1, r1, zoom=1.0, fy=.5, fx=.5):
    """Foto dentro un riquadro che va dall'incrocio (c0,r0) a (c1,r1), centrata sull'espositore."""
    x0, y0 = g(c0, r0)
    x1, y1 = g(c1, r1)
    fw, fh = x1 - x0, y1 - y0
    a1_, b1_, a2_, b2_ = BB[code]
    ss = max(fw, fh) * zoom
    if (a2_ - a1_) / 1024 * ss > fw + .5 or (b2_ - b1_) / 1024 * ss > fh + .5:
        print(f"  ! {code}: espositore tagliato nel riquadro {fw:.0f}x{fh:.0f} mm")
    s = max(fw, fh) * zoom
    a1, b1, a2, b2 = BB[code]
    cx = (a1 + (a2 - a1) * fx) / 1024 * s
    cy = (b1 + (b2 - b1) * fy) / 1024 * s
    ix = min(max(x0 + fw / 2 - cx, x0 + fw - s), x0)
    iy = min(max(y0 + fh / 2 - cy, y0 + fh - s), y0)
    return (f'<div class="frame" style="{bx(x0, y0, fw, fh)}">'
            f'<img src="img/sq/{code}.jpg" style="{bx(ix - x0, iy - y0, s, s)}" alt=""></div>')


def scontornata(code, cx_col, bottom_row, h, max_w=None):
    """Espositore scontornato appoggiato sulla griglia: centrato sulla colonna cx_col,
    base sulla riga bottom_row, alto h mm (ridotto se supera max_w mm di larghezza)."""
    a1, b1, a2, b2, n = CB[code]
    if max_w and h * (a2 - a1) / (b2 - b1) > max_w:
        h = max_w * (b2 - b1) / (a2 - a1)
    s = h / ((b2 - b1) / n)
    x, y = g(cx_col, bottom_row)
    ix = x - (a1 + a2) / 2 / n * s
    iy = y - b2 / n * s
    return f'<img class="cut" src="img/scontornate/{code}.png" style="{bx(ix, iy, s, s)}" alt="">'


def el(cls, html, col, row, w_cols=None):
    x, y = g(col, row)
    w = f";width:{g(col + w_cols, row)[0] - x:.2f}mm" if w_cols else ""
    return f'<div class="{cls}" style="{bx(x, y)}{w}">{html}</div>'


def plus(col, row):
    """Crocetta sempre su un incrocio reale della griglia di sfondo."""
    x, y = col * C, row * R
    return f'<div class="plus" style="{bx(x - 2, y - 2)}"></div>'


def testo(code):
    return DESCR.get(code) or PROGETTI[code][1] + ". " + TBD("[Descrizione del progetto.]")


def lista_lettere(items):
    return "".join(f'<div class="li"><b>{chr(65 + i)}</b><div><h5>{t}</h5><p>{d}</p></div></div>' for i, (t, d) in enumerate(items))


def cap(code):
    t, tip, sett = PROGETTI[code]
    return f'<b>{cid(code)} — {t}</b>{tip}'


# --------------------------------------------------------------------------
# pagine
# --------------------------------------------------------------------------
def voce_indice(n, t, p, r):
    return (el("bignum", n, .5, r) + el("index-t", t, 1.9, r + .2, 3.6)
            + el("index-p", f"{p:02d}", 5.8, r + .2, .7) + el("rule", "", .5, r + .78, 6))


def copertina():
    x, y = g(6.5, .45)
    return (el("small", "Vol. 01 — 2027", .5, .45)
            + el("small", "Progettato e prodotto da", .5, .75) + logo(g(.5, .9)[0], g(.5, .9)[1], 32)
            + el("small", "Cartotecnica ed espositori per il punto vendita: progettazione, prototipazione e produzione. "
                 "Cartone, cartoncino e materiali durevoli.", .5, 1.35, 2.6)
            + f'<img class="drawing" src="img/esploso-terra.svg" style="right:{W - x:.1f}mm;top:{y:.1f}mm;height:{H - 2 * MARG:.1f}mm" alt="">'
            + el("light-t", "Portfolio", .5, 2.3) + el("cover-t", "Espositori", .5, 2.62)
            + el("capline", "<b>Fig. 01</b>Espositore da terra — vista esplosa", .5, 3.5, 2)
            + plus(1, 1) + plus(4, 1) + plus(1, 4) + plus(4, 4))


def introduzione():
    sx = (el("h2", "Introduzione", .5, .45)
          + el("quote", "Ogni prodotto merita il suo spazio: struttura, materiale e grafica pensati insieme.", .5, .85, 4)
          + el("small cols", "Progettiamo e produciamo espositori da banco e da terra, pedane, totem e allestimenti per il punto vendita. "
               "Ogni progetto nasce in ufficio tecnico, viene prototipato, testato e poi prodotto internamente, "
               "dalla stampa alla fustellatura fino al confezionamento.", .5, 1.75, 5)
          + el("h6", "Cosa facciamo", .5, 2.45)
          + el("bullets big two", "".join(f"<li>{x}</li>" for x in [
              "Progettazione strutturale e grafica", "Prototipi in tempi brevi", "Stampa offset e digitale",
              "Fustellatura e incollaggio interni", "Cartone, forex, plexi, legno", "Spedizione piatta o premontata"]), .5, 2.7, 5)
          + el("bar", "", .5, 4.2, 6)
          + el("small", "Un unico interlocutore, dal primo disegno al bancale pronto a partire.", .5, 4.47, 3)
          + plus(6, 1) + plus(6, 2))
    dx = (el("h2", "Indice", .5, .45)
          + voce_indice("01", "Espositori da banco", 6, 1.0)
          + voce_indice("02", "Espositori da terra", 20, 2.0)
          + voce_indice("03", "Contatti", 28, 3.0)
          + el("small", "Una selezione di progetti realizzati per brand della cosmesi, della farmacia, dell'ottica, della ferramenta e del beverage.", .5, 4.47, 4))
    return sx, dx


def chi_siamo():
    sx = (el("h2", "Chi siamo", .5, .45)
          + el("quote", "Dal disegno al bancale, sotto lo stesso tetto.", .5, .85, 2.8)
          + el("small", f"Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. "
               "Un unico interlocutore significa tempi più rapidi, meno passaggi e un controllo costante sulla qualità.", .5, 1.55, 2.7)
          + el("letters big", lista_lettere([
              ("Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
              ("Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
              ("Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
              ("Logistica", "Spedizione piatta o premontata, in Italia e all'estero.")]), 3.6, .85, 2.9)
          + el("stats", f'<div><b>{TBD("35+")}</b>Anni</div><div><b>{TBD("400")}</b>Progetti l’anno</div><div><b>100%</b>Interno</div>', .5, 4.19, 3)
          + el("bignum right", "01", 5.0, 4.19, 1.5))
    dx = (el("quote", "Un espositore funziona quando si monta in un minuto, regge il carico e fa vedere il prodotto meglio dello scaffale.", .5, .45, 1.7)
          + el("small", "Ogni progetto parte da una domanda: dove verrà visto, da chi, per quanto tempo.", .5, 3.95, 1.7)
          + photo("B06", 2.4, .45, 6.5, 4.55))
    return sx, dx


def sezione(titolo, codes, num=""):
    a, b, c, d, e = codes
    sx = (el("h2", titolo, .5, .45)
          + photo(a, .5, .9, 2.62, 4.33) + photo(b, 2.72, .9, 4.85, 4.33)
          + el("capline", cap(a), .5, 4.4, 2) + el("capline", cap(b), 2.72, 4.4, 2)
          + el("h6", "Panoramica", 5.05, .9)
          + el("small", "Ogni progetto parte dal prodotto e dal punto vendita: dimensioni, peso, numero di facing, tempo di permanenza. "
               "Da lì scegliamo struttura e materiale, prototipiamo e produciamo.", 5.05, 1.1, 1.45)
          + el("small", "Nelle pagine che seguono, una selezione di progetti realizzati.", 5.05, 2.05, 1.45)
          + el("bignum right", num, 5.0, 4.12, 1.5))
    dx = (photo(c, .5, .45, 4.1, 4.33)
          + photo(d, 4.25, .45, 6.5, 2.3) + photo(e, 4.25, 2.45, 6.5, 4.33)
          + el("capline", cap(c), .5, 4.4, 3.4) + el("capline", f"{cid(d)} · {cid(e)} — {PROGETTI[d][0]}, {PROGETTI[e][0]}", 4.25, 4.4, 2.25))
    return sx, dx


def meta_html(tip, sett):
    return (f'<h5>Tipologia: {tip}</h5><h5>Settore: {sett}</h5><h5>Materiale: {TBD("[materiale]")}</h5>'
            f'<h5>Cliente: {TBD("[cliente]")} — {TBD("[anno]")}</h5>')


def progetto(num, main, small, sq, tall, cut=None):
    t, tip, sett = PROGETTI[main]
    sx = (photo(main, .5, .45, 4.1, 3.5)
          + el("bignum right", num, 4.3, .45, 2.2)
          + photo(small, 4.3, 1.35, 6.5, 3.5)
          + el("capline", cap(small), 4.3, 3.57, 2.2)
          + el("h6", "Il progetto", .5, 3.75)
          + el("small", testo(main), .5, 3.95, 1.7)
          + el("small", "Struttura, materiali e finiture definiti con il cliente e verificati su prototipo prima della produzione.", 2.35, 3.95, 1.75)
          + el("rule", "", .5, 4.53, 6))
    dx = (el("h2", t, .5, .45, 2) + el("code", cid(main), .5, 1.05)
          + el("h6", "Panoramica", .5, 1.45)
          + el("small", f"{tip}. " + TBD("[Esigenza del cliente e soluzione adottata.]"), .5, 1.65, 1.9)
          + el("meta", meta_html(tip, sett), .5, 2.4, 1.9)
          + el("quote sm", "Il prodotto al centro, la struttura al suo servizio.", .5, 3.75, 1.9)
          + el("rule", "", .5, 4.53, 6))
    if cut:
        dx += scontornata(cut, 3.5, 4.3, 125, max_w=90) + el("capline", cap(cut), 2.55, 4.37, 1.9)
    else:
        dx += photo(sq, 2.55, .45, 4.45, 2.75) + el("capline", cap(sq), 2.55, 2.82, 1.9)
    dx += photo(tall, 4.6, .45, 6.5, 3.2) + el("capline", cap(tall), 4.6, 3.27, 1.9)
    return sx, dx


def progetto_terra(num, a, b, cut):
    sx = (photo(a, .5, .45, 2.5, 4.33) + photo(b, 2.6, .45, 4.6, 4.33)
          + el("capline", cap(a), .5, 4.4, 2) + el("capline", cap(b), 2.6, 4.4, 2)
          + el("bignum right", num, 4.8, .45, 1.7)
          + el("h6", "Panoramica", 4.8, 4.0)
          + el("small", "Colonne autoportanti con header: la comunicazione sale sopra il prodotto e si legge anche dal fondo della corsia.", 4.8, 4.2, 1.7))
    t, tip, sett = PROGETTI[cut]
    dx = (el("h2", t, .5, .45, 3) + el("code", cid(cut), .5, .85)
          + el("h6", "Panoramica", .5, 1.25) + el("small", testo(cut), .5, 1.45, 1.9)
          + el("meta", meta_html(tip, sett), .5, 2.2, 1.9)
          + el("quote sm", "Leggibile da lontano, stabile a pieno carico.", .5, 3.75, 1.9)
          + scontornata(cut, 4.6, 4.55, 178))
    return sx, dx


def quote(code, cx_col, bottom_row, h, max_w):
    """Espositore scontornato con quote di altezza e larghezza (valori da completare).
    Ritorna (html, sinistra, destra, alto) in mm."""
    a1, b1, a2, b2, n = CB[code]
    if h * (a2 - a1) / (b2 - b1) > max_w:
        h = max_w * (b2 - b1) / (a2 - a1)
    w = h * (a2 - a1) / (b2 - b1)
    x, y = g(cx_col, bottom_row)
    l, r, t = x - w / 2, x + w / 2, y - h
    q = (f'<svg class="ov" viewBox="0 0 {W} {H}" style="{bx(0, 0, W, H)}">'
         f'<g stroke="#8C8C8C" stroke-width=".22" fill="none">'
         f'<line x1="{l - 5:.1f}" y1="{t:.1f}" x2="{l - 5:.1f}" y2="{y:.1f}"/><line x1="{l - 7:.1f}" y1="{t:.1f}" x2="{l - 3:.1f}" y2="{t:.1f}"/>'
         f'<line x1="{l - 7:.1f}" y1="{y:.1f}" x2="{l - 3:.1f}" y2="{y:.1f}"/>'
         f'<line x1="{l:.1f}" y1="{y + 4:.1f}" x2="{r:.1f}" y2="{y + 4:.1f}"/><line x1="{l:.1f}" y1="{y + 2:.1f}" x2="{l:.1f}" y2="{y + 6:.1f}"/>'
         f'<line x1="{r:.1f}" y1="{y + 2:.1f}" x2="{r:.1f}" y2="{y + 6:.1f}"/></g>'
         f'<text x="{l - 6.5:.1f}" y="{(t + y) / 2:.1f}" transform="rotate(-90 {l - 6.5:.1f} {(t + y) / 2:.1f})" class="dim" text-anchor="middle">H — mm</text>'
         f'<text x="{(l + r) / 2:.1f}" y="{y + 8.4:.1f}" class="dim" text-anchor="middle">L — mm</text></svg>')
    return scontornata(code, cx_col, bottom_row, h) + q, l, r, t


def tavole(titolo, gruppi, h):
    """Tavole di gamma: espositori scontornati grandi appoggiati sulla griglia, con quote e dati."""
    pages = []
    tot = len(gruppi)
    base = 3.92
    for k, codes in enumerate(gruppi):
        n = len(codes)
        span = 6 / n
        body = el("h6", f"{titolo} — tav. {k + 1}/{tot}", .5, .45) + el("bignum sm right", f"{k + 1:02d}", 5.3, .45, 1.2)
        for i, c in enumerate(codes):
            c0 = .5 + i * span
            cx = c0 + span / 2
            hh = min(h * {2: 1, 3: .9, 4: .75}[n], g(0, base)[1] - g(0, .95)[1])
            html, l, r, t = quote(c, cx, base, hh, span * C - 16)
            body += html
            t_, tip, sett = PROGETTI[c]
            body += el("gcode", cid(c), c0 + .12, 4.12)
            body += el("capline", f"<b>{t_}</b>{tip}<br>{sett} · {TBD('[materiale]')}", c0 + .12, 4.36, span - .3)
        pages.append(body)
    return pages


def contatti():
    return (el("h2", "Contatti", .5, .45)
            + el("quote", "Il prossimo progetto parte da un brief.", .5, .85, 3.5)
            + el("small", "Raccontaci il prodotto, il punto vendita, le quantità e i tempi: ti rispondiamo con un concept e un prototipo.", .5, 1.5, 3)
            + el("bignum right", "03", 5.0, .45, 1.5)
            + el("h5", "Telefono", .5, 2.45) + el("contact", TBD("+39 000 000 0000"), .5, 2.62, 2.5)
            + el("h5", "Email", 3.5, 2.45) + el("contact", TBD("info@azienda.it"), 3.5, 2.62, 2.5)
            + el("h5", "Indirizzo", .5, 3.2) + el("contact", TBD("Via Esempio 1, 00000 Città (XX)"), .5, 3.37, 2.8)
            + el("h5", "Web", 3.5, 3.2) + el("contact", TBD("www.azienda.it"), 3.5, 3.37, 2.5)
            + el("bar", "", .5, 4.2, 6)
            + el("small", AZ + " — Portfolio Espositori 2027", .5, 4.47, 3))


CONTATTI = [("Telefono", "049 630390"), ("Email", "info@onprint.it"), ("Web", "www.onprint.it"),
            ("Indirizzo", "Viale dell’Industria 26, 35030 Rubano (PD)")]


def contatti_retro(x, w, bottom=MARG):
    """Blocco contatti del retro: titoletto, filetto e righe etichetta/valore, ancorato al margine basso."""
    righe = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in CONTATTI)
    return (f'<div class="rcontatti" style="left:{x:.1f}mm;bottom:{bottom:.1f}mm;width:{w:.1f}mm">'
            f'<div class="h5">Contatti</div><dl>{righe}</dl></div>')


def retro():
    return (el("cover-t sm", "Portfolio", .5, .45) + el("small", AZ + " — Espositori 2027", .5, .97, 3)
            + contatti_retro(g(.5, 0)[0], 110) + logo(MARG, H - MARG - 13.5, 36, right=True)
            + plus(1, 1) + plus(6, 1) + plus(6, 4))


def build():
    banco = [c for c in PROGETTI if c[0] == "B"]
    terra = [c for c in PROGETTI if c[0] == "T"]
    pages = [copertina()]
    spreads = [introduzione(), chi_siamo(),
               sezione("Espositori da banco", ["B14", "B13", "B03", "B04", "B08"], "01"),
               progetto("01", "B02", "B17", "B09", "B07"),
               progetto("02", "B11", "B12", "B14", "B16"),
               progetto("03", "B10", "B15", "B05", "B08", cut="B06"),
               *zip(*[iter(tavole("Gamma da banco", [["B01", "B05", "B17"], ["B02", "B08", "B03"], ["B13", "B06", "B16"], ["B04", "B15", "B19"],
                                                   ["B10", "B11", "B12", "B14"], ["B07", "B09", "B18", "B20"]], 128))] * 2),
               sezione("Espositori da terra", ["T01", "T02", "T05", "T03", "T06"], "02"),
               progetto_terra("04", "T07", "T08", "T04"),
               *zip(*[iter(tavole("Gamma da terra", [["T01", "T02"], ["T03", "T04"], ["T05", "T06"], ["T07", "T08"]], 128))] * 2)]
    for a, b in spreads:
        pages += [a, b]
    pages += [contatti(), retro()]
    tot = len(pages)
    html = []
    for i, body in enumerate(pages, start=1):
        side = "pr" if i % 2 else "pl"
        folio = "" if i in (1, tot) else f'<div class="folio">{i:02d}</div>'
        html.append(f'<section class="page {side}">{body}{folio}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio-grid.css">
</head><body><main class="book">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-grid.html").write_text(doc, encoding="utf-8")
    print("portfolio-grid.html:", tot, "pagine")


def photo_page(code):
    return photo(code, .5, .45, 6.5, 4.55) + plus(.5, .45) + plus(6.5, 4.55)


if __name__ == "__main__":
    build()
