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
PG.BB["T09"] = [145, 83, 881, 883]
PG.BB["T10"] = [367, 16, 670, 1004]
PG.BB["T11"] = [377, 32, 656, 992]
PG.BB["T12"] = [379, 31, 678, 998]
PG.BB["B01"] = [216, 169, 800, 841]          # centrato sul solo espositore, senza oggetti di scena
PG.BB["T14"] = [0, 0, 1024, 1024]
PG.BB["T15"] = [0, 0, 1024, 1024]
PG.BB["T13"] = [358, 6, 701, 987]
PG.BB["B19"] = [270, 49, 875, 915]
PG.BB["B20"] = [195, 81, 950, 995]
PG.BB["B21"] = [201, 169, 875, 852]
PG.BB["B22"] = [243, 90, 858, 940]
PG.BB["B23"] = [302, 184, 801, 832]

el, photo, scontornata, g = PG.el, PG.photo, PG.scontornata, PG.g
W, H = PG.W, PG.H
BANCO, TERRA = "Espositori da banco", "Espositori da terra"
ESCLUSI = {"B14", "B18"}           # tolti su richiesta


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
          + t2("Introduzione", .5, .65, 4)
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
    dx = (head("Indice") + t2("Indice", .5, .65, 3)
          + voce("01", "Chi siamo e metodo", 4, 1.45) + voce("02", "Espositori da banco", 6, 2.2)
          + voce("03", "Espositori da terra", 18, 2.95) + voce("04", "Contatti", 26, 3.7))
    return sx, dx


