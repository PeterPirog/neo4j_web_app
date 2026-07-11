from neo4j import AsyncDriver

from app.db.neo4j import NEO4J_DATABASE, get_neo4j_driver
from app.modules.people import queries
from app.modules.people.schemas import PersonCreate, PersonUpdate


async def ensure_person_constraints(driver: AsyncDriver | None = None) -> None:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(queries.ENSURE_PERSON_CONSTRAINT)
        await result.consume()


async def list_people(driver: AsyncDriver | None = None) -> list[dict]:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(queries.LIST_PEOPLE)
        return await result.data()


async def get_person(
    person_id: str,
    driver: AsyncDriver | None = None,
) -> dict | None:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(queries.GET_PERSON, id=person_id)
        record = await result.single()
        return dict(record) if record else None


async def create_person(
    payload: PersonCreate,
    driver: AsyncDriver | None = None,
) -> dict:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            queries.CREATE_PERSON,
            name=payload.name,
            email=payload.email,
            note=payload.note,
        )
        record = await result.single(strict=True)
        return dict(record)


async def update_person(
    person_id: str,
    payload: PersonUpdate,
    driver: AsyncDriver | None = None,
) -> dict | None:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            queries.UPDATE_PERSON,
            id=person_id,
            name=payload.name,
            email=payload.email,
            note=payload.note,
        )
        record = await result.single()
        return dict(record) if record else None


async def delete_person(
    person_id: str,
    driver: AsyncDriver | None = None,
) -> bool:
    driver = driver or get_neo4j_driver()
    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(queries.DELETE_PERSON, id=person_id)
        summary = await result.consume()
        return summary.counters.nodes_deleted > 0
