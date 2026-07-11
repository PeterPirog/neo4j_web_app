from app.modules.ai.schemas import ModuleHealth


async def health() -> ModuleHealth:
    return ModuleHealth(module="ai", status="placeholder")
