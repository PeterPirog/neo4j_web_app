// Initial schema for the FastAPI + Neo4j application.
// This migration is idempotent and does not delete data.

CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT city_id_unique IF NOT EXISTS
FOR (c:City)
REQUIRE c.id IS UNIQUE;

CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person)
ON (p.name);

CREATE INDEX city_name_index IF NOT EXISTS
FOR (c:City)
ON (c.name);
