# Python
from typing import List
import functools

# FastAPI
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Body
from fastapi import status

# Models
from schemas.bases import BaseClass
from schemas.classes import ClassContent
from schemas.classes import ClassContentBasic

# Utils
from utils.functions import get_filename_json
from utils.functions import write_filename_json
from utils.functions import validate_unique_key
from utils.functions import validate_valid_key

classes_routes = APIRouter()


# Classes
@classes_routes.get(
    path="/",
    response_model=List[BaseClass],
    status_code=status.HTTP_200_OK,
    summary="get all class with a basic information",
    tags=["Classes"]
)
def all_classes():
    """
    This path operation returns all classes

    Parameters:

    Returns a list of classes with a BaseClass structure:
    """
    classes = get_filename_json('data/classes.json')
    
    return classes

@classes_routes.get(
    path="/{id_class}/basic",
    response_model=ClassContentBasic,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a class",
    tags=["Classes"]
)
def get_classes_basic(id_class):
    """
    This path operation return the basic description for a class

    Parameters:
        - id_class: str
    
    Returns a class with with a ClassContentBasic structure:
    """
    classes = get_filename_json('data/classes.json')

    # id_class mush be valid
    validate_valid_key(
        id_class, classes, 'id_class',
        f"Invalid id class '{id_class}'"
    )

    class_ = list(filter(lambda c: c["id_class"] == id_class, classes))[0]
    del classes

    # Parsing class resourses
    for r in class_["resourses"]:
        r["url"] = str(r["url"])
    
    return class_

@classes_routes.get(
    path="/{id_course}/{id_class}",
    response_model=ClassContent,
    status_code=status.HTTP_200_OK,
    summary="get a complete description of a class",
    tags=["Classes"]
)
def get_class(id_course, id_class):
    """
    This path operation return the complete description for a class

    Parameters:
        - id_class: str
    
    Returns a class with with a ClassContent structure:
    """
    courses = get_filename_json('data/courses.json')
    
    # id_course mush be valid
    validate_valid_key(
        id_course, courses, 'id_course',
        f"Invalid id course '{id_course}'"
    )

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

    classes = get_filename_json('data/classes.json')
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
    all_comments = get_filename_json('data/comments.json')
    comments = list(filter(lambda c: c['id_contribution'] in class_["id_comments"], all_comments))
    users = get_filename_json('data/users.json')
    
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

@classes_routes.post(
    path="/",
    response_model=ClassContentBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a class for a course",
    tags=["Classes"]
)
def post_classes(class_: ClassContentBasic = Body(...)):
    """
    This path operation create a new class

    Parameters:
        - class_: ClassContentBasic
    
    Return the new class in a json with a ClassContentBasic structure
    """
    class_ = class_.dict()
    classes = get_filename_json('data/classes.json')

    # id_class must be unique
    validate_unique_key(
        class_["id_class"], classes, 'id_class',
        f"Invalid id class '{class_['id_class']}'"
    )

    # name must be unique
    validate_unique_key(
        class_["name"], classes, 'name',
        f"Invalid id class '{class_['name']}'"
    )

    # id_comments must not be in class_
    if class_["id_comments"]:
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
    write_filename_json('data/classes.json', classes)

    return class_

@classes_routes.put(
    path="/{id_class}",
    response_model=ClassContentBasic,
    status_code=status.HTTP_200_OK,
    summary="update a class",
    tags=["Classes"]
)
def put_classes(id_class, class_: ClassContentBasic = Body(...)):
    """
    This path operation update a class

    Parameters:
        - class_: ClassContentBasic
    
    Return the updated class in a json with a ClassContentBasic structure
    """
    class_ = class_.dict()
    classes = get_filename_json('data/classes.json')
    
    # id_class must be valid
    validate_valid_key(
        id_class, classes, 'id_class',
        f"Invalid id class '{id_class}'"
    )
    
    classes = list(filter(lambda c: c["id_class"] != id_class, classes))

    # id_class must be unique
    validate_unique_key(
        class_["id_class"], classes, 'id_class',
        f"Invalid id class '{class_['id_class']}'"
    )
    
    # name must be unique
    validate_unique_key(
        class_["name"], classes, 'name',
        f"Invalid id class '{class_['name']}'"
    )

    # Parsing id_comments
    for i in range(len(class_["id_comments"])):
        class_["id_comments"][i] = str(class_["id_comments"][i])
    
    # id_comments must be valid
    comments = get_filename_json('data/comments.json')
    for c in class_["id_comments"]:
        validate_valid_key(
            c, comments, 'id_contribution',
            f"Invalid id comment '{c}'"
        )
    del comments

    # Parsing class resourses
    class_["video_url"] = str(class_["video_url"])
    for r in class_["resourses"]:
        r["url"] = str(r["url"])
    
    # Save the class_
    classes.append(class_)
    write_filename_json('data/classes.json', classes)
    
    return class_

@classes_routes.delete(
    path="/{id_class}",
    response_model=ClassContentBasic,
    status_code=status.HTTP_200_OK,
    summary="delete a class",
    tags=["Classes"]
)
def delete_classes(id_class):
    """
    This path operation delete a class

    Parameters:
        - id_class: str
    
    Return the deleted class in a json with a ClassContentBasic structure
    """
    classes = get_filename_json('data/classes.json')

    # id_class must be valid
    validate_valid_key(
        id_class, classes, 'id_class',
        f"Invalid id class '{id_class}'"
    )
        
    # delete class from courses
    courses = get_filename_json('data/courses.json')
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
    
    write_filename_json('data/courses.json', courses)
    del courses

    # Save the class_
    class_ = list(filter(lambda  c: c["id_class"] == id_class, classes))[0]
    classes = list(filter(lambda  c: c["id_class"] != id_class, classes))
    write_filename_json('data/classes.json', classes)
    
    return class_
