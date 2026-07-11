import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from neo4j import AsyncDriver, AsyncGraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


class Neo4jConnection:
    def __init__(self) -> None:
        self.driver: AsyncDriver | None = None
        self.startup_error: str | None = None

    async def connect(self) -> None:
        self.driver = AsyncGraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
        )

        await self.driver.verify_connectivity()
        self.startup_error = None

    async def close(self) -> None:
        if self.driver is not None:
            await self.driver.close()
            self.driver = None

    def get_driver(self) -> AsyncDriver:
        if self.driver is None:
            raise RuntimeError("Neo4j driver is not initialized.")
        return self.driver


neo4j_connection = Neo4jConnection()


@asynccontextmanager
async def neo4j_lifespan(app: object):
    try:
        await neo4j_connection.connect()
    except Exception as exc:
        neo4j_connection.startup_error = str(exc)
    try:
        yield
    finally:
        await neo4j_connection.close()
