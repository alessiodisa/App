"""PDF finali: tolta la pagina bianca provvisoria; versione di stampa con 3 mm di abbondanza e crocini."""
import sys, pymupdf
src, out, stampa = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None
mm = 72 / 25.4
d = pymupdf.open(src); d.delete_page(0); d.save(out, garbage=3, deflate=True)
if stampa:
    B, OFF, L = 3 * mm, 3 * mm, 5 * mm            # abbondanza, distanza crocini dal rifilo, lunghezza crocini
    E = B + OFF + L                               # margine totale attorno al formato rifilato
    n = pymupdf.open()
    for i, p in enumerate(d):
        W, H = p.rect.width, p.rect.height
        q = n.new_page(width=W + 2 * E, height=H + 2 * E)
        # abbondanza: la stessa pagina leggermente ingrandita dietro, così i fondi proseguono oltre il rifilo
        q.show_pdf_page(pymupdf.Rect(E - B, E - B, E + W + B, E + H + B), d, i)
        q.show_pdf_page(pymupdf.Rect(E, E, E + W, E + H), d, i)
        # bianco fuori dall'abbondanza
        for r in [(0, 0, W + 2 * E, E - B), (0, E + H + B, W + 2 * E, H + 2 * E),
                  (0, 0, E - B, H + 2 * E), (E + W + B, 0, W + 2 * E, H + 2 * E)]:
            q.draw_rect(pymupdf.Rect(*r), color=None, fill=(1, 1, 1), overlay=True)
        # crocini di taglio
        for x in (E, E + W):
            q.draw_line((x, 0), (x, L), color=(0, 0, 0), width=.25); q.draw_line((x, H + 2 * E - L), (x, H + 2 * E), color=(0, 0, 0), width=.25)
        for y in (E, E + H):
            q.draw_line((0, y), (L, y), color=(0, 0, 0), width=.25); q.draw_line((W + 2 * E - L, y), (W + 2 * E, y), color=(0, 0, 0), width=.25)
        q.set_trimbox(pymupdf.Rect(E, E, E + W, E + H)); q.set_bleedbox(pymupdf.Rect(E - B, E - B, E + W + B, E + H + B))
    n.save(stampa, garbage=3, deflate=True)
print(len(d), "pagine")
