#!/usr/bin/env python3
"""
Portfolio Espositori — versione A4 verticale (210 × 297 mm) delle pagine sul modello della reference.
Stessi contenuti e stessi schemi di portfolio_ref.py, ridisposti per la pagina verticale.

    python3 portfolio_ref_v.py   ->  portfolio-ref-v.html
"""
import portfolio_ref as R            # contenuti e componenti (va importato prima della versione verticale)
import portfolio_grid_v as GV        # copertina e retro verticali
from portfolio_ref import bx, foto, dwg, txt, blocco, kv, prod, zona, TIPO, INTRO, ZONE, BANCO, TERRA, TBD, AZ, cid, ROOT

W, H = 210, 297
M = 16
TOP, BOT = 36, 276
CW = W - 2 * M - 8                   # 170 mm di area utile
X0 = M + 4
COL = (CW - 8) / 2                   # due colonne da 81 mm


def pagina(titolo, sezione, corpo):
    return (f'<div class="ptitle" style="{bx(M, 17)}">{titolo}</div>'
            f'<div class="hdr" style="right:{M}mm;top:17mm"><span class="az">{AZ}</span><span class="pill">{sezione}</span></div>'
            + corpo)


def x2(i):
    return X0 + i * (COL + 8)


# --------------------------------------------------------------------------
# schemi della reference in verticale
# --------------------------------------------------------------------------
def overview(titolo, sez, code, intro, dati, extra=""):
    return pagina(titolo, sez, foto(code, X0, TOP + 4, CW, 150)
                  + txt(f'<h4>{sez}</h4><p>{intro}</p>{extra}', x2(0), 200, COL)
                  + txt(kv(dati) + prod(code), x2(1), 200, COL))


def overview_dwg(titolo, sez, src, intro, dati, extra=""):
    return pagina(titolo, sez, dwg(src, X0, TOP, CW, 158)
                  + txt(f'<h4>{sez}</h4><p>{intro}</p>{extra}', x2(0), 200, COL)
                  + txt(kv(dati), x2(1), 200, COL))


