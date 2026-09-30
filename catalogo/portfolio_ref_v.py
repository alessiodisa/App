#!/usr/bin/env python3
"""
Portfolio Espositori — versione A4 verticale (210 × 297 mm) delle pagine sul modello della reference.
Stessi contenuti e stessi schemi di portfolio_ref.py, ridisposti per la pagina verticale.

    python3 portfolio_ref_v.py   ->  portfolio-ref-v.html
"""
import portfolio_ref as R            # contenuti e componenti (va importato prima della versione verticale)
import portfolio_grid_v as GV        # copertina e retro verticali
from portfolio_ref import bx, foto, dwg, txt, blocco, kv, prod, nomf, legenda, tag, zona, TIPO, INTRO, ZONE, BANCO, TERRA, TBD, AZ, cid, ROOT

W, H = 210, 297
M = 16
TOP, BOT = 36, 276
CW = W - 2 * M - 8                   # 170 mm di area utile
X0 = M + 4
COL = (CW - 8) / 2                   # due colonne da 81 mm


def pagina(titolo, sezione, corpo):
    """Il titolo di pagina è sempre il nome della sezione; `titolo` resta come argomento degli schemi."""
    return (f'<div class="ptitle" style="{bx(M, 17)}">{sezione}</div>'
            f'<div class="hdr" style="right:{M}mm;top:17mm"><span class="az">{AZ}</span><span class="pill">{sezione}</span></div>'
            + corpo)


def x2(i):
    return X0 + i * (COL + 8)


# --------------------------------------------------------------------------
# schemi della reference in verticale
# --------------------------------------------------------------------------
def overview(titolo, sez, code, intro, dati, extra="", fh=150, mf=False, z=1.0):
    y = TOP + 14 + fh
    if z < 1 and code in R.ORIG:              # foto originale intera in un riquadro con le sue proporzioni
        iw, ih = R.ORIG[code]["size"]
        fwi = fh * iw / ih
        img = R.foto_orig(code, X0 + (CW - fwi) / 2, TOP + 4, fwi, fh)
    else:
        img = foto(code, X0, TOP + 4, CW, fh, z=z)
    return pagina(titolo, sez, img
                  + txt((f'<h4>{titolo}</h4>' if titolo != sez else '') + f'<p class="lead0">{intro}</p>{extra}', x2(0), y, COL)
                  + txt(kv(dati) + prod(code, mf), x2(1), y, COL))


def overview_dwg(titolo, sez, src, intro, dati, extra="", fh=178):
    y = TOP + 14 + fh
    return pagina(titolo, sez, dwg(src, X0, TOP + 4, CW, fh)
                  + txt(f'<p class="lead0">{intro}</p>{extra}', x2(0), y, COL)
                  + txt(kv(dati), x2(1), y, COL))


def affianca(sez, a, b, testo, h=108):
    """Foto quadrata e foto verticale originale affiancate alla stessa altezza, didascalie e testo sotto."""
    iw, ih = R.ORIG[b]["size"]
    wb = h * iw / ih
    wa = CW - wb - 8
    y = TOP + 4 + h + 6
    return pagina("", sez, foto(a, X0, TOP + 4, wa, h) + R.foto_orig(b, X0 + wa + 8, TOP + 4, wb, h)
                  + txt(nomf(a), X0, y, wa) + txt(nomf(b), X0 + wa + 8, y, wb)
                  + txt(f'<p class="lead0">{testo}</p>', X0, y + 24, CW))


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
                  + txt(f'<ul class="leg" style="margin-top:0">{legenda}</ul>', x2(1), TOP + 2 * COL + 16, COL))


def challenges(titolo, sez, small, big, testo):
    return pagina(titolo, sez, foto(big, X0, TOP + 4, CW, 140)
                  + txt(testo + prod(big) + prod(small), x2(0), 190, COL)
                  + foto(small, x2(1), 190, COL, COL))


