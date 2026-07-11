from app.modules.ml.schemas import ModuleHealth


async def health() -> ModuleHealth:
    return ModuleHealth(module="ml", status="placeholder")
