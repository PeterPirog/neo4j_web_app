# Neo4j Web App

Monorepo dla aplikacji grafowej opartej o Next.js, FastAPI i Neo4j.

```text
Browser
  |
  v
Next.js / React / TypeScript
  |
  v
FastAPI API
  |
  v
Service layer / query layer
  |
  v
Async Neo4j driver / neo4j-rust-ext
  |
  v
Neo4j
```

Docelowy frontend to `apps/web`. Stary edukacyjny szablon Jinja2 jest zachowany
w `apps/api/app/legacy_templates/` wyłącznie jako materiał historyczny.

## Struktura

- `apps/api` - backend FastAPI, moduły API, service layer, repository layer i Cypher query layer.
- `apps/web` - frontend Next.js App Router, React, TypeScript, Tailwind CSS.
- `packages/api-client` - klient OpenAPI oparty o `openapi-fetch` i typy generowane z FastAPI.
- `database/neo4j` - docelowe migracje, constrainty, indeksy, diagnostyka i seedy Neo4j.
- `cypher` - starszy katalog kompatybilnosciowy dla istniejacych lokalnych odwolan.
- `docs` - dokumentacja architektury, API, frontendu, modelu danych i ADR.
- `prompts` - prompty robocze dla Codexa.
- `.ai` - kontekst i reguły dla agentów.

## Wymagania

- Python 3.11+; projekt lokalnie był walidowany na Pythonie 3.12.
- Node.js LTS; lokalnie użyto Node `v24.13.0` i npm `11.6.2`.
- npm.
- Git.
- Lokalny Neo4j z włączonym Bolt.
- Opcjonalnie MCP Neo4j dla diagnostyki agentów.

## Neo4j

Domyślny lokalny URI:

```text
bolt://localhost:7687
```

Wymagane zmienne:

```text
NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
NEO4J_DATABASE
```

Prawdziwych plików `.env` i haseł nie commitujemy.

## Pliki .env

Root:

```powershell
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

Backend:

```powershell
cd apps/api
copy .env.example .env
```

Frontend:

```powershell
cd apps/web
copy .env.example .env.local
```

Różnice:

- Root `.env` jest wygodnym wspólnym plikiem lokalnym.
- `apps/api/.env` jest czytany przez FastAPI i zawiera dane Neo4j.
- `apps/web/.env.local` jest czytany przez Next.js i zawiera `NEXT_PUBLIC_API_BASE_URL`.

Przykładowe wartości:

```text
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=change_me
NEO4J_DATABASE=neo4j
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Backend Install

Windows:

```powershell
cd apps/api
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Właściwy plik zależności backendu to `apps/api/requirements.txt`.
Root `requirements.txt` jest tylko shimem zgodnościowym dla starszych komend i
deleguje do `apps/api/requirements.txt`.

## Backend Run

```powershell
cd apps/api
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Adresy:

