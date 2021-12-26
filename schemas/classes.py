# Python
from typing import Optional
from uuid import UUID
from typing import List

# Pydantic
from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import Field

# Models
from bases import BaseClass, BaseCourse
from contributions import ContributionAnswer, Resourse



class BaseModule(BaseModel):
    id_module: str = Field(...) # UUID
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


class ModuleBasic(BaseModule):
    id_classes: List[str] = Field(...)


class Module(BaseModule):
    classes: List[BaseClass] = Field(...)


class ClassContentBasic(BaseClass):
    video_url: HttpUrl = Field(...)
    description: Optional[str] = Field(default=None)
    resourses: Optional[List[Resourse]] = Field(default=[])
    id_comments: Optional[List[UUID]] = Field(default=[])


class ClassContent(BaseClass):
    course: BaseCourse = Field(...)
    modules: List[Module] = Field(...)
    video_url: HttpUrl = Field(...)
    description: Optional[str] = Field(default=None)
    resourses: Optional[List[Resourse]] = Field(default=[])
    comments: Optional[List[ContributionAnswer]] = Field(default=[])
