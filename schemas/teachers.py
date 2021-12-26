# Python
from typing import Optional
from typing import List

# Pydantic
from pydantic import Field

# Models
from schemas.bases import BaseCourse, BaseTeacher
from schemas.users import SocialNetwork



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
