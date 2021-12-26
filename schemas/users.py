# Python
from typing import Optional
from uuid import UUID
from datetime import date
from typing import List

# Pydantic
from pydantic import BaseModel
from pydantic import HttpUrl
from pydantic import EmailStr
from pydantic import Field

# Models
from enums import Social
from bases import BaseUser



class SocialNetwork(BaseModel):
    kind: Social = Field(...)
    url: HttpUrl = Field(...)


class UserLogin(BaseUser):
    email: EmailStr = Field(...)
    password: str = Field(
        ...,
        min_length=8,
    )
