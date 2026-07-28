from fastapi import APIRouter, status

from app.modules.people import service
from app.modules.people.schemas import (
    DeletePersonResponse,
    PersonCreate,
    PersonRead,
    PersonUpdate,
)


router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[PersonRead])
async def list_people() -> list[PersonRead]:
    return await service.list_people()


@router.post("", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
async def create_person(payload: PersonCreate) -> PersonRead:
    return await service.create_person(payload)


@router.get("/{person_id}", response_model=PersonRead)
async def get_person(person_id: str) -> PersonRead:
    return await service.get_person(person_id)


@router.patch("/{person_id}", response_model=PersonRead)
async def update_person(person_id: str, payload: PersonUpdate) -> PersonRead:
    return await service.update_person(person_id, payload)


@router.delete("/{person_id}", response_model=DeletePersonResponse)
async def delete_person(person_id: str) -> DeletePersonResponse:
    deleted = await service.delete_person(person_id)
    return DeletePersonResponse(deleted=deleted)
