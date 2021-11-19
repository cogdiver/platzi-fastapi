# Python
from typing import List
import json
import functools

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import HTTPException

app = FastAPI()

# Models
from models import *

# Home
@app.get(path="/")
def home():
    return {"Platzi": "It's Working"}

# Categories
@app.get(
    path="/categoria",
    response_model=List[BaseCategory],
    status_code=status.HTTP_200_OK,
    summary="get all categories",
    tags=["Categories"]
)
def all_categories():
    """
    This path operation returns all categories

    Parameters:

    Returns a list of categories with following attributes:
        - id_category: str
        - name: str

    """
    with open('./data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())
    
    categories = [{"id_category":c["id_category"],"name":c["name"]} for c in categories]
    return categories

@app.get(
    path="/categoria/{id_category}",
    response_model=CategoryRoutes,
    status_code=status.HTTP_200_OK,
    summary="get a category",
    tags=["Categories"]
)
def get_category(id_category):
    """
    This path operation the routes for a category

    Parameters:
        - id_category: str
    
    Returns a category with its routes' list with the following attributes:
        - id_route: str
        - name: str
        - image_url: HttpUrl
        - courses_number: str
    """

    with open('./data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())
    
    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    categories = list(filter(lambda c: c['id_category']==id_category, categories))[0]
    routes = list(filter(lambda r: r['id_route'] in categories['routes'], routes))

    categories['routes'] = list(map(lambda r: {
        "id_route": r["id_route"], 
        "name": r["name"], 
        "image_url": r["image_url"], 
        "courses_number": r["courses_number"]
    }, routes))

    return categories

@app.post(
    path="/categoria",
    response_model=BaseCategoryRoute,
    status_code=status.HTTP_201_CREATED,
    summary="create a category",
    tags=["Categories"]
)
def post_category(category: BaseCategoryRoute = Body(...)):
    """
    This path operation create a new category

    Parameters:
        - Category: BaseCategoryRoute
    
    Return a json with the new category
    """
    category = category.dict()

    with open('./data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())

    # id_category must be unique
    id_categories = list(map(lambda c: c['id_category'], categories))
    if category['id_category'] in id_categories:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id category '{r}'"
        )

    # name must be unique
    name_categories = list(map(lambda c: c['name'], categories))
    if category['name'] in name_categories:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name category '{r}'"
        )

    # the id_courses must be valid
    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    id_routes = list(map(lambda r: r['id_route'], routes))
    for r in category['routes']:
        if r not in id_routes:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id route '{r}'"
            )
    
    # Save the category
    categories.append(category)
    with open('./data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

    return category

@app.put(
    path="/categoria/{id_category}",
    response_model=BaseCategoryRoute,
    status_code=status.HTTP_200_OK,
    summary="update a category",
    tags=["Categories"]
)
def put_category(id_category, category: BaseCategoryRoute = Body(...)):
    """
    This path operation update a category

    Parameters:
        - id_category: str
        - Category: BaseCategoryRoute
    
    Return a json with the updated category
    """
    category = category.dict()

    # Considering remove this restriction
    if id_category != category['id_category']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid ids category '{id_category}' and '{category['id_category']}'"
        )

    with open('./data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())

    # id_category must be valid
    id_categories = list(map(lambda c: c['id_category'], categories))
    del categories
    if id_category not in id_categories:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id category '{id_category}'"
        )
    del id_categories
    
    with open('./data/routes.json', 'r', encoding='utf-8') as f2:
        routes = json.loads(f2.read())
    
    # id_routes must be valid
    id_routes = list(map(lambda r: r['id_route'], routes))
    del routes
    for r in category['routes']:
        if r not in id_routes:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id route: '{r}'"
            )
    del id_routes

    categories = list(filter(lambda c: c['id_category']!=id_category, categories))
    categories.append(category)
        
    with open('./data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

    return category

@app.delete(
    path="/categoria/{id_category}",
    response_model=BaseCategoryRoute,
    status_code=status.HTTP_200_OK,
    summary="delete a category",
    tags=["Categories"]
)
def delete_category(id_category):
    """
    This path operation delete a category

    Parameters:
        - id_category: str
    
    Return a json with the delete category
    """
    with open('./data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())

    id_categories = list(map(lambda c: c['id_category'], categories))
    
    if id_category not in id_categories:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id category '{id_category}'"
        )

    category = list(filter(lambda c: c['id_category'] == id_category, categories))[0]
    categories = list(filter(lambda c: c['id_category'] != id_category, categories))
        
    with open('./data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

    return category

# Routes
@app.get(
    path="/rutas",
    response_model=List[BaseRoute],
    status_code=status.HTTP_200_OK,
    summary="get all routes",
    tags=["Routes"]
)
def routes():
    """
    This path operation returns all routes

    Parameters:

    Returns a list of routes with following attributes:
        - id_route: str
        - name: str
        - image_url: HttpUrl
        - courses_number: int
    """
    with open('./data/routes.json', 'r') as f:
        routes = json.loads(f.read())
    
    routes = list(map(lambda r: {
        "id_route": r["id_route"],
        "name": r["name"],
        "image_url": r["image_url"],
        "courses_number": r["courses_number"]
    }, routes))

    return routes

@app.get(
    path="/{id_route}",
    response_model=RouteDescription,
    status_code=status.HTTP_200_OK,
    summary="get a route",
    tags=["Routes"]
)
def get_route(id_route):
    """
    This path operation the description for a route

    Parameters:
        - id_route: str
    
    Returns a route with with the following attributes:
        - id_route: str
        - name: str
        - image_url: HttpUrl
        - courses_number: int
        - short_description: str
        - long_description: str
        - glosario: List[Glossary]
        - teachers: List[TeacherBasic]
        - sections: List[Section]
    """
    with open('./data/routes.json', 'r') as f:
        routes = json.loads(f.read())
    
    id_routes = list(map(lambda r: r['id_route'], routes))

    if id_route not in id_routes:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id route '{id_route}'"
        )
    
    route = list(filter(lambda r: r['id_route'] == id_route, routes))[0]
    del routes

    # get the glossary
    with open('./data/glossary.json', 'r') as f:
        glossary = json.loads(f.read())
    
    glossary = list(filter(lambda g: g['id_glossary'] in route["glossary"], glossary))
    route["glossary"] = glossary
    del glossary

    # get the courses
    with open('./data/courses.json', 'r') as f:
        all_courses = json.loads(f.read())
    
    id_courses = list(map(lambda s: s['courses'], route['sections']))
    
    for i in range(len(id_courses)):
        courses = list(filter(lambda c: c['id_course'] in id_courses[i], all_courses))
        courses = list(map(lambda c: {
            "id_course": c["id_course"],
            "name": c["name"],
            "image_url": c["image_url"]
        }, courses))
        route['sections'][i]["courses"] = courses
    
    del all_courses

    # get the teachers
    with open('./data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())
    
    teachers = list(filter(lambda t: t['id_teacher'] in route["teachers"], teachers))
    teachers = list(map(lambda t: {
        "id_teacher": t["id_teacher"],
        "name": t["name"],
        "image_teacher_url": t["image_teacher_url"],
        "work_position": t["work_position"],
        "short_description": t["short_description"]
    }, teachers))
    route["teachers"] = teachers

    return route

@app.post(
    path="/",
    response_model=BaseRoute,
    status_code=status.HTTP_201_CREATED,
    summary="create a route",
    tags=["Routes"]
)
def post_route(route: RouteDescriptionCreate = Body(...)):
    """
    This path operation create a new route

    Parameters:
        - Route: RouteDescription
    
    Return the new route in a json with a BaseRoute structure
    """
    route = route.dict()
    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    # id_route must be unique
    id_routes = list(map(lambda r: r['id_route'], routes))
    if route["id_route"] in id_routes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id route '{route['id_route']}'"
        )
    
    # name must be unique
    name_routes = list(map(lambda r: r['name'], routes))
    if route["name"] in name_routes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name route '{route['name']}'"
        )
    
    # the id_glossaries must be valid if exist
    if 'glossary' in route:
        with open('./data/glossary.json', 'r') as f:
            glossary = json.loads(f.read())
        
        id_glossary = list(map(lambda g: g['id_glossary'], glossary))
        for g in route["glossary"]:
            if g not in id_glossary:
                raise HTTPException(
                    status_code=404,
                    detail=f"HTTP_404_NOT_FOUND: Invalid id glossary '{g}'"
                )
    
    # the id_teachers must be valid
    with open('./data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())
    
    id_teachers = list(map(lambda t: t['id_teacher'], teachers))
    del teachers
    for t in route["teachers"]:
        if t not in id_teachers:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id teacher '{t}'"
            )
    
    # the id_courses must be valid
    with open('./data/courses.json', 'r') as f:
        courses = json.loads(f.read())
    
    id_courses = list(map(lambda c: c['id_course'], courses))
    courses = list(map(lambda s: s["courses"], route["sections"]))
    courses = functools.reduce(lambda a,b: a + b, courses)

    for c in courses:
        if c not in id_courses:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id course '{c}'"
            )

    # Parsing route
    route["image_url"] = str(route["image_url"])
    for s in route["sections"]:
        s["level"] = s["level"].value

    # Save the route
    routes.append(route)
    with open('./data/routes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(routes, ensure_ascii=False))

    return route

@app.put(
    path="/{id_route}",
    response_model=RouteDescriptionCreate,
    status_code=status.HTTP_200_OK,
    summary="update a route",
    tags=["Routes"]
)
def put_route(id_route, route: RouteDescriptionCreate = Body(...)):
    """
    This path operation update a route

    Parameters:
        - id_route: str
        - Route: RouteDescription
    
    Return the updated route in a json with a BaseRoute structure
    """
    route = route.dict()
    
    # Considering remove this restriction
    if id_route != route['id_route']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid ids route '{id_route}' and '{route['id_route']}'"
        )

    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    # id_route must be valid
    id_routes = list(map(lambda r: r['id_route'], routes))
    if id_route not in id_routes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_404_NOT_FOUND: Invalid id route '{id_route}'"
        )
    del id_routes
    
    # the id_glossaries must be valid if exist
    if 'glossary' in route:
        with open('./data/glossary.json', 'r') as f:
            glossary = json.loads(f.read())
        
        id_glossary = list(map(lambda g: g['id_glossary'], glossary))
        del glossary
        for g in route["glossary"]:
            if g not in id_glossary:
                raise HTTPException(
                    status_code=404,
                    detail=f"HTTP_404_NOT_FOUND: Invalid id glossary '{g}'"
                )
        del id_glossary
    
    # the id_teachers must be valid
    with open('./data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())
    
    id_teachers = list(map(lambda t: t['id_teacher'], teachers))
    del teachers
    for t in route["teachers"]:
        if t not in id_teachers:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id teacher '{t}'"
            )
    del id_teachers
    
    # the id_courses must be valid
    with open('./data/courses.json', 'r') as f:
        courses = json.loads(f.read())
    
    id_courses = list(map(lambda c: c['id_course'], courses))
    courses = list(map(lambda s: s["courses"], route["sections"]))
    courses = functools.reduce(lambda a,b: a + b, courses)

    for c in courses:
        if c not in id_courses:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id course '{c}'"
            )
    del courses
    del id_courses

    # Parsing route
    route["image_url"] = str(route["image_url"])
    for s in route["sections"]:
        s["level"] = s["level"].value

    # Save the route
    routes = list(filter(lambda r: r["id_route"] != id_route, routes))
    routes.append(route)
    with open('./data/routes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(routes, ensure_ascii=False))

    return route

@app.delete(
    path="/{id_route}",
    response_model=RouteDescriptionCreate,
    status_code=status.HTTP_200_OK,
    summary="delete a route",
    tags=["Routes"]
)
def delete_route(id_route):
    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    # id_route must be unique
    id_routes = list(map(lambda r: r['id_route'], routes))
    if id_route not in id_routes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_404_NOT_FOUND: Invalid id route '{id_route}'"
        )
    del id_routes

    # Removing route of all categories
    with open('./data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())
    
    for c in categories:
        if id_route in c["routes"]:
            c["routes"] = list(filter(lambda r: r != id_route, c["routes"]))
    
    # Save the categories
    with open('./data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))
    del categories

    # Save the routes
    route = list(filter(lambda r: r['id_route'] == id_route, routes))[0]
    routes = list(filter(lambda r: r['id_route'] != id_route, routes))
    with open('./data/routes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(routes, ensure_ascii=False))
    
    return route

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

