"""File per la tipografia, dal PDF a video (24 facciate A4):
copertina (I-IV, II e III bianche), interno (20 facciate), maschera della vernice lucida (solo I).
Tutti con 3 mm di abbondanza, crocini, TrimBox e BleedBox."""
import sys, pymupdf

MM = 72 / 25.4
B, OFF, L = 3 * MM, 3 * MM, 5 * MM          # abbondanza, distanza crocini dal rifilo, lunghezza crocini
E = B + OFF + L


def con_abbondanza(src, pagine, out, estendi=True):
    n = pymupdf.open()
    for i in pagine:
        p = src[i]
        W, H = p.rect.width, p.rect.height
        q = n.new_page(width=W + 2 * E, height=H + 2 * E)
        if estendi:                             # i fondi proseguono oltre il rifilo
            q.show_pdf_page(pymupdf.Rect(E - B, E - B, E + W + B, E + H + B), src, i)
        q.show_pdf_page(pymupdf.Rect(E, E, E + W, E + H), src, i)
        for r in [(0, 0, W + 2 * E, E - B), (0, E + H + B, W + 2 * E, H + 2 * E),
                  (0, 0, E - B, H + 2 * E), (E + W + B, 0, W + 2 * E, H + 2 * E)]:
            q.draw_rect(pymupdf.Rect(*r), color=None, fill=(1, 1, 1), overlay=True)
        for x in (E, E + W):
            q.draw_line((x, 0), (x, L), color=(0, 0, 0), width=.25)
            q.draw_line((x, H + 2 * E - L), (x, H + 2 * E), color=(0, 0, 0), width=.25)
        for y in (E, E + H):
            q.draw_line((0, y), (L, y), color=(0, 0, 0), width=.25)
            q.draw_line((W + 2 * E - L, y), (W + 2 * E, y), color=(0, 0, 0), width=.25)
        q.set_trimbox(pymupdf.Rect(E, E, E + W, E + H))
        q.set_bleedbox(pymupdf.Rect(E - B, E - B, E + W + B, E + H + B))
    n.save(out, garbage=3, deflate=True)
    return len(n)


BANDELLA = 100 * MM                              # aletta della copertina, ripiegata all'interno


def copertina_bandelle(src, fondo, out, maschera=None, dorso=0.0):
    """Copertina stesa, lato esterno: bandella retro | IV | dorso | I | bandella prima.
    La bandella della I si ripiega verso destra, quella della IV verso sinistra.
    Con `maschera` produce la stessa stesa per la vernice lucida (solo la I, fondo bianco)."""
    W, H = src[0].rect.width, src[0].rect.height
    pannelli = [BANDELLA, W, dorso, W, BANDELLA]
    TW = sum(pannelli)
    n = pymupdf.open()
    q = n.new_page(width=TW + 2 * E, height=H + 2 * E)
    x = [E]
    for w in pannelli:
        x.append(x[-1] + w)                     # x[0] bordo sinistro ... x[5] bordo destro
    if maschera is None:
        # fondo continuo (griglia della copertina) su tutta la stesa, abbondanze comprese
        q.show_pdf_page(pymupdf.Rect(x[0] - B, E - B, x[1], E + H + B), fondo, 0, clip=pymupdf.Rect(W - BANDELLA - B, 0, W, H))
        q.show_pdf_page(pymupdf.Rect(x[1], E - B, x[2], E + H + B), fondo, 0)
        if dorso:
            q.draw_rect(pymupdf.Rect(x[2], E - B, x[3], E + H + B), color=None, fill=(.941, .941, .933))
        q.show_pdf_page(pymupdf.Rect(x[3], E - B, x[4], E + H + B), fondo, 0)
        q.show_pdf_page(pymupdf.Rect(x[4], E - B, x[5] + B, E + H + B), fondo, 0, clip=pymupdf.Rect(0, 0, BANDELLA + B, H))
        q.show_pdf_page(pymupdf.Rect(x[1], E, x[2], E + H), src, len(src) - 1)     # IV di copertina (retro)
        q.show_pdf_page(pymupdf.Rect(x[3], E, x[4], E + H), src, 0)                # I di copertina
    else:
        q.show_pdf_page(pymupdf.Rect(x[3], E, x[4], E + H), maschera, 0)
    for r in [(0, 0, TW + 2 * E, E - B), (0, E + H + B, TW + 2 * E, H + 2 * E),
              (0, 0, E - B, H + 2 * E), (E + TW + B, 0, TW + 2 * E, H + 2 * E)]:
        q.draw_rect(pymupdf.Rect(*r), color=None, fill=(1, 1, 1), overlay=True)
    nero = (0, 0, 0)
    for xx in (x[0], x[5]):                     # crocini di taglio
        q.draw_line((xx, 0), (xx, L), color=nero, width=.25)
        q.draw_line((xx, H + 2 * E - L), (xx, H + 2 * E), color=nero, width=.25)
    for y in (E, E + H):
        q.draw_line((0, y), (L, y), color=nero, width=.25)
        q.draw_line((TW + 2 * E - L, y), (TW + 2 * E, y), color=nero, width=.25)
    pieghe = [x[1], x[2], x[4]] + ([x[3]] if dorso else [])
    for xx in pieghe:                            # segni di piega, tratteggiati
        q.draw_line((xx, 0), (xx, L), color=nero, width=.25, dashes="[1.5 1.5] 0")
        q.draw_line((xx, H + 2 * E - L), (xx, H + 2 * E), color=nero, width=.25, dashes="[1.5 1.5] 0")
    q.set_trimbox(pymupdf.Rect(E, E, E + TW, E + H))
    q.set_bleedbox(pymupdf.Rect(E - B, E - B, E + TW + B, E + H + B))
    if maschera is None:                         # lato interno della copertina: bianco, non stampato
        r = n.new_page(width=TW + 2 * E, height=H + 2 * E)
        r.set_trimbox(pymupdf.Rect(E, E, E + TW, E + H))
    n.save(out, garbage=3, deflate=True)
    return round(TW / MM)


if __name__ == "__main__":
    bozza, lucido, fondo, cartella = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    d, m, f = pymupdf.open(bozza), pymupdf.open(lucido), pymupdf.open(fondo)
    assert len(d) == 24, len(d)
    print("copertina stesa (mm)", copertina_bandelle(d, f, f"{cartella}/01-copertina.pdf"))
    print("interno", con_abbondanza(d, range(2, 22), f"{cartella}/02-interno.pdf"))
    print("lucido (mm)", copertina_bandelle(d, f, f"{cartella}/03-copertina-vernice-lucida.pdf", maschera=m))
