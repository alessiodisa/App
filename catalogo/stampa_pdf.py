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


if __name__ == "__main__":
    bozza, lucido, cartella = sys.argv[1], sys.argv[2], sys.argv[3]
    d, m = pymupdf.open(bozza), pymupdf.open(lucido)
    assert len(d) == 24, len(d)
    print("copertina", con_abbondanza(d, [0, 1, 22, 23], f"{cartella}/01-copertina.pdf"))
    print("interno", con_abbondanza(d, range(2, 22), f"{cartella}/02-interno.pdf"))
    print("lucido", con_abbondanza(m, [0], f"{cartella}/03-copertina-vernice-lucida.pdf", estendi=False))
