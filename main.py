# Python
from typing import List

# FastAPI
from fastapi import FastAPI
from fastapi import status

app = FastAPI()

# Models
from models import *

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
def all_categories():
    pass

@app.get(
    path="/categorias/{id_category}",
    response_model=CategoryRoutes,
    status_code=status.HTTP_200_OK,
    summary="get a category",
    tags=["Categories"]
)
def get_category():
    pass

@app.post(
    path="/categorias/{id_category}",
    response_model=CategoryRoutes,
    status_code=status.HTTP_201_CREATED,
    summary="create a category",
    tags=["Categories"]
)
def post_category():
    pass

@app.put(
    path="/categorias/{id_category}",
    response_model=CategoryRoutes,
    status_code=status.HTTP_200_OK,
    summary="update a category",
    tags=["Categories"]
)
def put_category():
    pass

@app.delete(
    path="/categorias/{id_category}",
    response_model=CategoryRoutes,
    status_code=status.HTTP_200_OK,
    summary="delete a category",
    tags=["Categories"]
)
def delete_category():
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
def get_route():
    pass

@app.post(
    path="/{id_route}",
    response_model=RouteDescription,
    status_code=status.HTTP_201_CREATED,
    summary="create a route",
    tags=["Routes"]
)
def post_route():
    pass

@app.put(
    path="/{id_route}",
    response_model=RouteDescription,
    status_code=status.HTTP_200_OK,
    summary="update a route",
    tags=["Routes"]
)
def put_route():
    pass

@app.delete(
    path="/{id_route}",
    response_model=RouteDescription,
    status_code=status.HTTP_200_OK,
    summary="delete a route",
    tags=["Routes"]
)
def delete_route():
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
def get_course():
    pass

@app.post(
    path="/cursos/{id_course}",
    response_model=CourseInfoComplete,
    status_code=status.HTTP_201_CREATED,
    summary="create a course",
    tags=["Courses"]
)
def post_course():
    pass

@app.put(
    path="/cursos/{id_course}",
    response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="update a course",
    tags=["Courses"]
)
def put_course():
    pass

@app.delete(
    path="/cursos/{id_course}",
    response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="delete a course",
    tags=["Courses"]
)
def delete_course():
    pass

# Classes
@app.get(
    path="/clases",
    response_model=List[BaseClass],
    status_code=status.HTTP_200_OK,
    summary="get all class with a basic information",
    tags=["Class"]
)
def all_classes():
    pass

@app.get(
    path="/clases/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a class",
    tags=["Class"]
)
def get_classes():
    pass

@app.post(
    path="/clases/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_201_CREATED,
    summary="create a class for a course",
    tags=["Class"]
)
def post_classes():
    pass

@app.put(
    path="/clases/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_200_OK,
    summary="update a class",
    tags=["Class"]
)
def put_classes():
    pass

@app.delete(
    path="/clases/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_200_OK,
    summary="delete a class from a course",
    tags=["Class"]
)
def delete_classes():
    pass

# Contributions

## Comments
@app.get(
    path="/comentarios",
    response_model=List[ContributionAnswer],
    status_code=status.HTTP_200_OK,
    summary="get all comments",
    tags=["Comments"]
)
def all_comments():
    pass

@app.get(
    path="/comentario/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="get a comment",
    tags=["Comments"]
)
def get_comment():
    pass

@app.post(
    path="/comentario/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_201_CREATED,
    summary="create a comment",
    tags=["Comments"]
)
def post_comment():
    pass

@app.put(
    path="/comentario/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="update a comment",
    tags=["Comments"]
)
def put_comment():
    pass

@app.delete(
    path="/comentario/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="delete a comment",
    tags=["Comments"]
)
def delete_comment():
    pass

## Blog
@app.get(
    path="/blogs",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all blogs",
    tags=["Blog"],
)
def all_blogs():
    pass

@app.get(
    path="/blog/{id_bog}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a blog publication",
    tags=["Blog"],
)
def get_blog():
    pass

@app.post(
    path="/blog/{id_bog}",
    response_model=ContributionTitle,
    status_code=status.HTTP_201_CREATED,
    summary="create a blog publication",
    tags=["Blog"],
)
def post_blog():
    pass

@app.put(
    path="/blog/{id_bog}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="update a blog publication",
    tags=["Blog"],
)
def put_blog():
    pass

@app.delete(
    path="/blog/{id_bog}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="delete a blog publication",
    tags=["Blog"],
)
def delete_blog():
    pass

## Foro
@app.get(
    path="/foros",
    response_model=List[ContributionAnswer],
    status_code=status.HTTP_200_OK,
    summary="get all foros",
    tags=["Foro"]
)
def all_foros():
    pass

@app.get(
    path="/comunidad/{id_foro}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="get a foro publication",
    tags=["Foro"]
)
def get_foro():
    pass

@app.post(
    path="/comunidad/{id_foro}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_201_CREATED,
    summary="create a foro publication",
    tags=["Foro"]
)
def post_foro():
    pass

@app.put(
    path="/comunidad/{id_foro}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="update a foro publication",
    tags=["Foro"]
)
def put_foro():
    pass

@app.delete(
    path="/comunidad/{id_foro}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="delete a foro publication",
    tags=["Foro"]
)
def delete_foro():
    pass

## Tutorial
@app.get(
    path="/tutorials",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all tutorials",
    tags=["Tutorial"]
)
def all_tutorials():
    pass

@app.get(
    path="/tutorial/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a tutorial publication",
    tags=["Tutorial"]
)
def get_tutorial():
    pass

@app.post(
    path="/tutorial/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_201_CREATED,
    summary="create a tutorial publication",
    tags=["Tutorial"]
)
def post_tutorial():
    pass

@app.put(
    path="/tutorial/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="update a tutorial publication",
    tags=["Tutorial"]
)
def put_tutorial():
    pass

@app.delete(
    path="/tutorial/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="delete a tutorial publication",
    tags=["Tutorial"]
)
def delete_tutorial():
    pass

