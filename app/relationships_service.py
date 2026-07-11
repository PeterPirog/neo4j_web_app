from neo4j import AsyncDriver

from app.db import NEO4J_DATABASE


async def list_lives_in_relationships(driver: AsyncDriver) -> list[dict]:
    query = """
    MATCH (p:Person)-[r:MIESZKA_W]->(c:City)
    RETURN
        p.id AS person_id,
        p.name AS person_name,
        c.id AS city_id,
        c.name AS city_name,
        properties(c)['country'] AS city_country,
        properties(r)['created_at'] AS created_at,
        properties(r)['updated_at'] AS updated_at
    ORDER BY p.name, c.name
    LIMIT 100
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(query)
        return await result.data()


async def assign_person_to_city(
    driver: AsyncDriver,
    person_id: str,
    city_id: str,
) -> bool:
    query = """
    MATCH (p:Person {id: $person_id})
    MATCH (c:City {id: $city_id})
    MERGE (p)-[r:MIESZKA_W]->(c)
    ON CREATE SET r.created_at = datetime()
    SET r.updated_at = datetime()
    RETURN p.id AS person_id, c.id AS city_id
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            person_id=person_id,
            city_id=city_id,
        )
        records = await result.data()
        return bool(records)


async def remove_lives_in_relationship(
    driver: AsyncDriver,
    person_id: str,
    city_id: str,
) -> None:
    query = """
    MATCH (p:Person {id: $person_id})-[r:MIESZKA_W]->(c:City {id: $city_id})
    DELETE r
    """

    async with driver.session(database=NEO4J_DATABASE) as session:
        result = await session.run(
            query,
            person_id=person_id,
            city_id=city_id,
        )
        await result.consume()
