# Python
from typing import Optional
from uuid import UUID
from datetime import date
from typing import List

# Pydantic
from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import Field

# Models
from schemas.bases import BaseUser
from schemas.enums import TypeContribution



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
    date_publication: date = Field(...)
    likes: int = Field(..., gt=0)


class BaseContributionUser(BaseContribution):
    user: BaseUser = Field(...)


class BaseContributionBasic(BaseContributionUser):
    content: str = Field(
        ...,
        min_length=1,
    )


class Contribution(BaseContributionBasic):
    kind: TypeContribution = Field(...)


### Comments
class ContributionAnswer(Contribution):
    answers: Optional[List[Contribution]] = Field(default=[])


class BaseContributionTitle(BaseContributionUser):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100
    )


### Blogs, Tutorials and Forums
class ContributionTitle(BaseContributionTitle):
    comments: Optional[List[ContributionAnswer]] = Field(default=[])


### Contributions Basic
class ContributionBasic(BaseContribution):
    id_user: UUID = Field(...)
    kind: TypeContribution = Field(...)
    content: str = Field(
        ...,
        min_length=1,
    )
    id_answers: Optional[List[UUID]] = Field(default=[])


class ContributionTitleBasic(BaseContribution):
    id_user: UUID = Field(...)
    id_comments: Optional[List[UUID]] = Field(default=[])
    kind: TypeContribution = Field(...)
    title: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
