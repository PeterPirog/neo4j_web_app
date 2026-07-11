# Definition of Done

Zmiana jest gotowa, gdy spełnia poniższe warunki:

- Zachowuje architekturę FastAPI + async Neo4j driver.
- Nie dodaje Django, SQLAlchemy, neomodel, OGM ani GraphQL.
- Nie dodaje MCP Neo4j jako zależności runtime.
- Używa parametryzowanego Cyphera.
- Nie zapisuje sekretów w repozytorium.
- Nie modyfikuje `.env`.
- Nie wykonuje destrukcyjnych operacji na Neo4j bez zgody.
- Jest spójna z istniejącymi plikami w `app/`.
- Ma podstawową weryfikację: test, uruchomienie aplikacji, sprawdzenie importów albo opis ograniczeń.

Przy zmianach w danych lub schemacie dodatkowo:

- dodano lub zaktualizowano `cypher/schema.cypher`,
- dodano bezpieczne zapytanie diagnostyczne,
- opisano wpływ na istniejące dane.
