"""Drug template."""
from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel as BaseModel
from pydantic import Field

metamodel_version = "None"
version = "None"


class WeakRefShimBaseModel(BaseModel):
    __slots__ = "__weakref__"


class ConfiguredBaseModel(
    WeakRefShimBaseModel,
    validate_assignment=True,
    validate_all=True,
    underscore_attrs_are_private=True,
    extra="forbid",
    arbitrary_types_allowed=True,
):
    pass


class ClinicalNote(ConfiguredBaseModel):
    age: Optional[int] = Field(None, description="""age of the patient""")
    gender: Optional[str] = Field(None, description="""gender of the patient""")
    conditions: Optional[List[str]] = Field(default_factory=list)
    observations: Optional[List[str]] = Field(default_factory=list)
    medications: Optional[List[str]] = Field(default_factory=list)
    procedures: Optional[List[str]] = Field(default_factory=list)


class ExtractionResult(ConfiguredBaseModel):
    """A result of extracting knowledge on text."""

    input_id: Optional[str] = Field(None)
    input_title: Optional[str] = Field(None)
    input_text: Optional[str] = Field(None)
    raw_completion_output: Optional[str] = Field(None)
    prompt: Optional[str] = Field(None)
    extracted_object: Optional[Any] = Field(
        None, description="""The complex objects extracted from the text"""
    )
    named_entities: Optional[List[Any]] = Field(
        default_factory=list, description="""Named entities extracted from the text"""
    )


class NamedEntity(ConfiguredBaseModel):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")


class Procedure(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")

class Medication(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")

class Observation(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")

class Condition(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")

class Gender(NamedEntity):
    id: Optional[str] = Field(None, description="""A unique identifier for the named entity""")
    label: Optional[str] = Field(None, description="""The label (name) of the named thing""")



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
ClinicalNote.update_forward_refs()
ExtractionResult.update_forward_refs()
NamedEntity.update_forward_refs()
Procedure.update_forward_refs()
Medication.update_forward_refs()
Observation.update_forward_refs()
Condition.update_forward_refs()
Gender.update_forward_refs()