def philosophy(titolo, sez, codes, alto=70):
    corpo = ""
    riga = alto + 40
    for i, c in enumerate(codes):
        x, y = x2(i % 2), TOP + 4 + (i // 2) * (riga + 6)
        corpo += foto(c, x, y, COL, alto) + txt(prod(c), x, y + alto + 4, COL)
    return pagina(titolo, sez, corpo)


def urban(titolo, sez, big, small, testo):
    return pagina(titolo, sez, foto(big, X0, TOP + 4, CW, 128)
                  + txt(prod(big) + f'<div class="gap">{testo}</div>', x2(0), 178, COL)
                  + foto(small, x2(1), 178, COL, COL) + txt(prod(small), x2(1), 178 + COL + 4, COL))


def creative(titolo, sez, codes, testo):
    corpo = "".join(foto(c, x2(i % 2), TOP + 4 + (i // 2) * (COL + 6), COL, COL) for i, c in enumerate(codes))
    legenda = "".join(f'<li><b>{cid(c)}</b>{TIPO[c]}</li>' for c in codes)
    return pagina(titolo, sez, corpo + txt(testo, x2(0), TOP + 2 * COL + 16, COL)
                  + txt(f'<ul class="leg" style="margin-top:0">{legenda}</ul>'
                        f'<p class="note">Materiali e finiture: {TBD("[da completare per ogni codice]")}</p>', x2(1), TOP + 2 * COL + 16, COL))


def challenges(titolo, sez, small, big, testo):
    return pagina(titolo, sez, foto(big, X0, TOP + 4, CW, 140)
                  + txt(testo + prod(big) + prod(small), x2(0), 190, COL)
                  + foto(small, x2(1), 190, COL, COL))


def academic(titolo, sez, a, b, tall, testo):
    return pagina(titolo, sez, foto(a, x2(0), TOP + 4, COL - 4, 72) + foto(b, x2(0), TOP + 80, COL - 4, 72)
                  + foto(tall, x2(1) - 4, TOP + 4, COL + 4, 148)
                  + txt(testo + prod(a) + prod(b), x2(0), 196, COL) + txt(prod(tall), x2(1), 196, COL))


def technical(titolo, sez, src, sx, dx):
    return pagina(titolo, sez, dwg(src, X0, TOP, CW, 170) + txt(sx, x2(0), 214, COL) + txt(dx, x2(1), 214, COL, "blk right"))


def coppia(titolo, sez, a, b, testo):
    return pagina(titolo, sez, foto(a, x2(0), TOP + 4, COL, 176) + foto(b, x2(1), TOP + 4, COL, 176)
                  + txt(testo, x2(0), TOP + 188, COL) + txt(prod(b), x2(1), TOP + 188, COL))


def space(titolo, sez, a, b, testo):
    return pagina(titolo, sez, foto(a, x2(0), TOP + 4, COL, 176)
                  + foto(b, x2(1), TOP + 4, COL, COL) + txt(testo, x2(1), TOP + COL + 12, COL))


# --------------------------------------------------------------------------
# pagine di testo
# --------------------------------------------------------------------------
def indice():
    voci = [("01", "Introduzione", 4), ("02", "Chi siamo", 5), ("03", "Espositori da banco", 6),
            ("04", "Espositori da terra", 12), ("05", "Contatti", 18)]
    li = "".join(f'<li><span class="n">{n}</span><span class="t">{t}</span><span class="p">{p:02d}</span></li>' for n, t, p in voci)
    return pagina("Indice", "Indice", txt(f'<ul class="toc">{li}</ul>', X0, TOP + 10, CW)
                  + txt('<p class="big">Un catalogo illustrativo: le immagini raccontano i progetti, '
                        'le schede riportano solo i dati tecnici essenziali.</p>', X0, 140, 120))


def metodo():
    intro = (f'<p class="lead3">Dal {TBD("[anno]")} progettiamo e produciamo espositori in cartotecnica e materiali '
             "durevoli: dal primo schizzo al bancale pronto a partire, tutto sotto lo stesso tetto.</p>"
             '<p class="note2" style="margin-top:0">Espositori da banco e da terra per cosmesi, farmacia, ottica, '
             "ferramenta e beverage: progettazione, prototipi, stampa e fustellatura interni.</p>")
    fasi = "".join(f'<div class="fase"><span>0{i + 1}</span>{blocco(t, d)}</div>' for i, (t, d) in enumerate([
        ("Schizzo", "Proporzioni, ingombri e altezze dei ripiani."),
        ("Disegno tecnico", "Tracciati di fustella e render 3D."),
        ("Prototipo", "Campione fisico, test di carico e montaggio."),
        ("Produzione", "Stampa, fustellatura e confezionamento interni.")]))
    return pagina("Dal progetto alla realizzazione", "Introduzione",
                  f'<div class="dwg" style="{bx(x2(0), TOP, COL, 150)}"><img src="img/schizzo-terra.png" alt=""></div>'
                  + f'<div class="dwg mult" style="{bx(x2(1), TOP, COL, 150)}"><img src="img/metodo-prodotto.jpg" alt=""></div>'
                  + txt(intro, x2(0), 196, COL) + txt(fasi, x2(1), 196, COL))


def chi_siamo():
    fasi = [("01", "Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
            ("02", "Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
            ("03", "Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
            ("04", "Logistica", "Spedizione piatta o premontata, in Italia e all’estero.")]
    corpo = ""
    for i, (n, t, d) in enumerate(fasi):
        x, y = x2(i % 2), TOP + 4 + (i // 2) * 92
        corpo += f'<div class="tile" style="{bx(x, y, COL, 58)}"><span>{n}</span></div>' + txt(blocco(t, d), x, y + 63, COL)
    corpo += txt(f'<div class="stats">'
                 f'<div><b>{TBD("35+")}</b>Anni di esperienza</div><div><b>{TBD("400")}</b>Progetti l’anno</div>'
                 f'<div><b>100%</b>Prodotto internamente</div></div>', X0, 236, CW)
    return pagina("Chi siamo", "Chi siamo", corpo)


def contatti():
    rows = [("Telefono", TBD("+39 000 000 0000")), ("Email", TBD("info@azienda.it")),
            ("Indirizzo", TBD("Via Esempio 1, 00000 Città (XX)")), ("Web", TBD("www.azienda.it"))]
    return pagina("Contatti", "Contatti", txt('<p class="big">Il prossimo progetto parte da un brief. Raccontaci il prodotto, '
                                              'il punto vendita, le quantità e i tempi.</p>', X0, TOP + 10, 130)
                  + txt(kv(rows), X0, 110, CW, "blk contacts"))


# --------------------------------------------------------------------------
def build():
    B, T = BANCO, TERRA
    zb = lambda i: f'<div class="gap">{zona(B, i)}</div>'
    zt = lambda i: f'<div class="gap">{zona(T, i)}</div>'
    interne = [
        indice(), metodo(), chi_siamo(),
        overview("Espositori da banco", B, "B13", INTRO[B],
                 [("Formati", "Da 20 × 15 a 60 × 40 cm"), ("Materiali", "Cartone, cartoncino, forex, plexi, legno"),
                  ("Montaggio", "Pochi secondi, senza colla")]),
        philosophy("Progetti", B, ["B02", "B17", "B09", "B11"], alto=82),
        urban("Stampa e finiture", B, "B12", "B16", zb(2)),
        creative("Su misura", B, ["B06", "B05", "B01", "B10"], zb(3)),
        challenges("Struttura", B, "B15", "B03", zb(0)),
        academic("Materiali", B, "B08", "B04", "B07", zb(1)),
        overview_dwg("Espositori da terra", T, "img/disegni/terra-tavola.svg", INTRO[T],
                     [("Altezze", "Da 140 a 180 cm"), ("Ripiani", "Da 3 a 5, con header"),
                      ("Spedizione", "Piatta, montaggio in pochi minuti")], zt(1)),
        overview("Logistica", T, "T05", ZONE[T][3][1], []),
        philosophy("Progetti", T, ["T01", "T02", "T03", "T06"], alto=82),
        space("Stampa e finiture", T, "T04", "T09", zt(2) + prod("T04") + prod("T09")),
        challenges("Portata", T, "T07", "T08", zt(0)),
        coppia("Grafica e brand", T, "T10", "T11", '<div class="gap">' + R.GRAFICA + "</div>" + prod("T10")),
        contatti(),
    ]
    # pagina bianca provvisoria prima della copertina (da rimuovere in seguito): la copertina resta pagina 1
    pages = [("blank pre", ""), ("grid", GV.copertina()), ("blank", "")] + [("ref", p) for p in interne] + [("grid", GV.retro())]
    html = []
    for i, (cls, body) in enumerate(pages, start=0):
        side = "pr" if i % 2 else "pl"
        foot = "" if cls.split()[0] in ("grid", "blank") else (f'<div class="pn" style="{bx(M, 280)}">{i:02d}</div>'
                                                                f'<div class="ft" style="right:{M}mm;top:282mm">Portfolio Espositori 2026</div>')
        html.append(f'<section class="page {side} {cls}">{body}{foot}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori — verticale</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio-grid.css">
<link rel="stylesheet" href="portfolio-grid-v.css">
<link rel="stylesheet" href="portfolio-v2.css">
<link rel="stylesheet" href="portfolio-ref.css">
<link rel="stylesheet" href="portfolio-ref-v.css">
</head><body><main class="book pre">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-ref-v.html").write_text(doc, encoding="utf-8")
    print("portfolio-ref-v.html:", len(pages), "pagine")


if __name__ == "__main__":
    build()
