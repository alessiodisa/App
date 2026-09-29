#!/usr/bin/env python3
"""
Portfolio Espositori v2 — A4 orizzontale (297 × 210 mm), impaginato sul modello
"Architecture Portfolio": pagine chiare, titoli bold, etichetta di sezione, disegni tecnici.
Copertina e retro restano quelli della versione su griglia.

    python3 portfolio_v2.py   ->  portfolio-v2.html
"""
import json
import portfolio_grid as PG
from portfolio_grid import PROGETTI, TBD, AZ, cid, ROOT

PROGETTI["T09"] = ("Stand a ripiani", "Colonne con header ad arco e fianco inclinato", "Nuove proposte")
PG.BB["T09"] = [137, 76, 877, 943]

el, photo, scontornata, g = PG.el, PG.photo, PG.scontornata, PG.g
W, H = PG.W, PG.H
BANCO, TERRA = "Espositori da banco", "Espositori da terra"


def img(src, col, row, h_mm, align="left"):
    x, y = g(col, row)
    side = f"left:{x:.1f}mm" if align == "left" else f"right:{W - x:.1f}mm"
    return f'<img class="drawing" src="{src}" style="{side};top:{y:.1f}mm;height:{h_mm:.1f}mm" alt="">'


def head(sezione):
    return el("brand", AZ, .5, .45) + el("pill", f"<span>{sezione}</span>", 4.5, .41, 2)


def t2(testo, col, row, w=3):
    return el("t2", testo, col, row, w)


def t3(testo, col, row, w=2):
    return el("t3", testo, col, row, w)


def txt(testo, col, row, w=2):
    return el("txt", testo, col, row, w)


def cap(code, col, row, w=2):
    t, tip, sett = PROGETTI[code]
    return el("cap2", f"<b>{cid(code)} — {t}</b>{tip}", col, row, w)


