#!/usr/bin/env python3
"""
Genera index.html del Portfolio Espositori.

Foto: ogni riquadro ha un codice (es. BAN-01). Se esiste img/BAN-01.jpg
(o .jpeg/.png/.webp) viene usata automaticamente, altrimenti resta il
segnaposto con la descrizione dello scatto che serve.

    python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
AZIENDA = '<span class="tbd">[Nome Azienda]</span>'
ANNO = "2026"
W, H, M = 230, 300, 15  # mm


# --------------------------------------------------------------------------
# helper
# --------------------------------------------------------------------------
def box(x, y, w, h):
    return f"left:{x}mm;top:{y}mm;width:{w}mm;height:{h}mm"


def at(x, y, w=None):
    s = f"left:{x}mm;top:{y}mm"
    return s + (f";width:{w}mm" if w else "")


def foto(code, what, x, y, w, h, cls=""):
    for ext in ("jpg", "jpeg", "png", "webp"):
        f = ROOT / "img" / f"{code}.{ext}"
        if f.exists():
            return f'<div class="ph {cls}" style="{box(x, y, w, h)}"><img src="img/{f.name}" alt=""></div>'
    return (f'<div class="ph {cls}" style="{box(x, y, w, h)}">'
            f'<span class="code">{code}</span><span class="what">{what}</span></div>')


def kv(rows, cls=""):
    return f'<dl class="kv {cls}">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def cap(n, titolo, desc, x, y, w):
    return (f'<div class="cap" style="{at(x, y, w)}"><div class="t"><span class="n">/{n:02d}</span>{titolo}</div>'
            f'<div class="d">{desc}</div></div>')


BRAND = '<span class="tbd">[Brand]</span>'
STAR = ('<svg class="star" viewBox="0 0 24 24"><path d="M12 1v22M1 12h22M4.2 4.2l15.6 15.6M19.8 4.2 4.2 19.8"/></svg>')


# --------------------------------------------------------------------------
# contenuti — sezioni per tipologia di prodotto
# --------------------------------------------------------------------------
SEZIONI = [
    dict(code="BAN", tipo="main", nome="Espositori da banco", titolo="Espositori<br>da banco",
         claim="Piccoli formati, grande impatto.",
         testo="Nascono per stare accanto alla cassa, dove la scelta si fa in un attimo. Compatti, stabili, "
               "stampabili su ogni superficie visibile e pronti da montare in pochi secondi.",
         kv=[("Materiali", "Cartoncino teso, microonda E/B, plexiglass, forex"),
             ("Formati", '<span class="tbd">Da 20 × 15 cm a 60 × 40 cm</span>'),
             ("Varianti", "Con header, a gradini, girevoli, con tester, porta-leaflet"),
             ("Finiture", "Offset, digitale, UV selettiva, lamina a caldo, soft-touch")],
         hero="foto principale: espositore da banco carico di prodotto, still-life su fondo neutro",
         progetti=[("A gradini con header", "Microonda E, stampa offset"),
                   ("Con vano tester", "Cartoncino teso + plexi"),
                   ("Girevole", "Cartoncino teso, base MDF"),
                   ("Porta-leaflet", "Cartoncino 400 g"),
                   ("Espositore cassa", "Microonda E, stampa digitale"),
                   ("Edizione limitata", "Soft-touch + lamina oro")]),
    dict(code="TER", tipo="main", nome="Espositori da terra", titolo="Espositori<br>da terra",
         claim="Il classico che funziona.",
         testo="Strutture multipiano autoportanti con header, crowner e ripiani rinforzati: portano il prodotto "
               "all'altezza dello sguardo, in qualsiasi punto del negozio.",
         kv=[("Materiali", "Ondulato onda B e BC, alveolare, rinforzi interni"),
             ("Portata", '<span class="tbd">Fino a 15 kg per ripiano</span>'),
             ("Varianti", "A ripiani, con ganci, bifacciali, 1/4 pallet, con vasca"),
             ("Consegna", "Spedizione piatta o premontata")],
         hero="foto principale: espositore da terra ambientato nel punto vendita, verticale",
         progetti=[("4 ripiani con header", "Onda BC, stampa offset"),
                   ("Con ganci e barre", "Onda B + barre metalliche"),
                   ("Bifacciale", "Alveolare, stampa digitale"),
                   ("Con crowner sagomato", "Onda BC, fustella speciale")]),
    dict(code="PAL", tipo="main", nome="Pallet display & isole", titolo="Pallet display<br>&amp; isole",
         claim="Il prodotto al centro della scena.",
         testo="Isole a 360° per la grande distribuzione: si caricano in magazzino, viaggiano sul bancale "
               "e sono pronte a vendere appena tolto il film.",
         kv=[("Formati", "Pallet 80 × 120, half 80 × 60, quarter 60 × 40"),
             ("Materiali", "Onda BC rinforzata, alveolare, base in legno o cartone"),
             ("Varianti", "A ripiani, a vasca, con header, fasce e skirt per pallet"),
             ("Portata", '<span class="tbd">Fino a 250 kg</span>')],
         hero="foto principale: isola promozionale in GDO, vista 3/4 con prodotto",
         progetti=[("Isola 4 lati", "Onda BC, stampa offset"),
                   ("Half pallet a vasca", "Onda BC, stampa digitale"),
                   ("Quarter con header", "Onda B, stampa offset"),
                   ("Skirt per pallet", "Microonda E, stampa digitale")]),
    dict(code="DUR", tipo="main", nome="Espositori durevoli", titolo="Espositori<br>durevoli",
         claim="Fatti per restare.",
         testo="Quando l'espositore deve durare stagioni e non settimane: plexiglass, legno, forex e metallo, "
               "lavorati e assemblati con la stessa precisione della carta.",
         kv=[("Materiali", "Plexiglass, legno e MDF, forex, dibond, metallo"),
             ("Lavorazioni", "Taglio laser, fresatura CNC, piegatura a caldo, stampa UV diretta"),
             ("Varianti", "Da banco, da terra, corner, shop-in-shop, arredo negozio"),
             ("Ideale per", "Allestimenti permanenti e semi-permanenti")],
         hero="foto principale: espositore permanente in plexi/legno, luce morbida, dettaglio materico",
         progetti=[("Corner in plexi e legno", "PMMA 5 mm + rovere"),
                   ("Espositore luminoso", "Plexi satinato, LED"),
                   ("Shop-in-shop", "MDF laccato + dibond"),
                   ("Da banco premium", "Plexi fumé, stampa UV"),
                   ("Parete attrezzata", "Legno + metallo"),
                   ("Testata permanente", "Forex + plexi")]),
    dict(code="TOT", tipo="compact", nome="Totem & display verticali", titolo="Totem &amp;<br>display verticali",
         claim="Comunicare in verticale.",
         testo="Totem monofacciali, bifacciali, a tre e quattro lati: comunicazione e segnaletica per ingressi, "
               "vetrine, fiere ed eventi.",
         kv=[("Materiali", "Alveolare, onda BC, forex"), ("Varianti", "2, 3 e 4 facce, con vano prodotto, porta-depliant")],
         hero="totem in ambiente (ingresso negozio o fiera)"),
    dict(code="CES", tipo="compact", nome="Cestoni & dump bin", titolo="Cestoni &amp;<br>dump bin",
         claim="Prendere senza pensarci.",
         testo="Contenitori per prodotto sfuso e promozioni, robusti e veloci da montare. Tondi, quadrati, ottagonali, "
               "con o senza header.",
         kv=[("Materiali", "Onda BC, onda doppia rinforzata"), ("Varianti", "Tondi, quadrati, ottagonali, con divisori")],
         hero="cestone carico di prodotto, vista dall'alto 3/4"),
    dict(code="SCA", tipo="compact", nome="Allestimento scaffale", titolo="Allestimento<br>scaffale",
         claim="Lo scaffale diventa comunicazione.",
         testo="Testate di gondola, crowner, shelf-ready packaging e piccoli formati che fanno rumore: "
               "wobbler, stopper, shelf-talker, fasce ripiano e divisori.",
         kv=[("Prodotti", "Testate, crowner, SRP, wobbler, stopper, strip"), ("Materiali", "Cartoncino, microonda, PVC, PET")],
         hero="testata di gondola allestita in supermercato"),
    dict(code="VET", tipo="compact", nome="Vetrofanie & vetrine", titolo="Vetrofanie<br>&amp; vetrine",
         claim="La prima cosa che si vede.",
         testo="Vetrofanie adesive ed elettrostatiche, allestimenti vetrina in cartone e forex, fondali, pedane "
               "ed elementi sospesi: la vetrina come primo espositore del negozio.",
         kv=[("Prodotti", "Vetrofanie mono e bifacciali, elettrostatiche, calpestabili, allestimenti vetrina"),
             ("Stampa", "Digitale UV, bianco coprente, retro-stampa")],
         hero="vetrina allestita vista dall'esterno, con vetrofanie"),
    dict(code="SAG", tipo="compact", nome="Sagome & cartonati", titolo="Sagome<br>&amp; cartonati",
         claim="A grandezza naturale.",
         testo="Sagome autoportanti, standee, cartonati con piede e sagome da banco: personaggi, prodotti fuori scala "
               "e photo-opportunity per eventi e lanci.",
         kv=[("Materiali", "Alveolare, onda BC, forex"), ("Varianti", "Autoportanti, da banco, con vano, fotocartonati")],
         hero="sagoma a grandezza naturale in ambiente"),
    dict(code="PKG", tipo="compact", nome="Packaging speciale", titolo="Packaging<br>speciale",
         claim="La scatola è già un messaggio.",
         testo="PR box, kit lancio, cofanetti rigidi, scatole con finestra e inserti sagomati. "
               "Quando l'apertura fa parte dell'esperienza.",
         kv=[("Prodotti", "PR box, cofanetti, calendari dell'avvento, kit campioni"),
             ("Finiture", "Carte rivestite, lamina, rilievo, inserti in cartone o EVA")],
         hero="PR box aperto con prodotti, still-life dall'alto"),
    dict(code="GRA", tipo="compact", nome="Grafica punto vendita", titolo="Grafica<br>punto vendita",
         claim="Ogni superficie parla.",
         testo="Pannelli in forex e dibond, adesivi da pavimento, cartelli, soffittature ed elementi sospesi, "
               "bandiere e roll-up: l'identità del brand su tutto il punto vendita.",
         kv=[("Prodotti", "Pannelli, floor graphic, pendenti, cartelli prezzo, roll-up"),
             ("Materiali", "Forex, dibond, PVC, tessuto, carta sintetica")],
         hero="negozio con grafiche sospese e adesivi a pavimento"),
    dict(code="CAR", tipo="compact", nome="Cartotecnica per il marketing", titolo="Cartotecnica<br>per il marketing",
         claim="La carta che accompagna la vendita.",
         testo="Cartelle, campionari, cataloghi, porta-listini, blocchi e calendari: strumenti per la rete vendita "
               "e per il cliente finale, curati come un espositore.",
         kv=[("Prodotti", "Cartelle, campionari, cataloghi, calendari, blocchi"),
             ("Finiture", "Fustelle, tasche, plastificazione, rilegature speciali")],
         hero="campionario / cartella aperta su tavolo, dettaglio carta"),
]

FRONT_PAGES = 9
for i, s in enumerate(SEZIONI):
    s["n"] = i + 1
start = FRONT_PAGES + 1
for s in SEZIONI:
    s["pag"] = start
    start += 4 if s["tipo"] == "main" else 2
BACK_START = start  # sostenibilità


# --------------------------------------------------------------------------
# pagine
# --------------------------------------------------------------------------
def run(sezione="", photo=False):
    cls = "run on-photo" if photo else "run"
    return f'<div class="{cls}"><b>{AZIENDA}</b><span>{sezione}</span></div>'


def folio(n, testo="Portfolio Espositori " + ANNO, photo=False):
    cls = "folio on-photo" if photo else "folio"
    return f'<div class="{cls}"><span>{n:02d}</span><span>{testo}</span></div>'


def copertina():
    return ("", f"""
  {foto("GEN-01", "Copertina: il vostro espositore più iconico, foto verticale d'impatto (still-life o dettaglio materico)", 0, 0, W, H)}
  <div class="cover-panel">
    <div class="logo">{AZIENDA}</div>
    <div>
      <div class="xl light" style="color:#fff">Portfolio</div>
      <div class="xl" style="color:#fff">Espositori</div>
      <div class="label" style="margin-top:6mm;color:rgba(255,255,255,.6)">Cartotecnica · Espositori · Materiali durevoli</div>
    </div>
  </div>
  <div class="cover-year">/&thinsp;{ANNO}</div>""")


def indice_chi_siamo():
    righe = "".join(
        f'<li><span class="p">{s["pag"]:02d}</span><span class="t">{s["nome"]}</span><span class="k">/{s["n"]:02d}</span></li>'
        for s in SEZIONI)
    extra = (f'<li><span class="p">{BACK_START:02d}</span><span class="t">Sostenibilità</span><span class="k"></span></li>'
             f'<li><span class="p">{BACK_START+2:02d}</span><span class="t">Settori &amp; clienti</span><span class="k"></span></li>'
             f'<li><span class="p">{BACK_START+4:02d}</span><span class="t">Su misura &amp; contatti</span><span class="k"></span></li>')
    sx = ("dark", f"""
  {run("Indice")}
  <div class="abs" style="{at(M, 30, 70)}"><div class="l">Indice</div>
    <p class="body" style="margin-top:6mm">Chi siamo · 03<br>Manifesto · 04<br>Il processo · 06<br>Materiali &amp; finiture · 08</p></div>
  <div class="abs" style="{at(92, 30, 123)}"><ul class="toc">{righe}{extra}</ul></div>
  {folio(2)}""")
    dx = ("", f"""
  {run("Chi siamo")}
  {foto("GEN-02", "Stabilimento o reparto produzione: ampia, luce naturale", M, 28, 92, 132)}
  <div class="abs" style="{at(115, 28, 100)}">
    <div class="l">Chi<br>siamo</div>
    <p class="statement sm" style="margin-top:8mm">Dal <span class="tbd">[anno]</span> progettiamo e produciamo cartotecnica ed espositori per il punto vendita. Tutto sotto lo stesso tetto.</p>
  </div>
  <div class="abs" style="{at(115, 128, 100)}">{kv([("Sede", '<span class="tbd">[Città, Provincia]</span>'), ("Stabilimento", '<span class="tbd">[6.000] m²</span>'), ("Persone", '<span class="tbd">[40]</span> tra ufficio tecnico, grafica e produzione')], "narrow")}</div>
  <div class="abs body cols2" style="{at(M, 176, 200)}">
    Seguiamo ogni progetto internamente, dal primo schizzo all'ultimo bancale: ufficio tecnico e grafico, campionatura, stampa, fustellatura, incollaggio e confezionamento. Un unico interlocutore significa tempi più rapidi, meno passaggi e un controllo costante sulla qualità.
    Lavoriamo con brand e agenzie della cosmetica, della farmaceutica, dell'alimentare e dell'oggettistica, in Italia e all'estero, con la stessa cura per la tiratura da cento pezzi e per quella da diecimila.
  </div>
  <div class="abs" style="{at(M, 222, 200)}"><div class="stats">
    <div><b class="tbd">35+</b><span class="label">Anni di esperienza</span></div>
    <div><b class="tbd">400</b><span class="label">Progetti all'anno</span></div>
    <div><b>100%</b><span class="label">Progettato e prodotto internamente</span></div>
  </div></div>
  {folio(3)}""")
    return [sx, dx]


def manifesto():
    sx = ("", f"""
  {foto("GEN-03", "Foto d'atmosfera: mani al lavoro su un prototipo, luce forte e ombre nette", 0, 0, W, H)}
  {run("Manifesto", photo=True)}""")
    dx = ("", f"""
  {run("Manifesto")}
  <div class="abs label" style="{at(M, 28, 60)}"><span class="tbd">[Città]</span>, Italia<br>Portfolio {ANNO}</div>
  {foto("GEN-04", "Dettaglio: cordonatura / fustella", 95, 28, 58, 78)}
  {foto("GEN-05", "Dettaglio: stampa / finitura", 157, 28, 58, 78)}
  <div class="abs" style="{at(M, 128)}">{STAR}</div>
  <div class="abs" style="{at(95, 126, 120)}">
    <p class="statement">Crediamo che un buon espositore nasca dall'incontro tra ingegneria della carta, cura artigianale e conoscenza del punto vendita.</p>
    <p class="body" style="margin-top:6mm">Ogni progetto parte da una domanda semplice: dove verrà visto, da chi, per quanto tempo. Da lì scegliamo struttura, materiale e finiture, prototipiamo, testiamo e solo allora produciamo. Il risultato sono espositori che si montano in fretta, reggono il carico e fanno il loro lavoro: vendere.</p>
  </div>
  <div class="abs big-num" style="{at(M, 238)}">/00</div>
  <div class="abs" style="{at(95, 226, 56)}"><div class="label" style="margin-bottom:2mm">Servizi</div>
    <ul class="list"><li>Progettazione strutturale</li><li>Grafica &amp; render 3D</li><li>Prototipazione</li><li>Stampa &amp; produzione</li></ul></div>
  <div class="abs" style="{at(159, 226, 56)}"><div class="label" style="margin-bottom:2mm">In numeri</div>
    <ul class="list"><li><span class="tbd">400</span> progetti l'anno</li><li><span class="tbd">150</span> clienti attivi</li><li><span class="tbd">12</span> Paesi serviti</li><li><span class="tbd">5 gg</span> per un prototipo</li></ul></div>
  {folio(5)}""")
    return [sx, dx]


def processo():
    steps = [("01", "Brief", "Prodotto, punto vendita, quantità, budget e tempi."),
             ("02", "Concept", "Studio strutturale e grafico, render 3D e tracciati."),
             ("03", "Prototipo", "Campione bianco e stampato, test di carico e montaggio."),
             ("04", "Produzione", "Stampa, fustellatura, accoppiatura e incollaggio in casa."),
             ("05", "Consegna", "Confezionamento, spedizione piatta o premontata, allestimento.")]
    cols = "".join(f'<div><div class="big-num">{n}</div><div><div class="s" style="margin-bottom:1.5mm">{t}</div>'
                   f'<p class="body">{d}</p></div></div>' for n, t, d in steps)
    sx = ("", f"""
  {foto("GEN-06", "Foto orizzontale sulle due pagine: reparto produzione / fustellatrice in funzione", 0, 0, W, H, "spread-l")}
  {run("Il processo", photo=True)}
  {folio(6, photo=True)}""")
    dx = ("", f"""
  {foto("GEN-06", "", 0, 0, W, H, "spread-r")}
  <div class="abs" style="{box(0, 30, W, 240)};background:rgba(38,37,36,.9);color:#fff;padding:12mm {M}mm 0">
    <div class="l" style="color:#fff">Il processo</div>
    <p class="statement sm" style="margin-top:6mm;max-width:150mm;color:rgba(255,255,255,.85)">Dal brief al bancale con un unico interlocutore. Tempo medio: <span class="tbd">3–5 settimane</span>.</p>
  </div>
  <div class="steps" style="{box(M, 150, W - 2*M, 110)}">{cols}</div>
  {folio(7, photo=True)}""")
    return [sx, dx]


def materiali():
    mats = [("Cartone ondulato", "Onda E, B, BC: leggero, resistente, riciclabile."),
            ("Cartoncino teso", "Da 300 a 600 g/m², resa di stampa premium."),
            ("Cartone alveolare", "Honeycomb: strutture portanti a basso peso."),
            ("Forex &amp; PVC", "Semi-permanente, stampa diretta UV."),
            ("Plexiglass", "Trasparente, satinato, colorato, fumé."),
            ("Legno &amp; MDF", "Per l'espositore permanente e l'arredo."),
            ("Metallo", "Barre, ganci, strutture e basi.")]
    fins = [("Offset", "Fino a 6 colori + vernice"), ("Digitale", "Tirature brevi e varianti"),
            ("Serigrafia", "Colori pieni su rigidi"), ("UV selettiva", "Lucido/opaco, a rilievo"),
            ("Lamina a caldo", "Oro, argento, olografica"), ("Soft-touch", "Plastificazione vellutata"),
            ("Rilievo a secco", "Goffratura e debossing"), ("Fustelle speciali", "Sagome, finestre, incastri")]
    sx = ("", f"""
  {run("Materiali &amp; finiture")}
  <div class="abs" style="{at(M, 28, 200)}"><div class="xl">Materiali<br><span class="light">&amp; finiture</span></div></div>
  <div class="abs" style="{at(M, 100, 200)}">{kv([(m, d) for m, d in mats])}</div>
  <div class="abs" style="{at(M, 208, 110)}"><p class="statement sm">Scegliamo il materiale in base a quanto deve durare l'espositore, a quanto deve reggere e a dove andrà.</p></div>
  {foto("MAT-01", "Macro: sezione del cartone ondulato", 135, 208, 80, 72)}
  {folio(8)}""")
    tiles = [("MAT-02", "Macro: cartoncino teso stampato"), ("MAT-03", "Macro: pannello alveolare"),
             ("MAT-04", "Macro: plexiglass"), ("MAT-05", "Macro: legno / MDF")]
    grid = "".join(foto(c, d, M + (i % 2) * 102, 28 + (i // 2) * 82, 98, 78) for i, (c, d) in enumerate(tiles))
    fin = "".join(f"<div><b>{t}</b><span class='label'>{d}</span></div>" for t, d in fins)
    dx = ("", f"""
  {run("Materiali &amp; finiture")}
  {grid}
  <div class="abs" style="{at(M, 204, 200)}"><div class="m" style="margin-bottom:5mm">Finiture</div><div class="fin">{fin}</div></div>
  {folio(9)}""")
    return [sx, dx]


# ---------- sezioni principali (4 pagine) ----------
def testata_sezione(s, x, y, w):
    return f"""<div class="abs" style="{at(x, y, w)}">
    <div class="label" style="margin-bottom:4mm">Sezione /{s['n']:02d}</div>
    <div class="xl">{s['titolo']}</div>
    <p class="statement sm" style="margin-top:7mm"><b style="font-weight:600">{s['claim']}</b> {s['testo']}</p>
  </div>"""


def main_apertura(s, p):
    c = s["code"]
    hero = foto(f"{c}-01", s["hero"], 0, 0, W, H)
    if s["n"] % 2:  # foto a sinistra, testo a destra
        sx = ("", f"{hero}{run(s['nome'], photo=True)}")
        dx = ("", f"""
  {run(s['nome'])}
  {foto(f"{c}-02", "Dettaglio", M, 28, 98, 84)}
  {foto(f"{c}-03", "Dettaglio / montaggio", 117, 28, 98, 84)}
  {testata_sezione(s, M, 126, 200)}
  <div class="abs" style="{at(M, 226, 200)}">{kv(s['kv'])}</div>
  {folio(p + 1)}""")
    else:  # testo a sinistra, foto a destra
        sx = ("carta", f"""
  {run(s['nome'])}
  {testata_sezione(s, M, 28, 200)}
  {foto(f"{c}-02", "Dettaglio orizzontale", M, 122, 200, 96)}
  <div class="abs" style="{at(M, 226, 200)}">{kv(s['kv'])}</div>
  {folio(p)}""")
        dx = ("", f"{foto(f'{c}-03', s['hero'], 0, 0, W, H)}{run(s['nome'], photo=True)}")
    return [sx, dx]


def gallery_file(s, p):
    """Per pagina: un progetto grande orizzontale (5:3) + due piccoli (3:2)."""
    c, pr = s["code"], s["progetti"]
    pages = []
    for side in (0, 1):
        k = side * 3
        items = foto(f"{c}-{k+4:02d}", "Progetto: foto orizzontale (3:2 o 16:10)", M, 56, 200, 120)
        items += cap(k + 1, f"{BRAND} — {pr[k][0]}", pr[k][1], M, 179, 150)
        for i in range(2):
            x = M + i * 102
            items += foto(f"{c}-{k+5+i:02d}", "Progetto: foto orizzontale (3:2)", x, 196, 98, 66)
            items += cap(k + 2 + i, f"{BRAND} — {pr[k+1+i][0]}", pr[k+1+i][1], x, 265, 98)
        head = (f'<div class="abs" style="{at(M, 28, 120)}"><div class="l">Progetti</div></div>'
                f'<div class="abs label" style="{at(160, 30, 55)}">Una selezione di progetti realizzati per brand di settori diversi.</div>'
                if side == 0 else
                f'<div class="abs" style="{at(M, 28, 200)}"><p class="statement sm" style="max-width:150mm">Ogni progetto è studiato sul prodotto: dimensioni, peso, numero di facing e tempo di permanenza a scaffale.</p></div>')
        pages.append(("", f"""{run(s['nome'])}{head}{items}{folio(p + 2 + side, s['nome'])}"""))
    return pages


def gallery_collage(s, p):
    """Due progetti in evidenza, uno per pagina."""
    c, pr = s["code"], s["progetti"]
    sx = ("", f"""
  {run(s['nome'])}
  {foto(f"{c}-04", "Progetto 1: vista principale", M, 28, 128, 150)}
  {foto(f"{c}-05", "Progetto 1: dettaglio", 147, 28, 68, 72)}
  {foto(f"{c}-06", "Progetto 1: dettaglio", 147, 106, 68, 72)}
  <div class="abs" style="{at(M, 196, 125)}"><div class="l">{BRAND}<span class="num">/01</span></div>
    <p class="label" style="margin-top:2mm">{pr[0][0]}</p></div>
  <div class="abs" style="{at(147, 196, 68)}"><p class="body">Breve descrizione del progetto: obiettivo del cliente, soluzione strutturale, risultato.</p></div>
  <div class="abs" style="{at(M, 240, 200)}">{kv([("Materiale", pr[0][1]), ("Formato", '<span class="tbd">60 × 40 × 170 cm</span>'), ("Tiratura", '<span class="tbd">500 pz</span>')], "narrow")}</div>
  {folio(p + 2, s['nome'])}""")
    dx = ("", f"""
  {run(s['nome'])}
  {foto(f"{c}-07", "Progetto 2: foto verticale (3:4)", M, 28, 98, 131)}
  {foto(f"{c}-08", "Progetto 2: ambientata (3:2)", 117, 28, 98, 63)}
  {foto(f"{c}-09", "Progetto 2: dettaglio (3:2)", 117, 96, 98, 63)}
  <div class="abs" style="{at(M, 176, 98)}"><div class="l">{BRAND}<span class="num">/02</span></div>
    <p class="label" style="margin-top:2mm">{pr[1][0]}</p></div>
  <div class="abs" style="{at(117, 176, 98)}">{kv([("Materiale", pr[1][1]), ("Formato", '<span class="tbd">120 × 80 × 160 cm</span>'), ("Tiratura", '<span class="tbd">200 pz</span>')], "narrow")}
    <p class="body" style="margin-top:4mm">Breve descrizione del progetto: obiettivo del cliente, soluzione strutturale, risultato.</p></div>
  {folio(p + 3, s['nome'])}""")
    return [sx, dx]


def gallery_griglia(s, p):
    """Foto piena a sinistra, griglia 2×2 a destra."""
    c, pr = s["code"], s["progetti"]
    sx = ("", f"""
  {foto(f"{c}-04", "Progetto in evidenza: foto a piena pagina", 0, 0, W, H)}
  {run(s['nome'], photo=True)}
  <div class="abs" style="{box(M, 232, 100, 50)};background:#fff;padding:5mm">
    <div class="s">{BRAND} — {pr[0][0]}</div><p class="label" style="margin-top:1.5mm">{pr[0][1]} · <span class="tbd">80 × 120 × 160 cm</span></p>
  </div>""")
    tiles = "".join(foto(f"{c}-{i+5:02d}", "Progetto: foto quadrata", M + (i % 2) * 102, 28 + (i // 2) * 102, 98, 98) for i in range(4))
    caps = "".join(cap(i + 1, f"{BRAND} — {t}", d, M + (i % 2) * 102, 232 + (i // 2) * 16, 98) for i, (t, d) in enumerate(pr[:4]))
    dx = ("", f"""{run(s['nome'])}{tiles}{caps}{folio(p + 3, s['nome'])}""")
    return [sx, dx]


GALLERIE = [gallery_file, gallery_collage, gallery_griglia, gallery_file]


# ---------- sezioni compatte (2 pagine) ----------
def compact(s, p, variante):
    c = s["code"]
    titolo = f'<div class="label" style="margin-bottom:3mm">Sezione /{s["n"]:02d}</div><div class="l">{s["titolo"]}</div>'
    if variante == 0:
        sx = ("", f"""
  {foto(f"{c}-01", s['hero'], 0, 0, W, 160)}
  {run(s['nome'], photo=True)}
  <div class="abs" style="{at(M, 172, 110)}">{titolo}</div>
  <div class="abs" style="{at(130, 172, 85)}"><p class="body"><b style="color:var(--nero)">{s['claim']}</b> {s['testo']}</p></div>
  <div class="abs" style="{at(M, 240, 200)}">{kv(s['kv'])}</div>
  {folio(p)}""")
        dx = ("", f"""
  {run(s['nome'])}
  {foto(f"{c}-02", "Progetto: vista principale", M, 28, 200, 150)}
  {foto(f"{c}-03", "Progetto: dettaglio", M, 184, 98, 76)}
  {foto(f"{c}-04", "Progetto: dettaglio", 117, 184, 98, 76)}
  {cap(1, BRAND + " — [Nome progetto]", "Materiale · formato", M, 264, 98)}
  {cap(2, BRAND + " — [Nome progetto]", "Materiale · formato", 117, 264, 98)}
  {folio(p + 1, s['nome'])}""")
    else:
        tiles = "".join(foto(f"{c}-{i+1:02d}", "Progetto: foto verticale", M + (i % 2) * 102, 28 + (i // 2) * 116, 98, 112) for i in range(4))
        sx = ("", f"""{run(s['nome'])}{tiles}
  {cap(1, BRAND + " — [Nome progetto]", "Materiale · formato", M, 264, 98)}
  {cap(2, BRAND + " — [Nome progetto]", "Materiale · formato", 117, 264, 98)}
  {folio(p, s['nome'])}""")
        dx = ("carta", f"""
  {run(s['nome'])}
  <div class="abs" style="{at(M, 28, 120)}">{titolo}</div>
  <div class="abs" style="{at(145, 30, 70)}"><p class="body"><b style="color:var(--nero)">{s['claim']}</b> {s['testo']}</p></div>
  {foto(f"{c}-05", s['hero'], M, 108, 200, 128)}
  <div class="abs" style="{at(M, 244, 200)}">{kv(s['kv'])}</div>
  {folio(p + 1)}""")
    return [sx, dx]


# ---------- chiusura ----------
def sostenibilita(p):
    pil = [("Monomateriale", "Espositori 100% carta, riciclabili senza separare i componenti."),
           ("Carte certificate", '<span class="tbd">FSC® / PEFC</span> su richiesta, filiera tracciata.'),
           ("Meno sfridi", "Tracciati ottimizzati per il minimo scarto in fustellatura."),
           ("Spedizione piatta", "Meno volume, meno viaggi, meno emissioni.")]
    pills = "".join(f'<div><div class="s">{t}</div><p class="body" style="margin-top:1.5mm">{d}</p></div>' for t, d in pil)
    sx = ("", f"""
  {foto("GEN-07", "Foto orizzontale sulle due pagine: materia prima, bobine di carta o bancali di cartone", 0, 0, W, 150, "spread-l")}
  {run("Sostenibilità", photo=True)}
  <div class="abs" style="{at(M, 166, 200)}"><div class="xl">Leggeri<br><span class="light">sul pianeta.</span></div></div>
  <div class="abs" style="{at(M, 226, 150)}"><p class="statement sm">La carta è il materiale da espositore più riciclato al mondo. Noi la progettiamo perché consumi meno, viaggi piatta e torni in circolo.</p></div>
  {folio(p)}""")
    dx = ("", f"""
  {foto("GEN-07", "", 0, 0, W, 150, "spread-r")}
  <div class="abs" style="{at(M, 170, 200)}"><div class="pillars">{pills}</div></div>
  {folio(p + 1)}""")
    return [sx, dx]


def settori_clienti(p):
    settori = ["Cosmetica &amp; profumeria", "Farmaceutica &amp; parafarmacia", "Alimentare &amp; GDO", "Beverage",
               "Oggettistica &amp; regalo", "Elettronica", "Pet care", "Editoria &amp; cartoleria", "Moda &amp; accessori"]
    li = "".join(f'<li>{t}<span>/{i+1:02d}</span></li>' for i, t in enumerate(settori))
    loghi = "".join('<div>Logo cliente</div>' for _ in range(12))
    sx = ("", f"""
  {run("Settori")}
  <div class="abs" style="{at(M, 28, 200)}"><div class="xl">Settori</div>
    <p class="statement sm" style="margin-top:7mm;max-width:160mm">Ogni settore ha le sue regole: normative, tempi, canali. Le conosciamo.</p></div>
  <div class="abs" style="{at(M, 118, 200)}"><ul class="sectors">{li}</ul></div>
  {folio(p)}""")
    dx = ("", f"""
  {run("Clienti")}
  <div class="abs" style="{at(M, 28, 200)}"><div class="xl">Hanno scelto<br><span class="light">di farsi notare.</span></div></div>
  <div class="abs" style="{at(M, 128, 200)}"><div class="logos">{loghi}</div></div>
  {folio(p + 1)}""")
    return [sx, dx]


def su_misura_contatti(p):
    passi = [("Scrivici", "Prodotto, quantità, punto vendita e tempi."),
             ("Progettiamo", "Concept e render in pochi giorni."),
             ("Tocchi con mano", "Prototipo fisico prima della produzione.")]
    pp = "".join(f'<div><div class="s" style="color:#fff">{i+1}. {t}</div><p class="body" style="margin-top:1.5mm">{d}</p></div>' for i, (t, d) in enumerate(passi))
    sx = ("dark2", f"""
  {run("Su misura")}
  <div class="abs" style="{at(M, 28)}">{STAR}</div>
  <div class="abs" style="{at(M, 96, 200)}"><div class="xl" style="font-size:58pt">Hai un prodotto?<br><span class="light">Noi il suo palco.</span></div></div>
  <div class="abs" style="{at(M, 196, 200)}"><p class="statement sm" style="color:rgba(255,255,255,.85)">Ogni progetto di questo portfolio è nato da un brief. Il prossimo può essere il tuo.</p></div>
  <div class="abs" style="{at(M, 240, 200)}"><div class="pillars" style="grid-template-columns:1fr 1fr 1fr">{pp}</div></div>
  {folio(p)}""")
    dx = ("", f"""
  {foto("GEN-08", "Foto del team / ufficio tecnico: persone al lavoro", 0, 0, W, 150)}
  {run("Contatti", photo=True)}
  <div class="abs" style="{at(M, 164, 200)}"><div class="xl">Parliamone.</div></div>
  <div class="abs" style="{at(M, 214, 200)}">{kv([
        ("Email", '<span class="tbd">info@azienda.it</span>'),
        ("Telefono", '<span class="tbd">+39 000 000 0000</span>'),
        ("Sede &amp; stabilimento", '<span class="tbd">Via Esempio 1, 00000 Città (XX)</span>'),
        ("Web", '<span class="tbd">www.azienda.it</span>'),
        ("Social", '<span class="tbd">@azienda</span>')])}</div>
  {folio(p + 1)}""")
    return [sx, dx]


def retro():
    return ("dark2", f"""
  <div class="abs" style="{at(M, 136, 200)};text-align:center">
    <div class="logo" style="font-size:18pt">{AZIENDA}</div>
    <p class="label" style="margin-top:3mm">Cartotecnica · Espositori · Materiali durevoli</p>
  </div>
  <div class="abs" style="{box(0, H - 34, 80, 34)};background:#6E6B66"></div>
  <div class="folio" style="justify-content:flex-end"><span>Stampato su carta riciclabile · <span class="tbd">FSC®</span></span></div>""")


# --------------------------------------------------------------------------
# assemblaggio
# --------------------------------------------------------------------------
def build():
    pages = [copertina()]
    pages += indice_chi_siamo()
    pages += manifesto()
    pages += processo()
    pages += materiali()
    assert len(pages) == FRONT_PAGES, len(pages)
    k_main = k_comp = 0
    for s in SEZIONI:
        p = len(pages) + 1
        assert p == s["pag"], (s["nome"], p, s["pag"])
        if s["tipo"] == "main":
            pages += main_apertura(s, p)
            pages += GALLERIE[k_main](s, p)
            k_main += 1
        else:
            pages += compact(s, p, k_comp % 2)
            k_comp += 1
    pages += sostenibilita(len(pages) + 1)
    pages += settori_clienti(len(pages) + 1)
    pages += su_misura_contatti(len(pages) + 1)
    pages.append(retro())
    assert len(pages) % 4 == 0, f"pagine: {len(pages)} (serve un multiplo di 4)"

    out = []
    for i, (cls, html) in enumerate(pages, start=1):
        side = "pr" if i % 2 else "pl"
        out.append(f'<section class="page {side} {cls}" data-p="{i}">{html}\n</section>')

    doc = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio Espositori {ANNO}</title>
<link rel="stylesheet" href="fonts/fonts.css">
<link rel="stylesheet" href="catalogo.css">
</head>
<body>
<!-- File generato da build.py: modificare i contenuti lì, non qui. -->
<main class="book">
{chr(10).join(out)}
</main>
</body>
</html>
"""
    (ROOT / "index.html").write_text(doc, encoding="utf-8")
    print(f"index.html: {len(pages)} pagine")


if __name__ == "__main__":
    build()
