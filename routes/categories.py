# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *
from utils.functions import *

categories_routes = APIRouter()


# Categories
@categories_routes.get(
    path="/",
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
    categories = get_filename_json('data/categories.json')
    
    categories = [{"id_category":c["id_category"],"name":c["name"]} for c in categories]
    return categories

@categories_routes.get(
    path="/{id_category}",
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
    categories = get_filename_json('data/categories.json')
    routes = get_filename_json('data/routes.json')
    
    category = list(filter(lambda c: c['id_category']==id_category, categories))[0]
    del categories
    
    routes = list(filter(lambda r: r['id_route'] in category['routes'], routes))
    category['routes'] = routes

    return category

@categories_routes.post(
    path="/",
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
    categories = get_filename_json('data/categories.json')

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
    routes = get_filename_json('data/routes.json')
    
    id_routes = list(map(lambda r: r['id_route'], routes))
    for r in category['routes']:
        if r not in id_routes:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id route '{r}'"
            )
    
    # Save the category
    categories.append(category)
    write_filename_json('data/categories.json', categories)

    return category

@categories_routes.put(
    path="/{id_category}",
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
    categories = get_filename_json('data/categories.json')

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
    
    routes = get_filename_json('data/routes.json')
    
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
    write_filename_json('data/categories.json', categories)

    return category

@categories_routes.delete(
    path="/{id_category}",
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
    categories = get_filename_json('data/categories.json')
    id_categories = list(map(lambda c: c['id_category'], categories))
    
    if id_category not in id_categories:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id category '{id_category}'"
        )

    category = list(filter(lambda c: c['id_category'] == id_category, categories))[0]
    categories = list(filter(lambda c: c['id_category'] != id_category, categories))
    write_filename_json('data/categories.json', categories)

    return category
