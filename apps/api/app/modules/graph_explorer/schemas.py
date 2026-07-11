from pydantic import BaseModel


class ModuleHealth(BaseModel):
    module: str
    status: str
