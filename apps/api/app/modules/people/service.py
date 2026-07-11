from app.core.errors import NotFoundError
from app.modules.people import repository
from app.modules.people.schemas import PersonCreate, PersonRead, PersonUpdate


async def list_people() -> list[PersonRead]:
    rows = await repository.list_people()
    return [PersonRead(**row) for row in rows]


async def get_person(person_id: str) -> PersonRead:
    row = await repository.get_person(person_id)
    if row is None:
        raise NotFoundError("Person not found.")
    return PersonRead(**row)


async def create_person(payload: PersonCreate) -> PersonRead:
    row = await repository.create_person(payload)
    return PersonRead(**row)


async def update_person(person_id: str, payload: PersonUpdate) -> PersonRead:
    row = await repository.update_person(person_id, payload)
    if row is None:
        raise NotFoundError("Person not found.")
    return PersonRead(**row)


async def delete_person(person_id: str) -> bool:
    deleted = await repository.delete_person(person_id)
    if not deleted:
        raise NotFoundError("Person not found.")
    return deleted
