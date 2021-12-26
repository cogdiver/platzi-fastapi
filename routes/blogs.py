# Python
from typing import List

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

# Utils
from utils.functions import get_filename_json
from utils.functions import write_filename_json
from utils.functions import get_all_contributions
from utils.functions import get_contribution
from utils.functions import get_contribution_basic
from utils.functions import post_contribution
from utils.functions import put_contribution
from utils.functions import delete_contribution

blogs_routes = APIRouter()


# Blog
@blogs_routes.get(
    path="/",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all blogs",
    tags=["Blogs"]
)
def all_blogs():
    """
    This path operation returns all blogs

    Parameters:

    Returns a list of blogs with a ContributionTitle structure:
    """
    blogs = get_all_contributions('blogs')
    
    return blogs

@blogs_routes.get(
    path="/{id_blog}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a blog publication",
    tags=["Blogs"]
)
def get_blog(id_blog):
    """
    This path operation returns a blog

    Parameters:

    Returns a blog with a ContributionTitle structure:
    """
    blog = get_contribution('blogs', id_blog)
    
    return blog

@blogs_routes.get(
    path="/{id_blog}/basic",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="get a blog publication",
    tags=["Blogs"]
)
def get_blog_basic(id_blog):
    """
    This path operation returns the basic description for a blog

    Parameters:

    Returns a blog with a ContributionTitleBasic structure:
    """
    blog = get_contribution_basic('blogs', id_blog)

    return blog

@blogs_routes.post(
    path="/",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a blog publication",
    tags=["Blogs"]
)
def post_blog(blog: ContributionTitleBasic = Body(...)):
    """
    This path operation create a new blog

    Parameters:
        - blog: ContributionTitleBasic

    Return the new blog in a json with a ContributionTitleBasic structure
    """
    blog = post_contribution('blogs', blog)

    return blog

@blogs_routes.put(
    path="/{id_blog}",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="update a blog publication",
    tags=["Blogs"]
)
def put_blog(id_blog, blog: ContributionTitleBasic = Body(...)):
    """
    This path operation update a blog

    Parameters:
        - id_blog: str
        - blog: ContributionTitleBasic

    Return the updated blog in a json with a ContributionTitleBasic structure
    """
    blog = put_contribution('blogs', id_blog, blog)
    
    return blog

@blogs_routes.delete(
    path="/{id_blog}",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="delete a blog publication",
    tags=["Blogs"]
)
def delete_blog(id_blog):
    """
    This path operation delete a blog

    Parameters:
        - id_blog: str
    
    Return the deleted blog in a json with a ContributionTitleBasic structure
    """
    blog = delete_contribution('blogs', id_blog)
    
    return blog
