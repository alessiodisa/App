#!/usr/bin/env python3
"""
Portfolio Espositori — A4 verticale (210 × 297 mm), impaginato a doppia pagina.

    python3 portfolio_a4.py   ->  portfolio-a4.html
"""
from portfolio import PROGETTI, DESCR, BB, ROOT

W, H, M = 210, 297, 15
CW = W - 2 * M
AZ = '<span class="tbd">[Nome Azienda]</span>'
BANCO, TERRA = "Espositori da banco", "Espositori da terra"


def TBD(s):
    return f'<span class="tbd">{s}</span>'


def bx(x, y, w=None, h=None):
    s = f"left:{x:.2f}mm;top:{y:.2f}mm"
    if w is not None:
        s += f";width:{w:.2f}mm"
    if h is not None:
        s += f";height:{h:.2f}mm"
    return s


def cid(c):
    return f"{c[0]}.{c[1:]}"


def photo(code, frame, zoom=1.0, fy=None, cls=""):
    """Foto quadrata dentro un riquadro, centrata sull'espositore e ritagliata
    senza lasciare vuoti. zoom > 1 ingrandisce; fy sposta il centro verticale (0–1 del soggetto)."""
    fx, fyy, fw, fh = frame
    s = max(fw, fh) * zoom
    x1, y1, x2, y2 = BB[code]
    cx = (x1 + x2) / 2 / 1024 * s
    cy = (y1 + (y2 - y1) * (fy if fy is not None else .5)) / 1024 * s
    ix = min(max(fx + fw / 2 - cx, fx + fw - s), fx)
    iy = min(max(fyy + fh / 2 - cy, fyy + fh - s), fyy)
    return (f'<div class="frame {cls}" style="{bx(fx, fyy, fw, fh)}">'
            f'<img src="img/sq/{code}.jpg" style="{bx(ix - fx, iy - fyy, s, s)}" alt=""></div>')


def title(code, x, y, w, size="t1"):
    tt, tip, sett = PROGETTI[code]
    return (f'<div class="{size}" style="{bx(x, y, w)}">{tt}<span class="n">/{cid(code)}</span></div>')


def spec(code, x, y, w):
    tt, tip, sett = PROGETTI[code]
    return (f'<dl class="spec" style="{bx(x, y, w)}"><dt>Tipologia</dt><dd>{tip}</dd><dt>Settore</dt><dd>{sett}</dd>'
            f'<dt>Materiale</dt><dd>{TBD("[materiale]")}</dd><dt>Cliente</dt><dd>{TBD("[cliente]")}</dd></dl>')


def cap(code, x, y, w):
    tt, tip, sett = PROGETTI[code]
    return (f'<div class="cap" style="{bx(x, y, w)}"><b>{cid(code)}</b>&ensp;{tt}'
            f'<span>{tip}</span></div>')


def descr(code):
    return DESCR.get(code) or PROGETTI[code][1] + ". " + TBD("[Descrizione del progetto: esigenza, soluzione, risultato.]")


def txt(html, x, y, w, cls="body"):
    return f'<div class="{cls}" style="{bx(x, y, w)}">{html}</div>'


def lbl(s, x, y):
    return f'<div class="lbl" style="{bx(x, y)}">{s}</div>'


# --------------------------------------------------------------------------
# doppie pagine
# --------------------------------------------------------------------------
def feature(a, b=None, c=None, sez=""):
    """Foto al vivo a sinistra; a destra due foto piccole, testo e titolo grande."""
    sx = photo(a, (0, 0, W, H), zoom=1.0)
    dx = lbl("Progetto in evidenza", M, 26)
    if b and c:
        dx += photo(b, (M, 34, 87, 87)) + photo(c, (M + 95, 34, 87, 87))
        dx += cap(b, M, 124, 87) + cap(c, M + 95, 124, 87)
    else:
        dx += photo(a, (M, 34, CW, 120), zoom=2.1, fy=.2)
        dx += txt("Dettaglio: header e primo ripiano", M, 157, CW, "cap-s")
    ty = 142 if (b and c) else 172
    dx += txt(descr(a), M, ty, 87) + txt(
        "Ogni scelta strutturale parte dal prodotto: peso, ingombro, numero di facing e tempo di permanenza nel punto vendita.",
        M + 95, ty, 87)
    dx += title(a, M, 200, CW) + spec(a, M, 236, CW)
    return [("bleed", sx), ("", dx)]


