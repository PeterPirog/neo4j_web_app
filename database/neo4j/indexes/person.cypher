CREATE INDEX person_name_index IF NOT EXISTS
FOR (p:Person)
ON (p.name);
