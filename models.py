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
    question = "question"
    tutorial = "tutorial"
    blog = "blog"
    foro = "foro"

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
        max_length=100
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    image_url: HttpUrl = Field(...)

### Base Class
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

### Base Route
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

### Base Category
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

### Base Teacher
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

### Base User
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
    id_project: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    description: str = Field(
        ...,
        min_length=20,
        max_length=100
    )
    image_url: Optional[HttpUrl] = Field(default=None)

class Resourse(BaseModel):
    description: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    url: HttpUrl = Field(...)

class BaseContribution(BaseModel):
    id_contribution: UUID = Field(...)
    user: BaseUser = Field(...)
    date_publication: date = Field(...)
    likes: int = Field(..., ge=0)

class BaseContributionBasic(BaseContribution):
    content: str = Field(
        ...,
        min_length=1,
    )

class Contribution(BaseContributionBasic):
    kind: TypeContribution = Field(...)

### Comments and Foro
class ContributionAnswer(Contribution):
    answers: Optional[List[BaseContributionBasic]] = Field(default=[])

class BaseContributionTitle(BaseContribution):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100
    )

### Blogs and Tutorials
class ContributionTitle(BaseContributionTitle):
    answers: Optional[List[ContributionAnswer]] = Field(default=[])


## Classes
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
    video_url: HttpUrl = Field(...)
    modules: List[Module] = Field(...)
    description: Optional[str] = Field(default=None)
    resourses: Optional[List[Resourse]] = Field(default=[])
    comments: Optional[List[ContributionAnswer]] = Field(default=[])


## Teachers
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


## Routes
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
    glossary: Optional[List[str]] = Field(...)
    teachers: List[str] = Field(...)
    sections: List[SectionCreate] = Field(...)

class RouteDescription(BaseRouteDescription):
    glossary: Optional[List[Glossary]] = Field(...)
    teachers: List[TeacherBasic] = Field(...)
    sections: List[Section] = Field(...)


## Categories
class BaseCategoryRoute(BaseCategory):
    routes: List[str] = Field(...)

class CategoryRoutes(BaseCategory):
    routes: List[BaseRoute] = Field(...)

