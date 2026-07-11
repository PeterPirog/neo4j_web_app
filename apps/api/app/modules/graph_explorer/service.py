from app.modules.graph_explorer.schemas import ModuleHealth


async def health() -> ModuleHealth:
    return ModuleHealth(module="graph_explorer", status="placeholder")
