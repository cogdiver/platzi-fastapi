# Python
from typing import Optional
from uuid import UUID

# Pydantic
from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import Field

# Models
from enums import Status, TypeUser



class BaseCourse(BaseModel):
    id_course: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    image_url: HttpUrl = Field(...)


class BaseClass(BaseModel):
    id_class: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


class BaseRoute(BaseModel):
    id_route: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    image_url: HttpUrl = Field(...)
    courses_number: int = Field(...)


class BaseCategory(BaseModel):
    id_category: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


class BaseTeacher(BaseModel):
    id_teacher: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    image_teacher_url: HttpUrl = Field(...)


class BaseUser(BaseModel):
    id_user: UUID = Field(...)
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    image_url: HttpUrl = Field(...)
    kind: Optional[TypeUser] = Field(default="student")
    status: Optional[Status] = Field(default="public")
    teacher: Optional[BaseTeacher] = Field(default=None)
