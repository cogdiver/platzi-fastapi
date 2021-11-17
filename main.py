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
    return {"Platzi":"It's Working"}

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
def course():
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

# Comments
@app.get(
    path="/comentario/{id_comment}",
    # response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="get a comment",
    tags=["Comments"]
)
def course():
    pass

# Blog
@app.get(
    path="/blog/{id_bog}",
    # response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="get a blog publication",
    tags=["Blog"]
)
def course():
    pass

# Foro
@app.get(
    path="/comunidad/{id_foro}",
    # response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="get a foro publication",
    tags=["Foro"]
)
def course():
    pass