from unittest import IsolatedAsyncioTestCase

from app.core.errors import NotFoundError
from app.modules.relations import service
from app.modules.relations.schemas import RelationshipCreate


class FakeRelationsRepository:
    async def list_relations(self) -> list[dict]:
        return [
            {
                "id": "relationship-1",
                "source_id": "person-1",
                "source_name": "Ada Smith",
                "target_id": "person-2",
                "target_name": "Grace Hopper",
                "relationship_type": "KNOWS",
                "note": None,
                "strength": 3,
            },
            {
                "id": None,
                "source_id": "person-2",
                "source_name": "Grace Hopper",
                "target_id": "person-1",
                "target_name": "Ada Smith",
                "relationship_type": "KNOWS",
                "note": None,
                "strength": None,
            },
        ]

    async def create_relationship(
        self,
        payload: RelationshipCreate,
    ) -> dict | None:
        if payload.source_person_id == "missing":
            return None
        return {
            "id": "relationship-created",
            "source_id": payload.source_person_id,
            "source_name": "Ada Smith",
            "target_id": payload.target_person_id,
            "target_name": "Grace Hopper",
            "relationship_type": payload.relationship_type,
            "note": payload.note,
            "strength": payload.strength,
        }

    async def delete_relationship(self, relationship_id: str) -> bool:
        return relationship_id == "relationship-1"


class RelationsServiceTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.original_repository = service.repository
        service.repository = FakeRelationsRepository()

    async def asyncTearDown(self) -> None:
        service.repository = self.original_repository

    async def test_list_relations_filters_rows_without_ids(self) -> None:
        relationships = await service.list_relations()

        self.assertEqual(len(relationships), 1)
        self.assertEqual(relationships[0].id, "relationship-1")

    async def test_create_relationship_raises_when_people_are_missing(self) -> None:
        payload = RelationshipCreate(
            source_person_id="missing",
            target_person_id="person-2",
            relationship_type="KNOWS",
        )

        with self.assertRaises(NotFoundError):
            await service.create_relationship(payload)

    async def test_delete_relationship_raises_for_missing_relationship(self) -> None:
        with self.assertRaises(NotFoundError):
            await service.delete_relationship("missing")
