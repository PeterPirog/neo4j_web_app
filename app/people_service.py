from neo4j import AsyncDriver

from app.db import NEO4J_DATABASE


async def ensure_constraints(driver: AsyncDriver) -> None:
    query = """
    CREATE CONSTRAINT person_id_unique IF NOT EXISTS
    FOR (p:Person)
    REQUIRE p.id IS UNIQUE
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query)
        await result.consume()


async def list_people(driver: AsyncDriver) -> list[dict]:
    query = """
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
    LIMIT 100
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query)
        return await result.data()


async def get_person(driver: AsyncDriver, person_id: str) -> dict | None:
    query = """
    MATCH (p:Person {id: $id})
    RETURN
        p.id AS id,
        p.name AS name,
        properties(p)['email'] AS email,
        properties(p)['note'] AS note
    LIMIT 1
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query, id=person_id)
        records = await result.data()
        return records[0] if records else None


async def create_person(
    driver: AsyncDriver,
    name: str,
    email: str,
    note: str,
) -> str:
    query = """
    CREATE (p:Person {
        id: randomUUID(),
        name: $name,
        email: $email,
        note: $note,
        created_at: datetime(),
        updated_at: datetime()
    })
    RETURN p.id AS id
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            name=name,
            email=email,
            note=note,
        )
        records = await result.data()
        return records[0]["id"]


async def update_person(
    driver: AsyncDriver,
    person_id: str,
    name: str,
    email: str,
    note: str,
) -> bool:
    query = """
    MATCH (p:Person {id: $id})
    SET
        p.name = $name,
        p.email = $email,
        p.note = $note,
        p.updated_at = datetime()
    RETURN p.id AS id
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            id=person_id,
            name=name,
            email=email,
            note=note,
        )
        records = await result.data()
        return bool(records)


async def delete_person(driver: AsyncDriver, person_id: str) -> None:
    query = """
    MATCH (p:Person {id: $id})
    DETACH DELETE p
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query, id=person_id)
        await result.consume()
