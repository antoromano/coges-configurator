# SPEC — Coges Configurator (Prototipo)

> **Attenzione**: questo documento descrive un **prototipo con dati fittizi**.
> Prezzi, moltiplicatori, soglie di sconto e range dimensionali sono valori
> di esempio scelti per dimostrare il funzionamento del sistema, **non**
> listini prezzi reali. Prima della messa in produzione andranno sostituiti
> con i dati reali forniti dal cliente.

## Cosa è reale e cosa è fittizio

Il prototipo copre 3 famiglie prodotto (Finestre, Portoncini, Pergole),
modellate sulla struttura reale del catalogo di
[cogesinfissi.it](https://www.cogesinfissi.it):

- **Nomi di categoria, marche e sistemi** (Schuco AWS, Schuco Block System,
  AURA, Dierre, Oikos, KE) sono presi dal sito pubblico di Coges Infissi.
- **I dati tecnici del profilo AURA** (permeabilità aria Classe 4, tenuta
  acqua Classe 9A, resistenza vento Classe C3/B3, prestazione acustica
  Rw 41dB, lega EN AW-6060) sono **reali**, pubblicati su
  `cogesinfissi.it/aura-2/`.
- **Tutti i moltiplicatori e importi di prezzo, tutte le soglie di sconto, e
  i dati tecnici di Schuco/Dierre/Oikos/KE** (che non erano pubblicati con
  dettaglio tecnico verificabile sul sito Coges) **sono fittizi/plausibili**,
  creati per il prototipo. Non sono listini né certificazioni reali.

---

## 1. Schema dati

Le entità sono modellate come tabelle di lookup nel backend (SQLModel, in
`backend/app/models/{finestre,portoncini,pergole}.py`) e rispecchiate come
TypeScript types nel frontend (`frontend/src/types/index.ts`).

Ogni famiglia prodotto ha una formula di pricing isolata e indipendente
(`backend/app/services/pricing_{finestre,portoncini,pergole}.py`), perché i
parametri e la logica differiscono per famiglia (vedi sezione 3).

### 1.1 Finestre

Gerarchia di selezione: **Materiale → Sistema → Profilo** (sul modello di
configuratori reali del settore, es. finestre.com). Un Sistema appartiene a
un Materiale; un Profilo appartiene a un Sistema.

#### WindowOpeningType

Tipo di apertura: definisce anche il range dimensionale ammesso e il prezzo
base al m².

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "1 Anta" / "2 Ante" / "Portafinestra" / "Scorrevole" |
| description | string | — |
| base_price_per_sqm | float | €/m², diverso per tipo (180 / 195 / 210 / 260) |
| min_width_mm, max_width_mm | int | mm |
| min_height_mm, max_height_mm | int | mm |

#### WindowMaterial

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "PVC" / "PVC-Alluminio" / "Legno" / "Legno-Alluminio" / "Alluminio" |
| price_multiplier | float | 0.85 / 1.05 / 1.4 / 1.55 / 1.0 |

#### WindowSystem

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | es. "Schuco AWS - Anta a Vista" |
| material_id | int (FK) | → WindowMaterial.id — filtra i sistemi disponibili per il materiale scelto |
| description | string | — |
| price_multiplier | float | — |

#### WindowProfile

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | es. "COGES 72 TS" |
| system_id | int (FK) | → WindowSystem.id |
| description | string | — |
| air_permeability_class | string \| null | reale solo per AURA/COGES 72 TS |
| water_tightness_class | string \| null | reale solo per AURA/COGES 72 TS |
| wind_resistance_class | string \| null | reale solo per AURA/COGES 72 TS |
| acoustic_performance_db | string \| null | reale solo per AURA/COGES 72 TS |
| price_multiplier | float | — |

#### WindowGlassType, WindowColor, WindowExtraOption

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | vedi valori sezione 3.1 |
| extra_cost | float | € |

### 1.2 Portoncini

Range dimensionale fisso (porta a battente singola): non varia in base a un
tipo di apertura come per le finestre, quindi non c'è una tabella
equivalente a `WindowOpeningType`. Larghezza 700–1300mm, altezza
2000–2400mm.

#### DoorMaterial

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "Acciaio blindato" / "Alluminio design" / "Legno-Alluminio" |
| price_multiplier | float | 1.0 / 1.25 / 1.35 |

#### DoorBrand

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "Dierre" / "Oikos" / "Schuco" |
| description | string | — |
| price_multiplier | float | 1.0 / 1.35 / 1.2 |

#### DoorSecurityClass

Nomenclatura standard EN 1627 (RC2–RC4); descrizioni indicative, non
certificazioni di uno specifico prodotto.

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "RC2" / "RC3" / "RC4" |
| description | string | — |
| price_multiplier | float | 1.0 / 1.2 / 1.45 |

#### DoorColor, DoorExtraOption

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | vedi valori sezione 3.2 |
| extra_cost | float | € |

### 1.3 Pergole

Range dimensionale fisso: larghezza 2000–6000mm, sporgenza (profondità)
2000–4000mm.

#### PergolaMaterial

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "Alluminio anodizzato" / "Alluminio verniciato RAL" |
| price_multiplier | float | 1.0 / 1.15 |

#### PergolaSystem

Tipo di copertura.

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | "KE Copertura Fissa" / "KE Lamelle Orientabili Bioclimatica" |
| description | string | — |
| price_multiplier | float | 1.0 / 1.45 |

#### PergolaColor, PergolaExtraOption

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| name | string | vedi valori sezione 3.3 |
| extra_cost | float | € |

### 1.4 QuoteRequest

Richiesta di preventivo inviata dal cliente tramite il form "Richiedi
preventivo" in fondo a ciascun configuratore. Il prezzo mostrato è una stima
indicativa non vincolante (etichetta visibile in `PriceBreakdown.tsx`);
diventa un'offerta reale solo dopo la conferma di un membro dello staff
Coges dalla pagina interna `/api/quote-requests` (protetta da password, vedi
sezione 2). Il prezzo salvato viene **sempre ricalcolato lato server** con
lo stesso servizio di pricing usato da `/api/calculate-price/{family}` — il
client non può inviare (né manomettere) un prezzo diretto. La forma della
configurazione varia per famiglia prodotto, quindi è salvata come JSON
invece di colonne fisse per parametro.

| Campo | Tipo | Note |
|---|---|---|
| id | int | chiave primaria |
| product_family | string | "finestre" \| "portoncini" \| "pergole" |
| configuration | dict (JSON) | stessa forma del body di `POST /api/calculate-price/{family}` (senza i campi di contatto) |
| final_price | float | € — ricalcolato lato server |
| breakdown | dict (JSON) | stessa forma del campo `breakdown` della response di calculate-price |
| customer_name | string | — |
| customer_email | string | validata come email |
| customer_phone | string | — |
| customer_note | string | opzionale |
| status | string | "in_attesa" (default) \| "confermato" \| "rifiutato" |
| created_at | datetime | — |

---

## 2. Contratto API

Base URL locale: `http://localhost:8000`. Swagger UI interattivo su `/docs`.

### `GET /api/product-families`

Ritorna le famiglie prodotto disponibili (metadati di navigazione, non dati
di catalogo).

**Response 200:**

```json
[
  { "slug": "finestre", "name": "Finestre", "description": "Finestre, portefinestre e scorrevoli in alluminio, PVC e legno." },
  { "slug": "portoncini", "name": "Portoncini", "description": "Porte blindate d'ingresso." },
  { "slug": "pergole", "name": "Pergole", "description": "Pergole bioclimatiche per esterni." }
]
```

### `GET /api/catalog/finestre`

**Response 200 (estratto):**

```json
{
  "opening_types": [
    { "id": 1, "name": "1 Anta", "description": "Finestra a battente singola anta.", "base_price_per_sqm": 180.0, "min_width_mm": 400, "max_width_mm": 1200, "min_height_mm": 400, "max_height_mm": 1500 }
  ],
  "materials": [
    { "id": 5, "name": "Alluminio", "price_multiplier": 1.0 }
  ],
  "systems": [
    { "id": 8, "name": "AURA - Profilo Coges", "material_id": 5, "description": "Profilo di design originale Coges Infissi, in lega di alluminio EN AW-6060.", "price_multiplier": 1.20 }
  ],
  "profiles": [
    { "id": 9, "name": "COGES 72 TS", "system_id": 8, "description": "Profili metallici estrusi in lega primaria alluminio EN AW-6060...", "air_permeability_class": "Classe 4", "water_tightness_class": "Classe 9A", "wind_resistance_class": "Classe C3/B3", "acoustic_performance_db": "Rw 41 dB (C;Ctr)", "price_multiplier": 1.0 }
  ],
  "glass_types": [{ "id": 1, "name": "Normale", "extra_cost": 0.0 }],
  "colors": [{ "id": 1, "name": "Bianco", "extra_cost": 0.0 }],
  "extra_options": [{ "id": 1, "name": "Zanzariera", "extra_cost": 45.0 }]
}
```

### `POST /api/calculate-price/finestre`

**Request body:**

```json
{
  "opening_type_id": 1,
  "width_mm": 1000,
  "height_mm": 1000,
  "material_id": 5,
  "system_id": 8,
  "profile_id": 9,
  "glass_type_id": 1,
  "color_id": 1,
  "extra_option_ids": []
}
```

**Validazione:**
- `width_mm`/`height_mm`: devono rientrare nel range del `WindowOpeningType` indicato
- `system_id` deve appartenere al `material_id` indicato (altrimenti 422)
- `profile_id` deve appartenere al `system_id` indicato (altrimenti 422)
- ogni id deve corrispondere a una riga esistente
- input non valido → **HTTP 422** con `detail` testuale (mai 500 o crash)

**Response 200:**

```json
{
  "final_price": 216.0,
  "breakdown": {
    "area_m2": 1.0,
    "base_price_area": 180.0,
    "material_name": "Alluminio",
    "material_multiplier": 1.0,
    "price_after_material": 180.0,
    "system_name": "AURA - Profilo Coges",
    "system_multiplier": 1.2,
    "price_after_system": 216.0,
    "profile_name": "COGES 72 TS",
    "profile_multiplier": 1.0,
    "price_after_profile": 216.0,
    "glass_name": "Normale",
    "glass_extra_cost": 0.0,
    "color_name": "Bianco",
    "color_extra_cost": 0.0,
    "extra_options": [],
    "extra_options_total": 0.0,
    "subtotal_before_discount": 216.0,
    "volume_discount_applied": false,
    "volume_discount_amount": 0.0,
    "final_price": 216.0
  }
}
```

### `GET /api/catalog/portoncini` / `POST /api/calculate-price/portoncini`

Stessa forma logica delle Finestre, senza sistema/profilo. Il body accetta
`{ width_mm, height_mm, material_id, brand_id, security_class_id, color_id, extra_option_ids }`;
il `breakdown` di risposta include `material_name/multiplier`,
`brand_name/multiplier`, `security_class_name/multiplier`, `color_name`,
`extra_options`, `final_price` (nessun campo di sconto volume: vedi
sezione 3.2).

### `GET /api/catalog/pergole` / `POST /api/calculate-price/pergole`

Il body accetta
`{ width_mm, depth_mm, material_id, system_id, color_id, extra_option_ids }`
(nota: `depth_mm` invece di `height_mm`, perché la pergola si sviluppa in
larghezza × sporgenza, non larghezza × altezza). Il `breakdown` include
`material_name/multiplier`, `system_name/multiplier`, `color_name`,
`extra_options`, `subtotal_before_discount`, `volume_discount_applied`,
`volume_discount_amount`, `final_price`.

### `POST /api/quote-requests/{family}`

Pubblico, nessuna autenticazione richiesta. Uno per famiglia
(`/finestre`, `/portoncini`, `/pergole`). Il body è la stessa configurazione
di `POST /api/calculate-price/{family}` più i dati di contatto:

```json
{
  "opening_type_id": 1, "width_mm": 1000, "height_mm": 1000,
  "material_id": 5, "system_id": 8, "profile_id": 9,
  "glass_type_id": 1, "color_id": 1, "extra_option_ids": [],
  "customer_name": "Mario Rossi",
  "customer_email": "mario.rossi@example.com",
  "customer_phone": "3331234567",
  "customer_note": "Interessato a consegna rapida"
}
```

Il prezzo viene ricalcolato e validato esattamente come in
`calculate-price` (stessa funzione condivisa `validate_and_price` in
`routes/{family}.py`), poi salvato come `QuoteRequest` con
`status="in_attesa"`.

**Response 200:**

```json
{ "id": 2, "final_price": 216.0, "status": "in_attesa" }
```

### `GET /api/quote-requests` — area staff

Richiede l'header `X-Staff-Token` con la password configurata in
`STAFF_ACCESS_TOKEN` (vedi `.env`). Ritorna tutte le richieste di tutte le
famiglie, più recenti prima. Senza header o con password errata: **401**.

### `PATCH /api/quote-requests/{id}/status` — area staff

Stesso header richiesto. Body: `{ "status": "confermato" }` (o
`"rifiutato"`, `"in_attesa"`). Ritorna la richiesta aggiornata.

### `GET /api/health`

Endpoint di verifica rapida che l'API sia raggiungibile. Ritorna `{"status": "ok"}`.

---

## 3. Formule di calcolo prezzo (v1 — dati fittizi)

> Tutti i valori numerici sotto (prezzi al m², moltiplicatori, sovrapprezzi,
> soglie e percentuali di sconto) sono **dati dichiaratamente fittizi** per
> il prototipo, salvo dove indicato diversamente. Ogni formula è isolata in
> un modulo `backend/app/services/pricing_*.py` dedicato, per rendere la
> sostituzione con il listino reale indipendente dal resto del sistema.

### 3.1 Finestre

1. **Area in m²**: `area_m2 = (larghezza_mm × altezza_mm) / 1_000_000`
2. **Prezzo base per area**: `area_m2 × base_price_per_sqm` (dipende dal
   tipo di apertura: 1 Anta 180, 2 Ante 195, Portafinestra 210, Scorrevole 260 €/m²)
3. **Moltiplicatori a cascata**: `× moltiplicatore_materiale × moltiplicatore_sistema × moltiplicatore_profilo`
4. **Costo vetro** (aggiunta fissa): Normale +0 / Basso emissivo +80 / Triplo vetro +150 / Acustico +130 €
5. **Supplemento colore** (aggiunta fissa): Bianco +0 (incluso) / Grigio +30 / Nero +50 €
6. **Opzioni extra** (somma di ogni opzione selezionata): Zanzariera +45 / Grata di sicurezza +120 / Apertura motorizzata +280 €
7. **Sconto volume**: se `area_m2 > 1.5`, sconto del 10% sul totale (economia di scala)
8. **Arrotondamento**: risultato finale a 2 decimali

### 3.2 Portoncini

Prezzo base al m² più alto delle finestre (420 €/m², fittizio), per
riflettere la maggiore robustezza costruttiva di una porta blindata.
**Nessuno sconto volume**: a differenza di una vetrata, un portoncino è
un'unità singola con range dimensionale ristretto — non ha senso applicare
un'economia di scala legata all'area.

1. **Area in m²**: `area_m2 = (larghezza_mm × altezza_mm) / 1_000_000`
2. **Prezzo base per area**: `area_m2 × 420`
3. **Moltiplicatori a cascata**: `× moltiplicatore_materiale × moltiplicatore_marca × moltiplicatore_classe_sicurezza`
4. **Supplemento colore** (aggiunta fissa): Bianco +0 / Grigio antracite +60 / Rovere naturale +90 €
5. **Opzioni extra** (somma): Spioncino digitale +150 / Maniglione antipanico +180 / Serratura maggiorata a 5 punti +220 €
6. **Arrotondamento**: risultato finale a 2 decimali

### 3.3 Pergole

Prezzo base al m² 260 €/m² (fittizio). Soglia e percentuale di sconto
volume diverse dalle finestre, perché le superfici tipiche di una pergola
sono molto più grandi.

1. **Area in m²**: `area_m2 = (larghezza_mm × sporgenza_mm) / 1_000_000`
2. **Prezzo base per area**: `area_m2 × 260`
3. **Moltiplicatori a cascata**: `× moltiplicatore_materiale × moltiplicatore_sistema/copertura`
4. **Supplemento colore** (aggiunta fissa): Bianco +0 / Grigio antracite +80 / Testa di moro +100 €
5. **Opzioni extra** (somma): Chiusure laterali in vetro +850 / Illuminazione LED +320 / Sensori pioggia/vento +380 €
6. **Sconto volume**: se `area_m2 > 15`, sconto dell'8% sul totale
7. **Arrotondamento**: risultato finale a 2 decimali

Ogni funzione `calculate_price()` ritorna sia il prezzo finale sia il
breakdown completo di ogni componente (usato sia per debug che per la
visualizzazione lato utente in `PriceBreakdown.tsx`).
