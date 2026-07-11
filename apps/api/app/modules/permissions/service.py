from app.modules.permissions.schemas import ModuleHealth


async def health() -> ModuleHealth:
    return ModuleHealth(module="permissions", status="placeholder")
