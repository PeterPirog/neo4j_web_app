from neo4j import AsyncDriver

from app.db import NEO4J_DATABASE


async def list_cities(driver: AsyncDriver) -> list[dict]:
    query = """
    MATCH (c:City)
    OPTIONAL MATCH (p:Person)-[:MIESZKA_W]->(c)
    RETURN
        c.id AS id,
        c.name AS name,
        properties(c)['country'] AS country,
        properties(c)['note'] AS note,
        count(p) AS residents_count
    ORDER BY c.name
    LIMIT 100
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query)
        return await result.data()


async def get_city(driver: AsyncDriver, city_id: str) -> dict | None:
    query = """
    MATCH (c:City {id: $id})
    RETURN
        c.id AS id,
        c.name AS name,
        properties(c)['country'] AS country,
        properties(c)['note'] AS note
    LIMIT 1
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query, id=city_id)
        records = await result.data()
        return records[0] if records else None


async def create_city(
    driver: AsyncDriver,
    name: str,
    country: str,
    note: str,
) -> str:
    query = """
    CREATE (c:City {
        id: randomUUID(),
        name: $name,
        country: $country,
        note: $note,
        created_at: datetime(),
        updated_at: datetime()
    })
    RETURN c.id AS id
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            name=name,
            country=country,
            note=note,
        )
        records = await result.data()
        return records[0]["id"]


async def update_city(
    driver: AsyncDriver,
    city_id: str,
    name: str,
    country: str,
    note: str,
) -> bool:
    query = """
    MATCH (c:City {id: $id})
    SET
        c.name = $name,
        c.country = $country,
        c.note = $note,
        c.updated_at = datetime()
    RETURN c.id AS id
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            id=city_id,
            name=name,
            country=country,
            note=note,
        )
        records = await result.data()
        return bool(records)


async def delete_city(driver: AsyncDriver, city_id: str) -> None:
    query = """
    MATCH (c:City {id: $id})
    DETACH DELETE c
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query, id=city_id)
        await result.consume()
