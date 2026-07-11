# Architecture

## Warstwy

1. `app/main.py`
   Endpointy HTTP, walidacja wejścia na poziomie formularzy, przekierowania, odpowiedzi JSON i renderowanie szablonów.

2. `app/*_service.py`
   Logika aplikacyjna związana z Neo4j. Tu powinny trafiać zapytania Cypher i operacje na sesjach drivera.

3. `app/db.py`
   Konfiguracja `AsyncGraphDatabase`, lifespan FastAPI, zamykanie drivera.

4. `app/templates/`
   Szablony Jinja2 i markup Bootstrap.

## Zasady zależności

- Endpointy mogą wołać serwisy.
- Serwisy mogą używać async drivera Neo4j.
- Szablony nie zawierają logiki dostępu do danych.
- MCP Neo4j nie jest importowany w kodzie aplikacji.

## Sesje Neo4j

Używaj:

```python
async with driver.session(database=NEO4J_DATABASE) as session:
    result = await session.run(query, parameter=value)
```

Nie używaj synchronicznych sesji ani globalnego klienta innego niż zarządzany async driver.

## Model danych

Aktualny model startowy:

- `(:Person {id, name, email, note, created_at, updated_at})`

Docelowo model może obejmować użytkowników, zasoby, role, relacje dostępu, dokumenty, embeddingi i relacje predykcyjne.
