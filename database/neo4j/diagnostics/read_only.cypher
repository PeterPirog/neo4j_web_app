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
