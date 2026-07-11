from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.modules.relations.constants import ALLOWED_RELATIONSHIP_TYPES


RelationshipType = Literal[
    "KNOWS",
    "WORKS_WITH",
    "MANAGES",
    "REPORTS_TO",
    "RELATED_TO",
]


def _blank_to_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


class RelationshipCreate(BaseModel):
    source_person_id: str = Field(..., min_length=1)
    target_person_id: str = Field(..., min_length=1)
    relationship_type: RelationshipType
    note: str | None = None
    strength: int | None = Field(default=None, ge=1, le=10)

    @field_validator("source_person_id", "target_person_id")
    @classmethod
    def normalize_required_id(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("id is required")
        return stripped

    @field_validator("note")
    @classmethod
    def normalize_note(cls, value: str | None) -> str | None:
        return _blank_to_none(value)

    @field_validator("relationship_type")
    @classmethod
    def validate_relationship_type(cls, value: str) -> str:
        if value not in ALLOWED_RELATIONSHIP_TYPES:
            raise ValueError("relationship_type is not allowed")
        return value

    @model_validator(mode="after")
    def validate_distinct_people(self) -> "RelationshipCreate":
        if self.source_person_id == self.target_person_id:
            raise ValueError("source_person_id and target_person_id must be different")
        return self


class RelationshipRead(BaseModel):
    id: str
    source_id: str
    source_name: str
    target_id: str
    target_name: str
    relationship_type: str
    note: str | None = None
    strength: int | None = None


class DeleteRelationshipResponse(BaseModel):
    deleted: bool
