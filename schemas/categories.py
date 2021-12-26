# Python
from typing import List

# Pydantic
from pydantic import Field

# Models
from bases import BaseCategory, BaseRoute



class BaseCategoryRoute(BaseCategory):
    routes: List[str] = Field(...)


class CategoryRoutes(BaseCategory):
    routes: List[BaseRoute] = Field(...)

