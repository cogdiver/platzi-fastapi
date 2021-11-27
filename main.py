# Python
import json
import functools
from typing import List

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body

app = FastAPI()

# Models
from models import *

# Home
from home import HOME

@app.get(path="/")
def home():
    print(HOME)
    return {
        "Platzi": "Never stop learning, because life never stops teaching"
    }


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
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id category '{category['id_category']}'"
        )

    # name must be unique
    name_categories = list(map(lambda c: c['name'], categories))
    if category['name'] in name_categories:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name category '{category['id_category']}'"
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

    # name must be unique
    temp_categories = list(filter(lambda c: c["id_category"] != id_category, categories))
    name_categories = list(map(lambda c: c['name'], temp_categories))
    if category["name"] in name_categories:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name category '{category['name']}'"
        )
    del temp_categories
    del name_categories
    
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

    Returns a list of routes with a BaseRoute structure:
    """
    with open('./data/routes.json', 'r') as f:
        routes = json.loads(f.read())

    return routes

@app.get(
    path="/rutas/{id_route}",
    response_model=RouteDescription,
    status_code=status.HTTP_200_OK,
    summary="get a route",
    tags=["Routes"]
)
def get_route(id_route):
    """
    This path operation return the description for a route

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
        route['sections'][i]["courses"] = courses
    del all_courses

    # get the teachers
    with open('./data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())
    
    teachers = list(filter(lambda t: t['id_teacher'] in route["teachers"], teachers))
    route["teachers"] = teachers

    return route

@app.get(
    path="/rutas/{id_route}/basic",
    response_model=RouteDescriptionCreate,
    status_code=status.HTTP_200_OK,
    summary="get a route with a basic information",
    tags=["Routes"]
)
def get_route_basic(id_route):
    """
    This path operation the basic information for a route

    Parameters:
        - id_route: str
    
    Returns a route with a RouteDescriptionCreate structure:
    """
    with open('./data/routes.json', 'r') as f:
        routes = json.loads(f.read())
    
    route = list(filter(lambda r: r['id_route'] == id_route, routes))
    del routes
    if not route:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id route '{id_route}'"
        )


    return route[0]

