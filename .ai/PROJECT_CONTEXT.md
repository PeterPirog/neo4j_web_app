# Project Context

Ten projekt to aplikacja webowa FastAPI + Neo4j. Obecny zakres obejmuje edukacyjny interfejs Jinja2/Bootstrap oraz operacje na węzłach `Person`, węzłach `City` i relacjach `MIESZKA_W`.

## Stos

- FastAPI jako framework HTTP.
- Jinja2 Templates jako warstwa widoków HTML.
- Bootstrap 5 jako podstawowy system UI.
- Oficjalny async Neo4j driver przez `neo4j-rust-ext`.
- Czysty, parametryzowany Cypher.
- Lokalna baza Neo4j.
- MCP Neo4j wyłącznie jako narzędzie diagnostyczne agenta.

## Granice projektu

Aplikacja runtime nie może zależeć od MCP. Runtime komunikuje się z bazą wyłącznie przez `AsyncGraphDatabase`.

Nie dodawaj Django, SQLAlchemy, neomodel, OGM, GraphQL ani synchronicznego drivera Neo4j.

## Aktualny model danych

- `(:Person {id, name, email, note, created_at, updated_at})`
- `(:City {id, name, country, note, created_at, updated_at})`
- `(:Person)-[:MIESZKA_W {created_at, updated_at}]->(:City)`

Relacja `MIESZKA_W` jest tworzona przez formularz przypisania osoby do miasta. Usuwanie osoby lub miasta używa ograniczonego `MATCH` po `id` i usuwa także relacje tej encji, żeby można było ćwiczyć pełny cykl CRUD w lokalnej bazie.

## Obecne pliki aplikacji

- `app/main.py` - endpointy FastAPI, obsługa formularzy, renderowanie Jinja2.
- `app/db.py` - konfiguracja i cykl życia async drivera Neo4j.
- `app/people_service.py` - warstwa serwisowa dla `Person` oraz idempotentne constrainty i indeksy.
- `app/cities_service.py` - warstwa serwisowa dla `City`.
- `app/relationships_service.py` - warstwa serwisowa dla relacji `MIESZKA_W`.
- `app/templates/people.html` - jeden edukacyjny widok HTML dla osób, miast i relacji.

## Pliki Cypher

- `cypher/schema.cypher` - constrainty i indeksy dla `Person` oraz `City`.
- `cypher/diagnostics.cypher` - bezpieczne zapytania odczytujące etykiety, typy relacji, osoby, miasta i `MIESZKA_W`.
- `cypher/seed_dev.cypher` - niedestrukcyjny seed lokalny oparty o `MERGE`.
- `cypher/dangerous_reset.cypher` - celowo nieaktywny szablon resetu z ostrzeżeniami.

## Kierunek rozwoju

Projekt ma iść w stronę profesjonalnego systemu grafowego z relacjami, uprawnieniami do zasobów, GraphRAG, agentami oraz późniejszym użyciem GDS.
