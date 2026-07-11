Jesteś agentem GPT Codex pracującym lokalnie w PyCharm nad projektem FastAPI + Neo4j.

Twoje zadanie:
Przekształć obecny edukacyjny projekt FastAPI + Jinja2 + Neo4j w docelową strukturę projektu przygotowaną na wieloletni rozwój, zgodnie z architekturą:

Browser
  ↓
Frontend: React / TypeScript / Next.js
  ↓
Backend API: FastAPI
  ↓
Service layer / query layer
  ↓
Async Neo4j driver / neo4j-rust-ext
  ↓
Neo4j

Docelowy stack frontendu:

| Element         | Rola                                                                   |
| --------------- | ---------------------------------------------------------------------- |
| React           | komponenty UI                                                          |
| TypeScript      | typy i kontrakty                                                       |
| Next.js         | routing, layouty, SSR/BFF, organizacja aplikacji                       |
| TanStack Query  | pobieranie danych, cache po stronie klienta, invalidation po mutacjach |
| React Hook Form | formularze                                                             |
| Zod             | walidacja po stronie frontendu                                         |
| Tailwind CSS    | design system na tym etapie                                            |
| Playwright      | testy end-to-end                                                       |
| OpenAPI client  | automatycznie generowany klient API z FastAPI                          |

Bardzo ważne zasady bezpieczeństwa Git:

1. Przed jakąkolwiek zmianą wykonaj:
   git branch --show-current

2. Jeżeli aktualna gałąź NIE nazywa się dokładnie:
   React-TypeScript-Next.js

   to natychmiast przerwij pracę i napisz:
   "Nie jestem na gałęzi React-TypeScript-Next.js. Przerywam, żeby nie naruszyć main."

3. Nie przełączaj się na main.
4. Nie wykonuj merge z main.
5. Nie wykonuj rebase na main.
6. Nie pushuj zmian.
7. Nie commituj zmian automatycznie, chyba że użytkownik później wyraźnie o to poprosi.
8. Pracuj tylko na aktualnej gałęzi roboczej.
9. Na początku pokaż wynik:
   git status --short

Bardzo ważne zasady dotyczące Neo4j:

1. Nie usuwaj danych z bazy.
2. Nie wykonuj:
   MATCH (n) DETACH DELETE n
3. Nie usuwaj constraintów.
4. Nie usuwaj indeksów.
5. Nie resetuj bazy.
6. Nie twórz dużych danych testowych.
7. Jeżeli potrzebujesz danych testowych, utwórz maksymalnie 2-3 węzły Person i 1-2 relacje, ale tylko wtedy, gdy baza jest pusta.
8. MCP Neo4j może być używany wyłącznie jako narzędzie diagnostyczne agenta.
9. MCP Neo4j nie może zostać dodane jako dependency runtime aplikacji.
10. Aplikacja musi komunikować się z Neo4j przez oficjalny async Neo4j driver / neo4j-rust-ext.

Bardzo ważne zasady architektury:

1. Nie używaj Django.
2. Nie używaj Django ORM.
3. Nie używaj SQLAlchemy.
4. Nie używaj neomodel.
5. Nie używaj OGM.
6. Nie dodawaj GraphQL na tym etapie.
7. Nie umieszczaj Cyphera w frontendzie.
8. Nie pozwól frontendowi komunikować się bezpośrednio z Neo4j.
9. Frontend komunikuje się wyłącznie z FastAPI.
10. FastAPI komunikuje się z Neo4j przez service layer / repository / query layer.

Najpierw przeczytaj, jeśli istnieją:

- AGENTS.md
- README.md
- .ai/PROJECT_CONTEXT.md
- .ai/ARCHITECTURE.md
- .ai/AGENT_RULES.md
- .ai/CYPHER_STYLE_GUIDE.md
- .ai/MCP_NEO4J_GUIDE.md
- .ai/SECURITY_RULES.md
- .ai/DEFINITION_OF_DONE.md

Jeżeli te pliki nie istnieją, nie przerywaj pracy. Kontynuuj według tej specyfikacji.

