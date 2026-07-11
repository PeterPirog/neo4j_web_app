from app.modules.relations.constants import ALLOWED_RELATIONSHIP_TYPES


LIST_RELATIONS = """
MATCH (source:Person)-[r]->(target:Person)
RETURN
    properties(r)['id'] AS id,
    source.id AS source_id,
    source.name AS source_name,
    target.id AS target_id,
    target.name AS target_name,
    type(r) AS relationship_type,
    properties(r)['note'] AS note,
    properties(r)['strength'] AS strength
ORDER BY coalesce(
    properties(r)['updated_at'],
    properties(r)['created_at']
) DESC
LIMIT 200
"""

CREATE_RELATIONSHIP_TEMPLATE = """
MATCH (source:Person {id: $source_person_id})
MATCH (target:Person {id: $target_person_id})
MERGE (source)-[r:RELATIONSHIP_TYPE]->(target)
ON CREATE SET
    r.id = randomUUID(),
    r.created_at = datetime()
SET
    r.id = coalesce(properties(r)['id'], randomUUID()),
    r.note = $note,
    r.strength = $strength,
    r.updated_at = datetime()
RETURN
    properties(r)['id'] AS id,
    source.id AS source_id,
    source.name AS source_name,
    target.id AS target_id,
    target.name AS target_name,
    type(r) AS relationship_type,
    properties(r)['note'] AS note,
    properties(r)['strength'] AS strength
"""

DELETE_RELATIONSHIP = """
MATCH ()-[r]->()
WHERE properties(r)['id'] = $relationship_id
DELETE r
"""


def create_relationship_query(relationship_type: str) -> str:
    if relationship_type not in ALLOWED_RELATIONSHIP_TYPES:
        raise ValueError("Relationship type is not allowed.")
    return CREATE_RELATIONSHIP_TEMPLATE.replace("RELATIONSHIP_TYPE", relationship_type)
