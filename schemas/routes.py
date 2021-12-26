# Python
from typing import Optional
from uuid import UUID
from typing import List

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Models
from schemas.bases import BaseCourse, BaseRoute
from schemas.teachers import TeacherBasic
from schemas.enums import Levels



class BaseSection(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    level: Levels = Field(...)


class SectionCreate(BaseSection):
    courses: List[str] = Field(...)


class Section(BaseSection):
    courses: List[BaseCourse] = Field(...)


class Glossary(BaseModel):
    id_glossary: UUID = Field(...)
    title: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


class BaseRouteDescription(BaseRoute):
    short_description: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    long_description: str = Field(
        ...,
        min_length=1
    )


class RouteDescriptionCreate(BaseRouteDescription):
    glossary: Optional[List[str]] = Field(default=[])
    teachers: List[str] = Field(...)
    sections: List[SectionCreate] = Field(...)


class RouteDescription(BaseRouteDescription):
    glossary: Optional[List[Glossary]] = Field(default=[])
    teachers: List[TeacherBasic] = Field(...)
    sections: List[Section] = Field(...)