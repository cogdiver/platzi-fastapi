# Python
from typing import List

# FastAPI
from fastapi import FastAPI
from fastapi import status

# Models
from models import *

app = FastAPI()

# Home
@app.get(path="/")
def home():
    return {"Platzi": "It's Working"}

# Categories
@app.get(
    path="/categorias",
    response_model=List[BaseCategory],
    status_code=status.HTTP_200_OK,
    summary="get all categories",
    tags=["Categories"]
)
def categories():
    pass

@app.get(
    path="/categorias/{id_category}",
    response_model=CategoryRoutes,
    status_code=status.HTTP_200_OK,
    summary="get a category",
    tags=["Categories"]
)
def category():
    pass

# Routes
@app.get(
    path="/rutas",
    response_model=List[BaseRoute],
    status_code=status.HTTP_200_OK,
    summary="get all routes",
    tags=["Routes"]
)
def routes():
    pass

@app.get(
    path="/{id_route}",
    response_model=RouteDescription,
    status_code=status.HTTP_200_OK,
    summary="get a route",
    tags=["Routes"]
)
def route():
    pass

# Courses
@app.get(
    path="/cursos",
    response_model=List[BaseCourse],
    status_code=status.HTTP_200_OK,
    summary="get all courses",
    tags=["Courses"]
)
def courses():
    pass

@app.get(
    path="/clases/{id_course}",
    response_model=CourseInfo,
    status_code=status.HTTP_200_OK,
    summary="get a basic description of a course",
    tags=["Courses"]
)
def class_course():
    pass

@app.get(
    path="/cursos/{id_course}",
    response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a course",
    tags=["Courses"]
)
def course():
    pass

# Classes
@app.get(
    path="/clases/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a class",
    tags=["Class"]
)
def classes():
    pass

# Contributions

## Comments
@app.get(
    path="/comentarios",
    response_model=List[ContributionAnswer],
    status_code=status.HTTP_200_OK,
    summary="get all comments",
    tags=["Contributions", "Comments"]
)
def comments():
    pass

@app.get(
    path="/comentario/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="get a comment",
    tags=["Contributions", "Comments"]
)
def comment():
    pass

## Blog
@app.get(
    path="/blogs",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all blogs",
    tags=["Contributions", "Blog"],
)
def blog():
    pass

@app.get(
    path="/blog/{id_bog}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a blog publication",
    tags=["Contributions", "Blog"],
)
def blog():
    pass

## Foro
@app.get(
    path="/foros",
    response_model=List[ContributionAnswer],
    status_code=status.HTTP_200_OK,
    summary="get all foros",
    tags=["Contributions", "Foro"]
)
def foro():
    pass

@app.get(
    path="/comunidad/{id_foro}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="get a foro publication",
    tags=["Contributions", "Foro"]
)
def foro():
    pass

## Tutorial
@app.get(
    path="/tutorials",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all tutorials",
    tags=["Contributions", "Tutorial"]
)
def tutorials():
    pass

@app.get(
    path="/tutorial/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a tutorial publication",
    tags=["Contributions", "Tutorial"]
)
def tutorial():
    pass

