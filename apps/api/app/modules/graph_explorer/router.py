from fastapi import APIRouter

from app.modules.graph_explorer import service
from app.modules.graph_explorer.schemas import ModuleHealth


router = APIRouter(prefix="/graph", tags=["graph_explorer"])


@router.get("/health", response_model=ModuleHealth)
async def health() -> ModuleHealth:
    return await service.health()