- `http://127.0.0.1:8000/api/v1/health`
- `http://127.0.0.1:8000/api/health` - legacy alias
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/openapi.json`

## Frontend Install

Z root projektu:

```powershell
npm install
```

## Frontend Run

```powershell
npm run dev:web
```

Adres:

```text
http://127.0.0.1:3000
```

## Uruchomienie jednym skryptem

Z root projektu:

```powershell
python scripts/dev_start.py
```

Skrypt sprawdza dostępność Neo4j Bolt, uruchamia brakujący backend FastAPI,
czeka na `/api/v1/health`, generuje OpenAPI client, uruchamia frontend Next.js i
wypisuje końcowe adresy aplikacji. Nie uruchamia Neo4j samodzielnie i nie
modyfikuje danych w bazie.

Przydatne flagi:

```powershell
python scripts/dev_start.py --check-only
python scripts/dev_start.py --open-browser
python scripts/dev_start.py --skip-openapi
python scripts/dev_start.py --api-port 8001 --web-port 3001
```

`--check-only` tylko sprawdza stan plików i usług: nie tworzy `.env`, nie
instaluje zależności i nie uruchamia procesów. Jeżeli skrypt uruchomi backend
lub frontend, zatrzyma tylko własne procesy po `Ctrl+C`. Istniejące procesy na
portach `8000` lub `3000` są używane, jeśli odpowiadają poprawnie; skrypt nie
zabija ich automatycznie.

## Zatrzymywanie usług uruchomionych lokalnie

Z root projektu:

```powershell
python scripts/dev_stop.py --check-only
python scripts/dev_stop.py --dry-run
python scripts/dev_stop.py
python scripts/dev_stop.py --yes
```

Skrypt zatrzymuje tylko lokalne procesy FastAPI/Uvicorn i Next.js pasujące do
tego projektu. Domyślne `python scripts/dev_stop.py` działa w dwóch trybach:
w terminalu pyta `y/N`, a w PyCharm albo innym runnerze bez interaktywnego
stdin pokazuje okno `Yes/No` przez `tkinter`.

`--dry-run` tylko wypisuje kandydatów i niczego nie zatrzymuje. `--check-only`
tylko sprawdza porty i procesy. `--yes` zatrzymuje wykryte procesy backendu i
frontendu bez pytania, co jest przydatne w PyCharm.

Neo4j nie jest zatrzymywany przez ten skrypt. `dev_start.py` tylko sprawdza
dostępność Neo4j Bolt i nie uruchamia bazy danych, więc `dev_stop.py` celowo nie
zamyka portów `7474` ani `7687`.

## Kolejność Uruchamiania

Terminal 1: Neo4j.

Terminal 2: backend FastAPI:

```powershell
cd apps/api
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Terminal 3: frontend Next.js:

```powershell
npm run dev:web
```

## OpenAPI Client

Najpierw backend musi działać na porcie `8000`.

Z root projektu:

```powershell
npm run generate:api-client
```

FastAPI generuje `openapi.json`, `openapi-typescript` generuje
`packages/api-client/src/schema.d.ts`, a frontend korzysta z klienta i typów z
`packages/api-client`.

## Testy I Walidacja

Backend:

```powershell
cd apps/api
python -m compileall app
python -c "from app.main import app; print('OK')"
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

OpenAPI, przy działającym backendzie:

```powershell
npm run generate:api-client
```

Frontend:

```powershell
npm run typecheck:web
npm run lint:web
npm run test:e2e
```

Obecne testy Playwright są smoke testami UI i nie modyfikują danych Neo4j.

## MCP Neo4j

MCP Neo4j jest narzędziem diagnostycznym dla agenta/Codexa. Aplikacja runtime
nie importuje MCP i MCP nie jest dependency backendu.

Przykładowe zapytania read-only:

```cypher
CALL dbms.components();
SHOW CONSTRAINTS;
SHOW INDEXES;
MATCH (p:Person) RETURN count(p) AS people_count;
```

Nie używaj MCP do destrukcyjnych operacji bez wyraźnego polecenia.

### Konfiguracja MCP dla agentów

Projekt zawiera gotowe pliki konfiguracyjne MCP Neo4j:

- `opencode.jsonc` – konfiguracja MCP dla OpenCode (używa zmiennych środowiskowych)
- `.mcp.neo4j.example.json` – przykład konfiguracji dla innych klientów MCP (Cursor, Claude Desktop itp.)

**OpenCode** – po skopiowaniu `.env.example` → `.env` i ustawieniu hasła, MCP Neo4j
jest automatycznie dostępne po uruchomieniu `opencode` w katalogu projektu.

**Inne klienty MCP** – skopiuj `.mcp.neo4j.example.json` do odpowiedniego pliku
konfiguracyjnego klienta (np. `.cursor/mcp.json` dla Cursor) i podmień hasło.

Szczegółowe zasady użycia MCP Neo4j przez agentów znajdują się w `.ai/MCP_NEO4J_GUIDE.md`.

## Porty

- Neo4j Browser: zwykle `7474`.
- Neo4j Bolt: `7687`.
- FastAPI: `8000`.
- Next.js: `3000`.

## API Endpoints

- `GET /api/v1/health`
- `GET /api/v1/people`
- `POST /api/v1/people`
- `GET /api/v1/people/{person_id}`
- `PATCH /api/v1/people/{person_id}`
- `DELETE /api/v1/people/{person_id}`
- `GET /api/v1/relations`
- `POST /api/v1/relations`
- `DELETE /api/v1/relations/{relationship_id}`
- `GET /api/v1/permissions/health`
- `GET /api/v1/graph/health`
- `GET /api/v1/ai/health`
- `GET /api/v1/ml/health`

Stare endpointy `/api/...` sa utrzymane jako aliasy kompatybilnosciowe, ale
nowe integracje powinny uzywac `/api/v1/...`.

## Frontend Routes

- `/`
- `/people`
- `/relations`

## Zasady Architektury

- Frontend nie łączy się z Neo4j.
- Frontend nie zawiera Cyphera.
- Backend ukrywa strukturę grafu za API.
- Cypher znajduje się w query layer.
- Service layer zawiera logikę aplikacyjną.
- FastAPI jest kontraktem API.
- OpenAPI client zapewnia typy dla TypeScript.

## Zakazane Technologie

Na tym etapie nie używamy:

- Django.
- Django ORM.
- SQLAlchemy.
- neomodel.
- OGM.
- GraphQL.

## Troubleshooting

### Neo4j connection failed

Sprawdź, czy Neo4j działa, czy Bolt jest dostępny na `7687`, oraz czy
`NEO4J_URI`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` i `NEO4J_DATABASE` są poprawne.