============================================================
CEL TRANSFORMACJI
============================================================

Obecny projekt edukacyjny ma zostać przekształcony w strukturę typu monorepo:

project-root/
  apps/
    api/
      app/
        main.py
        core/
        db/
        modules/
          people/
          relations/
          permissions/
          graph_explorer/
          ai/
          ml/
      requirements.txt
      README.md

    web/
      Next.js application

  packages/
    api-client/
      TypeScript OpenAPI client generated from FastAPI

  cypher/
    migrations/
    constraints/
    indexes/
    diagnostics/
    seed/

  docs/
    architecture/
    adr/
    onboarding/
    data-model/
    api-contracts/
    frontend/

  prompts/

  AGENTS.md
  README.md
  package.json
  .gitignore
  .env.example

Jeżeli przeniesienie aktualnego backendu do apps/api jest możliwe bez dużego ryzyka, wykonaj je.

Jeżeli projekt ma jeszcze prostą strukturę:

app/
  main.py
  db.py
  people_service.py
  relations_service.py
  templates/

to przenieś ją do:

apps/api/app/

i popraw importy tak, aby backend uruchamiał się z katalogu apps/api komendą:

uvicorn app.main:app --reload --port 8000

Nie usuwaj starego kodu bez upewnienia się, że nowy układ działa.

============================================================
CZĘŚĆ 1 — AUDYT PRZED ZMIANAMI
============================================================

Wykonaj audyt projektu:

1. Sprawdź aktualną gałąź:
   git branch --show-current

2. Sprawdź status:
   git status --short

3. Sprawdź strukturę plików.

4. Sprawdź istniejące endpointy FastAPI.

5. Sprawdź, czy backend używa:
   - FastAPI
   - async Neo4j driver
   - czystego Cyphera
   - Jinja2 jako starego UI

6. Sprawdź, czy są endpointy:
   - /
   - /health
   - /people/create
   - /people/update
   - /people/delete
   - /relations
   - /relations/create
   - /relations/delete

7. Sprawdź, czy istnieje warstwa service dla Neo4j.

8. Sprawdź requirements.txt.

9. Jeżeli MCP Neo4j jest dostępny, wykonaj diagnostykę:

CALL dbms.components();

SHOW CONSTRAINTS;

SHOW INDEXES;

MATCH (p:Person)
RETURN count(p) AS people_count;

MATCH (:Person)-[r]->(:Person)
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;

Nie wykonuj zapytań destrukcyjnych.

============================================================
CZĘŚĆ 2 — BACKEND FASTAPI JAKO API JSON
============================================================

Przekształć backend w docelowe API JSON dla frontendu Next.js.

Backend ma znajdować się w:

apps/api/app/

Docelowa struktura backendu:

apps/api/app/
  main.py

  core/
    config.py
    cors.py
    errors.py
    logging.py

  db/
    neo4j.py

  modules/
    people/
      router.py
      schemas.py
      service.py
      repository.py
      queries.py

    relations/
      router.py
      schemas.py
      service.py
      repository.py
      queries.py

    permissions/
      router.py
      schemas.py
      service.py

    graph_explorer/
      router.py
      schemas.py
      service.py

    ai/
      router.py
      schemas.py
      service.py

    ml/
      router.py
      schemas.py
      service.py

Zasady:

1. app/main.py ma tylko:
   - tworzyć FastAPI app,
   - konfigurować lifespan,
   - konfigurować CORS,
   - rejestrować routery,
   - definiować root endpoint i health endpoint.

2. Zapytania Cypher nie mogą być w main.py.

3. Zapytania Cypher mają być w:
   modules/<module>/queries.py

4. Bezpośrednie wywołania Neo4j mają być w:
   modules/<module>/repository.py

5. Logika biznesowa ma być w:
   modules/<module>/service.py

6. Modele wejścia/wyjścia mają być w:
   modules/<module>/schemas.py

7. Endpointy HTTP mają być w:
   modules/<module>/router.py

8. Używaj Pydantic response_model.

