# Python
from enum import Enum

class TypeContribution(Enum):
    comment = "comment"
    question = "question"
    tutorial = "tutorial"
    blog = "blog"
    forum = "forum"
    answers = "answers"

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