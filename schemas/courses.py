# Python
from typing import Optional
from uuid import UUID
from typing import List

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# Models
from schemas.bases import BaseCourse, BaseRoute, BaseTeacher
from schemas.contributions import BaseContributionTitle, Contribution, Project
from schemas.classes import Module, ModuleBasic
from schemas.teachers import TeacherBasic



class BaseCourseInfo(BaseCourse):
    time_content: int = Field(..., gt=1, le=7)


class CourseInfoBasic(BaseCourse):
    id_teacher: str = Field(...)
    id_routes: Optional[List[str]] = Field(default=[])
    modules: List[ModuleBasic] = Field(...)
    id_project: Optional[str] = Field(default=None)
    id_tutorials: Optional[List[UUID]] = Field(default=[])
    id_comments: Optional[List[UUID]] = Field(default=[])
    description: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    time_practice: int = Field(..., gt=1, le=25)
    previous_knowledge: Optional[List[str]] = Field(default=[])
    software: Optional[List[str]] = Field(default=[])


class CourseInfoClass(BaseCourse):
    teacher: BaseTeacher = Field(...)
    routes: Optional[List[BaseRoute]] = Field(default=[])
    modules: List[Module] = Field(...)
    project: Optional[Project] = Field(default=None)


class CourseInfo(CourseInfoClass):
    tutorials: Optional[List[BaseContributionTitle]] = Field(default=[])
    comments: Optional[List[Contribution]] = Field(default=[])


class CourseInfoComplete(CourseInfoClass):
    description: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    time_practice: int = Field(..., gt=1, le=25)
    previous_knowledge: Optional[List[str]] = Field(default=[])
    software: Optional[List[str]] = Field(default=[])
    teacher: TeacherBasic = Field(...)


class Option(BaseModel):
    option: str = Field(...)
    answer: bool = Field(...)


class Question(BaseModel):
    question: str = Field(...)
    opcions: List[Option] = Field(...)


class CourseExam(BaseCourse):
    exam: List[Question] = Field(...)
    time: int = Field(...)
