# MCP Neo4j Guide

## Rola MCP

MCP Neo4j służy agentowi do diagnostyki i weryfikacji danych. Nie jest częścią runtime aplikacji i nie może być importowane przez kod FastAPI.

## Dozwolone użycia

- Odczyt schematu grafu.
- Liczenie węzłów i relacji.
- Podgląd przykładowych danych.
- Analiza planu zapytania.
- Weryfikacja, czy constrainty i indeksy istnieją.

## Bezpieczne zapytania

```cypher
MATCH (n)
RETURN labels(n) AS labels, count(*) AS count
ORDER BY count DESC
```

```cypher
MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC
```

```cypher
MATCH (p:Person)
RETURN p.id AS id, p.name AS name
ORDER BY p.name
LIMIT 25
```

```cypher
MATCH (c:City)
RETURN c.id AS id, c.name AS name, properties(c)['country'] AS country
ORDER BY c.name
LIMIT 25
```

```cypher
MATCH (p:Person)-[r:MIESZKA_W]->(c:City)
RETURN
    p.name AS person_name,
    type(r) AS relationship_type,
    c.name AS city_name
ORDER BY person_name, city_name
LIMIT 25
```

## Niedozwolone bez zgody

- `DETACH DELETE`
- `DELETE`
- `DROP CONSTRAINT`
- `DROP INDEX`
- `REMOVE` na masowych danych
- `SET` bez ograniczonego `MATCH`
- reset bazy danych

## Konfiguracja

Użyj `.mcp.neo4j.example.json` jako przykładu lokalnej konfiguracji. Prawdziwa konfiguracja z hasłami powinna pozostać poza repozytorium albo w pliku ignorowanym przez Git.
