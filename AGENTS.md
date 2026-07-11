# AGENTS.md

## Cel projektu

Projekt to aplikacja webowa dla Neo4j oparta o:

- FastAPI
- Jinja2 Templates
- Bootstrap 5
- async Neo4j driver / neo4j-rust-ext
- czysty Cypher
- lokalną bazę Neo4j
- MCP Neo4j jako narzędzie diagnostyczne agenta

Aplikacja ma być rozwijana w kierunku dużego profesjonalnego systemu grafowego z obsługą:

- relacji w Neo4j,
- uprawnień użytkowników do zasobów,
- AI / GraphRAG,
- agentów,
- GDS / predykcji relacji.

Aktualny zakres edukacyjny obejmuje:

- węzły `Person`,
- węzły `City`,
- relację `(:Person)-[:MIESZKA_W]->(:City)`,
- prosty interfejs CRUD do ćwiczenia dodawania, edycji i usuwania danych oraz relacji.

## Architektura obowiązkowa

Nie używaj:

- Django
- Django ORM
- SQLAlchemy
- neomodel
- OGM
- GraphQL na obecnym etapie
- synchronicznego drivera Neo4j

Używaj:

- FastAPI
- async/await
- `from neo4j import AsyncGraphDatabase`
- surowego Cyphera
- zapytań parametryzowanych
- warstwy serwisowej dla zapytań do Neo4j
- Jinja2 + Bootstrap dla prostego UI

## Zasady pracy z Neo4j

Kod aplikacji komunikuje się z Neo4j przez async Neo4j driver.

MCP Neo4j może być używany przez agenta do:

- diagnostyki,
- sprawdzania schematu,
- liczenia węzłów,
- podglądu relacji,
- testowania zapytań Cypher.

MCP Neo4j nie jest częścią runtime aplikacji.

Nie wolno usuwać danych z bazy bez wyraźnego polecenia użytkownika.

## Bezpieczeństwo Cypher

Zawsze parametryzuj dane użytkownika.

Dobrze:

```cypher
MATCH (p:Person {id: $person_id})
RETURN p
```

Źle:

```python
query = f"MATCH (p:Person {{id: '{person_id}'}}) RETURN p"
```

Nie wykonuj zapytań `DELETE`, `DETACH DELETE`, `DROP CONSTRAINT`, `DROP INDEX` ani masowych `SET` bez jasnej zgody użytkownika.

## Praca agenta

Przed zmianami w kodzie agent powinien:

- przeczytać `README.md`, `AGENTS.md` i pliki w `.ai/`,
- sprawdzić obecne wzorce w `app/`,
- ustalić, czy zmiana dotyczy aplikacji runtime czy wyłącznie diagnostyki,
- nie instalować nowych pakietów bez polecenia użytkownika,
- nie modyfikować `.env` i nie dodawać sekretów do repozytorium.

## Definition of Done

Zmiana jest zakończona, gdy:

- nie narusza architektury FastAPI + async Neo4j driver,
- nie wprowadza ORM, OGM, SQLAlchemy ani runtime MCP,
- używa parametryzowanego Cyphera,
- ma jasną separację endpointów, serwisów i szablonów,
- została zweryfikowana testem, uruchomieniem lub opisem ryzyka, jeżeli testy nie istnieją.