def challenges3(titolo, sez, small, big, extra, testo):
    return pagina(titolo, sez, foto(big, x2(0), TOP + 4, COL, 140) + R.foto_orig(extra, x2(1), TOP + 4, COL, 140)
                  + txt(testo + prod(big) + prod(extra) + prod(small), x2(0), 190, COL)
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


def terzetto(titolo, sez, codes):
    """Tre immagini verticali affiancate, schede sotto."""
    w = (CW - 12) / 3
    return pagina(titolo, sez, "".join(foto(c, X0 + i * (w + 6), TOP + 4, w, 165) + txt(prod(c), X0 + i * (w + 6), TOP + 179, w)
                                       for i, c in enumerate(codes)))


def duo(titolo, sez, a, b, c):
    """Due immagini affiancate in alto, la terza sotto a sinistra con testo e scheda a destra."""
    return pagina(titolo, sez, foto(a, x2(0), TOP + 4, COL, 102) + foto(b, x2(1), TOP + 4, COL, 102)
                  + txt(prod(a), x2(0), TOP + 112, COL) + txt(prod(b), x2(1), TOP + 112, COL)
                  + foto(c, x2(0), TOP + 148, COL, 90)
                  + txt('<div class="gap">' + R.GRAFICA + "</div>" + prod(c), x2(1), TOP + 150, COL))


def duo2(titolo, sez, a, b):
    """Due immagini affiancate, schede sotto."""
    return pagina(titolo, sez, foto(a, x2(0), TOP + 4, COL, 120) + foto(b, x2(1), TOP + 4, COL, 120)
                  + txt(prod(a), x2(0), TOP + 134, COL) + txt(prod(b), x2(1), TOP + 134, COL))


def griglia(sez, codes, h=96, mf=False):
    """2×2 immagini più alte che larghe, scheda breve sotto ognuna (senza materiali e finiture)."""
    corpo = ""
    for i, c in enumerate(codes):
        x, y = x2(i % 2), TOP + 4 + (i // 2) * (h + 22)
        corpo += foto(c, x, y, COL, h) + txt(prod(c, mf), x, y + h + 3, COL)
    return pagina("", sez, corpo)


def didascalie(sez, big, small, testo):
    """Foto grande con la sua didascalia subito sotto; a destra foto piccola con didascalia;
    a sinistra, separata da un filetto, la descrizione generale della sezione."""
    return pagina("", sez, foto(big, X0, TOP + 4, CW, 128) + txt(nomf(big), x2(0), TOP + 136, COL)
                  + foto(small, x2(1), TOP + 136, COL, COL) + txt(nomf(small), x2(1), TOP + 139 + COL, COL)
                  + txt(f'<div class="desc">{testo}</div>', x2(0), TOP + 170, COL))


def quattro(sez, codes, testo):
    """Griglia 2×2 con numero identificativo sotto ogni immagine, testo e legenda in basso."""
    h = COL - 4
    corpo = ""
    for i, c in enumerate(codes):
        x, y = x2(i % 2), TOP + 4 + (i // 2) * (h + 12)
        corpo += foto(c, x, y, COL, h) + tag(c, x, y + h + 2.5, COL)
    yb = TOP + 4 + 2 * (h + 12) + 6
    return pagina("", sez, corpo + txt(testo, x2(0), yb, COL)
                  + txt(legenda(codes), x2(1), yb, COL))


def tre_legenda(sez, a, b, tall):
    """Due foto impilate a sinistra, una alta a destra, numeri sotto le foto e legenda in basso."""
    return pagina("", sez, foto(a, x2(0), TOP + 4, COL, 84) + tag(a, x2(0), TOP + 90.5, COL)
                  + foto(b, x2(0), TOP + 100, COL, 84) + tag(b, x2(0), TOP + 186.5, COL)
                  + foto(tall, x2(1), TOP + 4, COL, 180, z=.76) + tag(tall, x2(1), TOP + 186.5, COL)
                  + txt(legenda([a, b, tall]), X0, TOP + 200, CW))


def terna(sez, a, b, c, z=.8):
    """Due foto affiancate in alto, la terza sotto a sinistra con testo e scheda a destra (inquadratura più larga)."""
    return pagina("", sez, foto(a, x2(0), TOP + 4, COL, 102, z=z) + foto(b, x2(1), TOP + 4, COL, 102, z=z)
                  + txt(nomf(a), x2(0), TOP + 110, COL) + txt(nomf(b), x2(1), TOP + 110, COL)
                  + foto(c, x2(0), TOP + 136, COL, 90, z=z) + txt(nomf(c), x2(0), TOP + 229, COL)
                  + txt(R.GRAFICA, x2(1), TOP + 138, COL))


def coppia_z(sez, a, b, z=.8):
    return pagina("", sez, foto(a, x2(0), TOP + 4, COL, 120, z=z) + foto(b, x2(1), TOP + 4, COL, 120, z=z)
                  + txt(nomf(a), x2(0), TOP + 130, COL) + txt(nomf(b), x2(1), TOP + 130, COL))


def galleria(sez, codes, h=98, z=1.32):
    """2×2 foto verticali ravvicinate, senza schede: solo il numero sotto e la legenda in fondo su due colonne."""
    corpo = ""
    for i, c in enumerate(codes):
        x, y = x2(i % 2), TOP + 4 + (i // 2) * (h + 12)
        corpo += foto(c, x, y, COL, h, z=z) + tag(c, x, y + h + 2.5, COL)
    yl = TOP + 4 + 2 * (h + 12) + 2
    return pagina("", sez, corpo + txt(legenda(codes[:2]), x2(0), yl, COL) + txt(legenda(codes[2:]), x2(1), yl, COL))


def space(titolo, sez, a, b, testo):
    return pagina(titolo, sez, foto(a, x2(0), TOP + 4, COL, 176)
                  + foto(b, x2(1), TOP + 4, COL, COL) + txt(testo, x2(1), TOP + COL + 12, COL))


# --------------------------------------------------------------------------
# pagine di testo
# --------------------------------------------------------------------------
def indice():
    voci = [("01", "Introduzione", 4), ("02", "Chi siamo", 5), ("03", "Espositori da banco", 6),
            ("04", "Espositori da terra", 14), ("05", "Contatti", 22)]
    li = "".join(f'<li><span class="n">{n}</span><span class="t">{t}</span><span class="p">{p:02d}</span></li>' for n, t, p in voci)
    return pagina("Indice", "Indice", txt(f'<ul class="toc">{li}</ul>', X0, TOP + 10, CW)
                  + txt('<p class="big">Un catalogo illustrativo: le immagini raccontano i progetti, '
                        'le schede riportano solo i dati tecnici essenziali.</p>', X0, 140, 120))


def metodo():
    intro = (f'<h4>Dal progetto alla realizzazione</h4><p class="lead3" style="margin-top:2mm">Dal {TBD("[anno]")} progettiamo e produciamo espositori in cartotecnica e materiali '
             "durevoli: dal primo schizzo al bancale pronto a partire, tutto sotto lo stesso tetto.</p>"
             '<p class="note2" style="margin-top:0">Espositori da banco e da terra per cosmesi, farmacia, ottica, '
             "ferramenta e beverage: progettazione, prototipi, stampa e fustellatura interni.</p>")
    fasi = "".join(f'<div class="fase"><span>0{i + 1}</span>{blocco(t, d)}</div>' for i, (t, d) in enumerate([
        ("Schizzo", "Proporzioni, ingombri e altezze dei ripiani."),
        ("Disegno tecnico", "Tracciati di fustella e render 3D."),
        ("Prototipo", "Campione fisico, test di carico e montaggio."),
        ("Produzione", "Stampa, fustellatura e confezionamento interni.")]))
    return pagina("Dal progetto alla realizzazione", "Introduzione",
                  R.tre_fasi(X0 + 4, CW - 8, TOP + 132, 95)
                  + txt(intro, x2(0), 196, COL) + txt(fasi, x2(1), 196, COL))


def chi_siamo():
    fasi = [("01", "Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
            ("02", "Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
            ("03", "Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
            ("04", "Logistica", "Spedizione piatta o premontata, in Italia e all’estero.")]
    corpo = ""
    for i, (n, t, d) in enumerate(fasi):
        x, y = x2(i % 2), TOP + 4 + (i // 2) * 92
        corpo += (dwg(f"img/disegni/chi-{n}.svg", x, y, COL, 58)
                  + f'<div class="tagc" style="{bx(x, y + 62)}">{n}</div>' + txt(blocco(t, d), x, y + 66, COL))
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
        griglia(B, ["B02", "B17", "B09", "B11"]),
        didascalie(B, "B12", "B16", zona(B, 2)),
        quattro(B, ["B06", "B05", "B01", "B10"], zona(B, 3)),
        didascalie(B, "B03", "B15", zona(B, 0)),
        tre_legenda(B, "B08", "B04", "B07"),
        terna(B, "B19", "B20", "B21"),
        coppia_z(B, "B22", "B23"),
        overview_dwg("Espositori da terra", T, "img/disegni/terra-tavola.svg", INTRO[T],
                     [("Altezze", "Da 140 a 180 cm"), ("Ripiani", "Da 3 a 5, con header"),
                      ("Spedizione", "Piatta, montaggio in pochi minuti")]),
        overview("Logistica", T, "T05", ZONE[T][3][1], [], fh=178),
        galleria(T, ["T01", "T02", "T03", "T06"]),
        overview("Stampa e finiture", T, "T04", ZONE[T][2][1], []),
        overview("Due finiture", T, "T09", "Stessa struttura, due finiture: cambia la grafica, la fustella resta la stessa.", []),
        challenges3("Portata", T, "T07", "T08", "T13", zt(0)),
        coppia("Grafica e brand", T, "T10", "T11", '<div class="gap">' + R.GRAFICA + "</div>" + prod("T10")),
        overview("Colonna", T, "T12", "Colonna stretta con ripiani laterali: poco ingombro a terra e grafica a tutta altezza.", [], fh=165),
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
