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

class Social(Enum):
    facebook = "facebook"
    twitter = "twitter"
    instagram = "instagram"


# Models

## Users
class SocialNetwork(BaseModel):
    kind: Social = Field(...)
    url: HttpUrl = Field(...)

class BaseUser(BaseModel):
    id_user: UUID = Field(...)
    name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    image_url: HttpUrl = Field(...)
    kind: Optional[TypeUser] = Field(default="student")
    status: Optional[Status] = Field(default="public")

## Teachers
class BaseTeacher(BaseUser):
    id_teacher: str = Field(
        ...,
        min_length=1,
        max_length=15
    )
    image_teacher_url: HttpUrl = Field(...)

class TeacherBasic(BaseTeacher):
    work_position: str = Field(
        ...,
        min_length=10
    )
    short_description: str = Field(
        ...,
        min_length=15,
        max_length=100
    )

class TeacherComplete(TeacherBasic):
    long_description: str = Field(
        ...,
        min_length=50
    )
    social_network: Optional[list[SocialNetwork]] = Field(default=None)
    courses: list[BaseCourse] = Field(...)

## Courses
class Project(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=200
    )
    image_url: Optional[HttpUrl] = Field(default=None)

class Resourse(BaseModel):
    description: str = Field(
        ...,
        min_length=1,
        max_length=15
    )
    url: HttpUrl = Field(...)

class BaseContribution(BaseModel):
    user: BaseUser = Field(...)
    date: date = Field(...)
    likes: Optional[int] = Field(default=0)
    
class BaseContributionBasic(BaseContribution):
    content: str = Field(
        ...,
        min_length=1,
    )

class Contribution(BaseContributionBasic):
    id_contribution: UUID = Field(...)
    kind: TypeContribution = Field(...)

class ContributionAnswer(Contribution):
    answers: Optional[list[BaseContributionBasic]] = Field(default=None)

class BaseClass(BaseModel):
    id_class: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

class ClassContent(BaseClass):
    course: BaseCourse = Field(...)
    video_url: HttpUrl = Field(...)
    description: Optional[str] = Field(default=None)
    resourses: Optional[list[Resourse]] = Field(default=None)
    contribution: Optional[list[ContributionAnswer]] = Field(default=None)

class Module(BaseModel):
    id_module: UUID = Field(...)
    name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    classes: list[BaseClass] = Field(...)

class BaseTutorial(BaseContribution):
    title: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

class Tutorial(BaseTutorial):
    answers: Optional[list[ContributionAnswer]] = Field(default=None)

class BaseCourse(BaseModel):
    id_course: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    image_url: HttpUrl = Field(...)

class CourseInfoBasic(BaseCourse):
    teacher: BaseTeacher = Field(...)
    routes: Optional[list[BaseRoute]] = Field(...)
    modules: list[Module] = Field(...)
    time_content: int = Field(..., gt=1, le=7)
    project: Optional[Project] = Field(default=None)

class CourseInfo(CourseInfoBasic):
    tutorials: Optional[List[BaseTutorial]] = Field(default=None)
    comments: Optional[List[Contribution]] = Field(default=None)

class CourseInfoComplete(CourseInfoBasic):
    description: str = Field(
        ...,
        min_length=1,
        max_length=200
    )
    time_practice: int = Field(..., gt=1, le=25)
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
    title: str = Field(
        ...,
        min_length=1,
        max_length=15
    )
    level: Levels = Field(...)
    courses: list[BaseCourse] = Field(...)

class BaseRoute(BaseModel):
    id_route: str = Field(
        ...,
        min_length=1,
        max_length=15
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    image_url: HttpUrl = Field(...)

class RouteDescription(BaseRoute):
    short_description: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    long_description: str = Field(
        ...,
        min_length=1
    )
    glosario: list[str] = Field(...)
    teachers: list[TeacherBasic] = Field(...)
    sections: list[Section] = Field(...)

class BaseCategory(BaseModel):
    id_category: str = Field(
        ...,
        min_length=1,
        max_length=10
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=15
    )

class CategoryRoutes(BaseCategory):
    routes: list[BaseRoute] = Field(...)
    teachers: list[TeacherBasic] = Field(...)