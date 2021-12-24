# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

courses_routes = APIRouter()


# Courses
@courses_routes.get(
    path="/",
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
    with open('data/courses.json') as f:
        courses = json.loads(f.read())
    
    return courses

@courses_routes.get(
    path="/clases/{id_course}",
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
    with open('data/courses.json') as f:
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
    with open('data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())

    teacher = list(filter(lambda t: t["id_teacher"] == course["id_teacher"], teachers))[0]
    del teachers
    course["teacher"] = teacher
    del teacher

    # get the routes information
    with open('data/routes.json', 'r') as f:
        routes = json.loads(f.read())

    routes = list(filter(lambda r: r["id_route"] in course["id_routes"], routes))
    course["routes"] = routes
    del routes

    # get the class information
    with open('data/classes.json', 'r') as f:
        all_classes = json.loads(f.read())
    
    for m in course["modules"]:
        classes = list(filter(lambda c: c["id_class"] in m["id_classes"], all_classes))
        m["classes"] = classes
    del all_classes

    # get the project information
    with open('data/projects.json', 'r') as f:
        projects = json.loads(f.read())

    project = list(filter(lambda p: p['id_project']==course['id_project'], projects))[0]
    del projects
    course['project'] = project
    del project

    # get the tutorials information
    with open('data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())
    
    tutorials = list(filter(lambda t: t["id_contribution"] in course["id_tutorials"], tutorials))

    ## get the user information for the tutorials
    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    for t in tutorials:
        t["user"] = list(filter(lambda u: u["id_user"] == t["id_user"], users))[0]
    
    course["tutorials"] = tutorials
    del tutorials

    # get the comments information
    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    comments = list(filter(lambda c: c["id_contribution"] in course["id_comments"], comments))
    
    ## get the user information for the comments
    for c in comments:
        c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]
    
    del users
    course["comments"] = comments
    del comments

    return course

@courses_routes.get(
    path="/{id_course}/basic",
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
    with open('data/courses.json') as f:
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

@courses_routes.get(
    path="/{id_course}",
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
    with open('data/courses.json') as f:
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
    with open('data/teachers.json', 'r') as f:
        teachers = json.loads(f.read())

    teacher = list(filter(lambda t: t["id_teacher"] == course["id_teacher"], teachers))[0]
    del teachers
    course["teacher"] = teacher
    del teacher

    # get the routes information
    with open('data/routes.json', 'r') as f:
        routes = json.loads(f.read())

    routes = list(filter(lambda r: r["id_route"] in course["id_routes"], routes))
    course["routes"] = routes
    del routes

    # get the class information
    with open('data/classes.json', 'r') as f:
        all_classes = json.loads(f.read())
    
    for m in course["modules"]:
        classes = list(filter(lambda c: c["id_class"] in m["id_classes"], all_classes))
        m["classes"] = classes
    del all_classes

    # get the project information
    with open('data/projects.json', 'r') as f:
        projects = json.loads(f.read())

    project = list(filter(lambda p: p['id_project']==course['id_project'], projects))[0]
    del projects
    course['project'] = project
    del project

    # get the tutorials information
    with open('data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())
    
    tutorials = list(filter(lambda t: t["id_contribution"] in course["id_tutorials"], tutorials))

    ## get the user information for the tutorials
    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    for t in tutorials:
        t["user"] = list(filter(lambda u: u["id_user"] == t["id_user"], users))[0]
    
    course["tutorials"] = tutorials
    del tutorials

    # get the comments information
    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    comments = list(filter(lambda c: c["id_contribution"] in course["id_comments"], comments))
    
    ## get the user information for the comments
    for c in comments:
        c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]
    
    del users
    course["comments"] = comments
    del comments

    return course

@courses_routes.post(
    path="/",
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
    with open('data/courses.json', 'r', encoding='utf-8') as f:
        courses = json.loads(f.read())
    
    # id_course must be unique
    id_courses = list(map(lambda c: c['id_course'], courses))
    if course["id_course"] in id_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id route '{course['id_course']}'"
        )
    del id_courses

    # name must be unique
    name_courses = list(map(lambda c: c['name'], courses))
    if course["name"] in name_courses:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid name course '{course['name']}'"
        )
    del name_courses

    # the id in the key must be valid
    keys = ["id_teacher", "id_project"]
    for key in keys:
        with open(f'data/{key.split("_")[1]}s.json', 'r') as f:
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
            with open(f'data/{key.split("_")[1]}.json', 'r') as f:
                temp_file = json.loads(f.read())
            
            id_temps = list(map(lambda t: t[id_file], temp_file))
            for t in course[key]:
                if t not in id_temps:
                    raise HTTPException(
                        status_code=404,
                        detail=f"HTTP_404_NOT_FOUND: Invalid id {key.split('_')[1][:-1]} '{t}'"
                    )
    
    # the id_classes must be valid
    with open('data/classes.json', 'r') as f:
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
    with open('data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    
    return course

@courses_routes.put(
    path="/{id_course}",
    response_model=CourseInfoBasic,
    status_code=status.HTTP_200_OK,
    summary="update a course",
    tags=["Courses"]
)
def put_course(id_course, course: CourseInfoBasic = Body(...)):
    """
    This path operation update a course

    Parameters:
        - course: CourseInfoBasic
    
    Return the new course in a json with a CourseInfoBasic structure
    """
    course = course.dict()
    with open('data/courses.json', 'r', encoding='utf-8') as f:
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
        with open(f'data/{key.split("_")[1]}s.json', 'r') as f:
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
            with open(f'data/{key.split("_")[1]}.json', 'r') as f:
                temp_file = json.loads(f.read())
            
            id_temps = list(map(lambda t: t[id_file], temp_file))
            for t in course[key]:
                if t not in id_temps:
                    raise HTTPException(
                        status_code=404,
                        detail=f"HTTP_404_NOT_FOUND: Invalid id {key.split('_')[1][:-1]} '{t}'"
                    )
    
    # the id_classes must be valid
    with open('data/classes.json', 'r') as f:
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
    with open('data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    
    return course

@courses_routes.delete(
    path="/{id_course}",
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
    with open('data/courses.json', 'r', encoding='utf-8') as f:
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
    with open('data/courses.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(courses, ensure_ascii=False))
    
    return course
