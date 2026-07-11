ENSURE_PERSON_CONSTRAINT = """
CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE
"""

CREATE_PERSON = """
CREATE (p:Person {
    id: randomUUID(),
    name: $name,
    email: $email,
    note: $note,
    created_at: datetime(),
    updated_at: datetime()
})
RETURN
    p.id AS id,
    p.name AS name,
    properties(p)['email'] AS email,
    properties(p)['note'] AS note
"""

LIST_PEOPLE = """
MATCH (p:Person)
RETURN
    p.id AS id,
    p.name AS name,
    properties(p)['email'] AS email,
    properties(p)['note'] AS note
ORDER BY coalesce(
    properties(p)['updated_at'],
    properties(p)['created_at']
) DESC
LIMIT 200
"""

GET_PERSON = """
MATCH (p:Person {id: $id})
RETURN
    p.id AS id,
    p.name AS name,
    properties(p)['email'] AS email,
    properties(p)['note'] AS note
LIMIT 1
"""

UPDATE_PERSON = """
MATCH (p:Person {id: $id})
SET
    p.name = coalesce($name, p.name),
    p.email = coalesce($email, properties(p)['email']),
    p.note = coalesce($note, properties(p)['note']),
    p.updated_at = datetime()
RETURN
    p.id AS id,
    p.name AS name,
    properties(p)['email'] AS email,
    properties(p)['note'] AS note
"""

DELETE_PERSON = """
MATCH (p:Person {id: $id})
DETACH DELETE p
"""
