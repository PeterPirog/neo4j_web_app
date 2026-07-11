from neo4j import AsyncDriver

from app.db.neo4j import NEO4J_DATABASE, get_neo4j_driver
from app.modules.relations import queries
from app.modules.relations.schemas import RelationshipCreate


async def list_relations(driver: AsyncDriver | None = None) -> list[dict]:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(queries.LIST_RELATIONS)
        return await result.data()


async def create_relationship(
    payload: RelationshipCreate,
    driver: AsyncDriver | None = None,
) -> dict | None:
    driver = driver or get_neo4j_driver()
    query = queries.create_relationship_query(payload.relationship_type)

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            source_person_id=payload.source_person_id,
            target_person_id=payload.target_person_id,
            note=payload.note,
            strength=payload.strength,
        )
        record = await result.single()
        return dict(record) if record else None


async def delete_relationship(
    relationship_id: str,
    driver: AsyncDriver | None = None,
) -> bool:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            queries.DELETE_RELATIONSHIP,
            relationship_id=relationship_id,
        )
        summary = await result.consume()
        return summary.counters.relationships_deleted > 0
