#!/usr/bin/env python3
"""
Portfolio Espositori v3 — A4 orizzontale, pagine interne sul modello "Architecture Portfolio".

Struttura dei contenuti:
  - apertura di ogni sezione: poche righe che presentano il prodotto
  - 4 zone di testo per sezione, distribuite nelle pagine
  - per ogni espositore solo dati tecnici: tipologia, materiali, finiture

    python3 portfolio_v3.py   ->  portfolio-v3.html
"""
import portfolio_grid as PG
import portfolio_v2 as V2
from portfolio_grid import TBD, AZ, cid, ROOT

W, H, MG, GUT = PG.W, PG.H, 15, 4.8
TITLE_Y = 24                                         # titolo di pagina
Y0 = 41                                              # inizio della griglia
CW = (W - 2 * MG - 4 * GUT) / 5                      # 5 colonne
CH = (H - MG - Y0 - 2 * GUT) / 3                     # 3 righe
BANCO, TERRA = "Espositori da banco", "Espositori da terra"

# tipologia tecnica di ogni espositore (da confermare)
TIPO = {
    "B01": "Espositore da banco a 2 gradini con header",
    "B02": "Espositore da banco inclinato a 3 scomparti con header",
    "B03": "Espositore da banco con crowner sagomato",
    "B04": "Espositore da banco a vassoio con fondale",
    "B05": "Espositore da banco a 2 gradini con header",
    "B06": "Espositore da banco a pedana con fondale",
    "B07": "Espositore da banco a colonna con ganci",
    "B08": "Espositore da banco a box con header",
    "B09": "Espositore da banco a libreria con 3 ripiani",
    "B10": "Espositore da banco a pedana curva con fondale",
    "B11": "Espositore da banco a 4 ripiani a sbalzo con fondale",
    "B12": "Espositore da banco a fondale con 3 nicchie",
    "B13": "Espositore da banco a pedana con fondale",
    "B15": "Espositore da banco a box con doppio fondale",
    "B16": "Espositore da banco monoprodotto con fondale",
    "B17": "Espositore da banco a 3 gradini con header",
    "B19": "Espositore da banco con fondale e vassoio inclinato a gradini",
    "B20": "Espositore da banco a 2 gradini con header ad arco",
    "B21": "Espositore da banco a vassoio alveolare con fondale",
    "B22": "Espositore da banco a 4 vassoi su 2 livelli con fondale",
    "B23": "Espositore da banco porta locandina a cornice con base",
    "T01": "Espositore da terra a 3 ripiani con header",
    "T02": "Espositore da terra a ganci con header",
    "T03": "Espositore da terra a 4 ripiani a sbalzo",
    "T04": "Espositore da terra a 4 ripiani",
    "T05": "Espositore da terra a 4 ripiani con header",
    "T06": "Espositore da terra a 4 ripiani con crowner",
    "T07": "Espositore da terra a podio con fondale",
    "T08": "Espositore da terra a totem con 4 nicchie",
    "T09": "Espositore da terra a 3 ripiani con fianchi inclinati e header ad arco",
    "T10": "Espositore da terra a 4 ripiani con fianco sagomato e vassoio",
    "T11": "Espositore da terra a colonna con vano a gradini e header",
    "T12": "Espositore da terra a colonna con 4 ripiani laterali e header sagomato",
    "T14": "Espositore da terra a colonna con 3 vani a vassoio e base porta depliant",
    "T15": "Espositore da terra a 3 ripiani sfalsati con fianchi sagomati e base",
    "T13": "Espositore da terra a 5 ripiani con fianchi a colonna e header",
}

INTRO = {
    BANCO: "Gli espositori da banco lavorano nel punto più vicino alla scelta: accanto alla cassa, sul banco della "
           "farmacia, in vetrina. Strutture compatte che portano il prodotto all’altezza dello sguardo e si montano in pochi gesti.",
    TERRA: "Gli espositori da terra portano il prodotto fuori dallo scaffale e lo rendono visibile da lontano. "
           "Strutture autoportanti a più ripiani, con header per la comunicazione, pensate per reggere il carico e montarsi in pochi minuti.",
}

