"""Maschera per la vernice UV lucida selettiva della copertina: nero 100% dove va il lucido
(linee del disegno esploso e titolo CATALOGO ESPOSITORI), bianco altrove. Stessa impaginazione della copertina."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
s = (ROOT / "portfolio-ref-v.html").read_text(encoding="utf-8")
head = s[:s.index("<body")]
sec = [m.start() for m in re.finditer(r'<section class="page', s)]
cov = s[sec[1]:sec[2]]
keep = re.findall(r'<img class="drawing"[^>]*>|<div class="light-t[^"]*"[^>]*>[^<]*</div>|<div class="cover-t"[^>]*>[^<]*</div>', cov)
css = """<style>
html, body { background: #FFFFFF !important; }
.page.mask { background: #FFFFFF !important; }
.page.mask .light-t, .page.mask .cover-t { color: #000000 !important; }
.page.mask .drawing { filter: brightness(0); }
</style>"""
head = head.replace("</head>", css + "</head>")
(ROOT / "copertina-lucido.html").write_text(head + '<body><main class="book"><section class="page pr mask">' + "".join(keep)
                                           + "\n</section></main></body></html>", encoding="utf-8")
print(len(keep), "elementi")