def chi_siamo():
    lettere = [("Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
               ("Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
               ("Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
               ("Logistica", "Spedizione piatta o premontata, in Italia e all’estero.")]
    li = "".join(f'<div class="li"><b>{chr(65 + i)}</b><div><h5>{t}</h5><p>{d}</p></div></div>' for i, (t, d) in enumerate(lettere))
    sx = (head("Chi siamo") + t2("Chi siamo", .5, .65, 3)
          + el("lead", "Dal disegno al bancale, sotto lo stesso tetto.", .5, 1.3, 2.8)
          + txt(f"Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli. "
                "Un unico interlocutore significa tempi più rapidi, meno passaggi e un controllo costante sulla qualità.", .5, 2.0, 2.6)
          + el("letters2", li, 3.6, 1.3, 2.9)
          + el("stats2", f'<div><b>{TBD("35+")}</b>Anni di esperienza</div><div><b>{TBD("400")}</b>Progetti l’anno</div>'
                         f'<div><b>100%</b>Prodotto internamente</div>', .5, 3.85, 6))
    dx = (head("Metodo") + t2("Dal disegno<br>al prodotto", .5, .65, 2.4)
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


# --------------------------------------------------------------------------
# griglia modulare: 5 × 3 celle quadrate per pagina, sotto la testata
# --------------------------------------------------------------------------
MG, GUT = 15, 4.8
CELL = (W - 2 * MG - 4 * GUT) / 5                  # ≈ 49,6 mm
Y0 = H - MG - (3 * CELL + 2 * GUT)                # la griglia finisce sul margine inferiore


def cell(c, r, cw=1, rh=1):
    return (MG + c * (CELL + GUT), Y0 + r * (CELL + GUT), cw * CELL + (cw - 1) * GUT, rh * CELL + (rh - 1) * GUT)


def _to_grid(x, y):
    return (x - MG) / ((W - 2 * MG) / 6) + .5, (y - MG) / ((H - 2 * MG) / 4.1) + .45


def foto(code, c, r, cw=1, rh=1):
    """Foto con sfondo (quella fornita) che riempie esattamente cw × rh celle, con etichetta del codice."""
    x, y, w, h = cell(c, r, cw, rh)
    c0, r0 = _to_grid(x, y)
    c1, r1 = _to_grid(x + w, y + h)
    return photo(code, c0, r0, c1, r1) + f'<div class="tag2" style="left:{x + 2.2:.2f}mm;top:{y + 2.2:.2f}mm">{cid(code)}</div>'


def box(cls, html, c, r, cw=1, rh=1, pad_top=0):
    x, y, w, h = cell(c, r, cw, rh)
    return f'<div class="{cls}" style="left:{x:.2f}mm;top:{y + pad_top:.2f}mm;width:{w:.2f}mm;height:{h - pad_top:.2f}mm">{html}</div>'


def disegno(src, c, r, cw, rh, cap_html=""):
    x, y, w, h = cell(c, r, cw, rh)
    return (f'<div class="dwg" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">'
            f'<img src="{src}" alt=""></div>' + (box("cellcap", cap_html, c, r, cw, rh) if cap_html else ""))


def legenda(codes):
    return "".join(f"<li><b>{cid(c)}</b>{PROGETTI[c][0]}<span>{PROGETTI[c][1]}</span></li>" for c in codes)


def scheda(code):
    t, tip, sett = PROGETTI[code]
    rows = [("Tipologia", tip), ("Settore", sett), ("Materiale", TBD("[materiale]")), ("Cliente", TBD("[cliente]")),
            ("Anno", TBD("[anno]"))]
    return '<dl class="meta2">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def testo_prog(code, extra=""):
    t, tip, sett = PROGETTI[code]
    return (f'<div class="t2">{t}</div><div class="code2" style="margin-top:3mm">{cid(code)}</div>'
            f'<div class="t3" style="margin-top:7mm">Panoramica</div><p class="txt">{descr(code)}</p>{extra}'
            f'<div style="margin-top:6mm">{scheda(code)}</div>')


def didascalia(code):
    t, tip, sett = PROGETTI[code]
    return f'<div class="cellcap2"><b>{cid(code)} — {t}</b>{tip}</div>'


def apertura_banco():
    intro = ('<div class="bignum2">02</div><div class="t2">Espositori<br>da banco</div><p class="txt" style="margin-top:5mm">'
             "Il punto più vicino alla scelta: strutture compatte che portano il prodotto all’altezza dello sguardo, "
             "accanto alla cassa.</p>")
    sx = head(BANCO) + box("cellt", intro, 0, 0, 2, 3) + foto("B13", 2, 0, 3, 3)
    dx = (head("Disegni tecnici")
          + box("cellt", '<div class="t2">Disegno<br>tecnico</div><p class="txt" style="margin-top:5mm">Assonometria con le '
                         "quote d’ingombro: ogni progetto parte da un disegno come questo, poi sviluppato in fustella e "
                         "verificato su prototipo.</p>", 0, 0, 1, 3)
          + disegno("img/disegni/banco-iso.svg", 1, 0, 2, 3)
          + box("cellcap", "<b>Fig. 03 — Espositore da banco a gradini</b>Quote indicative", 1, 2, 2, 1)
          + foto("B04", 3, 0, 2, 2) + box("cellt", didascalia("B04"), 3, 2, 2, 1))
    return sx, dx


def progetto(main, s1, s2):
    """Sinistra: foto 3×3 + testo. Destra: due foto 2×2 in diagonale + colonna di testo."""
    sx = head("Progetto") + foto(main, 0, 0, 3, 3) + box("cellt", testo_prog(main), 3, 0, 2, 3)
    punti = ('<div class="t3">Struttura</div><p class="txt">Pieghe e incastri progettati per il montaggio senza colla.</p>'
             '<div class="t3" style="margin-top:5mm">Grafica</div><p class="txt">Stampa a vivo su tutte le superfici visibili.</p>'
             '<div class="t3" style="margin-top:5mm">Prodotto</div><p class="txt">Dimensionato su peso, formato e numero di facing.</p>')
    dx = (head("Progetto") + foto(s1, 0, 0, 2, 2) + box("cellt", didascalia(s1), 0, 2, 2, 1)
          + box("cellt", punti, 2, 0, 1, 3)
          + box("cellt bottom", didascalia(s2), 3, 0, 2, 1) + foto(s2, 3, 1, 2, 2))
    return sx, dx


def coppia(a, b):
    """Due progetti a tutta altezza, uno per pagina, a specchio."""
    sx = head("Progetto") + foto(a, 0, 0, 3, 3) + box("cellt", testo_prog(a), 3, 0, 2, 3)
    dx = head("Progetto") + box("cellt", testo_prog(b), 0, 0, 2, 3) + foto(b, 2, 0, 3, 3)
    return sx, dx


def apertura_terra():
    intro = ('<div class="bignum2">03</div><div class="t2">Espositori<br>da terra</div><p class="txt" style="margin-top:5mm">'
             "Strutture autoportanti a più ripiani, pensate per reggere il carico e farsi vedere da lontano. "
             "Spedite piatte, montate in pochi minuti.</p>")
    sx = (head(TERRA) + box("cellt", intro + f'<div style="margin-top:8mm">{didascalia("T01")}{didascalia("T02")}</div>', 0, 0, 1, 3)
          + foto("T01", 1, 0, 2, 3) + foto("T02", 3, 0, 2, 3))
    dx = (head("Disegni tecnici")
          + box("cellt", '<div class="t2">Disegno<br>tecnico</div><p class="txt" style="margin-top:5mm">Colonna a quattro '
                         "ripiani con zoccolo e header: fianchi portanti, ripiani a vassoio agganciati con incastri, "
                         "spedizione piatta.</p>", 0, 0, 2, 2)
          + box("cellcap", "<b>Fig. 04 — Espositore da terra a ripiani</b>Quote indicative", 0, 2, 2, 1)
          + disegno("img/disegni/terra-iso.svg", 2, 0, 3, 3))
    return sx, dx


def coppia_terra(a, b, c, d):
    """Due espositori da terra per pagina, 2×3 celle ciascuno, con colonna di didascalie."""
    sx = (head(TERRA) + foto(a, 0, 0, 2, 3) + foto(b, 2, 0, 2, 3)
          + box("cellt bottom", didascalia(a) + didascalia(b), 4, 0, 1, 3))
    dx = (head(TERRA) + box("cellt bottom", didascalia(c) + didascalia(d), 0, 0, 1, 3)
          + foto(c, 1, 0, 2, 3) + foto(d, 3, 0, 2, 3))
    return sx, dx


def fustelle_mockup():
    sx = (head("Disegni tecnici")
          + box("cellt", '<div class="t2">Sviluppo<br>in piano</div><p class="txt" style="margin-top:5mm">Fianco, schienale e '
                         "ripiano dell’espositore da terra, stesi in piano come escono dalla fustellatrice: linee continue "
                         "di taglio, tratteggi di cordonatura.</p>", 0, 0, 1, 3)
          + disegno("img/disegni/terra-fustelle.svg", 1, 0, 4, 3))
    dx = (head(TERRA) + foto("T09", 0, 0, 3, 3)
          + box("cellt", testo_prog("T09", f'<p class="txt">{TBD("[Cliente, materiale e misure da confermare.]")}</p>'), 3, 0, 2, 3))
    return sx, dx


def contatti():
    return (head("Contatti") + t2("Contatti", .5, .65, 3)
            + el("lead", "Il prossimo progetto parte da un brief.", .5, 1.3, 3.5)
            + txt("Raccontaci il prodotto, il punto vendita, le quantità e i tempi: ti rispondiamo con un concept e un prototipo.", .5, 1.8, 2.6)
            + "".join(t3(k, c, r) + el("contact2", TBD(v), c, r + .2, 2.6)
                      for k, v, c, r in [("Telefono", "+39 000 000 0000", .5, 2.6), ("Email", "info@azienda.it", 3.5, 2.6),
                                         ("Indirizzo", "Via Esempio 1, 00000 Città (XX)", .5, 3.3), ("Web", "www.azienda.it", 3.5, 3.3)])
            + el("rule", "", .5, 4.3, 6) + el("brand", AZ + " — Portfolio Espositori 2026", .5, 4.42, 4))


# --------------------------------------------------------------------------
def build():
    pages = [("grid", PG.copertina())]
    for a, b in [introduzione(), chi_siamo(), apertura_banco(),
                 progetto("B02", "B17", "B09"), progetto("B11", "B12", "B16"),
                 progetto("B06", "B05", "B01"), progetto("B10", "B15", "B03"), coppia("B07", "B08"),
                 apertura_terra(), coppia_terra("T03", "T06", "T07", "T08"), fustelle_mockup(), coppia("T04", "T05")]:
        pages += [("", a), ("", b)]
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