def meta(code, col, row, w=2):
    t, tip, sett = PROGETTI[code]
    rows = [("Tipologia", tip), ("Settore", sett), ("Materiale", TBD("[materiale]")), ("Cliente", TBD("[cliente]")),
            ("Anno", TBD("[anno]"))]
    return el("meta2", "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows), col, row, w)


def descr(code):
    return PG.DESCR.get(code) or PROGETTI[code][1] + ". " + TBD("[Esigenza del cliente, soluzione adottata, risultato.]")


# --------------------------------------------------------------------------
# pagine
# --------------------------------------------------------------------------
def introduzione():
    sx = (head("Introduzione")
          + t2("Introduzione", .5, .85, 4)
          + el("lead", "Ogni prodotto merita il suo spazio: struttura, materiale e grafica pensati insieme.", .5, 1.3, 3.6)
          + txt("Progettiamo e produciamo espositori da banco e da terra, pedane, totem e allestimenti per il punto vendita. "
                "Ogni progetto nasce in ufficio tecnico, viene prototipato, testato e poi prodotto internamente, "
                "dalla stampa alla fustellatura fino al confezionamento.", .5, 2.3, 2.7)
          + txt("Lavoriamo con brand della cosmesi, della farmacia, dell’ottica, della ferramenta e del beverage, "
                "con la stessa cura per la tiratura da cento pezzi e per quella da diecimila.", 3.5, 2.3, 2.7)
          + t3("Cosa facciamo", .5, 3.3)
          + el("bullets2", "".join(f"<li>{x}</li>" for x in [
              "Progettazione strutturale e grafica", "Prototipi in tempi brevi", "Stampa offset e digitale",
              "Fustellatura e incollaggio interni", "Cartone, forex, plexi, legno", "Spedizione piatta o premontata"]), .5, 3.55, 6))
    voce = lambda n, t, p, r: (el("idx-n", n, .5, r) + el("idx-t", t, 1.5, r + .05, 3.8)
                               + el("idx-p", f"{p:02d}", 5.8, r + .05, .7) + el("rule", "", .5, r + .55, 6))
    dx = (head("Indice") + t2("Indice", .5, .85, 3)
          + voce("01", "Chi siamo e metodo", 4, 1.45) + voce("02", "Espositori da banco", 6, 2.2)
          + voce("03", "Espositori da terra", 20, 2.95) + voce("04", "Contatti", 30, 3.7))
    return sx, dx


def chi_siamo():
    lettere = [("Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
               ("Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
               ("Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
               ("Logistica", "Spedizione piatta o premontata, in Italia e all’estero.")]
    li = "".join(f'<div class="li"><b>{chr(65 + i)}</b><div><h5>{t}</h5><p>{d}</p></div></div>' for i, (t, d) in enumerate(lettere))
    sx = (head("Chi siamo") + t2("Chi siamo", .5, .85, 3)
          + el("lead", "Dal disegno al bancale, sotto lo stesso tetto.", .5, 1.3, 2.8)
          + txt(f"Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. "
                "Un unico interlocutore significa tempi più rapidi, meno passaggi e un controllo costante sulla qualità.", .5, 2.0, 2.6)
          + el("letters2", li, 3.6, 1.3, 2.9)
          + el("stats2", f'<div><b>{TBD("35+")}</b>Anni di esperienza</div><div><b>{TBD("400")}</b>Progetti l’anno</div>'
                         f'<div><b>100%</b>Prodotto internamente</div>', .5, 3.85, 6))
    dx = (head("Metodo") + t2("Dal disegno<br>al prodotto", .5, .85, 2.4)
          + txt("Ogni espositore nasce da uno schizzo: proporzioni, ingombri e altezze dei ripiani vengono fissati "
                "prima ancora del disegno tecnico.", .5, 1.75, 2.2)
          + "".join(t3(f"{i + 1:02d} — {t}", .5, 2.45 + i * .5, 2.2) + txt(d, .5, 2.64 + i * .5, 2.2)
                    for i, (t, d) in enumerate([("Schizzo", "Proporzioni e misure principali."),
                                                ("Disegno tecnico", "Tracciati di fustella e render 3D."),
                                                ("Prototipo", "Campione fisico, test di carico e montaggio."),
                                                ("Produzione", "Stampa, fustellatura e confezionamento.")]))
          + img("img/schizzo-terra.png", 6.5, .75, 177, align="right")
          + el("cap2", "<b>Fig. 02 — Schizzo di studio</b>Espositore da terra a ripiani, misure di massima", 2.95, 4.25, 1.5))
    return sx, dx


def apertura(sezione, num, testo, a, b, disegno, dis_h, c, d, fig):
    sx = (head(sezione) + el("bignum2", num, .5, .8) + t2(sezione, .5, 1.55, 3)
          + txt(testo, .5, 2.05, 2.2)
          + photo(a, 2.7, .8, 4.55, 3.7) + photo(b, 4.65, .8, 6.5, 3.7)
          + cap(a, 2.7, 3.77, 1.8) + cap(b, 4.65, 3.77, 1.8))
    dx = (head("Disegni tecnici") + t2("Disegno tecnico", .5, .85, 3)
          + txt("Assonometria con le quote d’ingombro. Ogni progetto parte da un disegno come questo, "
                "poi sviluppato in fustella e verificato su prototipo.", .5, 1.3, 2)
          + img(disegno, 2.6, .8, dis_h)
          + el("cap2", f"<b>{fig}</b>Quote indicative, valori di esempio", .5, 4.2, 2)
          + photo(c, 5.0, .8, 6.5, 2.5) + photo(d, 5.0, 2.65, 6.5, 4.3)
          + cap(c, 5.0, 4.36, 1.5))
    return sx, dx


def progetto(main, s1, s2, s3, cut=None):
    t, tip, sett = PROGETTI[main]
    sx = (head("Progetto") + photo(main, .5, .8, 3.9, 4.55)
          + t2(t, 4.1, .8, 2.4) + el("code2", cid(main), 4.1, 1.3)
          + t3("Panoramica", 4.1, 1.7) + txt(descr(main), 4.1, 1.9, 2.4)
          + meta(main, 4.1, 2.75, 2.4))
    dx = head("Progetto")
    if cut:
        dx += (PG.scontornata(cut, 1.7, 3.6, 110, max_w=110) + cap(cut, .5, 3.7, 2.4)
               + photo(s1, 3.6, .8, 6.5, 3.3) + cap(s1, 3.6, 3.36, 2.9))
    else:
        dx += (photo(s1, .5, .8, 3.4, 3.3) + photo(s2, 3.6, .8, 6.5, 3.3)
               + cap(s1, .5, 3.36, 2.9) + cap(s2, 3.6, 3.36, 2.9))
    dx += (el("rule", "", .5, 3.85, 6)
           + t3("Struttura", .5, 3.98) + txt("Pieghe e incastri progettati per il montaggio senza colla.", .5, 4.17, 1.8)
           + t3("Grafica", 2.55, 3.98) + txt("Stampa a vivo su tutte le superfici visibili.", 2.55, 4.17, 1.8)
           + t3("Prodotto", 4.6, 3.98) + txt("Dimensionato su peso, formato e numero di facing.", 4.6, 4.17, 1.9))
    return sx, dx


def fustelle_mockup():
    sx = (head("Disegni tecnici") + t2("Sviluppo<br>in piano", .5, .85, 2)
          + txt("Fianco, schienale e ripiano dell’espositore da terra, stesi in piano come escono dalla fustellatrice: "
                "linee continue di taglio, tratteggi di cordonatura.", .5, 1.75, 1.6)
          + img("img/disegni/terra-fustelle.svg", 6.5, .75, 178, align="right"))
    dx = (head(TERRA) + photo("T09", .5, .8, 4.3, 4.55)
          + t2("Stand a ripiani", 4.5, .8, 2) + el("code2", "T.09", 4.5, 1.3)
          + txt("Colonne autoportanti con header ad arco e fianco inclinato: il prodotto si legge da tre lati. "
                + TBD("[Cliente, materiale e misure da confermare.]"), 4.5, 1.7, 2)
          + meta("T09", 4.5, 2.6, 2))
    return sx, dx


def progetto_terra(a, b, main):
    t, tip, sett = PROGETTI[main]
    sx = (head(TERRA) + photo(a, .5, .8, 2.45, 4.3) + photo(b, 2.55, .8, 4.5, 4.3)
          + cap(a, .5, 4.36, 1.9) + cap(b, 2.55, 4.36, 1.9)
          + t3("Panoramica", 4.7, .85) + txt("Colonne autoportanti con header: la comunicazione sale sopra il prodotto "
                                             "e si legge anche dal fondo della corsia.", 4.7, 1.05, 1.8))
    dx = (head("Progetto") + t2(t, .5, .85, 2.5) + el("code2", cid(main), .5, 1.35)
          + t3("Panoramica", .5, 1.75) + txt(descr(main), .5, 1.95, 2.2) + meta(main, .5, 2.8, 2.2)
          + scontornata(main, 4.6, 4.55, 170))
    return sx, dx


def tavole(titolo, gruppi, h):
    """Tavole di gamma: espositori scontornati appoggiati sulla stessa linea, con quote e dati."""
    pages, tot, base = [], len(gruppi), 3.85
    for k, codes in enumerate(gruppi):
        n = len(codes)
        span = 6 / n
        body = head(titolo) + t2(titolo, .5, .8, 3) + el("code2", f"Tavola {k + 1} / {tot}", 4.5, .85, 2)
        body = body.replace('class="code2"', 'class="code2 right"')
        for i, c in enumerate(codes):
            c0 = .5 + i * span
            hh = min(h * {2: 1, 3: .9, 4: .75}[n], g(0, base)[1] - g(0, 1.35)[1])
            html, l, r, t = PG.quote(c, c0 + span / 2, base, hh, span * PG.C - 16)
            tt, tip, sett = PROGETTI[c]
            body += html + el("gcode", cid(c), c0 + .12, 4.05)
            body += el("capline", f"<b>{tt}</b>{tip} · {sett} · {TBD('[materiale]')}", c0 + .12, 4.3, span - .3)
        pages.append(body)
    return pages


def contatti():
    return (head("Contatti") + t2("Contatti", .5, .85, 3)
            + el("lead", "Il prossimo progetto parte da un brief.", .5, 1.3, 3.5)
            + txt("Raccontaci il prodotto, il punto vendita, le quantità e i tempi: ti rispondiamo con un concept e un prototipo.", .5, 1.8, 2.6)
            + "".join(t3(k, c, r) + el("contact2", TBD(v), c, r + .2, 2.6)
                      for k, v, c, r in [("Telefono", "+39 000 000 0000", .5, 2.6), ("Email", "info@azienda.it", 3.5, 2.6),
                                         ("Indirizzo", "Via Esempio 1, 00000 Città (XX)", .5, 3.3), ("Web", "www.azienda.it", 3.5, 3.3)])
            + el("rule", "", .5, 4.3, 6) + el("brand", AZ + " — Portfolio Espositori 2026", .5, 4.42, 4))


# --------------------------------------------------------------------------
def build():
    pages = [("grid", PG.copertina())]
    spreads = [introduzione(), chi_siamo(),
               apertura(BANCO, "02", "Il punto più vicino alla scelta: strutture compatte che portano il prodotto "
                        "all’altezza dello sguardo, accanto alla cassa.", "B14", "B13",
                        "img/disegni/banco-iso.svg", 150, "B04", "B08", "Fig. 03 — Espositore da banco a gradini"),
               progetto("B02", "B17", "B09", "B07"),
               progetto("B11", "B12", "B16", None),
               progetto("B10", "B05", None, None, cut="B06")]
    for a, b in spreads:
        pages += [("", a), ("", b)]
    pages += [("", p) for p in tavole("Gamma da banco", [["B01", "B05", "B17"], ["B02", "B08", "B03"], ["B13", "B06", "B16"],
                                                         ["B04", "B15", "B19"], ["B10", "B11", "B12", "B14"], ["B07", "B09", "B18", "B20"]], 128)]
    for a, b in [apertura(TERRA, "03", "Strutture autoportanti a più ripiani, pensate per reggere il carico e farsi vedere "
                          "da lontano. Spedite piatte, montate in pochi minuti.", "T01", "T02",
                          "img/disegni/terra-iso.svg", 172, "T03", "T06", "Fig. 04 — Espositore da terra a ripiani"),
                 fustelle_mockup(), progetto_terra("T07", "T08", "T04")]:
        pages += [("", a), ("", b)]
    pages += [("", p) for p in tavole("Gamma da terra", [["T01", "T02"], ["T03", "T04"], ["T05", "T06"], ["T07", "T08"]], 128)]
    pages += [("", contatti()), ("grid", PG.retro())]
    tot = len(pages)
    html = []
    for i, (cls, body) in enumerate(pages, start=1):
        side = "pr" if i % 2 else "pl"
        folio = "" if i in (1, tot) else f'<div class="folio">{i:02d}</div>'
        html.append(f'<section class="page {side} {cls}">{body}{folio}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio-grid.css">
<link rel="stylesheet" href="portfolio-v2.css">
</head><body><main class="book">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-v2.html").write_text(doc, encoding="utf-8")
    print("portfolio-v2.html:", tot, "pagine")


if __name__ == "__main__":
    build()
