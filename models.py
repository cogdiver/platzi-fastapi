# Python
from typing import Optional
from uuid import UUID
from datetime import date
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

# Enums
class TypeContribution(Enum):
    comment = "comment"
    contribution = "contribution"
    question = "question"

class TypeUser(Enum):
    team = "team"
    teacher = "teacher"
    student = "student"

class Status(Enum):
    public = "public"
    private = "private"

class Levels(Enum):
    basic = "basic"
    intermediate = "intermediate"
    advanced = "advanced"
    complementary = "complementary"

# Models

## Users
class SocialNetwork(BaseModel):
    kind: Social = Field(...)
    url: HttpUrl = Field(...)

class BaseUser(BaseModel):
    id_user: UUID = Field(...)
    name: str = Field(...)
    image_url: HttpUrl = Field(...)
    kind: Optional[TypeUser] = Field(default="student")
    status: Optional[Status] = Field(default="public")

## Teachers
class BaseTeacher(BaseUser):
    id_teacher: str = Field(...)
    image_teacher_url: HttpUrl = Field(...)

class TeacherBasic(BaseTeacher):
    work_position: str = Field(...)
    short_description: str = Field(...)

class TeacherComplete(TeacherBasic):
    long_description: str = Field(...)
    social_network: Optional[list[SocialNetwork]] = Field(default=None)
    courses: BaseCourse

## Courses
class Project(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    image_url: Optional[HttpUrl] = Field(default=None)

class Resourse(BaseModel):
    description: str = Field(...)
    url: HttpUrl = Field(...)

class BaseContribution(BaseModel):
    user: BaseUser = Field(...)
    date: date = Field(...)
    likes: Optional[int] = Field(default=0)
    
class BaseContributionBasic(BaseContribution):
    content: str = Field(...)

class Contribution(BaseContributionBasic):
    id_contribution: UUID = Field(...)
    kind: TypeContribution = Field(...)

class ContributionAnswer(Contribution):
    answers: Optional[list[BaseContributionBasic]] = Field(default=None)

class BaseClass(BaseModel):
    id_class: str = Field(...)
    name: str = Field(...)

class ClassContent(BaseClass):
    course: BaseCourse = Field(...)
    video_url: HttpUrl = Field(...)
    description: Optional[str] = Field(default=None)
    resourses: Optional[list[Resourse]] = Field(default=None)
    contribution: Optional[list[ContributionAnswer]] = Field(default=None)

class Module(BaseModel):
    id_module: UUID = Field(...)
    name: str = Field(...)
    classes: list[BaseClass] = Field(...)

class BaseTutorial(BaseContribution):
    title: str = Field(...)

class Tutorial(BaseTutorial):
    answers: Optional[list[ContributionAnswer]] = Field(default=None)

class BaseCourse(BaseModel):
    id_course: str = Field(...)
    name: str = Field(...)
    image_url: HttpUrl = Field(...)

class CourseInfoBasic(BaseCourse):
    teacher: BaseTeacher = Field(...)
    routes: Optional[list[BaseRoute]] = Field(...)
    modules: list[Module] = Field(...)
    time_content: int = Field(...)
    project: Optional[Project] = Field(default=None)

class CourseInfo(CourseInfoBasic):
    tutorials: Optional[List[BaseTutorial]] = Field(default=None)
    comments: Optional[List[Contribution]] = Field(default=None)

class CourseInfoComplete(CourseInfoBasic):
    description: str = Field(...)
    time_practice: int = Field(...)
    previous_knowledge: Optional[list[str]] = Field(default=None)
    software: Optional[list[str]] = Field(default=None)
    teacher: TeacherBasic = Field(...)

class Option(BaseModel):
    option: str = Field(...)
    answer: bool = Field(...)

class Question(BaseModel):
    question: str = Field(...)
    opcions: list[Option] = Field(...)

class CourseExam(BaseCourse):
    exam: list[Question] = Field(...)
    time: int = Field(...)

## Routes
class Section(BaseModel):
    title: str = Field(...)
    level: Levels = Field(...)
    courses: list[BaseCourse] = Field(...)

class BaseRoute(BaseModel):
    id_route: str = Field(...)
    name: str = Field(...)
    image_url: HttpUrl = Field(...)

class RouteDescription(BaseRoute):
    short_description: str = Field(...)
    long_description: str = Field(...)
    glosario: list[str] = Field(...)
    teachers: list[TeacherBasic] = Field(...)
    sections: list[Section] = Field(...)

class BaseCategory(BaseModel):
    id_category: str = Field(...)
    name: str = Field(...)

class CategoryRoutes(BaseCategory):
    routes: list[BaseRoute] = Field(...)
    teachers: list[TeacherBasic] = Field(...)