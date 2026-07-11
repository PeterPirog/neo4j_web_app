// Read-only diagnostic queries for agents and maintainers.
// Run one statement at a time.

MATCH (n)
RETURN labels(n) AS labels, count(*) AS count
ORDER BY count DESC;

MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC;

MATCH (p:Person)
RETURN
    p.id AS id,
    p.name AS name,
    properties(p)['email'] AS email,
    properties(p)['note'] AS note,
    properties(p)['created_at'] AS created_at,
    properties(p)['updated_at'] AS updated_at
ORDER BY coalesce(properties(p)['updated_at'], properties(p)['created_at']) DESC
LIMIT 25;

MATCH (c:City)
RETURN
    c.id AS id,
    c.name AS name,
    properties(c)['country'] AS country,
    properties(c)['note'] AS note,
    properties(c)['created_at'] AS created_at,
    properties(c)['updated_at'] AS updated_at
ORDER BY coalesce(properties(c)['updated_at'], properties(c)['created_at']) DESC
LIMIT 25;

MATCH (p:Person)-[r:MIESZKA_W]->(c:City)
RETURN
    p.id AS person_id,
    p.name AS person_name,
    type(r) AS relationship_type,
    c.id AS city_id,
    c.name AS city_name,
    properties(c)['country'] AS city_country
ORDER BY p.name, c.name
LIMIT 50;

SHOW CONSTRAINTS;

SHOW INDEXES;