9. Używaj parametrów Cypher.
   Dobrze:
   MATCH (p:Person {id: $id})

   Źle:
   f"MATCH (p:Person {{id: '{id}'}})"

10. Wyjątek: dynamiczny typ relacji może być wstawiony do Cyphera tylko po walidacji whitelistą.

Whitelist relacji:

ALLOWED_RELATIONSHIP_TYPES = {
    "KNOWS",
    "WORKS_WITH",
    "MANAGES",
    "REPORTS_TO",
    "RELATED_TO",
}

============================================================
CZĘŚĆ 3 — ENDPOINTY BACKEND API
============================================================

Dodaj albo przekształć endpointy do formatu API JSON.

Health:

GET /api/health

Response:

{
  "status": "ok",
  "neo4j": "connected"
}

People:

GET /api/people

Response:
list[PersonRead]

POST /api/people

Body:
{
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "note": "opis"
}

Response:
PersonRead

GET /api/people/{person_id}

Response:
PersonRead

PATCH /api/people/{person_id}

Body:
{
  "name": "Nowa nazwa",
  "email": "nowy@example.com",
  "note": "nowa notatka"
}

Response:
PersonRead

DELETE /api/people/{person_id}

Response:
{
  "deleted": true
}

Relations:

GET /api/relations

Response:
list[RelationshipRead]

POST /api/relations

Body:
{
  "source_person_id": "...",
  "target_person_id": "...",
  "relationship_type": "KNOWS",
  "note": "znają się z projektu",
  "strength": 7
}

Response:
RelationshipRead

DELETE /api/relations/{relationship_id}

Response:
{
  "deleted": true
}

Permissions placeholder:

GET /api/permissions/health

Response:
{
  "module": "permissions",
  "status": "placeholder"
}

Graph explorer placeholder:

GET /api/graph/health

Response:
{
  "module": "graph_explorer",
  "status": "placeholder"
}

AI placeholder:

GET /api/ai/health

Response:
{
  "module": "ai",
  "status": "placeholder"
}

ML placeholder:

GET /api/ml/health

Response:
{
  "module": "ml",
  "status": "placeholder"
}

Te placeholdery są ważne, bo projekt ma być przygotowany pod długoterminowy rozwój przez osobne zespoły:
- database,
- machine learning,
- frontend,
- backend.

Nie implementuj jeszcze pełnej logiki permissions, AI ani ML.

============================================================
CZĘŚĆ 4 — MODELE PYDANTIC
============================================================

Dodaj modele Pydantic.

People:

PersonCreate:
- name: str
- email: str | None
- note: str | None

PersonUpdate:
- name: str | None
- email: str | None
- note: str | None

PersonRead:
- id: str
- name: str
- email: str | None
- note: str | None

Relations:

RelationshipCreate:
- source_person_id: str
- target_person_id: str
- relationship_type: str
- note: str | None
- strength: int | None

Walidacja:
- source_person_id wymagane
- target_person_id wymagane
- source_person_id != target_person_id
- relationship_type w whitelist
- strength jeśli podane, od 1 do 10

RelationshipRead:
- id: str
- source_id: str
- source_name: str
- target_id: str
- target_name: str
- relationship_type: str
- note: str | None
- strength: int | None

============================================================
CZĘŚĆ 5 — NEO4J DRIVER
============================================================

W apps/api/app/db/neo4j.py utwórz albo przenieś konfigurację Neo4j.

Wymagania:

1. Wczytuj konfigurację z .env:
   NEO4J_URI
   NEO4J_USERNAME
   NEO4J_PASSWORD
   NEO4J_DATABASE

2. Użyj:
   from neo4j import AsyncGraphDatabase

3. Utwórz driver raz w lifespan aplikacji.

4. Na starcie:
   await driver.verify_connectivity()

5. Na zamknięciu:
   await driver.close()

6. Każde zapytanie ma jawnie przekazywać database=NEO4J_DATABASE.

7. Przygotuj funkcję dependency albo globalny manager, który repository może bezpiecznie używać.

