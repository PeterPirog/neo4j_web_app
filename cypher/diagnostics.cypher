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

SHOW CONSTRAINTS;

SHOW INDEXES;
