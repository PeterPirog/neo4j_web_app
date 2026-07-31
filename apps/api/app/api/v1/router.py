from fastapi import APIRouter

from app.api.health import router as health_router
from app.modules.ai.router import router as ai_router
from app.modules.cities.router import router as cities_router
from app.modules.graph_explorer.router import router as graph_explorer_router
from app.modules.ml.router import router as ml_router
from app.modules.people.router import router as people_router
from app.modules.permissions.router import router as permissions_router
from app.modules.relations.router import router as relations_router
from app.modules.residences.router import router as residences_router


api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(people_router)
api_v1_router.include_router(cities_router)
api_v1_router.include_router(relations_router)
api_v1_router.include_router(residences_router)
api_v1_router.include_router(permissions_router)
api_v1_router.include_router(graph_explorer_router)
api_v1_router.include_router(ai_router)
api_v1_router.include_router(ml_router)


legacy_api_router = APIRouter(prefix="/api", include_in_schema=False)

legacy_api_router.include_router(health_router)
legacy_api_router.include_router(people_router)
legacy_api_router.include_router(cities_router)
legacy_api_router.include_router(relations_router)
legacy_api_router.include_router(residences_router)
legacy_api_router.include_router(permissions_router)
legacy_api_router.include_router(graph_explorer_router)
legacy_api_router.include_router(ai_router)
legacy_api_router.include_router(ml_router)
