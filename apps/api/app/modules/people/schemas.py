from pydantic import BaseModel, Field, field_validator


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class PersonCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: str | None = None
    note: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("name is required")
        return stripped

    @field_validator("email", "note")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        return _blank_to_none(value)


class PersonUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    note: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_optional_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("name cannot be blank")
        return stripped

    @field_validator("email", "note")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        return _blank_to_none(value)


class PersonRead(BaseModel):
    id: str
    name: str
    email: str | None = None
    note: str | None = None


class DeletePersonResponse(BaseModel):
    deleted: bool
