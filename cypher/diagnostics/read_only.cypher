CALL dbms.components();

SHOW CONSTRAINTS;

SHOW INDEXES;

MATCH (p:Person)
RETURN count(p) AS people_count;

MATCH (:Person)-[r]->(:Person)
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;

MATCH (c:City)
RETURN c.id AS id, c.name AS name, properties(c)['country'] AS country
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
