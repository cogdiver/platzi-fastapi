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

forums_routes = APIRouter()


# Forum
@forums_routes.get(
    path="/",
    response_model=List[ContributionTitle],
    status_code=status.HTTP_200_OK,
    summary="get all forums",
    tags=["Forums"]
)
def all_forums():
    """
    This path operation returns all forums

    Parameters:

    Returns a list of forums with a ContributionTitle structure:
    """
    forums = get_all_contributions('forums')

    return forums

@forums_routes.get(
    path="/{id_forum}",
    response_model=ContributionTitle,
    status_code=status.HTTP_200_OK,
    summary="get a forum publication",
    tags=["Forums"]
)
def get_forum(id_forum):
    """
    This path operation returns a forum

    Parameters:

    Returns a forum with a ContributionTitle structure:
    """
    forum = get_contribution('forums', id_forum)
    
    return forum

@forums_routes.get(
    path="/{id_forum}/basic",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="get a forum publication",
    tags=["Forums"]
)
def get_forum_basic(id_forum):
    """
    This path operation return the basic description for a forum

    Parameters:
        - id_forum: str
    
    Returns a forum with with a ContributionTitleBasic structure:
    """
    forum = get_contribution_basic('forums', id_forum)

    return forum

@forums_routes.post(
    path="/",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a forum publication",
    tags=["Forums"]
)
def post_forum(forum: ContributionTitleBasic = Body(...)):
    """
    This path operation create a new forum

    Parameters:
        - forum: ContributionTitleBasic

    Return the new forum in a json with a ContributionTitleBasic structure
    """
    forum = post_contribution('forums', forum)
    
    return forum

@forums_routes.put(
    path="/{id_forum}",
    response_model=ContributionTitleBasic,
    status_code=status.HTTP_200_OK,
    summary="update a forum publication",
    tags=["Forums"]
)
def put_forum(id_forum, forum: ContributionTitleBasic = Body(...)):
    """
    This path operation update a forum

    Parameters:
        - id_forum: str
        - forum: ContributionTitleBasic

    Return the updated forum in a json with a ContributionTitleBasic structure
    """
    forum = put_contribution('forums', id_forum, forum)
    
    return forum

@forums_routes.delete(
    path="/{id_forum}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="delete a forum publication",
    tags=["Forums"]
)
def delete_forum(id_forum):
    """
    This path operation delete a forum

    Parameters:
        - id_forum: str
    
    Return the deleted forum in a json with a ContributionTitleBasic structure
    """
    forum = delete_contribution('forums', id_forum)
    
    return forum
