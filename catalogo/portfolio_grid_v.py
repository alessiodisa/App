#!/usr/bin/env python3
"""
Portfolio Espositori — versione A4 verticale (210 × 297 mm) su griglia a vista 5 × 7.
Riusa contenuti e componenti di portfolio_grid.py.

    python3 portfolio_grid_v.py   ->  portfolio-grid-v.html
"""
import portfolio_grid as PG
from portfolio_grid import PROGETTI, TBD, AZ, cid, cap, testo, lista_lettere, ROOT

W, H = 210, 297
PG.W, PG.H, PG.C, PG.R = W, H, W / 5, H / 7        # i componenti condivisi leggono queste misure
C, R = PG.C, PG.R
MARG = 15                                           # margine uguale su tutti i lati (mm)
_g_griglia = PG.g


def _g_area(col, row):
    """Coordinate di impaginazione -> mm dentro l'area utile 15 mm (col .35–4.65, riga .6–6.6)."""
    return MARG + (col - .35) * (W - 2 * MARG) / 4.3, MARG + (row - .6) * (H - 2 * MARG) / 6


PG.g = _g_area
el, photo, scontornata, quote, g = PG.el, PG.photo, PG.scontornata, PG.quote, PG.g


def plus(col, row):
    """Crocetta sempre su un incrocio reale della griglia di sfondo."""
    x, y = col * C, row * R
    return f'<div class="plus" style="left:{x - 2:.2f}mm;top:{y - 2:.2f}mm"></div>'


def meta(code):
    t, tip, sett = PROGETTI[code]
    return (f'<h5>Tipologia: {tip}</h5><h5>Settore: {sett}</h5><h5>Materiale: {TBD("[materiale]")}</h5>'
            f'<h5>Cliente: {TBD("[cliente]")} — {TBD("[anno]")}</h5>')


# --------------------------------------------------------------------------
# pagine
# --------------------------------------------------------------------------
def copertina():
    x, y = g(4.65, .95)
    return (el("small", "Vol. 01 — 2027", .35, .6)
            + PG.logo(W - g(4.65, 0)[0], g(4.65, .6)[1], 36, right=True)
            + f'<img class="drawing" src="img/esploso-terra.svg" style="right:{W - x:.1f}mm;top:{y:.1f}mm;height:185mm" alt="">'
            + el("small", "Cartotecnica ed espositori per il punto vendita: progettazione, prototipazione e produzione. "
                 "Cartone, cartoncino e materiali durevoli.", .35, 1.3, 1.9)
            + el("capline", "<b>Fig. 01</b>Espositore da terra — vista esplosa", .35, 4.2, 1.9)
            + el("light-t xl", "Portfolio", .35, 4.85) + el("cover-t", "Espositori", .35, 5.15)
            + plus(1, 1) + plus(1, 4) + plus(4, 6))


def introduzione():
    return (el("h2", "Introduzione", .35, .6)
            + el("quote", "Ogni prodotto merita il suo spazio: struttura, materiale e grafica pensati insieme.", .35, 1.1, 3.6)
            + el("small cols", "Progettiamo e produciamo espositori da banco e da terra, pedane, totem e allestimenti per il punto vendita. "
                 "Ogni progetto nasce in ufficio tecnico, viene prototipato, testato e poi prodotto internamente, "
                 "dalla stampa alla fustellatura fino al confezionamento.", .35, 2.0, 4.3)
            + el("h6", "Cosa facciamo", .35, 3.4)
            + el("bullets big", "".join(f"<li>{x}</li>" for x in [
                "Progettazione strutturale e grafica", "Prototipi in tempi brevi", "Stampa offset e digitale",
                "Fustellatura e incollaggio interni", "Cartone, forex, plexi, legno", "Spedizione piatta o premontata"]), .35, 3.65, 2.6)
            + el("bar", "", .35, 6.2, 4.3)
            + el("small", "Un unico interlocutore, dal primo disegno al bancale pronto a partire.", .35, 6.52, 2.6)
            + plus(4, 1) + plus(4, 3))


def indice():
    voce = lambda n, t, p, r: (el("bignum", n, .35, r) + el("index-t", t, 1.75, r + .22, 2.3)
                               + el("index-p", f"{p:02d}", 4.1, r + .22, .55) + el("rule", "", .35, r + .78, 4.3))
    return (el("h2", "Indice", .35, .6)
            + voce("01", "Espositori da banco", 6, 1.5)
            + voce("02", "Espositori da terra", 20, 2.9)
            + voce("03", "Contatti", 28, 4.3)
            + el("small", "Una selezione di progetti realizzati per brand della cosmesi, della farmacia, dell'ottica, della ferramenta e del beverage.", .35, 6.47, 3))