def racconto(a, b, c, sez=""):
    """Sinistra: testo, foto grande e foto piccola. Destra: titolo in alto e foto al vivo sotto."""
    sx = lbl("Progetti", M, 26)
    sx += txt(descr(a), M, 34, 85) + txt(
        "La struttura è pensata per montarsi in pochi gesti e restare stabile anche a pieno carico.", M + 97, 34, 85)
    sx += photo(b, (M, 72, 120, 120)) + photo(c, (M + 126, 136, 56, 56))
    sx += cap(b, M, 195, 120) + cap(c, M + 126, 195, 56)
    sx += txt("Forme semplici, materiali pensati per il punto vendita, grafica al servizio del prodotto.", M, 232, 150, "quote")
    dx = title(a, M, 26, CW, "t1 big") + spec(a, M, 62, CW)
    dx += photo(a, (0, 92, W, H - 92))
    return [("", sx), ("", dx)]


def collage(a, b, c, d, sez=""):
    """Due progetti per pagina, foto di misure diverse."""
    sx = photo(a, (M, 26, 120, 120)) + photo(b, (M + 126, 26, 56, 56))
    sx += cap(b, M + 126, 85, 56)
    sx += title(a, M, 158, CW) + txt(descr(a), M, 180, 110) + spec(a, M, 214, 120)
    dx = photo(c, (M, 26, 86, 150), fy=.5) + photo(d, (M + 96, 26, 86, 86))
    dx += cap(d, M + 96, 115, 86)
    dx += title(c, M + 96, 140, 86, "t1 sm") + txt(descr(c), M + 96, 160, 86) + spec(c, M + 96, 196, 86)
    return [("", sx), ("", dx)]


def fila(codes, titolo, sez=""):
    """Fila di foto verticali (espositori da terra), tre per pagina."""
    out = []
    for p in range(2):
        body = ""
        if p == 0:
            body += f'<div class="t1 big" style="{bx(M, 24, CW)}">{titolo}</div>'
            body += txt("Colonne autoportanti: la comunicazione sale sopra il prodotto e si legge anche dal fondo della corsia.", M, 48, 110)
        else:
            body += txt("Stesso principio, proporzioni diverse: ripiani, ganci, vaschette e mensole a sbalzo secondo il prodotto.", M + 72, 30, 110)
        for i, c in enumerate(codes[p * 3:(p + 1) * 3]):
            x = M + i * 62.3
            body += photo(c, (x, 70, 57.3, 160))
            body += cap(c, x, 234, 57.3) + txt(TBD("[materiale]"), x, 248, 57.3, "cap-s")
        out.append(("", body))
    return out


def apertura(num, titolo, testo, hero, codes, pages):
    sx = photo(hero, (0, 0, W, H))
    idx = "".join(f"<li><b>{cid(c)}</b>{PROGETTI[c][0]}<span>{pages[c]:02d}</span></li>" for c in codes)
    dx = (f'<div class="bignum" style="{bx(M - 2, 22)}">{num}</div>'
          f'<div class="t1 big" style="{bx(M, 78, CW)}">{titolo}</div>'
          + txt(testo, M, 112, 120, "lead")
          + f'<ul class="idx" style="{bx(M, 160, CW)}">{idx}</ul>')
    return [("bleed", sx), ("", dx)]


def copertina():
    return ("bleed", photo("B06", (0, 0, W, 200), zoom=1.05)
            + f'<div class="panel dark" style="{bx(0, 168, 140, 129)}">'
              f'<div class="lbl w">{AZ}</div><div class="cover-t">Portfolio<br><b>Espositori</b></div>'
              f'<div class="lbl w">Cartotecnica · Espositori · Materiali durevoli</div></div>'
            + f'<div class="panel mid" style="{bx(140, 250, 70, 47)}"><div class="year">/ 2026</div></div>')


def indice_chi_siamo(pages):
    voci = [("01", "Espositori da banco", pages["B01"]), ("02", "Espositori da terra", pages["T05"]), ("", "Contatti", pages["contatti"])]
    li = "".join(f"<li><b>{n}</b>{t}<span>{p:02d}</span></li>" for n, t, p in voci)
    sx = (f'<div class="panel light" style="{bx(0, 0, W, H)}"></div>'
          f'<div class="t1 big" style="{bx(M, 120, CW)}">Indice</div>'
          f'<ul class="idx big" style="{bx(M + 60, 118, 122)}">{li}</ul>'
          + photo("B03", (M + 60, 190, 122, 80)))
    dx = (f'<div class="t1 big right" style="{bx(M, 26, CW)}">Chi siamo</div>'
          + txt(f"Dal {TBD('[anno]')} progettiamo e produciamo espositori in cartotecnica e materiali durevoli: dal primo disegno al bancale pronto a partire.", M + 70, 50, 112, "lead")
          + f'<div class="circle" style="{bx(M, 100, 88, 88)}">{photo("B09", (0, 0, 88, 88))}</div>'
          + txt(f"Seguiamo ogni progetto internamente: ufficio tecnico, campionatura, stampa, fustellatura, incollaggio e confezionamento. Un unico interlocutore significa tempi più rapidi e controllo costante sulla qualità.", M + 100, 104, 82)
          + txt("Ogni espositore parte da una domanda semplice: dove verrà visto, da chi, per quanto tempo. Da lì scegliamo struttura, materiale e finiture, prototipiamo, testiamo e solo allora produciamo.", M + 100, 146, 82)
          + f'<div class="stats" style="{bx(M, 214, CW)}"><div><b>{TBD("35+")}</b>Anni di esperienza</div>'
            f'<div><b>{TBD("400")}</b>Progetti all’anno</div><div><b>100%</b>Prodotto internamente</div></div>')
    return [("", sx), ("", dx)]


