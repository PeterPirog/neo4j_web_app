# Cypher Style Guide

## Parametry

Każda wartość pochodząca od użytkownika musi być parametrem.

```cypher
MATCH (p:Person {id: $id})
RETURN p
```

Nie sklejaj Cyphera przez interpolację stringów.

## Formatowanie

- Używaj wieloliniowych zapytań.
- Pisz słowa kluczowe Cyphera wielkimi literami.
- Nadawaj krótkie, znaczące aliasy: `p` dla `Person`, `u` dla `User`, `r` dla relacji.
- Zawsze dodawaj `LIMIT` do zapytań diagnostycznych zwracających przykładowe dane.
- Preferuj jawne `RETURN` z aliasami zamiast zwracania całych obiektów, gdy dane idą do UI.

## Tworzenie danych

Używaj `randomUUID()` dla publicznych identyfikatorów encji, jeżeli nie ma innego wymagania.

```cypher
CREATE (p:Person {
    id: randomUUID(),
    name: $name,
    created_at: datetime(),
    updated_at: datetime()
})
RETURN p.id AS id
```

## Aktualizacja danych

Zawsze ogranicz aktualizację przez stabilny identyfikator.

```cypher
MATCH (p:Person {id: $id})
SET
    p.name = $name,
    p.updated_at = datetime()
RETURN p.id AS id
```

## Relacje

Relacje zapisuj czasownikowo i wielkimi literami:

```cypher
MATCH (u:User {id: $user_id})
MATCH (r:Resource {id: $resource_id})
MERGE (u)-[:CAN_ACCESS]->(r)
```

Aktualna relacja edukacyjna w projekcie:

```cypher
MATCH (p:Person {id: $person_id})
MATCH (c:City {id: $city_id})
MERGE (p)-[:MIESZKA_W]->(c)
```

## Constrainty

Constrainty trzymaj w `cypher/schema.cypher` i twórz z `IF NOT EXISTS`.
