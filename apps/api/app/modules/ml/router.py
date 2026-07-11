from fastapi import APIRouter

from app.modules.ml import service
from app.modules.ml.schemas import ModuleHealth


router = APIRouter(prefix="/api/ml", tags=["ml"])


@router.get("/health", response_model=ModuleHealth)
async def health() -> ModuleHealth:
    return await service.health()
