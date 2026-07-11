from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from neo4j import AsyncDriver, AsyncGraphDatabase

from app.core.config import settings


NEO4J_DATABASE = settings.neo4j_database


class Neo4jManager:
    def __init__(self) -> None:
        self._driver: AsyncDriver | None = None

    async def connect(self) -> None:
        if self._driver is not None:
            return

        self._driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_username, settings.neo4j_password),
        )
        await self._driver.verify_connectivity()

    async def close(self) -> None:
        if self._driver is not None:
            await self._driver.close()
            self._driver = None

    async def verify_connectivity(self) -> None:
        driver = self.get_driver()
        await driver.verify_connectivity()

    def get_driver(self) -> AsyncDriver:
        if self._driver is None:
            raise RuntimeError("Neo4j driver is not initialized.")
        return self._driver


neo4j_manager = Neo4jManager()


def get_neo4j_driver() -> AsyncDriver:
    return neo4j_manager.get_driver()


@asynccontextmanager
async def neo4j_lifespan(app: FastAPI) -> AsyncIterator[None]:
    await neo4j_manager.connect()
    from app.modules.people.repository import ensure_person_constraints

    await ensure_person_constraints(neo4j_manager.get_driver())
    try:
        yield
    finally:
        await neo4j_manager.close()