### Port 8000 jest zajęty

Sprawdź procesy Uvicorn na Windows:

```powershell
Get-CimInstance Win32_Process -Filter "name = 'python.exe'" |
  Where-Object { $_.CommandLine -like '*uvicorn*' } |
  Select-Object ProcessId, CommandLine
```

Jeżeli to Twój proces z bieżącego terminala, zamknij go przez `Ctrl+C`.
Nie zabijaj cudzych procesów bez upewnienia się, co uruchamiają.

### Port 3000 jest zajęty

Next.js może zaproponować inny port. Dla standardowego uruchomienia zatrzymaj
poprzedni proces `npm run dev:web` przez `Ctrl+C`.

### CORS error

Backend dopuszcza lokalne originy:

```text
http://localhost:3000
http://127.0.0.1:3000
```

Jeżeli frontend działa na innym porcie, trzeba świadomie dodać origin w
`apps/api/app/core/config.py`.

### OpenAPI generation fails

Upewnij się, że backend działa:

```powershell
curl http://127.0.0.1:8000/openapi.json
```

Następnie uruchom:

```powershell
npm run generate:api-client
```

### schema.d.ts jest nieaktualny

Uruchom backend na `8000`, a potem:

```powershell
npm run generate:api-client
```

### Frontend nie widzi backendu

Sprawdź `NEXT_PUBLIC_API_BASE_URL` w `apps/web/.env.local`.
Domyślnie powinno być:

```text
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### Backend działa, ale frontend pokazuje error

Sprawdź:

- czy backend odpowiada na `/api/v1/health`,
- czy CORS dopuszcza origin frontendu,
- czy `packages/api-client/src/schema.d.ts` jest aktualny,
- czy w terminalu Next.js nie ma błędów requestów.

### npm audit moderate vulnerabilities

Aktualnie `npm audit` może zgłaszać podatność `postcss <8.5.10` przez `next`.
Npm proponuje naprawę tylko przez `npm audit fix --force`, co oznacza breaking
change. Nie wykonuj `--force` bez świadomej decyzji o większej aktualizacji.

### Next.js allowedDevOrigins warning

Podczas testów/dev servera Next.js może ostrzegać o przyszłej konfiguracji
`allowedDevOrigins`. Nie dodawaj tej opcji, dopóki lokalna wersja Next.js i jej
typy nie potwierdzają wsparcia konfiguracji.
