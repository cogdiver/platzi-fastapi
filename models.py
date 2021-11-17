# Python
from typing import Optional
from typing import List
from uuid import UUID
from datetime import date
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from pydantic import EmailStr

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

## Bases
### Base Course
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

### Base Class
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

### Base Route
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
    courses_number: int = Field(...)

### Base Category
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

### Base User
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

## Users
class SocialNetwork(BaseModel):
    kind: Social = Field(...)
    url: HttpUrl = Field(...)

class UserLogin(BaseUser):
    email: EmailStr = Field(...)
    password: str = Field(
        ...,
        min_length=8,
    )


## Contributions
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
    date_publication: date = Field(...)
    likes: int = Field(..., ge=0)
    
class BaseContributionBasic(BaseContribution):
    content: str = Field(
        ...,
        min_length=1,
    )

class Contribution(BaseContributionBasic):
    id_contribution: UUID = Field(...)
    kind: TypeContribution = Field(...)

class ContributionAnswer(Contribution):
    answers: Optional[List[BaseContributionBasic]] = Field(default=[])


## Classes
class Module(BaseModel):
    id_module: UUID = Field(...)
    name: str = Field(
        ...,
        min_length=1,
        max_length=20
    )
    classes: List[BaseClass] = Field(...)

class ClassContent(BaseClass):
    course: BaseCourse = Field(...)
    video_url: HttpUrl = Field(...)
    modules: List[Module] = Field(...)
    description: Optional[str] = Field(default=None)
    resourses: Optional[List[Resourse]] = Field(default=[])
    contribution: Optional[List[ContributionAnswer]] = Field(default=[])

class BaseTutorial(BaseContribution):
    title: str = Field(
        ...,
        min_length=1,
        max_length=30
    )

class Tutorial(BaseTutorial):
    answers: Optional[List[ContributionAnswer]] = Field(default=[])


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
    social_network: Optional[List[SocialNetwork]] = Field(default=[])
    courses: List[BaseCourse] = Field(...)


## Courses
class CourseInfoBasic(BaseCourse):
    teacher: BaseTeacher = Field(...)
    routes: Optional[List[BaseRoute]] = Field(default=[])
    modules: List[Module] = Field(...)
    time_content: int = Field(..., gt=1, le=7)
    project: Optional[Project] = Field(default=None)

class CourseInfo(CourseInfoBasic):
    tutorials: Optional[List[BaseTutorial]] = Field(default=[])
    comments: Optional[List[Contribution]] = Field(default=[])

class CourseInfoComplete(CourseInfoBasic):
    description: str = Field(
        ...,
        min_length=1,
        max_length=200
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


## Routes
class Section(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=15
    )
    level: Levels = Field(...)
    courses: List[BaseCourse] = Field(...)

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
    glosario: List[str] = Field(...)
    teachers: List[TeacherBasic] = Field(...)
    sections: List[Section] = Field(...)


## Categories
class CategoryRoutes(BaseCategory):
    routes: List[BaseRoute] = Field(...)


## Comments

## Blog

## Foro