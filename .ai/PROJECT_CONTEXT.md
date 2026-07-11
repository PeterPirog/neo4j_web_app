# Project Context

Ten projekt to aplikacja webowa FastAPI + Neo4j. Obecny zakres obejmuje prosty interfejs Jinja2/Bootstrap oraz operacje na węzłach `Person`.

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

## Obecne pliki aplikacji

- `app/main.py` - endpointy FastAPI, obsługa formularzy, renderowanie Jinja2.
- `app/db.py` - konfiguracja i cykl życia async drivera Neo4j.
- `app/people_service.py` - warstwa serwisowa z zapytaniami Cypher.
- `app/templates/people.html` - widok HTML.

## Kierunek rozwoju

Projekt ma iść w stronę profesjonalnego systemu grafowego z relacjami, uprawnieniami do zasobów, GraphRAG, agentami oraz późniejszym użyciem GDS.
