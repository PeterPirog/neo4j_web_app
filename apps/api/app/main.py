from fastapi import FastAPI
from pydantic import BaseModel

from app.api.health import HealthResponse, health as api_health
from app.api.v1.router import api_v1_router, legacy_api_router
from app.core.cors import configure_cors
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.db.neo4j import neo4j_lifespan


class RootResponse(BaseModel):
    service: str
    architecture: str
    api_docs: str


configure_logging()

app = FastAPI(
    title="Neo4j Web App API",
    version="0.1.0",
    lifespan=neo4j_lifespan,
)

configure_cors(app)
register_exception_handlers(app)

app.include_router(api_v1_router)
app.include_router(legacy_api_router)


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        service="Neo4j Web App API",
        architecture="Browser -> Next.js -> FastAPI -> service/query layer -> async Neo4j driver -> Neo4j",
        api_docs="/docs",
    )


@app.get("/health", response_model=HealthResponse, include_in_schema=False)
async def legacy_health() -> HealthResponse:
    return await api_health()
