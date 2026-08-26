# Coges Configurator — Prototipo

Prototipo di configuratore infissi multi-categoria (Finestre, Portoncini,
Pergole) con stima di prezzo. Dati fittizi, modellato sulla struttura reale
del catalogo di [cogesinfissi.it](https://www.cogesinfissi.it), pensato per
una demo con il cliente prima di sviluppare la versione di produzione con lo
stesso stack tecnologico. Per il dettaglio di schema dati, contratto API,
formula di pricing e cosa è reale vs fittizio vedi [SPEC.md](SPEC.md).

**Stack**: React + Vite + TypeScript + Tailwind (frontend) · FastAPI +
SQLModel (backend) · PostgreSQL (database, ospitato su Railway).

---

## 0. Prerequisiti

- Python 3.11+ (verifica con `python3 --version`)
- Node.js 18+ e npm (verifica con `node --version`)
- Un account [Railway](https://railway.app) con un servizio PostgreSQL già
  creato (vedi sezione 1)

---

## 1. Database (Railway)

Il database non gira in locale: è un servizio PostgreSQL su Railway,
raggiunto dal backend tramite connection string.

1. Su [railway.app](https://railway.app), crea un progetto → **New** →
   **Database** → **Add PostgreSQL**.
2. Apri il servizio Postgres creato → tab **Variables** → copia il valore
   di `DATABASE_PUBLIC_URL` (quello con hostname pubblico
   `*.proxy.rlwy.net` o simile — necessario per connettersi da fuori
   Railway, cioè dal tuo pc in locale. `DATABASE_URL`, senza "PUBLIC",
   funziona solo tra servizi dentro Railway).
3. Incolla quel valore come `DATABASE_URL` nel file `.env` del backend
   (vedi sezione 2).

Non serve avviare/fermare nulla in locale: il database è sempre attivo su
Railway finché il servizio esiste nel tuo progetto.

---

Terminale 1 — Backend:

cd /Users/antonio/workspace/prototipo1/coges-configurator/backend
source .venv/bin/activate
uvicorn app.main:app --reload

Aspetta che compaia una riga tipo Uvicorn running on http://127.0.0.1:8000.

Terminale 2 — Frontend:

cd /Users/antonio/workspace/prototipo1/coges-configurator/frontend
npm run dev

Aspetta la riga Local: http://localhost:5173/.

## 2. Setup ed avvio del backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # su Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
```

Apri `.env` e sostituisci `DATABASE_URL` con la connection string pubblica
copiata da Railway al punto 1.

Popola il database con i dati fittizi di catalogo (materiali, vetri, colori,
opzioni extra, tipo prodotto):

```bash
python seed.py
```

Avvia il backend:

```bash
uvicorn app.main:app --reload
```

Il backend è disponibile su `http://localhost:8000`. Swagger UI interattivo
su [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 3. Setup ed avvio del frontend

In un altro terminale, dalla root del progetto:

```bash
cd frontend
npm install
cp .env.example .env             
npm run dev
```

Il frontend è disponibile su `http://localhost:5173`.

---

## 4. Esecuzione dei test

I test coprono la logica di calcolo prezzo delle 3 famiglie prodotto
(`backend/app/services/pricing_finestre.py`, `pricing_portoncini.py`,
`pricing_pergole.py`):

```bash
cd backend
source .venv/bin/activate        # se non già attivo
pytest tests/ -v
```

---

## Struttura del progetto

```
coges-configurator/
├── backend/
│   ├── app/
│   │   ├── main.py                 # entrypoint FastAPI, CORS, router
│   │   ├── config.py               # lettura .env
│   │   ├── db.py                   # connessione database
│   │   ├── schemas/                # contratto request/response (Pydantic)
│   │   │   ├── common.py
│   │   │   ├── finestre.py
│   │   │   ├── portoncini.py
│   │   │   └── pergole.py
│   │   ├── models/                 # tabelle DB (SQLModel), una famiglia per file
│   │   │   ├── finestre.py         # Materiale -> Sistema -> Profilo, tipo apertura, vetro, colore, extra
│   │   │   ├── portoncini.py       # Materiale, Marca, Classe sicurezza, colore, extra
│   │   │   ├── pergole.py          # Materiale, Sistema/copertura, colore, extra
│   │   │   └── configuration.py    # SavedConfiguration (generica, JSON per famiglia)
│   │   ├── routes/                 # endpoint API, un router per famiglia
│   │   │   ├── product_families.py # GET /api/product-families
│   │   │   ├── finestre.py
│   │   │   ├── portoncini.py
│   │   │   └── pergole.py
│   │   └── services/               # business logic isolata, una formula per famiglia
│   │       ├── pricing_finestre.py
│   │       ├── pricing_portoncini.py
│   │       └── pricing_pergole.py
│   ├── tests/                      # test pytest sulla pricing logic, uno per famiglia
│   ├── alembic/                    # migrazioni database (predisposto, non ancora usato)
│   ├── seed.py                     # popola il DB con dati fittizi di catalogo (3 famiglie)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/              # componenti generici riutilizzabili tra famiglie
│   │   │   ├── OptionSelector.tsx        # scelta singola (radio)
│   │   │   ├── MultiOptionSelector.tsx   # scelta multipla (checkbox)
│   │   │   ├── DimensionSlider.tsx
│   │   │   ├── PriceBreakdown.tsx        # generico, a righe
│   │   │   └── BackToHomeLink.tsx
│   │   ├── pages/                   # HomePage (selezione categoria) + un configuratore per famiglia
│   │   │   ├── HomePage.tsx
│   │   │   ├── ConfiguratorFinestre.tsx
│   │   │   ├── ConfiguratorPortoncini.tsx
│   │   │   └── ConfiguratorPergole.tsx
│   │   ├── services/                # chiamate API
│   │   └── types/                   # TypeScript types condivisi
│   ├── package.json
│   └── .env.example
├── SPEC.md                     # schema dati, contratto API, formule pricing, cosa è reale vs fittizio
└── README.md
```

## Cosa NON è incluso nel prototipo

Deliberatamente fuori scope per questa fase: autenticazione/login, invio
email, generazione PDF, cache/code asincrone. Vedi [SPEC.md](SPEC.md) per il
dettaglio dei dati fittizi usati e per cosa cambierà nella versione di
produzione.
