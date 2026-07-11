# Codex Prompt: Audit Project

Przeprowadź audyt projektu FastAPI + Neo4j.

Kontekst:

- Aplikacja używa FastAPI, Jinja2, Bootstrap 5 i async Neo4j driver.
- Neo4j jest obsługiwany przez czysty, parametryzowany Cypher.
- Aktualny model edukacyjny obejmuje `Person`, `City` oraz relację `MIESZKA_W`.
- MCP Neo4j może być użyte tylko diagnostycznie.
- Nie dodawaj zależności runtime i nie modyfikuj `.env`.

Zadanie:

1. Przeczytaj `AGENTS.md` oraz pliki w `.ai/`.
2. Sprawdź strukturę `app/`.
3. Wypisz problemy według ważności.
4. Wskaż ryzyka bezpieczeństwa, architektury i Cyphera.
5. Nie wykonuj destrukcyjnych zapytań Neo4j.
6. Jeżeli proponujesz poprawki, zachowaj async Neo4j driver i warstwę serwisową.
