from unittest import IsolatedAsyncioTestCase

from app.core.errors import NotFoundError
from app.modules.people import service
from app.modules.people.schemas import PersonCreate, PersonUpdate


class FakePeopleRepository:
    async def list_people(self) -> list[dict]:
        return [
            {
                "id": "person-1",
                "name": "Ada Smith",
                "email": "ada@example.local",
                "note": None,
            }
        ]

    async def get_person(self, person_id: str) -> dict | None:
        if person_id == "person-1":
            return {
                "id": "person-1",
                "name": "Ada Smith",
                "email": "ada@example.local",
                "note": None,
            }
        return None

    async def create_person(self, payload: PersonCreate) -> dict:
        return {
            "id": "person-created",
            "name": payload.name,
            "email": payload.email,
            "note": payload.note,
        }

    async def update_person(
        self,
        person_id: str,
        payload: PersonUpdate,
    ) -> dict | None:
        if person_id != "person-1":
            return None
        return {
            "id": person_id,
            "name": payload.name or "Ada Smith",
            "email": payload.email,
            "note": payload.note,
        }

    async def delete_person(self, person_id: str) -> bool:
        return person_id == "person-1"


class PeopleServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.original_repository = service.repository
        service.repository = FakePeopleRepository()

    async def asyncTearDown(self) -> None:
        service.repository = self.original_repository

    async def test_list_people_maps_repository_rows(self) -> None:
        people = await service.list_people()

        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].id, "person-1")
        self.assertEqual(people[0].name, "Ada Smith")

    async def test_get_person_raises_for_missing_person(self) -> None:
        with self.assertRaises(NotFoundError):
            await service.get_person("missing")

    async def test_create_person_returns_created_person(self) -> None:
        person = await service.create_person(
            PersonCreate(name=" Grace Hopper ", email="", note=" test "),
        )

        self.assertEqual(person.id, "person-created")
        self.assertEqual(person.name, "Grace Hopper")
        self.assertIsNone(person.email)
        self.assertEqual(person.note, "test")

    async def test_delete_person_raises_for_missing_person(self) -> None:
        with self.assertRaises(NotFoundError):
            await service.delete_person("missing")