ZONE = {
    BANCO: [("Struttura", "Pieghe, incastri e rinforzi interni progettati per un montaggio rapido, senza colla, "
                          "e per restare stabili a pieno carico."),
            ("Materiali", "Microonda, cartoncino teso, forex, plexiglass e legno: il materiale si sceglie in base al peso "
                          "del prodotto, alla durata e al punto vendita."),
            ("Stampa e finiture", "Stampa offset e digitale a vivo, plastificazione opaca o lucida, vernice UV selettiva "
                                  "e lamina a caldo."),
            ("Su misura", "Forma, formato e grafica sono progettati sul prodotto, dal campione bianco al prototipo "
                          "stampato prima della produzione.")],
    TERRA: [("Portata", "Fianchi portanti e ripiani rinforzati sostengono il carico del prodotto su più livelli, "
                        "senza perdere stabilità."),
            ("Materiali", "Cartone ondulato onda B, BC ed EB, alveolare per le strutture più alte, forex e legno "
                          "per le soluzioni durevoli."),
            ("Stampa e finiture", "Stampa a vivo su fianchi, header e frontali, plastificazione per resistere "
                                  "all’uso nel punto vendita."),
            ("Logistica", "Spediti piatti in un unico imballo, si montano in pochi minuti senza attrezzi.")],
}


# --------------------------------------------------------------------------
# griglia e componenti
# --------------------------------------------------------------------------
def cell(c, r, cw=1, rh=1):
    return MG + c * (CW + GUT), Y0 + r * (CH + GUT), cw * CW + (cw - 1) * GUT, rh * CH + (rh - 1) * GUT


def box(cls, html, c, r, cw=1, rh=1):
    x, y, w, h = cell(c, r, cw, rh)
    return f'<div class="{cls}" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">{html}</div>'


def foto(code, c, r, cw=1, rh=1):
    x, y, w, h = cell(c, r, cw, rh)
    c0, r0 = V2._to_grid(x, y)
    c1, r1 = V2._to_grid(x + w, y + h)
    return PG.photo(code, c0, r0, c1, r1) + f'<div class="tag2" style="left:{x + 2.2:.2f}mm;top:{y + 2.2:.2f}mm">{cid(code)}</div>'


def disegno(src, c, r, cw, rh):
    x, y, w, h = cell(c, r, cw, rh)
    return (f'<div class="dwg" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">'
            f'<img src="{src}" alt=""></div>')


def pagina(sezione, titolo, corpo):
    return (f'<div class="brand" style="left:{MG}mm;top:{MG}mm">{AZ}</div>'
            f'<div class="pill" style="right:{MG}mm;top:{MG - 1.2}mm"><span>{sezione}</span></div>'
            f'<div class="ptitle3" style="left:{MG}mm;top:{TITLE_Y}mm">{titolo}</div>' + corpo)


def prodotto(code, align="top"):
    """Scheda tecnica minima: codice, tipologia, materiali, finiture."""
    return (f'<div class="prod {align}"><div class="prod-code">{cid(code)}</div><div class="prod-tipo">{TIPO[code]}</div>'
            f'<dl><dt>Materiali</dt><dd>{TBD("[materiali]")}</dd><dt>Finiture</dt><dd>{TBD("[finiture]")}</dd></dl></div>')


def zona(sezione, i):
    t, d = ZONE[sezione][i]
    return f'<div class="zona"><div class="zona-n">0{i + 1}</div><div class="zona-t">{t}</div><p>{d}</p></div>'


# --------------------------------------------------------------------------
# tipi di pagina
# --------------------------------------------------------------------------
def p_grande(sez, titolo, code, z=None, mirror=False):
    """Foto 3×3 + colonna con scheda prodotto (e zona di testo)."""
    col_txt, col_img = (0, 2) if mirror else (3, 0)
    corpo = foto(code, col_img, 0, 3, 3) + box("cellt", prodotto(code), col_txt, 0, 2, 1)
    if z is not None:
        corpo += box("cellt bottom", zona(sez, z), col_txt, 1, 2, 2)
    return pagina(sez, titolo, corpo)


def p_diagonale(sez, titolo, a, b, z=None):
    """Due foto 2×2 sfalsate + colonna centrale."""
    corpo = (foto(a, 0, 0, 2, 2) + box("cellt", prodotto(a), 0, 2, 2, 1)
             + box("cellt bottom", prodotto(b, "bottom"), 3, 0, 2, 1) + foto(b, 3, 1, 2, 2))
    if z is not None:
        corpo += box("cellt", zona(sez, z), 2, 0, 1, 3)
    return pagina(sez, titolo, corpo)


