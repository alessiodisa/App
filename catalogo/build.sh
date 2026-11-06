#!/bin/bash
# Rigenera il catalogo verticale e tutti i file finali (a video, digitale, stampa, zip).
#   bash build.sh
# Richiede: python3 con pymupdf, pillow, numpy, scipy; Chromium (Playwright) per HTML -> PDF.
set -e
cd "$(dirname "$0")"
CHROME=$(ls /opt/pw-browsers/chromium-*/chrome-linux*/chrome 2>/dev/null | head -1)
[ -x "$CHROME" ] || CHROME=$(command -v chromium || command -v google-chrome)
pdf() { "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 --print-to-pdf="$2" "file://$PWD/$1" 2>/dev/null; }
mkdir -p build stampa

# 1. catalogo verticale (HTML -> PDF di lavoro, con pagina bianca provvisoria in testa)
python3 portfolio_ref_v.py
pdf portfolio-ref-v.html build/portfolio-ref-v.pdf

# 2. PDF a video (24 facciate) e PDF unico con abbondanze
python3 finale_pdf.py build/portfolio-ref-v.pdf portfolio-ref-verticale-bozza.pdf portfolio-ref-verticale-stampa.pdf

# 3. maschera vernice lucida e fondo neutro della copertina (per le bandelle)
python3 stampa_lucido.py
pdf copertina-lucido.html build/lucido.pdf
python3 - <<'PY'
import re
from pathlib import Path
s = Path("portfolio-ref-v.html").read_text(encoding="utf-8")
sec = [m.start() for m in re.finditer(r'<section class="page', s)]
cov = s[sec[1]:sec[2]]
Path("copertina-fondo.html").write_text(s[:s.index("<body")] + '<body><main class="book">' + cov[:cov.index(">") + 1]
                                        + "\n</section></main></body></html>", encoding="utf-8")
PY
pdf copertina-fondo.html build/fondo.pdf

# 4. file per la tipografia: copertina stesa con bandelle, interno, lucido, scheda
python3 stampa_pdf.py portfolio-ref-verticale-bozza.pdf build/lucido.pdf build/fondo.pdf stampa
pdf stampa/scheda-di-stampa.html stampa/04-scheda-di-stampa.pdf
(cd stampa && rm -f ../catalogo-espositori-2027-stampa.zip && zip -q ../catalogo-espositori-2027-stampa.zip \
    01-copertina.pdf 02-interno.pdf 03-copertina-vernice-lucida.pdf 04-scheda-di-stampa.pdf)

# 5. versione digitale (senza pagine bianche) e panoramica a doppie pagine
python3 - <<'PY'
import pymupdf
from PIL import Image
d = pymupdf.open("portfolio-ref-verticale-bozza.pdf")
ims = []
for p in d:
    x = p.get_pixmap(dpi=36); ims.append(Image.frombytes("RGB", (x.width, x.height), x.samples))
w, h = ims[0].size; g = 14
sp = [[None, ims[0]]] + [[ims[i], ims[i + 1]] for i in range(1, len(ims) - 1, 2)] + [[ims[-1], None]]
cols = 4; rows = (len(sp) + cols - 1) // cols
sh = Image.new("RGB", (cols * (2 * w + g) + g, rows * (h + g) + g), (207, 205, 201))
for k, s in enumerate(sp):
    for j, im in enumerate(s):
        if im: sh.paste(im, (g + (k % cols) * (2 * w + g) + j * w, g + (k // cols) * (h + g)))
sh.save("catalogo-panoramica.png")
bianche = [i for i, p in enumerate(d) if not p.get_text().strip()
           and min(p.get_pixmap(dpi=10, colorspace=pymupdf.csGRAY).samples) >= 250]
d.delete_pages(bianche)
d.set_metadata({"title": "Catalogo Espositori 2027", "author": "Onprint", "subject": "Catalogo espositori da banco e da terra"})
d.save("catalogo-espositori-2027-digitale.pdf", garbage=4, deflate=True)
print("digitale:", len(d), "pagine")
PY
echo "fatto"