def contatti():
    sx = (f'<div class="t1 big" style="{bx(M, 26, CW)}">Contatti</div>'
          + txt("Ogni progetto di questo portfolio è nato da un brief. Il prossimo può essere il tuo.", M, 52, 130, "lead")
          + f'<dl class="spec big" style="{bx(M, 200, CW)}"><dt>Email</dt><dd>{TBD("info@azienda.it")}</dd><dt>Telefono</dt><dd>{TBD("+39 000 000 0000")}</dd>'
            f'<dt>Sede</dt><dd>{TBD("Via Esempio 1, Città")}</dd><dt>Web</dt><dd>{TBD("www.azienda.it")}</dd></dl>')
    dx = photo("B17", (0, 0, W, H))
    return [("", sx), ("bleed", dx)]


def retro():
    return ("", f'<div class="panel mid" style="{bx(0, 0, W, H)}"></div>'
                f'<div class="lbl w" style="{bx(M, 140, CW)};text-align:center">{AZ}<br><br>Portfolio Espositori 2026</div>')


# --------------------------------------------------------------------------
def build():
    # piano delle doppie pagine: (funzione, argomenti, sezione)
    spreads = [
        (indice_chi_siamo, "idx", ""),
        (apertura, ("01", "Espositori<br>da banco", "Il punto più vicino alla scelta: strutture compatte che portano il prodotto all’altezza dello sguardo, accanto alla cassa.", "B01"), BANCO),
        (feature, ("B02", "B03", "B04"), BANCO),
        (racconto, ("B06", "B05", "B08"), BANCO),
        (collage, ("B09", "B13", "B07", "B17"), BANCO),
        (feature, ("B11", "B10", "B12"), BANCO),
        (racconto, ("B14", "B15", "B16"), BANCO),
        (apertura, ("02", "Espositori<br>da terra", "Strutture autoportanti a più ripiani, pensate per reggere il carico e farsi vedere da lontano.", "T05"), TERRA),
        (fila, (["T01", "T02", "T03", "T04", "T06", "T07"], "Colonne da terra"), TERRA),
        (feature, ("T08",), TERRA),
        (contatti, (), ""),
    ]
    codes_of = {apertura: lambda a: [a[3]], feature: lambda a: list(a), racconto: lambda a: list(a),
                collage: lambda a: list(a), fila: lambda a: list(a[0])}
    pages, n = {}, 2
    for fn, args, _ in spreads:
        if fn in codes_of:
            for c in codes_of[fn](args):
                pages.setdefault(c, n)
        if fn is contatti:
            pages["contatti"] = n
        n += 2
    for fn, args, _ in spreads:           # indice di sezione: tutte le tavole
        pass
    out = [("cover", copertina(), "")]
    for fn, args, sez in spreads:
        if fn is indice_chi_siamo:
            pp = indice_chi_siamo(pages)
        elif fn is apertura:
            num, titolo, testo, hero = args
            sc = [c for c in PROGETTI if c[0] == hero[0]]
            pp = apertura(num, titolo, testo, hero, sc, pages)
        else:
            pp = fn(*args)
        for cls, body in pp:
            out.append((cls, body, sez))
    out.append(retro() + ("",))
    tot = len(out)
    html = []
    for i, (cls, body, sez) in enumerate(out, start=1):
        side = "pr" if i % 2 else "pl"
        hdr = ""
        if cls not in ("cover", "bleed") and i != tot:
            hdr = (f'<div class="hd" style="{bx(M, 11, CW)}"><span>{AZ} — Portfolio Espositori</span><span>{sez}</span></div>'
                   f'<div class="ft" style="{bx(M, 284, CW)}"><span>{i:02d}</span></div>')
        html.append(f'<section class="page {side} {cls}">{body}{hdr}\n</section>')
    doc = f"""<!DOCTYPE html>
<html lang="it"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori A4</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="portfolio-a4.css">
</head><body><main class="book">
{chr(10).join(html)}
</main></body></html>
"""
    (ROOT / "portfolio-a4.html").write_text(doc, encoding="utf-8")
    print("portfolio-a4.html:", tot, "pagine")


if __name__ == "__main__":
    build()
