from fastapi import FastAPI
from pydantic import BaseModel

from app.core.cors import configure_cors
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.db.neo4j import neo4j_lifespan, neo4j_manager
from app.modules.ai.router import router as ai_router
from app.modules.graph_explorer.router import router as graph_explorer_router
from app.modules.ml.router import router as ml_router
from app.modules.people.router import router as people_router
from app.modules.permissions.router import router as permissions_router
from app.modules.relations.router import router as relations_router


class RootResponse(BaseModel):
    service: str
    architecture: str
    api_docs: str


class HealthResponse(BaseModel):
    status: str
    neo4j: str


configure_logging()

app = FastAPI(
    title="Neo4j Web App API",
    version="0.1.0",
    lifespan=neo4j_lifespan,
)

configure_cors(app)
register_exception_handlers(app)

app.include_router(people_router)
app.include_router(relations_router)
app.include_router(permissions_router)
app.include_router(graph_explorer_router)
app.include_router(ai_router)
app.include_router(ml_router)


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        service="Neo4j Web App API",
        architecture="Browser -> Next.js -> FastAPI -> service/query layer -> async Neo4j driver -> Neo4j",
        api_docs="/docs",
    )


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    await neo4j_manager.verify_connectivity()
    return HealthResponse(status="ok", neo4j="connected")


@app.get("/health", response_model=HealthResponse, include_in_schema=False)
async def legacy_health() -> HealthResponse:
    return await health()
