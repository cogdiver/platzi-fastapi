# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

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
    with open('data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())
    
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

    with open('data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())
    
    with open('data/routes.json', 'r', encoding='utf-8') as f:
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

    with open('data/categories.json', 'r', encoding='utf-8') as f:
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
    with open('data/routes.json', 'r', encoding='utf-8') as f:
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
    with open('data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

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

    with open('data/categories.json', 'r', encoding='utf-8') as f:
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
    
    with open('data/routes.json', 'r', encoding='utf-8') as f2:
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
        
    with open('data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

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
    with open('data/categories.json', 'r', encoding='utf-8') as f:
        categories = json.loads(f.read())

    id_categories = list(map(lambda c: c['id_category'], categories))
    
    if id_category not in id_categories:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id category '{id_category}'"
        )

    category = list(filter(lambda c: c['id_category'] == id_category, categories))[0]
    categories = list(filter(lambda c: c['id_category'] != id_category, categories))
        
    with open('data/categories.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(categories, ensure_ascii=False))

    return category