def chi_siamo():
    return (el("h2", "Chi siamo", .35, .6)
            + el("quote", "Dal disegno al bancale, sotto lo stesso tetto.", .35, 1.05, 3.4)
            + el("small", f"Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. "
                 "Un unico interlocutore significa tempi più rapidi, meno passaggi e un controllo costante sulla qualità.", .35, 1.85, 2.6)
            + el("letters big", lista_lettere([
                ("Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
                ("Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
                ("Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
                ("Logistica", "Spedizione piatta o premontata, in Italia e all'estero.")]), .35, 2.8, 3.2)
            + el("bignum", "01", 3.55, 6.1)
            + el("stats", f'<div><b>{TBD("35+")}</b>Anni</div><div><b>{TBD("400")}</b>Progetti l’anno</div><div><b>100%</b>Interno</div>', .35, 6.25, 3))


def citazione():
    return (el("quote", "Un espositore funziona quando si monta in un minuto, regge il carico e fa vedere il prodotto meglio dello scaffale.", .35, .6, 3.4)
            + el("small", "Ogni progetto parte da una domanda: dove verrà visto, da chi, per quanto tempo.", .35, 1.75, 3)
            + photo("B06", .35, 2.3, 4.65, 6.6))


def sezione(titolo, codes, num):
    a, b, c, d, e = codes
    sx = (el("h2", titolo, .35, .6)
          + photo(a, .35, 1.1, 2.4, 3.8) + photo(b, 2.6, 1.1, 4.65, 3.8)
          + el("capline", cap(a), .35, 3.86, 2) + el("capline", cap(b), 2.6, 3.86, 2)
          + el("h6", "Panoramica", .35, 4.5)
          + el("small", "Ogni progetto parte dal prodotto e dal punto vendita: dimensioni, peso, numero di facing, tempo di permanenza. "
               "Da lì scegliamo struttura e materiale, prototipiamo e produciamo.", .35, 4.7, 2.05)
          + el("small", "Nelle pagine che seguono, una selezione di progetti realizzati.", 2.6, 4.7, 2)
          + el("bignum", num, 2.6, 6.15))
    dx = (photo(c, .35, .6, 4.65, 4.0)
          + el("capline", cap(c), .35, 4.06, 4)
          + photo(d, .35, 4.45, 2.4, 6.4) + photo(e, 2.6, 4.45, 4.65, 6.4)
          + el("capline", cap(d), .35, 6.46, 2) + el("capline", cap(e), 2.6, 6.46, 2))
    return [sx, dx]


def progetto(num, main, small, sq, tall, cut=None):
    t, tip, sett = PROGETTI[main]
    sx = (photo(main, .35, .6, 4.65, 3.9)
          + el("bignum", num, .35, 4.05)
          + el("h6", "Il progetto", .35, 5.0)
          + el("small", testo(main), .35, 5.2, 2.05)
          + el("small", "Struttura, materiali e finiture definiti con il cliente e verificati su prototipo prima della produzione.", .35, 5.85, 2.05)
          + photo(small, 2.6, 4.25, 4.65, 6.4)
          + el("capline", cap(small), 2.6, 6.46, 2))
    dx = (el("h2", t, .35, .6, 2) + el("code", cid(main), .35, 1.05)
          + el("h6", "Panoramica", .35, 1.45)
          + el("small", f"{tip}. " + TBD("[Esigenza del cliente e soluzione adottata.]"), .35, 1.65, 2)
          + el("meta", meta(main), .35, 2.4, 2)
          + photo(tall, 2.45, .6, 4.65, 3.6) + el("capline", cap(tall), 2.45, 3.66, 2.2))
    if cut:
        dx += (scontornata(cut, 1.35, 6.4, 95, max_w=88) + el("capline", cap(cut), .35, 6.46, 2)
               + photo(sq, 2.45, 4.1, 4.65, 6.4) + el("capline", cap(sq), 2.45, 6.46, 2.2))
    else:
        dx += (el("quote sm", "Il prodotto al centro, la struttura al suo servizio.", .35, 4.4, 1.9)
               + photo(sq, 2.45, 4.1, 4.65, 6.4) + el("capline", cap(sq), 2.45, 6.46, 2.2))
    return [sx, dx]


def progetto_terra(num, a, b, main):
    t, tip, sett = PROGETTI[main]
    sx = (photo(a, .35, .6, 2.45, 5.15) + photo(b, 2.55, .6, 4.65, 5.15)
          + el("capline", cap(a), .35, 5.21, 2) + el("capline", cap(b), 2.55, 5.21, 2)
          + el("bignum", num, .35, 6.15)
          + el("h6", "Panoramica", 2.6, 5.9)
          + el("small", "Colonne autoportanti con header: la comunicazione sale sopra il prodotto e si legge anche dal fondo della corsia.", 2.6, 6.1, 2))
    dx = (el("h2", t, .35, .6, 2) + el("code", cid(main), .35, 1.05)
          + el("h6", "Panoramica", .35, 1.45) + el("small", testo(main), .35, 1.65, 1.9)
          + el("meta", meta(main), .35, 2.4, 1.9)
          + el("quote sm", "Leggibile da lontano, stabile a pieno carico.", .35, 3.5, 1.8)
          + scontornata(main, 3.4, 6.5, 225, max_w=85))
    return [sx, dx]


def tavole_v(titolo, gruppi):
    """Gamma: espositori scontornati con quote. 4 per pagina (2+2) o 3 (1+2) o 2 affiancati."""
    pages = []
    tot = len(gruppi)
    for k, codes in enumerate(gruppi):
        body = el("h6", f"{titolo} — tav. {k + 1}/{tot}", .35, .6) + el("bignum sm right", f"{k + 1:02d}", 3.4, .6, 1.25)
        n = len(codes)
        if codes[0][0] == "T":
            righe, basi, hs = [codes], [6.08], [205]
        else:
            righe = [codes[:2], codes[2:]] if n == 4 else [codes[:1], codes[1:]]
            basi, hs = [3.3, 6.08], [80 if n == 4 else 90, 78]
        for riga, base, h in zip(righe, basi, hs):
            span = 4.3 / len(riga)
            for i, c in enumerate(riga):
                c0 = .35 + i * span
                html, l, r, t = quote(c, c0 + span / 2, base, h, min(span * C - 20, 120))
                body += html
                t_, tip, sett = PROGETTI[c]
                body += el("gcode", cid(c), c0 + .1, base + .1)
                body += el("capline", f"<b>{t_}</b>{tip}<br>{sett} · {TBD('[materiale]')}", c0 + .1, base + .32, span - .3)
        pages.append(body)
    return pages


def contatti():
    return (el("h2", "Contatti", .35, .6)
            + el("quote", "Il prossimo progetto parte da un brief.", .35, 1.05, 3.6)
            + el("small", "Raccontaci il prodotto, il punto vendita, le quantità e i tempi: ti rispondiamo con un concept e un prototipo.", .35, 1.8, 2.8)
            + el("bignum", "03", .35, 2.6)
            + el("h5", "Telefono", .35, 3.9) + el("contact", TBD("+39 000 000 0000"), .35, 4.05, 2)
            + el("h5", "Email", 2.6, 3.9) + el("contact", TBD("info@azienda.it"), 2.6, 4.05, 2)
            + el("h5", "Indirizzo", .35, 4.7) + el("contact", TBD("Via Esempio 1, 00000 Città (XX)"), .35, 4.85, 2.1)
            + el("h5", "Web", 2.6, 4.7) + el("contact", TBD("www.azienda.it"), 2.6, 4.85, 2)
            + el("bar", "", .35, 6.2, 4.3)
            + el("small", AZ + " — Portfolio Espositori 2027", .35, 6.52, 3)
            + plus(4, 1) + plus(4, 2))


def retro():
    return (el("cover-t sm", "Portfolio", .35, .6) + el("small", AZ + " — Espositori 2027", .35, 1.27, 3)
            + PG.contatti_retro(g(.35, 0)[0], 110) + PG.logo(MARG, H - MARG - 13.5, 36, right=True)
            + plus(1, 1) + plus(4, 1) + plus(4, 6))


def build():
    pages = [copertina(), introduzione(), indice(), chi_siamo(), citazione()]
    pages += sezione("Espositori da banco", ["B14", "B13", "B03", "B04", "B08"], "01")
    pages += progetto("01", "B02", "B17", "B09", "B07")
    pages += progetto("02", "B11", "B12", "B14", "B16")
    pages += progetto("03", "B10", "B15", "B05", "B08", cut="B06")
    pages += tavole_v("Gamma da banco", [["B01", "B05", "B17", "B03"], ["B02", "B08", "B13"], ["B06", "B16", "B14"],
                                         ["B04", "B15", "B19"], ["B10", "B11", "B12"], ["B07", "B09", "B18", "B20"]])
    pages += sezione("Espositori da terra", ["T01", "T02", "T05", "T03", "T06"], "02")
    pages += progetto_terra("04", "T07", "T08", "T04")
    pages += tavole_v("Gamma da terra", [["T01", "T02"], ["T03", "T04"], ["T05", "T06"], ["T07", "T08"]])
    pages += [contatti(), retro()]
    tot = len(pages)
    html = []
    for i, body in enumerate(pages, start=1):
        side = "pr" if i % 2 else "pl"
        folio = "" if i in (1, tot) else f'<div class="folio">{i:02d}</div>'
        html.append(f'<section class="page {side}">{body}{folio}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori — verticale</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio-grid.css">
<link rel="stylesheet" href="portfolio-grid-v.css">
</head><body><main class="book">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-grid-v.html").write_text(doc, encoding="utf-8")
    print("portfolio-grid-v.html:", tot, "pagine")


if __name__ == "__main__":
    build()
