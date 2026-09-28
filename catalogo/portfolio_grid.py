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
AZ = '<span class="tbd">[NOME AZIENDA]</span>'


def TBD(s):
    return f'<span class="tbd">{s}</span>'


def bx(x, y, w=None, h=None):
    s = f"left:{x:.2f}mm;top:{y:.2f}mm"
    if w is not None:
        s += f";width:{w:.2f}mm"
    if h is not None:
        s += f";height:{h:.2f}mm"
    return s


def g(col, row):
    """Coordinate in mm di un incrocio di griglia (colonne e righe anche frazionarie)."""
    return col * C, row * R


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
    if code in CB and zoom == 1.0 and not .8 <= fw / fh <= 1.25:
        return studio(code, x0, y0, fw, fh)
    s = max(fw, fh) * zoom
    a1, b1, a2, b2 = BB[code]
    cx = (a1 + (a2 - a1) * fx) / 1024 * s
    cy = (b1 + (b2 - b1) * fy) / 1024 * s
    ix = min(max(x0 + fw / 2 - cx, x0 + fw - s), x0)
    iy = min(max(y0 + fh / 2 - cy, y0 + fh - s), y0)
    return (f'<div class="frame" style="{bx(x0, y0, fw, fh)}">'
            f'<img src="img/sq/{code}.jpg" style="{bx(ix - x0, iy - y0, s, s)}" alt=""></div>')


def studio(code, x0, y0, fw, fh, fill=.82):
    """Riquadro con fondo da studio e l'espositore scontornato intero, appoggiato in basso."""
    a1, b1, a2, b2, n = CB[code]
    ow, oh = (a2 - a1) / n, (b2 - b1) / n
    s = min(fw * fill / ow, fh * fill / oh)
    ix = fw / 2 - (a1 + a2) / 2 / n * s
    iy = fh - (fh - oh * s) * .42 - b2 / n * s
    return (f'<div class="frame studio" style="{bx(x0, y0, fw, fh)}">'
            f'<img src="img/scontornate/{code}.png" style="{bx(ix, iy, s, s)}" alt=""></div>')


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
    w = f";width:{w_cols * C:.2f}mm" if w_cols else ""
    return f'<div class="{cls}" style="{bx(x, y)}{w}">{html}</div>'


def plus(col, row):
    x, y = g(col, row)
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
def copertina():
    return (el("small", "Vol. 01 — 2026", .35, .55)
            + el("small right", "Progettato e prodotto da", 4.6, .55, 2.05) + el("h3 right", AZ, 4.6, .8, 2.05)
            + el("light-t", "Espositori", .35, 1.6) + el("cover-t", "Portfolio", .3, 1.95)
            + el("small", "Cartotecnica ed espositori per il punto vendita: progettazione, prototipazione e produzione. "
                 "Cartone, cartoncino e materiali durevoli.", 4.6, 1.55, 2.05)
            + el("h5", "Telefono", .35, 3.35) + el("small", TBD("+39 000 000 0000"), .35, 3.5)
            + el("h5", "Email", 1.6, 3.35) + el("small", TBD("info@azienda.it"), 1.6, 3.5)
            + el("h5", "Indirizzo", .35, 3.95) + el("small", TBD("Via Esempio 1, 00000 Città (XX)"), .35, 4.1, 2.5)
            + photo("B01", 3.2, 3.1, 6.6, 4.6)
            + plus(1, 1) + plus(6, 1) + plus(1, 4) + plus(6, 4))


def introduzione():
    sx = (el("h2", "Introduzione", .5, .95)
          + el("h6", "Ogni prodotto merita il suo spazio: struttura, materiale e grafica pensati insieme.", .5, 1.3, 2.3)
          + photo("B03", .5, 2.0, 2.2, 3.7, zoom=1.35)
          + el("small cols", "Progettiamo e produciamo espositori da banco e da terra, pedane, totem e allestimenti per il punto vendita. "
               "Ogni progetto nasce in ufficio tecnico, viene prototipato, testato e poi prodotto internamente, "
               "dalla stampa alla fustellatura fino al confezionamento.", 3.35, .95, 3.2)
          + el("bullets", "".join(f"<li>{x}</li>" for x in [
              "Progettazione strutturale e grafica", "Prototipi in tempi brevi", "Stampa offset e digitale",
              "Fustellatura e incollaggio interni", "Cartone, forex, plexi, legno", "Spedizione piatta o premontata"]), 3.35, 2.15, 2.6)
          + el("bar", "", 3.35, 3.55, 2.6))
    idx = lambda cs: "".join(f"<li>{PROGETTI[c][0]}<span>{p:02d}</span></li>" for c, p in cs)
    dx = (el("h2", "Indice", .5, .95)
          + el("h5", "Espositori da banco", .5, 1.4) + el("index", idx([("B01", 6), ("B02", 8), ("B11", 10), ("B10", 12)]) + "<li>Gamma completa<span>14</span></li>", .5, 1.55, 2.4)
          + el("h5", "Espositori da terra", .5, 2.75) + el("index", idx([("T05", 16), ("T04", 18)]) + "<li>Gamma completa<span>20</span></li>", .5, 2.9, 2.4)
          + el("h5", "Contatti", .5, 3.7) + el("index", "<li>Parliamone<span>22</span></li>", .5, 3.85, 2.4)
          + photo("T05", 4.2, .45, 6.55, 4.55, fy=.45))
    return sx, dx


