from fastapi import APIRouter
from pydantic import BaseModel

from app.db.neo4j import neo4j_manager


class HealthResponse(BaseModel):
    status: str
    neo4j: str


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    await neo4j_manager.verify_connectivity()
    return HealthResponse(status="ok", neo4j="connected")
