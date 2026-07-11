from fastapi import APIRouter

from app.modules.permissions import service
from app.modules.permissions.schemas import ModuleHealth


router = APIRouter(prefix="/api/permissions", tags=["permissions"])


@router.get("/health", response_model=ModuleHealth)
async def health() -> ModuleHealth:
    return await service.health()
