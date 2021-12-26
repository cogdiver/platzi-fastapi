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

tutorials_routes = APIRouter()


# Tutorial
@tutorials_routes.get(
    path="/",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all tutorials",
    tags=["Tutorials"]
)
def all_tutorials():
    """
    This path operation returns all tutorials

    Parameters:

    Returns a list of tutorials with a ContributionTitle structure:
    """
    tutorials = get_all_contributions('tutorials')

    return tutorials

@tutorials_routes.get(
    path="/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a tutorial publication",
    tags=["Tutorials"]
)
def get_tutorial(id_tutorial):
    """
    This path operation returns a tutorial

    Parameters:

    Returns a tutorial with a ContributionTitle structure:
    """
    tutorial = get_contribution('tutorials', id_tutorial)
    
    return tutorial

@tutorials_routes.get(
    path="/{id_tutorial}/basic",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="get a tutorial publication",
    tags=["Tutorials"]
)
def get_tutorial_basic(id_tutorial):
    """
    This path operation return the basic description for a tutorial

    Parameters:
        - id_tutorial: str
    
    Returns a tutorial with with a ContributionTitleBasic structure:
    """
    tutorial = get_contribution_basic('tutorials', id_tutorial)

    return tutorial

@tutorials_routes.post(
    path="/",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a tutorial publication",
    tags=["Tutorials"]
)
def post_tutorial(tutorial: ContributionTitleBasic = Body(...)):
    """
    This path operation create a new tutorial

    Parameters:
        - tutorial: ContributionTitleBasic

    Return the new tutorial in a json with a ContributionTitleBasic structure
    """
    tutorial = post_contribution('tutorials', tutorial)
    
    return tutorial

@tutorials_routes.put(
    path="/{id_tutorial}",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="update a tutorial publication",
    tags=["Tutorials"]
)
def put_tutorial(id_tutorial, tutorial: ContributionTitleBasic = Body(...)):
    """
    This path operation update a tutorial

    Parameters:
        - id_tutorial: str
        - tutorial: ContributionTitleBasic

    Return the updated tutorial in a json with a ContributionTitleBasic structure
    """
    tutorial = put_contribution('tutorials', id_tutorial, tutorial)
    
    return tutorial

@tutorials_routes.delete(
    path="/{id_tutorial}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="delete a tutorial publication",
    tags=["Tutorials"]
)
def delete_tutorial(id_tutorial):
    """
    This path operation delete a tutorial

    Parameters:
        - id_tutorial: str
    
    Return the deleted tutorial in a json with a ContributionTitleBasic structure
    """
    tutorial = delete_contribution('tutorials', id_tutorial)
    
    return tutorial