@app.post(
    path="/rutas",
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
    path="/rutas/{id_route}",
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

    
    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    # id_route must be valid
    id_routes = list(map(lambda r: r['id_route'], routes))
    if id_route not in id_routes:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id route '{id_route}'"
        )
    del id_routes

    # name must be unique
    temp_routes = list(filter(lambda r: r["id_route"] != id_route, routes))
    name_routes = list(map(lambda r: r['name'], temp_routes))
    if route["name"] in name_routes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name route '{route['name']}'"
        )
    del temp_routes
    del name_routes
    
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
    path="/rutas/{id_route}",
    response_model=RouteDescriptionCreate,
    status_code=status.HTTP_200_OK,
    summary="delete a route",
    tags=["Routes"]
)
def delete_route(id_route):
    """
    This path operation delete a route

    Parameters:
        - id_route: str
    
    Return the deleted route in a json with a RouteDescriptionCreate structure
    """
    with open('./data/routes.json', 'r', encoding='utf-8') as f:
        routes = json.loads(f.read())
    
    # id_route must be unique
    id_routes = list(map(lambda r: r['id_route'], routes))
    if id_route not in id_routes:
        raise HTTPException(
            status_code=404,
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
    """
    This path operation returns all courses

    Parameters:

    Returns a list of routes with a BaseCourse structure:
    """
    with open('./data/courses.json') as f:
        courses = json.loads(f.read())
    
    return courses

@app.get(
    path="/cursos/clases/{id_course}",
    response_model=CourseInfo,
    status_code=status.HTTP_200_OK,
    summary="get a basic description of a course",
    tags=["Courses"]
)
def class_course(id_course):
    """
    This path operation return the description for a route

    Parameters:
        - id_course: str
    
    Returns a course with with a CourseInfo structure:
    """
    with open('./data/courses.json') as f:
        courses = json.loads(f.read())

    # id_course must be valid
    id_courses = list(map(lambda c: c['id_course'], courses))
    if id_course not in id_courses:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id course '{id_course}'"
        )
    del id_courses

    course = list(filter(lambda c: c["id_course"] == id_course, courses))[0]
    del courses

    # get the teacher information
    with open('./data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())

    teacher = list(filter(lambda t: t["id_teacher"] == course["id_teacher"], teachers))[0]
    del teachers
    course["teacher"] = teacher
    del teacher

    # get the routes information
    with open('./data/routes.json', 'r') as f:
        routes = json.loads(f.read())

    routes = list(filter(lambda r: r["id_route"] in course["id_routes"], routes))
    course["routes"] = routes
    del routes

    # get the class information
    with open('./data/classes.json', 'r') as f:
        all_classes = json.loads(f.read())
    
    for m in course["modules"]:
        classes = list(filter(lambda c: c["id_class"] in m["id_classes"], all_classes))
        m["classes"] = classes
    del all_classes

    # get the project information
    with open('./data/projects.json', 'r') as f:
        projects = json.loads(f.read())

    project = list(filter(lambda p: p['id_project']==course['id_project'], projects))[0]
    del projects
    course['project'] = project
    del project

    # get the tutorials information
    with open('./data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())
    
    tutorials = list(filter(lambda t: t["id_contribution"] in course["id_tutorials"], tutorials))

    ## get the user information for the tutorials
    with open('./data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    for t in tutorials:
        t["user"] = list(filter(lambda u: u["id_user"] == t["id_user"], users))[0]
    
    course["tutorials"] = tutorials
    del tutorials

    # get the comments information
    with open('./data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    comments = list(filter(lambda c: c["id_contribution"] in course["id_comments"], comments))
    
    ## get the user information for the comments
    for c in comments:
        c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]
    
    del users
    course["comments"] = comments
    del comments

    return course

@app.get(
    path="/cursos/{id_course}/basic",
    response_model=CourseInfoBasic,
    status_code=status.HTTP_200_OK,
    summary="get a basic description of a course",
    tags=["Courses"]
)
def class_course_basic(id_course):
    """
    This path operation return the basic description for a route

    Parameters:
        - id_route: str
    
    Returns a route with with a CourseInfoBasic structure:
    """
    with open('./data/courses.json') as f:
        courses = json.loads(f.read())

    # id_course must be valid
    id_courses = list(map(lambda c: c['id_course'], courses))
    if id_course not in id_courses:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id course {id_course}"
        )
    del id_courses
    course = list(filter(lambda c: c["id_course"] == id_course, courses))[0]

    return course

@app.get(
    path="/cursos/{id_course}",
    response_model=CourseInfoComplete,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a course",
    tags=["Courses"]
)
def get_course(id_course):
    """
    This path operation return the complete description for a route

    Parameters:
        - id_route: str
    
    Returns a route with with a CourseInfoComplete structure:
    """
    with open('./data/courses.json') as f:
        courses = json.loads(f.read())

    # id_course must be valid
    id_courses = list(map(lambda c: c['id_course'], courses))
    if id_course not in id_courses:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id course {id_course}"
        )
    del id_courses

    course = list(filter(lambda c: c["id_course"] == id_course, courses))[0]
    del courses

    # get the teacher information
    with open('./data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())

    teacher = list(filter(lambda t: t["id_teacher"] == course["id_teacher"], teachers))[0]
    del teachers
    course["teacher"] = teacher
    del teacher

    # get the routes information
    with open('./data/routes.json', 'r') as f:
        routes = json.loads(f.read())

    routes = list(filter(lambda r: r["id_route"] in course["id_routes"], routes))
    course["routes"] = routes
    del routes

    # get the class information
    with open('./data/classes.json', 'r') as f:
        all_classes = json.loads(f.read())
    
    for m in course["modules"]:
        classes = list(filter(lambda c: c["id_class"] in m["id_classes"], all_classes))
        m["classes"] = classes
    del all_classes

    # get the project information
    with open('./data/projects.json', 'r') as f:
        projects = json.loads(f.read())

    project = list(filter(lambda p: p['id_project']==course['id_project'], projects))[0]
    del projects
    course['project'] = project
    del project

    # get the tutorials information
    with open('./data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())
    
    tutorials = list(filter(lambda t: t["id_contribution"] in course["id_tutorials"], tutorials))

    ## get the user information for the tutorials
    with open('./data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    for t in tutorials:
        t["user"] = list(filter(lambda u: u["id_user"] == t["id_user"], users))[0]
    
    course["tutorials"] = tutorials
    del tutorials

    # get the comments information
    with open('./data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    comments = list(filter(lambda c: c["id_contribution"] in course["id_comments"], comments))
    
    ## get the user information for the comments
    for c in comments:
        c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]
    
    del users
    course["comments"] = comments
    del comments

    return course

@app.post(
    path="/cursos",
    response_model=CourseInfoBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a course",
    tags=["Courses"]
)
def post_course(course: CourseInfoBasic =  Body(...)):
    """
    This path operation create a new course

    Parameters:
        - course: CourseInfoBasic
    
    Return the new course in a json with a CourseInfoBasic structure
    """
    course = course.dict()
    with open('./data/courses.json', 'r', encoding='utf-8') as f:
        courses = json.loads(f.read())
    
    # id_course must be unique
    id_courses = list(map(lambda c: c['id_course'], courses))
    if course["id_course"] in id_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id route '{course['id_course']}'"
        )
    
    # name must be unique
    name_courses = list(map(lambda c: c['name'], courses))
    if course["name"] in name_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name course '{course['name']}'"
        )
    
    # the id in the key must be valid
    keys = ["id_teacher", "id_project"]
    for key in keys:
        with open(f'./data/{key.split("_")[1]}s.json', 'r') as f:
            temp_file = json.loads(f.read())
        
        id_temps = list(map(lambda t: t[key], temp_file))
        if course[key] not in id_temps:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id {key.split('_')[1]} '{course[key]}'"
            )
    
    # Parsing course
    course["image_url"] = str(course["image_url"])
    for key in ["id_tutorials", "id_comments"]:
        course[key] = [str(v) for v in course[key]]

    # the ids for the opcional keys must be valid if exist
    optionals = {
        "id_routes": "id_route",
        "id_tutorials": "id_contribution",
        "id_comments": "id_contribution"
    }
    for key, id_file in optionals.items():
        if key in course:
            with open(f'./data/{key.split("_")[1]}.json', 'r') as f:
                temp_file = json.loads(f.read())
            
            id_temps = list(map(lambda t: t[id_file], temp_file))
            for t in course[key]:
                if t not in id_temps:
                    raise HTTPException(
                        status_code=404,
                        detail=f"HTTP_404_NOT_FOUND: Invalid id {key.split('_')[1][:-1]} '{t}'"
                    )
    
    # the id_classes must be valid
    with open('./data/classes.json', 'r') as f:
        classes = json.loads(f.read())
    
    id_classes = list(map(lambda c: c['id_class'], classes))
    classes = list(map(lambda m: m["id_classes"], course["modules"]))
    classes = functools.reduce(lambda a,b: a + b, classes)

    for c in classes:
        if c not in id_classes:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id course '{c}'"
            )

    # Save the course
    courses.append(course)
    with open('./data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    
    return course

@app.put(
    path="/cursos/{id_course}",
    response_model=CourseInfoBasic,
    status_code=status.HTTP_200_OK,
    summary="update a course",
    tags=["Courses"]
)
def put_course(id_course, course: CourseInfoBasic = Body(...)):
    """
    This path operation update a new course

    Parameters:
        - course: CourseInfoBasic
    
    Return the new course in a json with a CourseInfoBasic structure
    """
    course = course.dict()
    with open('./data/courses.json', 'r', encoding='utf-8') as f:
        courses = json.loads(f.read())
    
    # id_course must be valid
    id_courses = list(map(lambda c: c['id_course'], courses))
    if id_course not in id_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id course '{id_course}'"
        )
    
    # name must be unique
    temp_courses = list(filter(lambda c: c["id_course"] != id_course, courses))
    name_courses = list(map(lambda c: c['name'], temp_courses))
    if course["name"] in name_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name course '{course['name']}'"
        )
    del temp_courses    
    del name_courses

    # the id in the key must be valid
    keys = ["id_teacher", "id_project"]
    for key in keys:
        with open(f'./data/{key.split("_")[1]}s.json', 'r') as f:
            temp_file = json.loads(f.read())
        
        id_temps = list(map(lambda t: t[key], temp_file))
        if course[key] not in id_temps:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id {key.split('_')[1]} '{course[key]}'"
            )
    
    # Parsing course
    course["image_url"] = str(course["image_url"])
    for key in ["id_tutorials", "id_comments"]:
        course[key] = [str(v) for v in course[key]]

    # the ids for the opcional keys must be valid if exist
    optionals = {
        "id_routes": "id_route",
        "id_tutorials": "id_contribution",
        "id_comments": "id_contribution"
    }
    for key, id_file in optionals.items():
        if key in course:
            with open(f'./data/{key.split("_")[1]}.json', 'r') as f:
                temp_file = json.loads(f.read())
            
            id_temps = list(map(lambda t: t[id_file], temp_file))
            for t in course[key]:
                if t not in id_temps:
                    raise HTTPException(
                        status_code=404,
                        detail=f"HTTP_404_NOT_FOUND: Invalid id {key.split('_')[1][:-1]} '{t}'"
                    )
    
    # the id_classes must be valid
    with open('./data/classes.json', 'r') as f:
        classes = json.loads(f.read())
    
    id_classes = list(map(lambda c: c['id_class'], classes))
    classes = list(map(lambda m: m["id_classes"], course["modules"]))
    classes = functools.reduce(lambda a,b: a + b, classes)

    for c in classes:
        if c not in id_classes:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id course '{c}'"
            )

    # Save the course
    courses = list(filter(lambda c: c["id_course"] != id_course, courses))
    courses.append(course)
    with open('./data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    
    return course

@app.delete(
    path="/cursos/{id_course}",
    response_model=CourseInfoBasic,
    status_code=status.HTTP_200_OK,
    summary="delete a course",
    tags=["Courses"]
)
def delete_course(id_course):
    """
    This path operation delete a new course

    Parameters:
        - course: CourseInfoBasic
    
    Return the deleted course in a json with a CourseInfoBasic structure
    """
    with open('./data/courses.json', 'r', encoding='utf-8') as f:
        courses = json.loads(f.read())
    
    # id_course must be valid
    id_courses = list(map(lambda c: c['id_course'], courses))
    if id_course not in id_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id course '{id_course}'"
        )
    
    # Save the course
    course = list(filter(lambda c: c["id_course"] == id_course, courses))[0]
    courses = list(filter(lambda c: c["id_course"] != id_course, courses))
    with open('./data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    
    return course


# Classes
@app.get(
    path="/clases",
    response_model=List[BaseClass],
    status_code=status.HTTP_200_OK,
    summary="get all class with a basic information",
    tags=["Class"]
)
def all_classes():
    """
    This path operation returns all classes

    Parameters:

    Returns a list of classes with a BaseClass structure:
    """
    with open('./data/classes.json') as f:
        classes = json.loads(f.read())
    
    return classes

@app.get(
    path="/clases/{id_class}/basic",
    response_model=ClassContentBasic,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a class",
    tags=["Class"]
)
def get_classes_basic(id_class):
    """
    This path operation return the basic description for a class

    Parameters:
        - id_class: str
    
    Returns a class with with a ClassContentBasic structure:
    """
    with open('./data/classes.json') as f:
        classes = json.loads(f.read())

    # id_class mush be valid
    id_classes = list(map(lambda c: c["id_class"], classes))
    if id_class not in id_classes:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id class '{id_class}'"
        )
    del id_classes

    class_ = list(filter(lambda c: c["id_class"] == id_class, classes))[0]
    del classes

    # Parsing class resourses
    for r in class_["resourses"]:
        r["url"] = str(r["url"])
    
    return class_