def p_affiancate(sez, titolo, a, b, z=None):
    """Due foto 2×2 affiancate con schede sotto + colonna laterale."""
    corpo = (foto(a, 0, 0, 2, 2) + foto(b, 2, 0, 2, 2)
             + box("cellt", prodotto(a), 0, 2, 2, 1) + box("cellt", prodotto(b), 2, 2, 2, 1))
    if z is not None:
        corpo += box("cellt bottom", zona(sez, z), 4, 0, 1, 3)
    return pagina(sez, titolo, corpo)


def p_colonne(sez, titolo, a, b, z=None, mirror=False):
    """Due espositori da terra verticali 2×3 + colonna con schede (e zona)."""
    cx, ca, cb = (0, 1, 3) if mirror else (4, 0, 2)
    col = prodotto(a) + prodotto(b) + (zona(sez, z) if z is not None else "")
    return pagina(sez, titolo, foto(a, ca, 0, 2, 3) + foto(b, cb, 0, 2, 3) + box("cellt stack", col, cx, 0, 1, 3))


def apertura(sez, num, hero, dis_src, fig, side=None, zone=()):
    sx = pagina(sez, sez, box("cellt", f'<div class="bignum3">{num}</div><p class="intro3">{INTRO[sez]}</p>', 0, 0, 2, 3)
                + foto(hero, 2, 0, 3, 3))
    corpo = disegno(dis_src, 0, 0, 3, 3) + box("cellt bottom", f'<div class="fig">{fig}</div>', 0, 2, 2, 1)
    if side:
        corpo += foto(side, 3, 0, 2, 2) + box("cellt", prodotto(side), 3, 2, 2, 1)
    else:
        corpo += box("cellt stack", "".join(zona(sez, i) for i in zone), 3, 0, 2, 3)
    return sx, pagina(sez, "Disegno tecnico", corpo)


def fustelle(sez, z):
    corpo = (disegno("img/disegni/terra-fustelle.svg", 1, 0, 4, 3)
             + box("cellt stack", '<p class="intro3 sm">Fianco, schienale e ripiano stesi in piano come escono dalla '
                                  "fustellatrice: linee continue di taglio, tratteggi di cordonatura.</p>" + zona(sez, z), 0, 0, 1, 3))
    return pagina(sez, "Sviluppo in piano", corpo)


# --------------------------------------------------------------------------
def build():
    B, T = BANCO, TERRA
    spreads = [
        V2.introduzione(), V2.chi_siamo(),
        apertura(B, "02", "B13", "img/disegni/banco-iso.svg", "<b>Fig. 03</b>Espositore da banco a gradini — quote indicative", side="B04"),
        (p_grande(B, "Struttura", "B02", z=0), p_diagonale(B, "Espositori da banco", "B17", "B09")),
        (p_affiancate(B, "Materiali", "B11", "B12", z=1), p_grande(B, "Espositori da banco", "B16", mirror=True)),
        (p_grande(B, "Espositori da banco", "B06"), p_diagonale(B, "Stampa e finiture", "B05", "B01", z=2)),
        (p_diagonale(B, "Espositori da banco", "B10", "B15"), p_grande(B, "Su misura", "B03", z=3, mirror=True)),
        (p_grande(B, "Espositori da banco", "B07"), p_grande(B, "Espositori da banco", "B08", mirror=True)),
        apertura(T, "03", "T05", "img/disegni/terra-iso.svg", "<b>Fig. 04</b>Espositore da terra a ripiani — quote indicative", zone=(0, 1)),
        (p_colonne(T, "Stampa e finiture", "T01", "T02", z=2), p_colonne(T, "Espositori da terra", "T03", "T06", mirror=True)),
        (fustelle(T, 3), p_grande(T, "Espositori da terra", "T09", mirror=True)),
        (p_colonne(T, "Espositori da terra", "T07", "T08"), p_grande(T, "Espositori da terra", "T04", mirror=True)),
    ]
    pages = [("grid", PG.copertina())]
    for a, b in spreads:
        pages += [("", a), ("", b)]
    pages += [("", V2.contatti()), ("grid", PG.retro())]
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
<link rel="stylesheet" href="portfolio-v3.css">
</head><body><main class="book">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-v3.html").write_text(doc, encoding="utf-8")
    print("portfolio-v3.html:", tot, "pagine")


if __name__ == "__main__":
    build()
