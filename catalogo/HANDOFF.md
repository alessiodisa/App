# Handoff — Catalogo Espositori 2027 (Onprint)

Documento di passaggio per chi (persona o Claude) deve realizzare un **nuovo catalogo aziendale** partendo
dal lavoro fatto per il *Catalogo Espositori 2027*. Contiene: dati aziendali, preferenze emerse con il
cliente, struttura e testi definitivi, sistema grafico, specifiche di stampa e istruzioni tecniche per
rigenerare tutto.

- Repository: `alessiodisa/App`, branch `claude/catalogo-cartotecnica-xtfkbb`, cartella `catalogo/`
- Stato: **catalogo verticale A4 consegnato per la stampa** (copertina con bandelle, interno 20 pagine,
  maschera vernice lucida, scheda di stampa) + versione digitale.
- Archivio di supporto: `catalogo-handoff-archivio.zip` (foto, grafica, font, PDF finali, questo documento).

---

## 1. Azienda

| Campo | Valore |
|---|---|
| Nome | **Onprint** (scritto così nei testi; il logo è "onprint" minuscolo) |
| Settore | Cartotecnica: espositori da banco e da terra per il punto vendita (progettazione, prototipi, produzione) |
| Indirizzo | Viale dell’Industria 26, 35030 Rubano (PD) |
| Telefono | 049 630390 |
| Email | info@onprint.it |
| Web | www.onprint.it |
| P. IVA / C.U. | 04693550289 / T04ZHR3 — **da NON stampare nel catalogo** (tolti su richiesta) |
| Logo | `img/logo-onprint.png` (quadrato blu #384B6B circa con "on" bianco + "print" blu, fondo bianco; in pagina usato con `mix-blend-mode: multiply`) |

---

## 2. Preferenze del cliente (regole emerse in sessione) — LEGGERE PRIMA DI TUTTO

**Foto**
- Usare le **foto originali intere**: niente sfondi sfocati, specchiati o allungati artificialmente.
  (Unica eccezione tollerata, poi superata: un prolungamento invisibile di fondale uniforme.)
- L’espositore deve essere **sempre intero** e **centrato** nel riquadro; mai tagliato (base, header).
- Espositori affiancati di **dimensioni simili** fra loro e con **basi allineate**.
- Nelle doppie pagine le immagini hanno **altezze allineate** fra pagina sinistra e destra.
- Il cliente chiede spesso "leggero zoom" / "riduci leggermente lo zoom": passi piccoli (±8–12%).
- Le foto dei prodotti sono in parte **rigraficate** per privacy (vedi nota in indice).

**Testi**
- **Pochissimo testo.** Sotto le foto solo **codice** (es. B.12) e **nome dell’espositore**.
- Nessuna voce "materiali e finiture" sui singoli prodotti.
- Didascalie **subito sotto** la foto; legende su **due colonne** (prime due voci a sinistra, terza a destra).
- Niente dettagli di **rilegatura** né di **tecnica di stampa** (offset/digitale) nei documenti per la tipografia.
- Non citare la **grammatura** della carta.
- Usare **"Catalogo"** e non "Portfolio". Anno: **2027**.
- Il cliente scrive in italiano informale e veloce: va interpretato; quando una richiesta è ambigua
  (es. "sostituisci T04T06") meglio chiedere con opzioni.

**Impaginazione**
- Formato principale **A4 verticale** (esiste anche una versione orizzontale non più curata).
- Copertina: "Vol. 01 — 2027" in alto a sinistra, logo Onprint in alto a destra, disegno esploso
  dell’espositore, titolo "CATALOGO / ESPOSITORI" medio-alto (non troppo in basso).
- Retro: "Espositori 2027" in alto a sinistra, "CATALOGO", contatti in basso a sinistra **senza titolo e
  senza linee divisorie**, logo in basso a destra.
- Numerazione: **l’indice è pagina 01**; copertina, retro e pagine bianche non numerate.
  Pagine **pari**: numero a sinistra + "Catalogo Espositori 2027" a destra; pagine **dispari**: solo
  numero, a destra.
- Codici espositori **progressivi in ordine di apparizione** (B.01…B.20, T.01…T.14), senza buchi.

---

## 3. Struttura del catalogo consegnato (24 facciate)

| Pagina | Contenuto |
|---|---|
| I copertina | Vol. 01 — 2027, logo, testo breve, disegno esploso espositore da terra (Fig. 01), CATALOGO ESPOSITORI |
| II | bianca (interno copertina) |
| 01 | Indice: 01 Introduzione 02 · 02 Espositori da banco 04 · 03 Espositori da terra 12 + frase + nota privacy |
| 02 | Introduzione: tre fasi (schizzo → bianco → finito, espositore Bioera) + testo metodo + 4 titoli fasi |
| 03 | 4 disegni a matita (Ufficio tecnico, Prototipazione, Produzione, Logistica) + "Un unico interlocutore…" |
| 04 | Apertura Banco: B.01 grande + intro + scheda (Materiali, Montaggio) |
| 05 | Griglia 2×2: B.02, B.03, B.04, B.05 |
| 06 | B.06 grande + B.07 + "Stampa e finiture" (testo + elenco 12 lavorazioni) |
| 07 | B.08 grande + B.09, B.10 |
| 08 | B.11, B.12 in alto + B.13 a tutta larghezza + legenda |
| 09 | B.14 a pagina intera |
| 10 | B.15 grande + B.16, B.17 + legenda 2 colonne |
| 11 | B.18, B.19 impilati + B.20 alto + legenda 2 colonne |
| 12 | Apertura Terra: tavola tecnica vettoriale (viste 3D + fustelle) + intro + scheda |
| 13 | "Configurazioni": T.01 grande + testo |
| 14–19 | coppie: T.02–T.03, T.04–T.05, T.06–T.07, T.08–T.09, T.10–T.11, T.12–T.13 |
| 20 | T.14 a pagina intera |
| III | bianca |
| IV retro | Espositori 2027, CATALOGO, contatti, logo |

Copertina **con bandelle da 100 mm**: quella della I si ripiega verso destra, quella della IV verso sinistra
(stesa 620 × 297 mm: bandella | IV | I | bandella). Le bandelle per ora hanno solo il fondo a griglia
(proposto al cliente di metterci presentazione o contatti: nessuna risposta).

---

## 4. Elenco espositori (definitivo)

Codice catalogo = numero stampato. Codice file = nome della foto in `img/orig/` (codice interno storico).

| Catalogo | File | Nome stampato | Marchio in foto | Pag. |
|---|---|---|---|---|
| B.01 | B13 | Espositore da banco con scivolo e fondale | skne (fichi) | 04 |
| B.02 | B02 | Espositore da banco a gradini | UNO | 05 |
| B.03 | B17 | Espositore da banco a 2 gradini sagomati | skne bianco | 05 |
| B.04 | B10 | Espositore da banco a pedana curva con fondale | Frecce Tricolori | 05 |
| B.05 | B11 | Espositore da banco a 4 ripiani a sbalzo con fondale | Eyewear | 05 |
| B.06 | B12 | Espositore da banco a fondale con 3 nicchie | Moschino | 06 |
| B.07 | B16 | Espositore da banco monoprodotto con fondale | Della Vita | 06 |
| B.08 | B04 | Espositore da banco a vassoio con fondale | Northfolk | 07 |
| B.09 | B21 | Espositore da banco a vassoio alveolare con fondale | Crush | 07 |
| B.10 | B19 | Espositore da banco a gradini inclinati con fondale | Remescar | 07 |
| B.11 | B06 | Espositore da banco a pedana con fondale | Payot | 08 |
| B.12 | B05 | Espositore da banco a 2 gradini con header | Oroil / Fiore d’Oriente | 08 |
| B.13 | B01 | Espositore da banco a pedana con gradino ad arco e fondale | Alizé | 08 |
| B.14 | B15 | Espositore da banco a box con doppio fondale | adidas | 09 |
| B.15 | B03 | Espositore da banco con vassoio sagomato | Bakina | 10 |
| B.16 | B22 | Espositore da banco a 4 vassoi su 2 livelli con fondale | Cristalfarma Relaxcol | 10 |
| B.17 | B23 | Podio in plexiglass | Arhetipa | 10 |
| B.18 | B20 | Espositore da banco a 2 gradini con header ad arco | Cristalfarma Cinarepa | 11 |
| B.19 | B08 | Espositore da banco a box con header | Olcore VitaminC | 11 |
| B.20 | B07 | Espositore da banco a colonna con header e vaschetta dispenser | Scotch | 11 |
| T.01 | T05 | Espositore da terra a 4 ripiani con header | Nutriglow | 13 |
| T.02 | T08 | Espositore da terra a totem con 4 nicchie | skne (colonna) | 14 |
| T.03 | T13 | Espositore da terra a 5 ripiani con fianchi a colonna e header | Solari | 14 |
| T.04 | T14 | Espositore da terra con nicchie inclinate | Hydrai | 15 |
| T.05 | T09 | Espositore da terra a 3 ripiani con fianchi inclinati e header ad arco | Stand display rosso | 15 |
| T.06 | T15 | Espositore da terra a 3 ripiani con fianchi | (ripiani sfalsati) | 16 |
| T.07 | T07 | Espositore da terra a podio con fondale | Eyewear | 16 |
| T.08 | T10 | Espositore da terra a 3 ripiani con sagoma frontale, top e base | waVEN | 17 |
| T.09 | T11 | Espositore da terra a colonna con vano a gradini e header | Tattoolab | 17 |
| T.10 | T01 | Espositore da terra a colonna sagomata con ripiani a sbalzo | Casa Aroma | 18 |
| T.11 | T02 | Espositore da terra a ganci con header e base | Apex | 18 |
| T.12 | T12 | Espositore da terra a colonna con 4 ripiani laterali e header sagomato | Ledum | 19 |
| T.13 | T03 | Espositore da terra a colonna con 3 vani a vista | Bigface | 19 |
| T.14 | T16 | Espositore da terra a podi esagonali con fondali | Reef | 20 |

Foto scartate in corso d’opera (ancora in `img/sq/`): B09, B14, B18, T04, T06 e le versioni precedenti
delle sostituite. `img/origine.json` collega i codici ai file sorgente del primo invio (`immagini-catalogo.zip`).

---

## 5. Testi definitivi

**Copertina** — Vol. 01 — 2027 · "Progettiamo e produciamo espositori per il punto vendita, dall’idea al
bancale." · Fig. 01 Espositore da terra — vista esplosa · CATALOGO ESPOSITORI

**Indice** — "Un catalogo illustrativo: le immagini raccontano i progetti." · nota: "Per motivi di privacy,
alcuni articoli sono stati completamente rigraficati."

**Introduzione (02)** — *Dal progetto alla realizzazione*: "Tutto parte da un confronto con il cliente: il
prodotto, il punto vendita, gli obiettivi. Da qui nasce un’idea, che diventa bozza e poi prototipo da
toccare con mano. Quando ogni dettaglio è a posto passiamo alla produzione e seguiamo il progetto fino
alla consegna." · Nota: "Espositori da banco e da terra per ogni esigenza: progettati, prodotti e seguiti
internamente." · Fasi: 01 Schizzo, 02 Disegno tecnico, 03 Prototipo, 04 Produzione.

**Pagina 03** — 01 Ufficio tecnico: Studio strutturale, render e tracciati di fustella. · 02 Prototipazione:
Campioni bianchi e stampati per testare carico e montaggio. · 03 Produzione: Stampa, fustellatura,
incollaggio e confezionamento interni. · 04 Logistica: Spedizione piatta o premontata, in Italia e
all’estero. · "Un unico interlocutore, dall’idea al punto vendita." (su una riga)

**Espositori da banco (04)** — "L’espositore da banco lavora dove si decide l’acquisto: accanto alla cassa,
sul banco della farmacia, in vetrina. Compatto e leggero, porta il prodotto all’altezza dello sguardo,
ordina la gamma in poco spazio e trasforma l’ultimo metro prima del pagamento in comunicazione di marca."
· Materiali: Cartone, cartoncino, forex, plexi, legno · Montaggio: Pochi secondi, senza colla

**Stampa e finiture (06)** — "Ogni espositore nasce per farsi notare: stampa e nobilitazioni trasformano il
cartone in una superficie di marca. Stampiamo in offset e in digitale su cartoncini e ondulati, in
quadricromia e a colori Pantone, e completiamo la grafica con lavorazioni che aggiungono luce, profondità
e tatto." + elenco: Stampa offset e digitale · Colori Pantone e metallizzati · Plastificazione opaca,
lucida e soft-touch · Vernice UV lucida, opaca e selettiva · UV a spessore ed effetti 3D · Lamina a caldo e
a freddo · Rilievi e bassorilievi a secco · Effetti glitter e perlescenti · Carte speciali, naturali e
goffrate · Accoppiatura su microonda e alveolare · Finestre in PET e fustellati sagomati · Grafiche a tutta
altezza e a vivo

**Espositori da terra (12)** — "L’espositore da terra crea un punto vendita nel punto vendita: porta il
prodotto fuori dallo scaffale, lo rende visibile da lontano e ne racconta la marca su tutta l’altezza.
Curiamo ogni dettaglio già in fase di progettazione: ogni espositore è studiato ad hoc, su misura del
prodotto e del punto vendita." · Altezze: Solitamente da 100 a 200 cm · Configurazioni: Ripiani, ganci,
vani, podi · Spedizione: Piatta, oppure montato e imballato

**Configurazioni (13)** — "Ogni espositore da terra prende forma dal prodotto e dal luogo in cui sarà
esposto: monofacciale o bifacciale, a ripiani, a ganci, a vani o a podi. Header e crowner portano il
messaggio in alto, visibile da lontano, mentre basi e fianchi rinforzati garantiscono stabilità anche a
pieno carico. Anche la logistica fa parte del progetto: l’espositore può viaggiare steso o già montato,
con ingombri e imballi studiati sulle misure di magazzini e bancali, EPAL e non solo."

---

## 6. Sistema grafico

- **Formato**: A4 verticale 210 × 297 mm; margine laterale 16 mm, contenuti da 20 mm; due colonne da ~81 mm
  (larghezza utile 170 mm).
- **Caratteri** (in `fonts/`, licenza OFL): **Inter Tight** per titoli/codici/numeri (300–800), **Inter**
  per il testo (300–600). Titolo copertina: Inter Tight 800, ~64 pt, maiuscolo; "Catalogo" Inter Tight 300
  grigio chiaro.
- **Colori**: carta copertina #F1F1F0 con griglia a vista #DCDCDA (moduli 42 mm × 297/7 mm) e crocette;
  pagine interne con sfumatura #FFFFFF → #F3F3F2 → #E3E3E2; nero testo #141414/#151515; testo corrente
  #5E5E5C; grigio secondario #8E8E8C.
- **Intestazione pagine interne**: titolo sezione a sinistra (Inter Tight 700 ~17 pt); a destra "Onprint"
  grigio + pillola nera con il nome della sezione.
- **Disegni**: esploso vettoriale `img/esploso-terra.svg` (copertina), assonometrie e fustelle
  `img/disegni/*.svg`, tavola tecnica ricalcata `img/disegni/terra-tavola.svg`, schizzi a matita
  `img/disegni/chi-0[1-4].svg`; fasi introduzione `img/intro-*.{png,jpg}`.

---

## 7. Stampa (consegnata)

File in `catalogo/stampa/` e nello zip `catalogo-espositori-2027-stampa.zip`:
1. `01-copertina.pdf` — stesa con bandelle (pag. 1 esterno, pag. 2 interno bianco), segni di piega tratteggiati
2. `02-interno.pdf` — 20 pagine
3. `03-copertina-vernice-lucida.pdf` — maschera (nero 100% = lucido) in registro con la copertina:
   linee del disegno esploso + scritta CATALOGO ESPOSITORI
4. `04-scheda-di-stampa.pdf` — specifiche (sorgente `stampa/scheda-di-stampa.html`)

Specifiche concordate: copertina in carta più spessa, stampata solo all’esterno, interno copertina bianco,
**plastificazione opaca + vernice lucida selettiva**; interno **patinata opaca** (alternativa satinata),
a colori fronte/retro. Tutti i file: 3 mm di abbondanza, crocini, TrimBox/BleedBox. File in **RGB**
(conversione CMYK richiesta alla tipografia). Dorso 0 mm, da adeguare alla rilegatura.

Versione digitale: `catalogo-espositori-2027-digitale.pdf` (22 pagine, senza le pagine bianche).

---

## 8. Parte tecnica

**Come è costruito**: script Python che scrivono HTML con posizioni assolute in mm → Chromium headless →
PDF → post-produzione con PyMuPDF.

| File | Ruolo |
|---|---|
| `portfolio_ref_v.py` | **catalogo verticale** (pagine interne): layout `overview`, `overview_dwg`, `griglia`, `didascalie`, `alto`, `quattro`, `grande`, `tris`, `tre_legenda`, `coppia`, `indice`, `metodo`, `chi_siamo`; elenco `interne = [...]`; piè di pagina e numerazione |
| `portfolio_ref.py` | componenti condivisi (`foto`, `foto_orig`, `txt`, `nomf`, `legenda`, `tag`), dizionari foto, testi (METODO_TXT, FINITURE…), numerazione codici `ORDINE`/`cid`; è anche la versione orizzontale |
| `portfolio_v3.py` | `TIPO` (nomi espositori), `INTRO`, `ZONE` |
| `portfolio_grid.py` / `portfolio_grid_v.py` | copertina e retro (griglia a vista), `logo()`, `CONTATTI`, `contatti_retro()` |
| `*.css` | stili (`portfolio-grid.css`, `portfolio-grid-v.css`, `portfolio-v2.css`, `portfolio-ref.css`, `portfolio-ref-v.css`) |
| `finale_pdf.py` | toglie la pagina bianca provvisoria iniziale e crea il PDF unico con abbondanze |
| `stampa_lucido.py` | genera `copertina-lucido.html` (maschera vernice) |
| `stampa_pdf.py` | file tipografia: copertina stesa con bandelle, interno, lucido |
| `build.sh` | **rigenera tutto** (bozza, stampa, lucido, zip, digitale, panoramica) |
| `img/orig/*.jpg` + `img/orig/orig.json` | foto originali usate e bbox dell’espositore `{"size":[w,h],"bb":[x1,y1,x2,y2]}` |

**Requisiti**: `python3 -m pip install pymupdf pillow numpy scipy`; Chromium (in `/opt/pw-browsers/…`).
Poi `bash catalogo/build.sh`. (Nel container nuovo può servire reinstallare pillow:
`python3 -m pip install --force-reinstall --ignore-installed pillow`.)

**Inquadratura foto** (`portfolio_ref.py`): `foto_orig` scala "cover" sul riquadro e centra sul `bb`;
lo zoom è sempre limitato perché l’espositore non venga tagliato.
- `FILL[code]` = quota d’altezza del riquadro occupata dall’espositore (per pareggiare i vicini)
- `ZOOM[code]` = ingrandimento extra
- `SHIFT[code]` = abbassa l’espositore (quota del riquadro) per allineare le basi
- Valori finali: ZOOM {B20 1.15, T11 1.12, T10 1.12, T09 1.12, T15 1.12}; FILL {T08 .761, T02 .68,
  T12 .76, B19 .8, B21 .8, B03 .72, T01 .78, B22 .78}; SHIFT {T08 .017, T15 .04, T07 .06, B21 .06}
- Non si può rimpicciolire sotto la scala "cover": serve una foto con più aria attorno.

**Sostituire una foto**: salvare in `img/orig/CODICE.jpg` (codice file, non di catalogo!), aggiornare
`orig.json` con size e bbox del solo espositore (esclusi oggetti di scena), rigenerare e controllare a
vista che l’espositore sia intero e alto come il vicino.

**Attenzioni**
- Il codice stampato (B.12) ≠ codice file (B05): la mappa è `ORDINE` in `portfolio_ref.py`.
- Il PDF di lavoro ha una pagina bianca provvisoria in testa (per l’anteprima a doppie pagine);
  `finale_pdf.py` la toglie: i PDF consegnati hanno 24 facciate.
- Le quote minuscole della tavola tecnica (pag. 12) usano un font di riserva: in un container diverso
  possono cambiare leggermente (es. sparisce il ":" in "FLUTE TYPE:").
- Ogni modifica va verificata guardando le anteprime renderizzate, non solo il codice.

---

## 9. Per il nuovo catalogo — punti da chiarire con il cliente
- Stesso marchio Onprint e stessa identità grafica (Inter Tight/Inter, griglia, grigi) o nuova linea?
- Stesso formato (A4 verticale, copertina con bandelle 100 mm, lucido selettivo) o diverso?
- Quali prodotti/categorie (solo espositori o altro: packaging, scatole, ecc.) e quali foto riusare.
- Cosa mettere sulle bandelle (rimaste vuote nel 2027).
- Numerazione e codici: ripartire da 01 o proseguire.
