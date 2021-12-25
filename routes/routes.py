# Python
from typing import List
import json
import functools

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
    routes = get_filename_json('data/routes.json')

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
    routes = get_filename_json('data/routes.json')
    
    # id route must be valid
    validate_valid_key(
        id_route, routes, 'id_route',
        f"Invalid id route '{id_route}'"
    )
    
    route = list(filter(lambda r: r['id_route'] == id_route, routes))[0]
    del routes

    # get the glossary
    glossary = get_filename_json('data/glossary.json')
    glossary = list(filter(lambda g: g['id_glossary'] in route["glossary"], glossary))
    route["glossary"] = glossary
    del glossary

    # get the courses
    all_courses = get_filename_json('data/courses.json')
    id_courses = list(map(lambda s: s['courses'], route['sections']))
    
    for i in range(len(id_courses)):
        courses = list(filter(lambda c: c['id_course'] in id_courses[i], all_courses))
        route['sections'][i]["courses"] = courses
    del all_courses

    # get the teachers
    teachers = get_filename_json('data/teachers.json')
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
    routes = get_filename_json('data/routes.json')
    
    # id route must be valid
    validate_valid_key(
        id_route, routes, 'id_route',
        f"Invalid id route '{id_route}'"
    )

    route = list(filter(lambda r: r['id_route'] == id_route, routes))[0]

    return route

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
    routes = get_filename_json('data/routes.json')
    
    # id_route must be unique
    validate_unique_key(
        route["id_route"], routes, 'id_route',
        f"Invalid id route '{route['id_route']}'"
    )
    
    # name must be unique
    validate_unique_key(
        route["name"], routes, 'name',
        f"Invalid name route '{route['name']}'"
    )
    
    # the id_glossaries must be valid if exist
    if 'glossary' in route:
        glossary = get_filename_json('data/glossary.json')

        for g in route["glossary"]:
            validate_valid_key(
                g, glossary, 'id_glossary',
                f"Invalid id glossary '{g}'"
            )
    
    # the id_teachers must be valid
    teachers = get_filename_json('data/teachers.json')
    for t in route["teachers"]:
        validate_valid_key(
            t, teachers, 'id_teacher',
            f"Invalid id teacher '{t}'"
        )
    del teachers
    
    # the id_courses must be valid
    courses = get_filename_json('data/courses.json')
    id_courses = list(map(lambda s: s["courses"], route["sections"]))
    id_courses = functools.reduce(lambda a,b: a + b, id_courses)

    for c in id_courses:
        validate_valid_key(
            c, courses, 'id_course',
            f"Invalid id course '{c}'"
        )
    del courses
    del id_courses

    # Parsing route
    route["image_url"] = str(route["image_url"])
    for s in route["sections"]:
        s["level"] = s["level"].value

    # Save the route
    routes.append(route)
    write_filename_json('data/routes.json', routes)

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
    routes = get_filename_json('data/routes.json')
    
    # id_route must be valid
    validate_valid_key(
        id_route, routes, 'id_route',
        f"Invalid id route '{id_route}'"
    )

    # name must be unique
    temp_routes = list(filter(lambda r: r["id_route"] != id_route, routes))
    validate_valid_key(
        route["name"], temp_routes, 'name',
        f"Invalid name route '{route['name']}'"
    )
    del temp_routes
    
    # the id_glossaries must be valid if exist
    if 'glossary' in route:
        glossary = get_filename_json('data/glossary.json')
        
        for g in route["glossary"]:
            validate_valid_key(
                g, glossary, 'id_glossary',
                f"Invalid id glossary '{g}'"
            )
        del glossary

    # the id_teachers must be valid
    teachers = get_filename_json('data/teachers.json')
    for t in route["teachers"]:
        validate_valid_key(
            t, teachers, 'id_teacher',
            f"Invalid id teacher '{t}'"
        )
    del teachers

    # the id_courses must be valid
    courses = get_filename_json('data/courses.json')
    id_courses = list(map(lambda s: s["courses"], route["sections"]))
    id_courses = functools.reduce(lambda a,b: a + b, id_courses)

    for c in id_courses:
        validate_valid_key(
            c, courses, 'id_course',
            f"Invalid id course '{c}'"
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
    write_filename_json('data/routes.json', routes)

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
    routes = get_filename_json('data/routes.json')
    
    # id_route must be valid
    validate_valid_key(
        id_route, routes, 'id_route',
        f"Invalid id route '{id_route}'"
    )

    # Removing route of all categories
    categories = get_filename_json('data/categories.json')
    
    for c in categories:
        if id_route in c["routes"]:
            c["routes"] = list(filter(lambda r: r != id_route, c["routes"]))
    
    # Save the categories
    write_filename_json('data/categories.json', categories)
    del categories

    # Save the routes
    route = list(filter(lambda r: r['id_route'] == id_route, routes))[0]
    routes = list(filter(lambda r: r['id_route'] != id_route, routes))
    write_filename_json('data/routes.json', routes)
    
    return route
