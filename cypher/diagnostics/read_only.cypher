CALL dbms.components();

SHOW CONSTRAINTS;

SHOW INDEXES;

MATCH (p:Person)
RETURN count(p) AS people_count;

MATCH (:Person)-[r]->(:Person)
RETURN type(r) AS relationship_type, count(r) AS count
ORDER BY count DESC;