8. Nie twórz nowego drivera per request.

============================================================
CZĘŚĆ 6 — CYPHER
============================================================

People queries:

Constraint:

CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;

Create Person:

CREATE (p:Person {
  id: randomUUID(),
  name: $name,
  email: $email,
  note: $note,
  created_at: datetime(),
  updated_at: datetime()
})
RETURN
  p.id AS id,
  p.name AS name,
  properties(p)['email'] AS email,
  properties(p)['note'] AS note;

List People:

MATCH (p:Person)
RETURN
  p.id AS id,
  p.name AS name,
  properties(p)['email'] AS email,
  properties(p)['note'] AS note
ORDER BY coalesce(
  properties(p)['updated_at'],
  properties(p)['created_at']
) DESC
LIMIT 200;

Get Person:

MATCH (p:Person {id: $id})
RETURN
  p.id AS id,
  p.name AS name,
  properties(p)['email'] AS email,
  properties(p)['note'] AS note
LIMIT 1;

Update Person:

MATCH (p:Person {id: $id})
SET
  p.name = coalesce($name, p.name),
  p.email = coalesce($email, properties(p)['email']),
  p.note = coalesce($note, properties(p)['note']),
  p.updated_at = datetime()
RETURN
  p.id AS id,
  p.name AS name,
  properties(p)['email'] AS email,
  properties(p)['note'] AS note;

Delete Person:

MATCH (p:Person {id: $id})
DETACH DELETE p;

Relations queries:

List Relations:

MATCH (source:Person)-[r]->(target:Person)
RETURN
  properties(r)['id'] AS id,
  source.id AS source_id,
  source.name AS source_name,
  target.id AS target_id,
  target.name AS target_name,
  type(r) AS relationship_type,
  properties(r)['note'] AS note,
  properties(r)['strength'] AS strength
ORDER BY coalesce(
  properties(r)['updated_at'],
  properties(r)['created_at']
) DESC
LIMIT 200;

Create Relationship:

MATCH (source:Person {id: $source_person_id})
MATCH (target:Person {id: $target_person_id})
MERGE (source)-[r:RELATIONSHIP_TYPE]->(target)
ON CREATE SET
  r.id = randomUUID(),
  r.created_at = datetime()
SET
  r.note = $note,
  r.strength = $strength,
  r.updated_at = datetime()
RETURN
  properties(r)['id'] AS id,
  source.id AS source_id,
  source.name AS source_name,
  target.id AS target_id,
  target.name AS target_name,
  type(r) AS relationship_type,
  properties(r)['note'] AS note,
  properties(r)['strength'] AS strength;

RELATIONSHIP_TYPE wolno wstawić do query tylko po walidacji whitelistą.

Delete Relationship:

MATCH ()-[r]->()
WHERE properties(r)['id'] = $relationship_id
DELETE r;

============================================================
CZĘŚĆ 7 — CORS
============================================================

Frontend Next.js będzie działał lokalnie na:

http://localhost:3000
http://127.0.0.1:3000

Backend FastAPI będzie działał lokalnie na:

http://localhost:8000
http://127.0.0.1:8000

Dodaj CORS middleware w backendzie.

Dozwolone origins w dev:

[
  "http://localhost:3000",
  "http://127.0.0.1:3000"
]

Nie ustawiaj allow_origins=["*"] jako docelowego rozwiązania.

============================================================
CZĘŚĆ 8 — FRONTEND NEXT.JS
============================================================

Utwórz aplikację Next.js w:

apps/web/

Użyj:

- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- ESLint
- src directory
- alias @/*

Jeżeli środowisko pozwala, użyj nieinteraktywnej komendy:

npx create-next-app@latest apps/web --ts --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm

Jeżeli create-next-app nie działa, utwórz strukturę ręcznie.

Dodaj dependencies:

- @tanstack/react-query
- react-hook-form
- zod
- @hookform/resolvers
- openapi-fetch

Dodaj devDependencies:

- openapi-typescript
- @playwright/test

Struktura frontendu:

apps/web/
  src/
    app/
      layout.tsx
      page.tsx
      people/
        page.tsx
      relations/
        page.tsx

    components/
      app-shell/
        AppShell.tsx
        Navigation.tsx

      people/
        PersonForm.tsx
        PeopleList.tsx

      relations/
        RelationshipForm.tsx
        RelationshipList.tsx

      ui/
        Button.tsx
        Input.tsx
        Select.tsx
        Textarea.tsx
        Card.tsx

    lib/
      api/
        client.ts
      query/
        QueryProvider.tsx
      config.ts

    features/
      people/
        api.ts
        schemas.ts
        hooks.ts

      relations/
        api.ts
        schemas.ts
        hooks.ts

  tests/
    smoke.spec.ts

Frontend pages:

1. /
   - dashboard
   - linki do People i Relations
   - krótki opis architektury

2. /people
   - lista osób
   - formularz tworzenia osoby
   - przycisk usuwania
   - opcjonalnie prosty tryb edycji

3. /relations
   - lista relacji
   - formularz tworzenia relacji
   - select source person
   - select target person
   - select relationship type
   - note
   - strength 1-10
   - przycisk usuwania relacji

Navbar:

- Dashboard
- People
- Relations
- Permissions
- AI / GraphRAG
- ML

Permissions, AI / GraphRAG i ML mogą być disabled albo prowadzić do placeholderów.

============================================================
CZĘŚĆ 9 — TANSTACK QUERY
============================================================

Dodaj QueryProvider w:

src/lib/query/QueryProvider.tsx

Użyj go w app/layout.tsx.

Dla People dodaj hooks:

usePeople()
useCreatePerson()
useUpdatePerson()
useDeletePerson()

Dla Relations dodaj hooks:

useRelations()
useCreateRelationship()
useDeleteRelationship()

Po mutacjach wykonuj invalidation:

queryClient.invalidateQueries({ queryKey: ["people"] })
queryClient.invalidateQueries({ queryKey: ["relations"] })

Przy tworzeniu/usuwaniu relacji invaliduj też people, jeśli potrzebne.

============================================================
CZĘŚĆ 10 — REACT HOOK FORM + ZOD
============================================================

Formularze mają używać:

- React Hook Form
- Zod
- @hookform/resolvers/zod

Person form schema:

name:
- required
- min length 1

email:
- optional
- email jeśli niepusty

note:
- optional

Relationship form schema:

source_person_id:
- required

target_person_id:
- required

relationship_type:
- enum:
  - KNOWS
  - WORKS_WITH
  - MANAGES
  - REPORTS_TO
  - RELATED_TO

note:
- optional

strength:
- optional
- number
- min 1
- max 10

Waliduj po stronie frontendu, ale pamiętaj:
Backend też musi walidować. Frontend validation nie zastępuje backend validation.

============================================================
CZĘŚĆ 11 — OPENAPI CLIENT
============================================================

Dodaj packages/api-client.

Struktura:

packages/api-client/
  package.json
  src/
    schema.d.ts
    client.ts
    index.ts

Użyj openapi-typescript do generowania typów z FastAPI.

Root package.json powinien zawierać workspaces:

{
  "private": true,
  "workspaces": [
    "apps/web",
    "packages/api-client"
  ],
  "scripts": {
    "dev:web": "npm --workspace apps/web run dev",
    "generate:api-client": "openapi-typescript http://127.0.0.1:8000/openapi.json -o packages/api-client/src/schema.d.ts",
    "typecheck:web": "npm --workspace apps/web run typecheck",
    "lint:web": "npm --workspace apps/web run lint",
    "test:e2e": "npm --workspace apps/web run test:e2e"
  }
}

packages/api-client/src/client.ts ma używać openapi-fetch.

Przykład:

import createClient from "openapi-fetch";
import type { paths } from "./schema";

export const apiClient = createClient<paths>({
  baseUrl: process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000",
});

Jeżeli generowanie typów nie może zostać wykonane, bo backend nie jest uruchomiony, przygotuj skrypt i opisz, jak go uruchomić po starcie backendu.

============================================================
CZĘŚĆ 12 — PLAYWRIGHT
============================================================

Dodaj Playwright w apps/web.

Minimalne testy:

1. Dashboard się ładuje.
2. Nawigacja zawiera:
   - People
   - Relations
   - Permissions
   - AI / GraphRAG
   - ML

3. Strona /people się ładuje.

4. Strona /relations się ładuje.

Nie wykonuj testów niszczących dane.
Nie wymagaj usuwania rekordów w e2e na tym etapie.

Jeśli backend nie jest uruchomiony, testy mogą sprawdzić tylko UI shell albo powinny być opisane jako wymagające backendu.

============================================================
CZĘŚĆ 13 — DOKUMENTACJA
============================================================

Zaktualizuj albo utwórz dokumentację:

README.md

Ma opisywać:

1. Architektura:
   Browser → Next.js → FastAPI → service/query layer → async Neo4j driver → Neo4j

2. Jak uruchomić backend:

cd apps/api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

3. Jak uruchomić frontend:

npm install
npm run dev:web

4. Jak wygenerować OpenAPI client:

Najpierw uruchom backend:
cd apps/api
uvicorn app.main:app --reload --port 8000

Potem w root:
npm run generate:api-client

5. Jak sprawdzić backend:

http://127.0.0.1:8000/api/health

6. Jak sprawdzić frontend:

http://127.0.0.1:3000

7. Jakie są moduły:
   - people
   - relations
   - permissions
   - graph_explorer
   - ai
   - ml

8. Czego nie wolno robić:
   - nie używać ORM/OGM
   - nie pisać Cyphera w frontendzie
   - nie łączyć frontendu z Neo4j
   - nie kasować danych bez jawnej zgody

Dodaj docs:

docs/architecture/target-architecture.md

Zawartość:

- diagram ASCII architektury
- opis warstw
- uzasadnienie rozdziału frontend/backend
- dlaczego frontend nie komunikuje się z Neo4j
- dlaczego FastAPI jest warstwą kontraktu
- dlaczego Cypher jest w query layer

docs/frontend/frontend-guide.md

Zawartość:

- React
- TypeScript
- Next.js App Router
- TanStack Query
- React Hook Form
- Zod
- Tailwind
- OpenAPI client
- Playwright
- jak dodać nową stronę
- jak dodać nowy formularz

docs/api/api-contracts.md

Zawartość:

- opis endpointów
- jak generować OpenAPI client
- zasada: frontend używa kontraktów API, nie Cyphera

docs/data-model/neo4j-model.md

Zawartość:

- Person
- relacje Person-Person
- docelowe placeholdery:
  User
  Role
  Permission
  Resource
  Action
  Prediction

docs/adr/0001-target-architecture-next-fastapi-neo4j.md

Zawartość:

- decyzja: Next.js + FastAPI + Neo4j
- kontekst
- konsekwencje
- alternatywy:
  - Jinja2 only
  - Vue/Nuxt
  - GraphQL-first
  - frontend bezpośrednio do Neo4j
- decyzja końcowa

============================================================
CZĘŚĆ 14 — PLIKI ŚRODOWISKOWE
============================================================

Root .env.example:

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=change_me
NEO4J_DATABASE=neo4j

NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

apps/web/.env.example:

NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

apps/api/.env.example:

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=change_me
NEO4J_DATABASE=neo4j

Nie nadpisuj prawdziwego .env.

============================================================
CZĘŚĆ 15 — GITIGNORE
============================================================

Zaktualizuj .gitignore:

.env
.env.local
apps/api/.env
apps/web/.env.local
.mcp.json
.mcp.local.json
__pycache__/
.venv/
apps/api/.venv/
node_modules/
.next/
playwright-report/
test-results/
coverage/
dist/
build/
.idea/
*.log

Nie ignoruj .env.example.

============================================================
CZĘŚĆ 16 — ZACHOWANIE STAREGO UI
============================================================

Jeżeli obecny backend ma Jinja2 templates, potraktuj je jako legacy educational UI.

Preferowane rozwiązanie:

1. Zachowaj stare szablony w:
   apps/api/app/legacy_templates/

2. Jeżeli istnieją stare endpointy HTML, możesz:
   - zostawić je pod /legacy
   albo
   - opisać w dokumentacji, że zostały zastąpione przez Next.js

3. Nie usuwaj ich bez potrzeby.

4. Nowy frontend Next.js jest docelowy.

============================================================
CZĘŚĆ 17 — TESTY I WERYFIKACJA
============================================================

Po zmianach uruchom, jeśli środowisko pozwala:

Python:

cd apps/api
python -m compileall app

Backend:

uvicorn app.main:app --reload --port 8000

Jeśli nie możesz zostawić procesu uruchomionego, uruchom tylko krótką weryfikację importów i compileall.

Frontend:

npm install
npm run typecheck:web
npm run lint:web

OpenAPI:

Jeżeli backend działa:
npm run generate:api-client

Playwright:

npm --workspace apps/web run test:e2e

Jeżeli Node/npm nie jest dostępny, nie przerywaj całego zadania. Utwórz pliki, opisz ograniczenie i pokaż komendy, które użytkownik ma uruchomić lokalnie.

============================================================
CZĘŚĆ 18 — MCP NEO4J WERYFIKACJA
============================================================

Jeżeli MCP Neo4j jest dostępny, użyj go po zmianach do weryfikacji, że baza nadal działa.

Uruchom tylko zapytania read-only:

CALL dbms.components();

SHOW CONSTRAINTS;

SHOW INDEXES;

MATCH (p:Person)
RETURN count(p) AS people_count;

MATCH (:Person)-[r]->(:Person)
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;

Nie wykonuj zapytań destructive.

============================================================
CZĘŚĆ 19 — MINIMALNY OCZEKIWANY REZULTAT UI
============================================================

Frontend Next.js ma mieć działające ekrany:

1. Dashboard:
   URL:
   http://127.0.0.1:3000/

   Zawartość:
   - tytuł projektu
   - krótki opis architektury
   - link do People
   - link do Relations

2. People:
   URL:
   http://127.0.0.1:3000/people

   Zawartość:
   - lista osób z API
   - formularz dodawania osoby
   - przycisk usuwania osoby
   - informacja o loading/error

3. Relations:
   URL:
   http://127.0.0.1:3000/relations

   Zawartość:
   - lista relacji z API
   - formularz tworzenia relacji
   - select source person
   - select target person
   - select relationship type
   - note
   - strength
   - przycisk usuwania relacji
   - informacja o loading/error

UI może być proste, ale ma być czyste, czytelne i modułowe.

============================================================
CZĘŚĆ 20 — FINALNY RAPORT
============================================================

Na końcu odpowiedz w uporządkowany sposób:

1. Czy potwierdzono pracę na gałęzi:
   React-TypeScript-Next.js

2. Lista zmienionych / utworzonych plików.

3. Co zmieniono w backendzie.

4. Co dodano we frontendzie.

5. Jak działa nowa architektura:

Browser
  ↓
Next.js
  ↓
FastAPI
  ↓
Service/query layer
  ↓
Async Neo4j driver
  ↓
Neo4j

6. Jak uruchomić backend.

7. Jak uruchomić frontend.

8. Jak wygenerować OpenAPI client.

9. Jak uruchomić testy.

10. Jakie kontrole przeszły:
    - compileall
    - typecheck
    - lint
    - e2e
    - MCP diagnostics

11. Jakie kontrole nie mogły zostać wykonane i dlaczego.

12. Czy wykonano jakiekolwiek operacje na bazie Neo4j.

13. Potwierdzenie:
    - main nie został zmodyfikowany,
    - nie było push,
    - nie było commit,
    - nie było destructive Cypher.

Nie kończ pracy po samej analizie. Wprowadź zmiany w projekcie zgodnie z tą specyfikacją, ale tylko na aktywnej gałęzi React-TypeScript-Next.js.