@app.get(
    path="/clases/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a class",
    tags=["Class"]
)
def get_class(id_course, id_class):
    """
    This path operation return the complete description for a class

    Parameters:
        - id_class: str
    
    Returns a class with with a ClassContent structure:
    """
    with open('./data/courses.json') as f:
        courses = json.loads(f.read())
    
    # id_course mush be valid
    id_courses = list(map(lambda c: c["id_course"], courses))
    if id_course not in id_courses:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id course '{id_course}'"
        )
    del id_courses

    # id_class mush be valid for id_course
    course = list(filter(lambda c: c["id_course"] == id_course, courses))[0]
    del courses
    id_classes = list(map(lambda c: c["id_classes"], course["modules"]))
    id_classes = functools.reduce(lambda a,b: a+b, id_classes)
    if id_class not in id_classes:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id class '{id_class}' for the id course '{id_course}'"
        )

    with open('./data/classes.json') as f:
        classes = json.loads(f.read())

    class_ = list(filter(lambda c: c["id_class"] == id_class, classes))[0]
    classes = list(filter(lambda c: c["id_class"] in id_classes, classes))
    classes = list(map(lambda c: {"id_class": c["id_class"], "name":c["name"]}, classes))

    # Parsing class resourses
    for r in class_["resourses"]:
        r["url"] = str(r["url"])

    # get course and modules
    course["modules"] = list(
        map(
            lambda m: {**m, **{"classes": list(
                filter(
                    lambda c: c["id_class"] in m["id_classes"],
                    classes
                )
            )}},
            course["modules"]
        )
    )
    class_["course"] = course
    del classes
    class_["modules"] = course["modules"]
    del course

    # get comments and answers
    with open('./data/comments.json') as f:
        all_comments = json.loads(f.read())
    
    comments = list(filter(lambda c: c['id_contribution'] in class_["id_comments"], all_comments))

    with open('./data/users.json') as f:
        users = json.loads(f.read())
    
    comments = list(
        map(
            lambda c: {
                **c,
                **{"user": list(
                    filter(
                        lambda u: u["id_user"] == c["id_user"],
                        users
                    )
                )[0]},
            },
            comments,
        )
    )
    comments = list(
        map(
            lambda c: {
                **c,
                **{"answers": list(
                    filter(
                        lambda a: a["id_contribution"] in c["id_answers"],
                        all_comments
                    )
                )},
            } if c['id_answers'] else c,
            comments
        )
    )
    comments = list(
        map(
            lambda c: {
                **c,
                **{"answers": list(
                    map(
                        lambda a: {**a, **{'user': list(
                            filter(
                                lambda u: u["id_user"] == a["id_user"],
                                users
                            )
                        )[0]}},
                        c["answers"]
                    )
                )},
            } if c['id_answers'] else c,
            comments,
        )
    )
    del all_comments

    class_["comments"] = comments

    return class_

