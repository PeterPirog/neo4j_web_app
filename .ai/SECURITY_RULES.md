# Security Rules

## Sekrety

- Nie commituj `.env`.
- Nie wpisuj prawdziwych haseł do dokumentacji, promptów ani przykładów.
- Używaj `.env.example` tylko z placeholderami.
- Lokalne konfiguracje MCP z hasłami powinny być ignorowane przez Git.

## Neo4j

- Dane użytkownika zawsze przekazuj jako parametry Cyphera.
- Nie wykonuj destrukcyjnych zapytań bez wyraźnej zgody.
- Nie uruchamiaj resetu bazy.
- Nie usuwaj danych testowo, jeżeli użytkownik o to nie poprosił.

## FastAPI

- Waliduj dane wejściowe na granicy endpointu lub w serwisie.
- Nie ujawniaj surowych sekretów w komunikatach błędów.
- Nie dodawaj debug endpointów zwracających pełne rekordy produkcyjne.

## MCP

MCP Neo4j ma służyć do diagnostyki agentów. Nie wolno dodawać go do `requirements.txt` jako zależności aplikacji runtime.
