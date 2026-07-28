from fastapi import APIRouter

from app.modules.ai import service
from app.modules.ai.schemas import ModuleHealth


router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/health", response_model=ModuleHealth)
async def health() -> ModuleHealth:
    return await service.health()
