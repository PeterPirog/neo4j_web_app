from app.core.errors import NotFoundError
from app.modules.relations import repository
from app.modules.relations.schemas import RelationshipCreate, RelationshipRead


async def list_relations() -> list[RelationshipRead]:
    rows = await repository.list_relations()
    return [RelationshipRead(**row) for row in rows if row.get("id")]


async def create_relationship(payload: RelationshipCreate) -> RelationshipRead:
    row = await repository.create_relationship(payload)
    if row is None:
        raise NotFoundError("Source or target person not found.")
    return RelationshipRead(**row)


async def delete_relationship(relationship_id: str) -> bool:
    deleted = await repository.delete_relationship(relationship_id)
    if not deleted:
        raise NotFoundError("Relationship not found.")
    return deleted
