# Agent Rules

## Priorytety

1. Nie psuj istniejącego działania aplikacji.
2. Nie dodawaj zależności runtime bez potrzeby i zgody.
3. Zachowaj FastAPI + async Neo4j driver jako główną architekturę.
4. Parametryzuj każde wejście użytkownika w Cypherze.
5. Traktuj MCP Neo4j jako narzędzie diagnostyczne, nie część aplikacji.

## Zakazane zmiany bez wyraźnej zgody

- Nadpisanie `.env`.
- Dodanie prawdziwych haseł, tokenów lub URI z sekretami.
- Reset bazy danych.
- Masowe usuwanie danych.
- Instalacja pakietów.
- Migracja na ORM, OGM lub GraphQL.
- Zastąpienie async drivera synchronicznym.

## Przed edycją

- Sprawdź istniejące pliki i wzorce.
- Jeżeli plik istnieje, scalaj treść zamiast nadpisywać.
- Jeżeli zmiana dotyczy danych w Neo4j, preferuj zapytania diagnostyczne `MATCH ... RETURN ... LIMIT`.
- Przy niepewności opisz ryzyko zamiast wykonywać destrukcyjne działanie.

## Po edycji

- Uruchom dostępne testy lub podstawową weryfikację.
- Jeżeli testy nie istnieją, opisz, czego nie zweryfikowano.
- Wskaż zmienione pliki i powód zmian.
