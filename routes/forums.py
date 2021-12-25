# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

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
    forums = get_filename_json('data/forums.json')

    comments = get_filename_json('data/comments.json')

    users = get_filename_json('data/users.json')

    # get comments and user for each blog
    forums = list(
        map(
            lambda f: {
                **f,
                **[{"comments": list(
                    filter(
                        lambda c: c["id_contribution"] in f["id_comments"],
                        comments
                    )
                )} if f["id_comments"] else {"comments": []}][0],
                **{"user": list(
                    filter(
                        lambda u: u["id_user"] == f["id_user"],
                        users
                    )
                )[0]}
            },
            forums
        )
    )

    # get users and answers for all forums
    for f in forums:
        for c in f["comments"]:
            # get user for each blog's comment
            c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]
    
            # get answers for each blog's comment
            if "id_answers" in c and c["id_answers"]:
                c["answers"] = list(
                    filter(
                        lambda a: a["id_contribution"] in c["id_answers"],
                        comments
                    )
                )
            
                ## get users for answers
                c["answers"] = list(
                    map(
                        lambda a: {**a, **{"user": list(
                            filter(
                                lambda u: u["id_user"] == a["id_user"],
                                users
                            )
                        )[0]}},
                        c["answers"]
                    )
                )
    
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
    forums = get_filename_json('data/forums.json')
    
    # id_forum must be valid
    id_forums = list(map(lambda f: f["id_contribution"], forums))
    if id_forum not in id_forums:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id forum '{id_forum}'"
        )
    del id_forums

    # get forum
    forum = list(filter(lambda f: f["id_contribution"] == id_forum, forums))[0]
    del forums

    comments = get_filename_json('data/comments.json')

    users = get_filename_json('data/users.json')

    # get comments
    forum["comments"] = list(
        filter(
            lambda c: c["id_contribution"] in forum["id_comments"],
            comments
        )
    ) if forum["id_comments"] else []

    # get user
    forum["user"] = list(filter(lambda u: u["id_user"] == forum["id_user"], users))[0]


    # get answers and users
    for c in forum["comments"]:
        # get user for each forum's comment
        c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]

        # get answers for each forum's comment
        if "id_answers" in c and c["id_answers"]:
            c["answers"] = list(
                filter(
                    lambda a: a["id_contribution"] in c["id_answers"],
                    comments
                )
            )
        
            ## get users for answers
            c["answers"] = list(
                map(
                    lambda a: {**a, **{"user": list(
                        filter(
                            lambda u: u["id_user"] == a["id_user"],
                            users
                        )
                    )[0]}},
                    c["answers"]
                )
            )
    
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
    forums = get_filename_json('data/forums.json')
    
    id_forums = list(map(lambda c: c["id_contribution"], forums))

    # id_forum must be valid
    if id_forum not in id_forums:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id forum '{id_forum}'"
        )
    del id_forums

    # get forum
    forum = list(filter(lambda c: c["id_contribution"]==id_forum, forums))[0]

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
    forum = forum.dict()
    forums = get_filename_json('data/forums.json')

    # Parsing
    forum["id_contribution"] = str(forum["id_contribution"])
    forum["id_user"] = str(forum["id_user"])
    forum["date_publication"] = str(forum["date_publication"])
    forum['kind'] = forum['kind'].value

    # id_contribution must be unique
    id_forums = list(map(lambda f: f['id_contribution'], forums))
    if forum["id_contribution"] in id_forums:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{forum['id_contribution']}'"
        )
    del id_forums
    
    users = get_filename_json('data/users.json')

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if forum["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{forum['id_user']}'"
        )
    del id_users

    # kind must be valid
    if forum['kind'] != "forum":
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid forum kind '{forum['kind']}'"
        )

    # id_answers must be empty
    if 'id_comments' in forum and forum['id_comments']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id comments, must be empty"
        )

    # Save forums
    forums.append(forum)
    write_filename_json('data/forums.json', forums)
    
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
    forums = get_filename_json('data/forums.json')
    
    # id_contribution must be valid
    id_forums = list(map(lambda c: c['id_contribution'], forums))
    if id_forum not in id_forums:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{id_forum}'"
        )
    del id_forums

    forums = list(filter(lambda c: c["id_contribution"] != id_forum, forums))
    forum = forum.dict()
    # Parsing
    forum["id_contribution"] = str(forum["id_contribution"])
    forum["id_user"] = str(forum["id_user"])
    forum["date_publication"] = str(forum["date_publication"])
    forum['kind'] = forum['kind'].value

    # id_contribution must be unique
    id_forums = list(map(lambda c: c['id_contribution'], forums))
    if forum["id_contribution"] in id_forums:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{forum['id_contribution']}'"
        )
    del id_forums

    comments = get_filename_json('data/comments.json')
    
    # id_comments must be valid
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    del comments
    for c in forum['id_comments']:
        if c not in id_comments:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id answers '{c}'"
            )
    del id_comments
    
    users = get_filename_json('data/users.json')

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if forum["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{forum['id_user']}'"
        )
    del id_users

    # kind must be valid
    if forum['kind'] != "forum":
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid forum kind '{forum['kind']}'"
        )

    # Save forums
    forums.append(forum)
    write_filename_json('data/forums.json', forums)
    
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
    forums = get_filename_json('data/forums.json')

    # id_forum must be valid
    id_forums = list(map(lambda c: c['id_forum'], forums))
    if id_forum not in id_forums:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id forum '{id_forum}'"
        )
    del id_forums

    # Save the forum
    forum = list(filter(lambda  c: c["id_forum"] == id_forum, forums))[0]
    forums = list(filter(lambda  c: c["id_forum"] != id_forum, forums))
    write_filename_json('data/forums.json', forums)
    
    return forum
