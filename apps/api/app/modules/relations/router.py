from fastapi import APIRouter, status

from app.modules.relations import service
from app.modules.relations.schemas import (
    DeleteRelationshipResponse,
    RelationshipCreate,
    RelationshipRead,
)


router = APIRouter(prefix="/relations", tags=["relations"])


@router.get("", response_model=list[RelationshipRead])
async def list_relations() -> list[RelationshipRead]:
    return await service.list_relations()


@router.post(
    "",
    response_model=RelationshipRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_relationship(payload: RelationshipCreate) -> RelationshipRead:
    return await service.create_relationship(payload)


@router.delete("/{relationship_id}", response_model=DeleteRelationshipResponse)
async def delete_relationship(
    relationship_id: str,
) -> DeleteRelationshipResponse:
    deleted = await service.delete_relationship(relationship_id)
    return DeleteRelationshipResponse(deleted=deleted)