@app.post(
    path="/clases",
    response_model=ClassContentBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a class for a course",
    tags=["Class"]
)
def post_classes(class_: ClassContentBasic = Body(...)):
    """
    This path operation create a new class

    Parameters:
        - class_: ClassContentBasic
    
    Return the new class in a json with a ClassContentBasic structure
    """
    class_ = class_.dict()
    with open('./data/classes.json', 'r', encoding='utf-8') as f:
        classes = json.loads(f.read())

    # id_class must be unique
    id_classes = list(map(lambda c: c['id_class'], classes))
    if class_["id_class"] in id_classes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id class '{class_['id_class']}'"
        )
    del id_classes

    # name must be unique
    name_classes = list(map(lambda c: c['name'], classes))
    if class_["name"] in name_classes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name class '{class_['name']}'"
        )
    del name_classes

    # id_comments must not be in class_
    if class_["id_comments"]:
        print(class_)
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid key 'id_comments'"
        )

    # Parsing class resourses
    class_["video_url"] = str(class_["video_url"])
    for r in class_["resourses"]:
        r["url"] = str(r["url"])
    
    # Save the class_
    classes.append(class_)
    with open('./data/classes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(classes, ensure_ascii=False))
    
    return class_

@app.put(
    path="/clases/{id_class}",
    response_model=ClassContentBasic,
    status_code=status.HTTP_200_OK,
    summary="update a class",
    tags=["Class"]
)
def put_classes(id_class, class_: ClassContentBasic = Body(...)):
    """
    This path operation update a new class

    Parameters:
        - class_: ClassContentBasic
    
    Return the updated class in a json with a ClassContentBasic structure
    """
    class_ = class_.dict()
    with open('./data/classes.json', 'r', encoding='utf-8') as f:
        classes = json.loads(f.read())
    
    # id_class must be valid
    id_classes = list(map(lambda c: c['id_class'], classes))
    if id_class not in id_classes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id class '{id_class}'"
        )
    
    classes = list(filter(lambda c: c["id_class"] != id_class, classes))

    # id_class must be unique
    if class_["id_class"] in id_classes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id class '{class_['id_class']}'"
        )
    del id_classes

    # name must be unique
    name_classes = list(map(lambda c: c['name'], classes))
    if class_["name"] in name_classes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name class '{class_['name']}'"
        )
    del name_classes

    # Parsing id_comments
    for i in range(len(class_["id_comments"])):
        class_["id_comments"][i] = str(class_["id_comments"][i])
    
    # id_comments must be valid
    with open('./data/comments.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())
    
    id_comments = list(map(lambda c: c["id_contribution"], comments))
    del comments

    for c in class_["id_comments"]:
        if c not in id_comments:
            raise HTTPException(
                status_code=406,
                detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id comment '{c}'"
            )

    # Parsing class resourses
    class_["video_url"] = str(class_["video_url"])
    for r in class_["resourses"]:
        r["url"] = str(r["url"])
    
    # Save the class_
    classes.append(class_)
    with open('./data/classes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(classes, ensure_ascii=False))
    
    return class_

@app.delete(
    path="/clases/{id_class}",
    response_model=ClassContentBasic,
    status_code=status.HTTP_200_OK,
    summary="delete a class",
    tags=["Class"]
)
def delete_classes(id_class):
    """
    This path operation delete a class

    Parameters:
        - id_class: str
    
    Return the deleted class in a json with a ClassContentBasic structure
    """
    with open('./data/classes.json', 'r', encoding='utf-8') as f:
        classes = json.loads(f.read())

    # id_class must be valid
    id_classes = list(map(lambda c: c['id_class'], classes))
    if id_class not in id_classes:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id class '{id_class}'"
        )
        
    # delete class from courses
    with open('./data/courses.json', 'r', encoding='utf-8') as f:
        courses = json.loads(f.read())
    
    courses = list(
        map(
            lambda c: {**c, **{"modules": list(
                map(
                    lambda m: {**m, **{"id_classes": [c for c in m["id_classes"] if c != id_class]}},
                    c["modules"]
                )
            )}},
            courses
        )
    )

    with open('./data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    del courses

    # Save the class_
    class_ = list(filter(lambda  c: c["id_class"] == id_class, classes))[0]
    classes = list(filter(lambda  c: c["id_class"] != id_class, classes))
    with open('./data/classes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(classes, ensure_ascii=False))
    
    return class_


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
    """
    This path operation returns all comments

    Parameters:

    Returns a list of comments with a ContributionAnswer structure:
    """
    with open('./data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    with open('./data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    comments = list(
        map(
            lambda c: {**c, **{"user": list(
                filter(
                    lambda u: u["id_user"] == c["id_user"],
                    users
                )
            )[0]}},
            comments
        )
    )
    del users

    comments = list(
        map(
            lambda c: {
                **c,
                **{"answers": list(
                    filter(
                        lambda a: a["id_contribution"] in c["id_answers"],
                        comments
                    )
                )}
            } if c["id_answers"] else c,
            comments
        )
    )
    
    return comments

@app.get(
    path="/comentario/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="get a comment",
    tags=["Comments"]
)
def get_comment(id_comment):
    """
    This path operation return the complete information for a comment

    Parameters:
        - id_comment: str
    
    Returns a comment with with a ContributionAnswer structure:
    """
    with open('./data/comments.json', 'r') as f:
        comments = json.loads(f.read())
    
    id_comments = list(map(lambda c: c["id_contribution"], comments))

    # id_comment must be valid
    if id_comment not in id_comments:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id id_comment '{id_comment}'"
        )
    del id_comments

    # get comment
    comment = list(filter(lambda c: c["id_contribution"]==id_comment, comments))[0]

    # get user for comment
    with open('./data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    comment["user"] = list(filter(lambda u: u["id_user"] == comment["id_user"], users))[0]
    
    # get answers
    if comment["id_answers"]:
        comment["answers"] = list(
            filter(
                lambda a: a["id_contribution"] in comment["id_answers"],
                comments
            )
        )
        del comments
    
        ## get users for answers
        comment["answers"] = list(
            map(
                lambda a: {**a, **{"user": list(
                    filter(
                        lambda u: u["id_user"] == a["id_user"],
                        users
                    )
                )[0]}},
                comment["answers"]
            )
        )
    
    return comment

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
    """
    This path operation returns all classes

    Parameters:

    Returns a list of classes with a BaseClass structure:
    """

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
    """
    This path operation returns all classes

    Parameters:

    Returns a list of classes with a BaseClass structure:
    """

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
    """
    This path operation returns all classes

    Parameters:

    Returns a list of classes with a BaseClass structure:
    """

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

