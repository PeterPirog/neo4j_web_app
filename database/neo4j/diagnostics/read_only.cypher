// Read-only diagnostics safe for MCP or Neo4j Browser.

MATCH (n)
RETURN labels(n) AS labels, count(*) AS count
ORDER BY count DESC;

MATCH ()-[r]->()
RETURN type(r) AS relationship_type, count(*) AS count
ORDER BY count DESC;

MATCH (p:Person)
RETURN p.id AS id, p.name AS name
ORDER BY p.name
LIMIT 25;

MATCH (c:City)
RETURN
    c.id AS id,
    c.name AS name,
    properties(c)['country'] AS country
ORDER BY c.name
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
