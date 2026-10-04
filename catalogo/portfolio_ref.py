#!/usr/bin/env python3
"""
Portfolio Espositori — pagine interne ricalcate sulla reference "Architecture Portfolio".
Copertina e retro restano quelli della versione su griglia.

Schemi di pagina della reference (A4 orizzontale, 297 × 210 mm):
  overview     foto grande a sinistra, colonna di testo e dati a destra
  philosophy   quattro immagini in fila, ognuna con titoletto e testo sotto
  construction colonna di testo a sinistra, disegno grande a destra
  technical    disegno a tutta larghezza, didascalie in basso ai due lati
  space        immagine verticale, seconda immagine, colonna di testo
  creative     griglia 2×2 di immagini, colonna di testo a destra in basso
  urban        foto grande a sinistra, dati + testo + foto piccola a destra
  challenges   testo e foto piccola a sinistra, foto grande a destra
  academic     colonna di testo a sinistra, due foto impilate + una alta a destra

    python3 portfolio_ref.py   ->  portfolio-ref.html
"""
import json
import portfolio_grid as PG
import portfolio_v3 as V3
from portfolio_grid import TBD, AZ, cid, ROOT, BB

W, H = 297, 210
M = 16                    # margine laterale
TOP, BOT = 36, 188        # fascia del contenuto
TIPO, INTRO, ZONE = V3.TIPO, V3.INTRO, V3.ZONE
BANCO, TERRA = V3.BANCO, V3.TERRA


# --------------------------------------------------------------------------
# componenti
# --------------------------------------------------------------------------
def bx(x, y, w=None, h=None):
    s = f"left:{x:.2f}mm;top:{y:.2f}mm"
    if w is not None:
        s += f";width:{w:.2f}mm"
    if h is not None:
        s += f";height:{h:.2f}mm"
    return s


PAD = 256                 # bordo aggiunto alle foto "zoomate indietro" (px su 1024)