def chi_siamo():
    sx = (el("h2", "Chi siamo", .5, 1.55)
          + el("small", f"Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. "
               "Un unico interlocutore, dal disegno al bancale.", .5, 1.9, 2.4)
          + photo("B09", 3.6, .45, 5.4, 2.05)
          + photo("B16", .5, 2.5, 1.6, 4.55)
          + el("letters", lista_lettere([
              ("Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
              ("Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
              ("Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni.")]), 1.85, 2.5, 2.6)
          + el("bignum", "01", 4.75, 3.35))
    dx = (el("quote", "Un espositore funziona quando si monta in un minuto, regge il carico e fa vedere il prodotto meglio dello scaffale.", .5, .95, 1.6)
          + el("small", "Ogni progetto parte da una domanda: dove verrà visto, da chi, per quanto tempo.", .5, 2.6, 1.6)
          + photo("B06", 2.4, .45, 6.55, 4.1))
    return sx, dx


def sezione(titolo, codes):
    a, b, c, d, e = codes
    sx = (el("h2", titolo, .5, .95)
          + photo(a, .5, 1.6, 1.95, 3.7) + photo(b, 2.05, 1.6, 3.5, 3.7)
          + el("h6", "Panoramica", 3.9, 2.35)
          + el("small", "Ogni progetto parte dal prodotto e dal punto vendita: dimensioni, peso, numero di facing, tempo di permanenza. "
               "Da lì scegliamo struttura e materiale, prototipiamo e produciamo.", 3.9, 2.55, 2.1)
          + el("small", "Nelle pagine che seguono, una selezione di progetti realizzati.", 3.9, 3.2, 2.1)
          + el("capline", cap(a), .5, 3.78, 1.45) + el("capline", cap(b), 2.05, 3.78, 1.45))
    dx = (photo(c, .5, .45, 3.6, 4.1)
          + photo(d, 3.85, .45, 5.95, 2.25) + photo(e, 3.85, 2.35, 5.95, 4.1)
          + el("capline", cap(c), .5, 4.18, 3) + el("capline", f"{cid(d)} · {cid(e)} — {PROGETTI[d][0]}, {PROGETTI[e][0]}", 3.85, 4.18, 2.1))
    return sx, dx


def progetto(num, main, small, sq, tall, cut=None):
    t, tip, sett = PROGETTI[main]
    sx = (photo(main, .5, .75, 3.6, 2.45)
          + el("bignum", num, 3.8, 1.2)
          + photo(small, 3.85, 2.55, 4.85, 3.55)
          + el("capline", cap(small), 3.85, 3.6, 1.6)
          + el("h6", "Il progetto", .5, 2.75)
          + el("small", testo(main), .5, 2.95, 2.9)
          + el("small", "Struttura, materiali e finiture sono stati definiti insieme al cliente e verificati su prototipo prima della produzione.", .5, 3.45, 2.9))
    meta = (f'<h5>Tipologia: {tip}</h5><h5>Settore: {sett}</h5><h5>Materiale: {TBD("[materiale]")}</h5>'
            f'<h5>Cliente: {TBD("[cliente]")} — {TBD("[anno]")}</h5>')
    dx = (el("h2", t, .5, .95, 3.3) + el("code", cid(main), .5, 1.35)
          + el("h6", "Panoramica", .5, 1.75)
          + el("small", f"{tip}. " + TBD("[Esigenza del cliente e soluzione adottata.]"), .5, 1.95, 1.9)
          + el("meta", meta, .5, 2.7, 1.9))
    if cut:
        dx += scontornata(cut, 3.3, 3.95, 118) + el("capline", cap(cut), 2.55, 4.05, 1.6)
    else:
        dx += photo(sq, 2.55, 1.6, 3.95, 3.0) + el("capline", cap(sq), 2.55, 3.05, 1.4)
    dx += photo(tall, 4.2, 1.6, 5.05, 3.45) + el("capline", cap(tall), 4.2, 3.5, 1.2)
    dx += el("quote sm", "Il prodotto al centro, la struttura al suo servizio.", 5.3, 1.6, 1.3)
    return sx, dx


def progetto_terra(num, a, b, cut):
    sx = (photo(a, .5, .75, 1.95, 3.7) + photo(b, 2.05, .75, 3.5, 3.7)
          + el("bignum", num, 3.8, .75)
          + el("h6", "Panoramica", 3.85, 1.95)
          + el("small", "Colonne autoportanti con header: la comunicazione sale sopra il prodotto e si legge anche dal fondo della corsia.", 3.85, 2.15, 2.2)
          + el("capline", cap(a), .5, 3.78, 1.45) + el("capline", cap(b), 2.05, 3.78, 1.45))
    t, tip, sett = PROGETTI[cut]
    meta = (f'<h5>Tipologia: {tip}</h5><h5>Settore: {sett}</h5><h5>Materiale: {TBD("[materiale]")}</h5>'
            f'<h5>Cliente: {TBD("[cliente]")} — {TBD("[anno]")}</h5>')
    dx = (el("h2", t, .5, .95, 3) + el("code", cid(cut), .5, 1.35)
          + el("h6", "Panoramica", .5, 1.75) + el("small", testo(cut), .5, 1.95, 1.9) + el("meta", meta, .5, 2.7, 1.9)
          + scontornata(cut, 4.3, 4.3, 170))
    return sx, dx


def gamma(titolo, codes, per_riga, righe, h, sub):
    """Tavola di gamma: espositori scontornati appoggiati sulla griglia, con codice e nome."""
    pages = []
    per_pag = per_riga * righe
    for p in range(0, len(codes), per_pag):
        body = el("h2", titolo if p == 0 else "", .5, .6) + el("small", sub if p == 0 else "", 3.4, .62, 3)
        step = 6 / per_riga
        for i, c in enumerate(codes[p:p + per_pag]):
            col = .5 + step * (i % per_riga) + step / 2
            row = (4.35 if righe == 1 else [2.55, 4.3][i // per_riga])
            body += scontornata(c, col, row - .1, h, max_w=step * C - 6)
            body += el("capline center", f"<b>{cid(c)}</b>{PROGETTI[c][0]}", col - step / 2, row, step)
        pages.append(body)
    return pages


def contatti():
    sx = (el("h2", "Contatti", .5, .95)
          + el("quote", "Il prossimo progetto parte da un brief.", .5, 1.4, 2.5)
          + el("h5", "Telefono", .5, 2.6) + el("small", TBD("+39 000 000 0000"), .5, 2.75)
          + el("h5", "Email", 2, 2.6) + el("small", TBD("info@azienda.it"), 2, 2.75)
          + el("h5", "Indirizzo", .5, 3.2) + el("small", TBD("Via Esempio 1, 00000 Città (XX)"), .5, 3.35, 2.5)
          + el("h5", "Web", 2, 3.2) + el("small", TBD("www.azienda.it"), 2, 3.35)
          + photo("B17", 3.85, .45, 6.55, 4.55))
    return sx


def retro():
    return (el("cover-t sm", "Portfolio", .35, 3.6) + el("small", AZ + " — Espositori 2026", .4, 4.2, 3)
            + plus(1, 1) + plus(6, 1) + plus(1, 4) + plus(6, 4))


def build():
    banco = [c for c in PROGETTI if c[0] == "B"]
    terra = [c for c in PROGETTI if c[0] == "T"]
    pages = [copertina()]
    spreads = [introduzione(), chi_siamo(),
               sezione("Espositori da banco", ["B01", "B17", "B03", "B04", "B08"]),
               progetto("01", "B02", "B13", "B09", "B07"),
               progetto("02", "B11", "B12", "B14", "B16"),
               progetto("03", "B10", "B15", "B05", "B05", cut="B06"),
               tuple(gamma("Gamma da banco", banco, 5, 2, 44, "Tutti i progetti della sezione, in scala relativa sulla griglia.")),
               sezione("Espositori da terra", ["T01", "T02", "T05", "T03", "T06"]),
               progetto_terra("04", "T07", "T08", "T04"),
               tuple(gamma("Gamma da terra", terra, 4, 1, 128, "Colonne, totem e podi: altezze e ingombri a confronto."))]
    for a, b in spreads:
        pages += [a, b]
    pages += [contatti(), photo_page("B04"), retro()]
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
