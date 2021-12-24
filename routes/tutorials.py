# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

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
    with open('data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())

    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())

    # get comments and user for each blog
    tutorials = list(
        map(
            lambda t: {
                **t,
                **[{"comments": list(
                    filter(
                        lambda c: c["id_contribution"] in t["id_comments"],
                        comments
                    )
                )} if t["id_comments"] else {"comments": []}][0],
                **{"user": list(
                    filter(
                        lambda u: u["id_user"] == t["id_user"],
                        users
                    )
                )[0]}
            },
            tutorials
        )
    )

    # get users and answers for all tutorials
    for t in tutorials:
        for c in t["comments"]:
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
    with open('data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())
    
    # id_tutorial must be valid
    id_tutorials = list(map(lambda t: t["id_contribution"], tutorials))
    if id_tutorial not in id_tutorials:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id tutorial '{id_tutorial}'"
        )
    del id_tutorials

    # get tutorial
    tutorial = list(filter(lambda t: t["id_contribution"] == id_tutorial, tutorials))[0]
    del tutorials

    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())

    # get comments
    tutorial["comments"] = list(
        filter(
            lambda c: c["id_contribution"] in tutorial["id_comments"],
            comments
        )
    ) if tutorial["id_comments"] else []

    # get user
    tutorial["user"] = list(filter(lambda u: u["id_user"] == tutorial["id_user"], users))[0]


    # get answers and users
    for c in tutorial["comments"]:
        # get user for each tutorial's comment
        c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]

        # get answers for each tutorial's comment
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
    with open('data/tutorials.json', 'r') as f:
        tutorials = json.loads(f.read())
    
    id_tutorials = list(map(lambda c: c["id_contribution"], tutorials))

    # id_tutorial must be valid
    if id_tutorial not in id_tutorials:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id tutorial '{id_tutorial}'"
        )
    del id_tutorials

    # get tutorial
    tutorial = list(filter(lambda c: c["id_contribution"]==id_tutorial, tutorials))[0]
    del tutorials

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
    tutorial = tutorial.dict()
    with open('data/tutorials.json', 'r', encoding='utf-8') as f:
        tutorials = json.loads(f.read())

    # Parsing
    tutorial["id_contribution"] = str(tutorial["id_contribution"])
    tutorial["id_user"] = str(tutorial["id_user"])
    tutorial["date_publication"] = str(tutorial["date_publication"])
    tutorial['kind'] = tutorial['kind'].value

    # id_contribution must be unique
    id_tutorials = list(map(lambda t: t['id_contribution'], tutorials))
    if tutorial["id_contribution"] in id_tutorials:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{tutorial['id_contribution']}'"
        )
    del id_tutorials
    
    with open('data/users.json', 'r', encoding='utf-8') as f:
        users = json.loads(f.read())

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if tutorial["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{tutorial['id_user']}'"
        )
    del id_users

    # kind must be valid
    if tutorial['kind'] != "tutorial":
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid tutorial kind '{tutorial['kind']}'"
        )

    # id_answers must be empty
    if 'id_comments' in tutorial and tutorial['id_comments']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id comments, must be empty"
        )

    # Save tutorials
    tutorials.append(tutorial)
    with open('data/tutorials.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tutorials, ensure_ascii=False))
    
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
    with open('data/tutorials.json', 'r', encoding='utf-8') as f:
        tutorials = json.loads(f.read())
    
    # id_contribution must be valid
    id_tutorials = list(map(lambda c: c['id_contribution'], tutorials))
    if id_tutorial not in id_tutorials:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{id_tutorial}'"
        )
    del id_tutorials

    tutorials = list(filter(lambda c: c["id_contribution"] != id_tutorial, tutorials))
    tutorial = tutorial.dict()
    # Parsing
    tutorial["id_contribution"] = str(tutorial["id_contribution"])
    tutorial["id_user"] = str(tutorial["id_user"])
    tutorial["date_publication"] = str(tutorial["date_publication"])
    tutorial['kind'] = tutorial['kind'].value

    # id_contribution must be unique
    id_tutorials = list(map(lambda c: c['id_contribution'], tutorials))
    if tutorial["id_contribution"] in id_tutorials:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{tutorial['id_contribution']}'"
        )
    del id_tutorials

    with open('data/comments.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())
    
    # id_comments must be valid
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    del comments
    for c in tutorial['id_comments']:
        if c not in id_comments:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id answers '{c}'"
            )
    del id_comments
    
    with open('data/users.json', 'r', encoding='utf-8') as f:
        users = json.loads(f.read())

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if tutorial["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{tutorial['id_user']}'"
        )
    del id_users

    # kind must be valid
    if tutorial['kind'] != "tutorial":
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid tutorial kind '{tutorial['kind']}'"
        )

    # Save tutorials
    tutorials.append(tutorial)
    with open('data/tutorials.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tutorials, ensure_ascii=False))
    
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
    with open('data/tutorials.json', 'r', encoding='utf-8') as f:
        tutorials = json.loads(f.read())

    # id_tutorial must be valid
    id_tutorials = list(map(lambda c: c['id_tutorial'], tutorials))
    if id_tutorial not in id_tutorials:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id tutorial '{id_tutorial}'"
        )
    del id_tutorials

    # Save the tutorial
    tutorial = list(filter(lambda  c: c["id_tutorial"] == id_tutorial, tutorials))[0]
    tutorials = list(filter(lambda  c: c["id_tutorial"] != id_tutorial, tutorials))
    with open('data/tutorials.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tutorials, ensure_ascii=False))
    
    return tutorial
