# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

routes_routes = APIRouter()


# Routes
@routes_routes.get(
    path="/",
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
    with open('data/routes.json', 'r') as f:
        routes = json.loads(f.read())

    return routes

@routes_routes.get(
    path="/{id_route}",
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
    with open('data/routes.json', 'r') as f:
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
    with open('data/glossary.json', 'r') as f:
        glossary = json.loads(f.read())
    
    glossary = list(filter(lambda g: g['id_glossary'] in route["glossary"], glossary))
    route["glossary"] = glossary
    del glossary

    # get the courses
    with open('data/courses.json', 'r') as f:
        all_courses = json.loads(f.read())
    
    id_courses = list(map(lambda s: s['courses'], route['sections']))
    
    for i in range(len(id_courses)):
        courses = list(filter(lambda c: c['id_course'] in id_courses[i], all_courses))
        route['sections'][i]["courses"] = courses
    del all_courses

    # get the teachers
    with open('data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())
    
    teachers = list(filter(lambda t: t['id_teacher'] in route["teachers"], teachers))
    route["teachers"] = teachers

    return route

@routes_routes.get(
    path="/{id_route}/basic",
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
    with open('data/routes.json', 'r') as f:
        routes = json.loads(f.read())
    
    route = list(filter(lambda r: r['id_route'] == id_route, routes))
    del routes
    if not route:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id route '{id_route}'"
        )


    return route[0]

@routes_routes.post(
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
    with open('data/routes.json', 'r', encoding='utf-8') as f:
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
        with open('data/glossary.json', 'r') as f:
            glossary = json.loads(f.read())
        
        id_glossary = list(map(lambda g: g['id_glossary'], glossary))
        for g in route["glossary"]:
            if g not in id_glossary:
                raise HTTPException(
                    status_code=404,
                    detail=f"HTTP_404_NOT_FOUND: Invalid id glossary '{g}'"
                )
    
    # the id_teachers must be valid
    with open('data/teachers.json', 'r') as f:
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
    with open('data/courses.json', 'r') as f:
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
    with open('data/routes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(routes, ensure_ascii=False))

    return route

@routes_routes.put(
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

    
    with open('data/routes.json', 'r', encoding='utf-8') as f:
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
        with open('data/glossary.json', 'r') as f:
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
    with open('data/teachers.json', 'r') as f:
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
    with open('data/courses.json', 'r') as f:
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
    with open('data/routes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(routes, ensure_ascii=False))

    return route

@routes_routes.delete(
    path="/{id_route}",
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
    with open('data/routes.json', 'r', encoding='utf-8') as f:
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
    with open('data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())
    
    for c in categories:
        if id_route in c["routes"]:
            c["routes"] = list(filter(lambda r: r != id_route, c["routes"]))
    
    # Save the categories
    with open('data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))
    del categories

    # Save the routes
    route = list(filter(lambda r: r['id_route'] == id_route, routes))[0]
    routes = list(filter(lambda r: r['id_route'] != id_route, routes))
    with open('data/routes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(routes, ensure_ascii=False))
    
    return route
