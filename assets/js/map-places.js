// Posti United sulla mappa. Aggiungi qui i luoghi da mostrare (cibo, esperienze, sport, altro).
// Questo file è il punto dove si aggiungono/editano i posti — non c'è ancora
// un pannello admin separato, ma la struttura dati è pronta per diventarne
// la fonte quando ne costruiremo uno.
//
// category: "food" | "experience" | "sport" | "other"
// placeType: sotto-categoria libera mostrata in lista, es. "Pizzeria", "Ristorante",
//            "Panificio", "Gelateria", "Bar" — utile a colpo d'occhio nella card
// videoLink: link al nostro video su quel posto (Instagram/TikTok/YouTube), o null
// tried: true per i posti provati e consigliati da noi (badge a 3 stelle)
// featured: true/false (scelti da noi per il tab "In evidenza")
// popularity: numero usato per il tab "Più gettonate"
// addedAt: data "AAAA-MM-GG" usata per il tab "Ultime"
//
// Le voci sotto sono demo/segnaposto per vedere come appare la sezione — sostituiscile con i posti reali.
window.UNITED_PLACES = [
  { name: "Bar United", category: "food", placeType: "Bar", lat: 45.6669, lng: 12.2431, description: "Il punto di ritrovo della community prima e dopo le partite.", videoLink: null, tried: true, featured: true, popularity: 24, addedAt: "2026-09-10" },
  { name: "Pizzeria Tre Stelle", category: "food", placeType: "Pizzeria", lat: 45.6705, lng: 12.2465, description: "La pizzeria di fiducia dello spogliatoio Treviso United.", videoLink: null, tried: true, featured: false, popularity: 41, addedAt: "2026-08-20" },
  { name: "Street Food Corner", category: "food", placeType: "Street food", lat: 45.6630, lng: 12.2390, description: "Panini e birra artigianale per il post-partita.", videoLink: null, tried: false, featured: true, popularity: 12, addedAt: "2026-09-15" },
  { name: "Allenamento Open Day", category: "experience", placeType: "Evento", lat: 45.6690, lng: 12.2510, description: "Una mattinata di allenamento aperto alla community United.", videoLink: null, tried: false, featured: true, popularity: 33, addedAt: "2026-09-05" },
  { name: "Presentazione Rosa 2026", category: "experience", placeType: "Evento", lat: 45.6610, lng: 12.2470, description: "L'evento di presentazione ufficiale della squadra.", videoLink: null, tried: false, featured: false, popularity: 58, addedAt: "2026-07-30" },
  { name: "United Community Run", category: "experience", placeType: "Evento", lat: 45.6650, lng: 12.2350, description: "Corsa di gruppo per tutta la community, non competitiva.", videoLink: null, tried: false, featured: true, popularity: 19, addedAt: "2026-09-18" }
];