def _pad(code):
    """Versione della foto con il fondo prolungato ai lati, per inquadrare l'espositore con più aria."""
    out = ROOT / "img" / "sq" / "pad" / f"{code}.jpg"
    src = ROOT / "img" / "sq" / f"{code}.jpg"
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        import cv2
        im = cv2.imread(str(src))
        import numpy as np
        n = im.shape[0] + 2 * PAD
        # fondo prolungato: versione piccola della foto, bordo ricostruito per diffusione, poi ingrandita e sfocata
        k = 16
        sm = cv2.resize(im, (im.shape[1] // k, im.shape[0] // k), interpolation=cv2.INTER_AREA)
        p = PAD // k
        sp = cv2.copyMakeBorder(sm, p, p, p, p, cv2.BORDER_CONSTANT, value=0)
        mask = np.full(sp.shape[:2], 255, np.uint8)
        mask[p:-p, p:-p] = 0
        sp = cv2.inpaint(sp, mask, 6, cv2.INPAINT_TELEA)
        soft = cv2.GaussianBlur(cv2.resize(sp, (n, n), interpolation=cv2.INTER_CUBIC), (0, 0), 25)
        big = soft.copy()
        big[PAD:PAD + im.shape[0], PAD:PAD + im.shape[1]] = im
        yy, xx = np.mgrid[0:n, 0:n]
        d = np.minimum.reduce([xx - PAD, n - PAD - 1 - xx, yy - PAD, n - PAD - 1 - yy]).astype(float)
        a = np.clip(d / 40, 0, 1)[..., None]        # la foto sfuma nel fondo ricostruito sugli ultimi 40 px
        out.parent.mkdir(exist_ok=True)
        cv2.imwrite(str(out), (big * a + soft * (1 - a)).astype("uint8"), [cv2.IMWRITE_JPEG_QUALITY, 90])
    return f"img/sq/pad/{code}.jpg"


ORIG = json.loads((ROOT / "img" / "orig" / "orig.json").read_text())


SQZOOM = {"B01": 1.18}                   # leggero zoom sulle foto quadrate, per poterle centrare sull'espositore
ZOOM = {"T10": 1.12, "T09": 1.12, "T15": 1.12}   # ingrandimenti mirati per pareggiare la scala tra foto affiancate
SHIFT = {"T15": .04, "T07": .06, "B21": .06}          # spostamento in basso dell'espositore (quota del riquadro), per allineare le basi
FILL = {"T02": .68, "T12": .68, "B19": .8, "B21": .8, "B03": .72, "T01": .78, "B22": .78}  # quota d'altezza del riquadro occupata dall'espositore (come i vicini)


def foto_orig(code, x, y, w, h):
    """Foto originale intera (non quadrata), scalata al minimo per coprire il riquadro: nessun fondo aggiunto."""
    (iw, ih), (a1, b1, a2, b2) = ORIG[code]["size"], ORIG[code]["bb"]
    k0 = max(w / iw, h / ih)
    kz = FILL[code] * h / (b2 - b1) if code in FILL else k0 * ZOOM.get(code, 1)
    k = max(k0, min(kz, .95 * h / (b2 - b1), .95 * w / (a2 - a1)))   # lo zoom non taglia mai l'espositore
    s_w, s_h = iw * k, ih * k
    ix = min(max(w / 2 - (a1 + a2) / 2 * k, w - s_w), 0)
    iy = min(max(h / 2 - (b1 + b2) / 2 * k + SHIFT.get(code, 0) * h, h - s_h), 0)
    return (f'<div class="ph" style="{bx(x, y, w, h)}"><img src="img/orig/{code}.jpg" '
            f'style="{bx(ix, iy, s_w, s_h)}" alt=""></div>')


def foto(code, x, y, w, h, fy=.5, z=1.0):
    """Foto con sfondo fornita, a riempire il riquadro, centrata sull'espositore.
    z < 1 allontana l'inquadratura (min. 0.67): l'espositore occupa meno spazio nel riquadro."""
    if code in ORIG:                          # foto originale fornita intera: nessun ritaglio quadrato
        return foto_orig(code, x, y, w, h)
    a1, b1, a2, b2 = BB[code]
    src, n, off = f"img/sq/{code}.jpg", 1024, 0
    if z < 1:
        src, n, off = _pad(code), 1024 + 2 * PAD, PAD
    s = max(w, h) * z * n / 1024 * SQZOOM.get(code, 1)
    cx = ((a1 + a2) / 2 + off) / n * s
    cy = (b1 + (b2 - b1) * fy + off) / n * s
    ix = min(max(w / 2 - cx, w - s), 0)
    iy = min(max(h / 2 - cy, h - s), 0)
    if (a2 - a1) / n * s > w + .5 or (b2 - b1) / n * s > h + .5:
        print(f"  ! {code}: tagliato in {w:.0f}×{h:.0f}")
    return (f'<div class="ph" style="{bx(x, y, w, h)}"><img src="{src}" style="{bx(ix, iy, s, s)}" alt=""></div>')


def dwg(src, x, y, w, h):
    return f'<div class="dwg" style="{bx(x, y, w, h)}"><img src="{src}" alt=""></div>'


def txt(html, x, y, w, cls="blk"):
    return f'<div class="{cls}" style="{bx(x, y, w)}">{html}</div>'


def blocco(titolo, testo):
    return f'<h4>{titolo}</h4><p>{testo}</p>'


def kv(rows):
    return '<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def prod(code, mf=False):
    """Scheda espositore: codice e tipologia; con mf anche Materiali e Finiture."""
    return (f'<div class="prod"><span class="code">{cid(code)}</span><h4>{TIPO[code]}</h4>'
            + (kv([("Materiali", TBD("[materiali]")), ("Finiture", TBD("[finiture]"))]) if mf else "") + "</div>")


def nomf(code):
    return prod(code, mf=False)


def legenda(codes):
    return '<ul class="leg" style="margin-top:0">' + "".join(f'<li><b>{cid(c)}</b>{TIPO[c]}</li>' for c in codes) + "</ul>"


def tag(code, x, y, w):
    """Numero identificativo sotto l'immagine, da ritrovare nella legenda."""
    return f'<div class="tagc" style="{bx(x, y, w)}">{cid(code)}</div>'


def zona(sez, i):
    t, d = ZONE[sez][i]
    return blocco(t, d)


def pagina(titolo, sezione, corpo, mostra=True):
    """Il titolo di pagina è sempre il nome della sezione; `titolo` resta come argomento degli schemi."""
    return ((f'<div class="ptitle" style="{bx(M, 17)}">{sezione}</div>' if mostra else "")
            + f'<div class="hdr" style="right:{M}mm;top:17mm"><span class="az">{AZ}</span><span class="pill">{sezione}</span></div>'
            + corpo)


# --------------------------------------------------------------------------
# schemi di pagina
# --------------------------------------------------------------------------
def overview(titolo, sez, code, intro, dati, extra="", z=1.0):
    """Foto grande a sinistra, testo + dati a destra (Project Overview)."""
    fw = 150
    fh = BOT - TOP - 8
    if z < 1 and code in ORIG:                # foto originale intera in un riquadro con le sue proporzioni
        (iw, ih), fwi = ORIG[code]["size"], fh * ORIG[code]["size"][0] / ORIG[code]["size"][1]
        img = foto_orig(code, M + 4 + (fw - fwi) / 2, TOP + 4, fwi, fh)
    else:
        img = foto(code, M + 4, TOP + 4, fw, fh, z=z)
    return pagina(titolo, sez, img
                  + txt((f'<h4>{titolo}</h4>' if titolo != sez else '') + f'<p class="lead0">{intro}</p>{extra}', M + fw + 16, TOP + 6, 99)
                  + txt(prod(code) + kv(dati), M + fw + 16, 112, 99))


def overview_dwg(titolo, sez, src, intro, dati, extra=""):
    """Come overview, ma con la tavola tecnica al posto della foto (senza sfondo)."""
    fw = 150                                  # stesse misure e posizioni di overview (apertura banco)
    return pagina(titolo, sez, dwg(src, M + 4, TOP + 4, fw, BOT - TOP - 8)
                  + txt(f'<p class="lead0">{intro}</p>{extra}', M + fw + 16, TOP + 6, 99)
                  + txt(kv(dati), M + fw + 16, 112, 99))


def affianca(sez, a, b, testo, h=126):
    """Foto quadrata e foto verticale originale affiancate alla stessa altezza, didascalie sotto, testo in fondo."""
    iw, ih = ORIG[b]["size"]
    wb = h * iw / ih
    wa = W - 2 * M - 8 - wb - 8
    y = TOP + 4 + h + 5
    return pagina("", sez, foto(a, M + 4, TOP + 4, wa, h) + foto_orig(b, M + 4 + wa + 8, TOP + 4, wb, h)
                  + txt(nomf(a), M + 4, y, wa / 2 - 4) + txt(f'<p class="lead0">{testo}</p>', M + 4 + wa / 2 + 4, y, wa / 2 - 4)
                  + txt(nomf(b), M + 4 + wa + 8, y, wb))


def philosophy(titolo, sez, codes, alto=58):
    """Quattro immagini in fila, sotto a ciascuna la scheda (Design Philosophy)."""
    gap = 6
    w = (W - 2 * M - 8 - 3 * gap) / 4
    corpo = ""
    for i, c in enumerate(codes):
        x = M + 4 + i * (w + gap)
        corpo += foto(c, x, TOP + 4, w, alto) + txt(nomf(c), x, TOP + alto + 10, w)
    return pagina(titolo, sez, corpo)


def construction(titolo, sez, blocchi, src, fig):
    """Colonna di testo a sinistra, disegno grande a destra (Construction)."""
    col = "".join(f'<div class="gap">{blocco(t, d)}</div>' for t, d in blocchi)
    return pagina(titolo, sez, txt(col, M + 4, TOP + 12, 78)
                  + dwg(src, 112, TOP, W - M - 112, BOT - TOP - 8)
                  + txt(f'<p class="fig">{fig}</p>', W - M - 90, BOT - 2, 90, "blk right"))


def technical(titolo, sez, src, sx, dx):
    """Disegno a tutta larghezza, testi in basso ai due lati (Technical Drawings)."""
    return pagina(titolo, sez, dwg(src, M + 4, TOP, W - 2 * M - 8, 122)
                  + txt(sx, M + 4, 164, 110) + txt(dx, W - M - 94, 164, 90, "blk right"))


def space(titolo, sez, a, b, testo):
    """Immagine verticale, seconda immagine accanto, colonna di testo (Space Planning)."""
    return pagina(titolo, sez, foto(a, M + 4, TOP + 4, 66, 144) + foto(b, M + 76, TOP + 4, 106, 144)
                  + txt(testo, M + 192, TOP + 30, 73))


GRAFICA = blocco("Comunicazione", "Fianchi, header e frontali stampati a tutta altezza trasformano la struttura "
                                  "in una superficie di comunicazione per il marchio.")


def coppia(titolo, sez, a, b, testo, h=108):
    """Due immagini verticali affiancate, didascalia subito sotto ciascuna, testo descrittivo sotto le didascalie."""
    w = 90
    xb = M + 4 + w + 8
    y = TOP + 4 + h
    return pagina(titolo, sez, foto(a, M + 4, TOP + 4, w, h) + foto(b, xb, TOP + 4, w, h)
                  + txt(nomf(a), M + 4, y + 5, w) + txt(nomf(b), xb, y + 5, w)
                  + txt(f'<div class="desc">{testo}</div>', M + 4, y + 21, w))


def terzetto(titolo, sez, codes, testo):
    """Tre immagini verticali affiancate, colonna di testo stretta a destra."""
    return pagina(titolo, sez, "".join(foto(c, M + 4 + i * 70, TOP + 4, 64, 144) for i, c in enumerate(codes))
                  + txt(testo, M + 214, TOP + 4, W - 2 * M - 214))


def duo(titolo, sez, *codes, h=126):
    """Due o tre immagini affiancate a tutta larghezza, schede sotto."""
    n, g = len(codes), 6
    w = (W - 2 * M - 8 - (n - 1) * g) / n
    return pagina(titolo, sez, "".join(foto(c, M + 4 + i * (w + g), TOP + 4, w, h, z=.8) + txt(nomf(c), M + 4 + i * (w + g), TOP + h + 9, w)
                                       for i, c in enumerate(codes)))


def tris(sez, big, a, b, h=126):
    """Foto grande e due foto verticali affiancate, alla stessa altezza; numeri sotto e legenda."""
    wb, g = 119, 6
    wa = (W - 2 * M - 8 - wb - 2 * g) / 2
    xs = [M + 4, M + 4 + wb + g, M + 4 + wb + g + wa + g]
    out = foto(big, xs[0], TOP + 4, wb, h) + foto(a, xs[1], TOP + 4, wa, h) + foto(b, xs[2], TOP + 4, wa, h)
    out += "".join(tag(c, x, TOP + h + 6.5, 40) for c, x in zip((big, a, b), xs))
    return pagina("", sez, out + txt(legenda([big, a, b]), xs[1], TOP + h + 13, 140))


def grande(sez, code, testo, h=126):
    """Una foto grande con scheda e testo descrittivo accanto."""
    return pagina("", sez, foto(code, M + 4, TOP + 4, 150, h)
                  + txt(nomf(code) + f'<div class="desc" style="margin-top:8mm">{testo}</div>', M + 170, TOP + 4, 95))


def alto(sez, big, a, b, h=126):
    """Foto grande a sinistra (stessa altezza della pagina a fianco), due foto piccole impilate a destra."""
    wb, s = 156, (h - 6) / 2
    xr = M + 4 + wb + 8
    return pagina("", sez, foto(big, M + 4, TOP + 4, wb, h) + txt(nomf(big), M + 4, TOP + h + 9, wb)
                  + foto(a, xr, TOP + 4, s, s) + txt(nomf(a), xr + s + 4, TOP + 4, W - M - 4 - xr - s - 4)
                  + foto(b, xr, TOP + 10 + s, s, s) + txt(nomf(b), xr + s + 4, TOP + 10 + s, W - M - 4 - xr - s - 4))


def creative(titolo, sez, codes, testo):
    """Griglia 2×2 a sinistra, colonna di testo a destra in basso (Creative Work)."""
    w, h, g = 84, 72, 4                       # righe allineate alle foto impilate di academic
    corpo = "".join(foto(c, M + 4 + (i % 2) * (w + g), TOP + 4 + (i // 2) * (h + g), w, h) for i, c in enumerate(codes))
    xl = M + 2 * w + g + 20
    return pagina(titolo, sez, corpo + txt(legenda(codes[:2]), xl, 88, 40) + txt(legenda(codes[2:]), xl + 43, 88, 40))


def urban(titolo, sez, big, small, testo):
    """Foto grande a sinistra; dati, testo e foto piccola a destra (Urban Design)."""
    h = 126                                   # stessa altezza delle foto della pagina a fianco (duo)
    return pagina(titolo, sez, foto(big, M + 4, TOP + 4, 140, h)
                  + txt(nomf(big) + f'<div class="desc" style="margin-top:8mm">{testo}</div>', M + 156, TOP + 4, 105)
                  + foto(small, M + 156, TOP + 4 + h - 46, 46, 46) + txt(nomf(small), M + 208, TOP + 4 + h - 46, 57))


def challenges(titolo, sez, small, big, testo):
    """Testo e foto piccola a sinistra, foto grande a destra (Design Challenges)."""
    return pagina(titolo, sez, txt(testo + nomf(big) + nomf(small), M + 4, TOP + 4, 88)
                  + foto(small, M + 4, 112, 76, 76)
                  + foto(big, 120, TOP + 4, 145, 144))


def challenges3(titolo, sez, small, big, extra, testo):
    """Come challenges, ma con una seconda foto verticale (originale intera) accanto a quella grande."""
    iw, ih = ORIG[small]["size"]
    hs = TOP + 148 - 100                    # foto piccola verticale, originale intera, base allineata alle foto grandi
    return pagina(titolo, sez, txt(testo + nomf(big) + nomf(extra) + nomf(small), M + 4, TOP + 4, 88)
                  + foto_orig(small, M + 4, 100, hs * iw / ih, hs)
                  + foto(big, 120, TOP + 4, 79, 144) + foto_orig(extra, 205, TOP + 4, 72, 144))


def academic(titolo, sez, a, b, tall, testo):
    """Colonna di testo a sinistra, due foto impilate e una alta a destra (Academic Projects)."""
    return pagina(titolo, sez, txt(testo + "".join(nomf(c) for c in (a, b, tall)), M + 4, TOP + 4, 80)
                  + foto(a, 108, TOP + 4, 72, 72) + foto(b, 108, TOP + 80, 72, 72)
                  + foto(tall, 182, TOP + 4, 83, 148))


# --------------------------------------------------------------------------
# pagine di testo
# --------------------------------------------------------------------------
def introduzione():
    return construction("Introduzione", "Introduzione", [
        ("Chi siamo", f"Dal {TBD('[anno]')} a {TBD('[città]')} progettiamo e produciamo espositori in cartotecnica e "
                      "materiali durevoli, dal primo disegno al bancale pronto a partire."),
        ("Cosa facciamo", "Progettazione strutturale e grafica, prototipi in tempi brevi, stampa offset e digitale, "
                          "fustellatura, incollaggio e confezionamento interni."),
        ("Per chi", "Brand della cosmesi, della farmacia, dell’ottica, della ferramenta e del beverage.")],
        "img/disegni/banco-iso.svg", "Espositore da banco a gradini — assonometria")


def indice():
    voci = [("01", "Introduzione", 4), ("02", "Espositori da banco", 6),
            ("03", "Espositori da terra", 14), ("04", "Contatti", 23)]
    li = "".join(f'<li><span class="n">{n}</span><span class="t">{t}</span><span class="p">{p:02d}</span></li>' for n, t, p in voci)
    return pagina("Indice", "Indice", txt(f'<ul class="toc">{li}</ul>', M + 4, TOP + 10, 150)
                  + txt('<p class="big">Un catalogo illustrativo: le immagini raccontano i progetti, '
                        'le schede riportano solo i dati tecnici essenziali.</p>', 190, TOP + 10, 75))


def chi_siamo():
    fasi = [("01", "Ufficio tecnico", "Studio strutturale, render e tracciati di fustella."),
            ("02", "Prototipazione", "Campioni bianchi e stampati per testare carico e montaggio."),
            ("03", "Produzione", "Stampa, fustellatura, incollaggio e confezionamento interni."),
            ("04", "Logistica", "Spedizione piatta o premontata, in Italia e all’estero.")]
    gap = 6
    w = (W - 2 * M - 8 - 3 * gap) / 4
    corpo = ""
    for i, (n, t, d) in enumerate(fasi):
        x = M + 4 + i * (w + gap)
        corpo += (dwg(f"img/disegni/chi-{n}.svg", x, TOP + 4, w, 58).replace('class="dwg"', 'class="dwg mult"')
                  + f'<div class="tagc" style="{bx(x, TOP + 68)}">{n}</div>' + txt(blocco(t, d), x, TOP + 72, w))
    corpo += txt(settori(), M + 4, 150, 120) + txt(chips(), W - M - 4 - 120, 150, 120)
    return pagina("", "Introduzione", corpo, mostra=False)


METODO_TXT = ("Tutto parte da un confronto con il cliente: ascoltiamo il prodotto, il punto vendita e gli obiettivi. "
              "Da qui sviluppiamo un’idea, la trasformiamo in una bozza e poi in un prototipo da toccare con mano. "
              "Quando ogni dettaglio è a posto passiamo alla produzione: seguiamo l’intero processo, "
              "dal primo incontro alla consegna.")
METODO_NOTA = ("Espositori da banco e da terra per ogni tipologia di esigenza e di applicazione: "
               "studiati, progettati e realizzati con cura e professionalità.")
CHI_FRASE = "Un unico interlocutore, dall’idea al punto vendita."
SETTORI = ["Cosmesi", "Farmacia", "Ottica", "Food &amp; beverage", "Ferramenta", "Moda e accessori", "Elettronica", "Pet care"]
FINITURE = (blocco("Stampa e finiture",
                   "Ogni espositore nasce per farsi notare: stampa e nobilitazioni trasformano il cartone in una superficie "
                   "di marca. Stampiamo in offset e in digitale su cartoncini e ondulati, in quadricromia e a colori Pantone, "
                   "e completiamo la grafica con lavorazioni che aggiungono luce, profondità e tatto.")
            + '<ul class="fin">' + "".join(f"<li>{v}</li>" for v in [
                "Stampa offset e digitale", "Colori Pantone e metallizzati", "Plastificazione opaca, lucida e soft-touch",
                "Vernice UV lucida, opaca e selettiva", "UV a spessore e effetti 3D", "Lamina a caldo e a freddo",
                "Rilievi e bassorilievi a secco", "Effetti glitter e perlescenti", "Carte speciali, naturali e goffrate",
                "Accoppiatura su microonda e alveolare", "Finestre in PET e fustellati sagomati",
                "Grafiche a tutta altezza e a vivo"]) + "</ul>")


def settori():
    return f'<p class="big">{CHI_FRASE}</p>'


def chips():
    return '<h4>Settori</h4><div class="chips">' + "".join(f"<span>{s}</span>" for s in SETTORI) + "</div>"


INTRO_IMG = [("img/intro-schizzo.png", 1364 / 2352, ""), ("img/intro-bianco.jpg", 320 / 1072, " mult"),
             ("img/intro-finito.jpg", 430 / 1378, " mult")]


def tre_fasi(x0, larg, base, H, finale=1.18, giu=.04):
    """Schizzo, espositore bianco ed espositore finito sulla stessa linea di base, con i centri equidistanti;
    l'ultimo (il risultato) un po' più grande e appena più in basso, così non sembra sollevato."""
    hs = [H, H, H * finale]
    ws = [r * h for (_, r, _), h in zip(INTRO_IMG, hs)]
    c0, c2 = x0 + ws[0] / 2, x0 + larg - ws[2] / 2
    centri = [c0, (c0 + c2) / 2, c2]
    basi = [base, base, base + H * giu]
    out = ""
    for (src, _, cls), w, h, c, y in zip(INTRO_IMG, ws, hs, centri, basi):
        out += f'<div class="dwg{cls}" style="{bx(c - w / 2, y - h, w, h)}"><img src="{src}" alt=""></div>'
    return out


def metodo():
    """Introduzione: dal progetto alla realizzazione, con schizzo e prodotto finito."""
    intro = (f'<h4>Dal progetto alla realizzazione</h4><p class="metodo">' + METODO_TXT + "</p>")
    fasi = "".join(f'<div class="fase"><span>0{i + 1}</span>{blocco(t, d)}</div>' for i, (t, d) in enumerate([
        ("Schizzo", "Proporzioni, ingombri e altezze dei ripiani."),
        ("Disegno tecnico", "Tracciati di fustella e render 3D."),
        ("Prototipo", "Campione fisico, test di carico e montaggio."),
        ("Produzione", "Stampa, fustellatura e confezionamento interni.")]))
    return pagina("Dal progetto alla realizzazione", "Introduzione",
                  tre_fasi(M + 8, 180, TOP + 134, 105)
                  + txt(intro + fasi + f'<p class="note2">{METODO_NOTA}</p>', 218, TOP + 2, 63))


def contatti():
    rows = [("Telefono", TBD("+39 000 000 0000")), ("Email", TBD("info@azienda.it")),
            ("Indirizzo", TBD("Via Esempio 1, 00000 Città (XX)")), ("Web", TBD("www.azienda.it"))]
    return pagina("Contatti", "Contatti", txt('<p class="big">Il prossimo progetto parte da un brief. Raccontaci il prodotto, '
                                              'il punto vendita, le quantità e i tempi.</p>', M + 4, TOP + 10, 120)
                  + txt(kv(rows), 170, TOP + 10, 95, "blk contacts"))


# --------------------------------------------------------------------------
def build():
    B, T = BANCO, TERRA
    zb = lambda i: f'<div class="gap">{zona(B, i)}</div>'
    zt = lambda i: f'<div class="gap">{zona(T, i)}</div>'
    interne = [
        indice(), metodo(), chi_siamo(),
        overview("Espositori da banco", B, "B13", INTRO[B],
                 [("Materiali", "Cartone, cartoncino, forex, plexi, legno"),
                  ("Montaggio", "Pochi secondi, senza colla")]),
        philosophy("Progetti", B, ["B02", "B17", "B09", "B11"]),
        urban("Stampa e finiture", B, "B12", "B16", FINITURE),
        alto(B, "B04", "B21", "B19"),
        creative("Su misura", B, ["B06", "B05", "B01", "B10"], zb(3)),
        grande(B, "B15", f"<p>{ZONE[B][0][1]}</p>"),
        tris(B, "B03", "B22", "B23"),
        academic("Materiali", B, "B20", "B08", "B07", zb(1)),
        overview_dwg("Espositori da terra", T, "img/disegni/terra-tavola.svg", INTRO[T],
                     [("Altezze", "Da 140 a 180 cm"), ("Ripiani", "Da 3 a 5, con header"), ("Spedizione", "Piatta, montaggio in pochi minuti")]),
        overview("Logistica", T, "T05", ZONE[T][3][1], []),
        coppia("Portata", T, "T08", "T13", blocco("Portata", ZONE[T][0][1])),
        coppia("Forme", T, "T14", "T09", blocco("Forme", "Vani incassati e fianchi sagomati: la struttura diventa parte del racconto del marchio, senza rinunciare alla portata.")),
        coppia("Ripiani", T, "T15", "T07", blocco("Ripiani", "Fianchi inclinati, ripiani a vista e header sagomato: struttura leggera, grafica a tutta superficie.")),
        coppia("Grafica e brand", T, "T10", "T11", GRAFICA),
        coppia("Progetti", T, "T01", "T02", blocco("Materiali", ZONE[T][1][1])),
        coppia("Colonna", T, "T12", "T03", blocco("Colonna", "Colonna stretta con ripiani laterali: poco ingombro a terra e grafica a tutta altezza.")),
        coppia("Stampa e finiture", T, "T04", "T06", blocco("Stampa e finiture", ZONE[T][2][1])),
        contatti(),
    ]
    # pagina bianca provvisoria prima della copertina (da rimuovere in seguito): la copertina resta pagina 1
    pages = [("blank pre", ""), ("grid", PG.copertina()), ("blank", "")] + [("ref", p) for p in interne] + [("grid", PG.retro())]
    tot = len(pages)
    html = []
    for i, (cls, body) in enumerate(pages, start=0):
        side = "pr" if i % 2 else "pl"
        foot = "" if cls.split()[0] in ("grid", "blank") else (f'<div class="pn" style="{bx(M, 192)}">{i:02d}</div>'
                                         f'<div class="ft" style="right:{M}mm;top:194mm">Portfolio Espositori 2026</div>')
        html.append(f'<section class="page {side} {cls}">{body}{foot}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio-grid.css">
<link rel="stylesheet" href="portfolio-v2.css">
<link rel="stylesheet" href="portfolio-ref.css">
</head><body><main class="book pre">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-ref.html").write_text(doc, encoding="utf-8")
    print("portfolio-ref.html:", tot, "pagine")


if __name__ == "__main__":
    build()
