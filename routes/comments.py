# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import Query
from fastapi import status

# Models
from models import *

comments_routes = APIRouter()


# Comments
@comments_routes.get(
    path="/",
    response_model=List[ContributionAnswer],
    status_code=status.HTTP_200_OK,
    summary="get all comments",
    tags=["Comments"]
)
def all_comments():
    """
    This path operation returns all comments

    Parameters:

    Returns a list of comments with a ContributionAnswer structure:
    """
    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())
    
    comments = list(
        map(
            lambda c: {**c, **{"user": list(
                filter(
                    lambda u: u["id_user"] == c["id_user"],
                    users
                )
            )[0]}},
            comments
        )
    )
    del users

    comments = list(
        map(
            lambda c: {
                **c,
                **{"answers": list(
                    filter(
                        lambda a: a["id_contribution"] in c["id_answers"],
                        comments
                    )
                )}
            } if c["id_answers"] else c,
            comments
        )
    )
    
    return comments

@comments_routes.get(
    path="/{id_comment}",
    response_model=ContributionAnswer,
    status_code=status.HTTP_200_OK,
    summary="get a comment",
    tags=["Comments"]
)
def get_comment(id_comment):
    """
    This path operation return the complete information for a comment

    Parameters:
        - id_comment: str
    
    Returns a comment with with a ContributionAnswer structure:
    """
    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())
    
    id_comments = list(map(lambda c: c["id_contribution"], comments))

    # id_comment must be valid
    if id_comment not in id_comments:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id comment '{id_comment}'"
        )
    del id_comments

    # get comment
    comment = list(filter(lambda c: c["id_contribution"]==id_comment, comments))[0]

    # get user for comment
    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())

    comment["user"] = list(filter(lambda u: u["id_user"] == comment["id_user"], users))[0]
    
    # get answers
    if comment["id_answers"]:
        comment["answers"] = list(
            filter(
                lambda a: a["id_contribution"] in comment["id_answers"],
                comments
            )
        )
        del comments
    
        ## get users for answers
        comment["answers"] = list(
            map(
                lambda a: {**a, **{"user": list(
                    filter(
                        lambda u: u["id_user"] == a["id_user"],
                        users
                    )
                )[0]}},
                comment["answers"]
            )
        )
    
    return comment

@comments_routes.get(
    path="/{id_comment}/basic",
    response_model=ContributionBasic,
    status_code=status.HTTP_200_OK,
    summary="get a comment",
    tags=["Comments"]
)
def get_comment_basic(id_comment):
    """
    This path operation return the basic description for a comment

    Parameters:
        - id_comment: str

    Returns a comment with with a ContributionAnswer structure:
    """
    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())
    
    id_comments = list(map(lambda c: c["id_contribution"], comments))

    # id_comment must be valid
    if id_comment not in id_comments:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id comment '{id_comment}'"
        )
    del id_comments

    # get comment
    comment = list(filter(lambda c: c["id_contribution"]==id_comment, comments))[0]

    return comment

@comments_routes.post(
    path="/",
    response_model=ContributionBasic,
    status_code=status.HTTP_201_CREATED,
    summary="create a comment",
    tags=["Comments"]
)
def post_comment(comment: ContributionBasic = Body(...)):
    """
    This path operation create a new comment

    Parameters:
        - comment: ContributionBasic

    Return the new comment in a json with a ContributionBasic structure
    """
    comment = comment.dict()
    with open('data/comments.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())

    # Parsing
    comment["id_contribution"] = str(comment["id_contribution"])
    comment["id_user"] = str(comment["id_user"])
    comment["date_publication"] = str(comment["date_publication"])
    comment['kind'] = comment['kind'].value

    # id_contribution must be unique
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    if comment["id_contribution"] in id_comments:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{comment['id_contribution']}'"
        )
    del id_comments
    
    with open('data/users.json', 'r', encoding='utf-8') as f:
        users = json.loads(f.read())

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if comment["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{comment['id_user']}'"
        )
    del id_users

    # kind must be valid
    if comment['kind'] not in ["comment", "question"]:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid comment kind '{comment['kind']}'"
        )

    # id_answers must be empty
    if 'id_answers' in comment and comment['id_answers']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id answers, must be empty"
        )

    # Save comments
    comments.append(comment)
    with open('data/comments.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(comments, ensure_ascii=False))
    
    return comment

@comments_routes.put(
    path="/{id_comment}",
    response_model=ContributionBasic,
    status_code=status.HTTP_200_OK,
    summary="update a comment",
    tags=["Comments"]
)
def put_comment(id_comment, comment: ContributionBasic = Body(...)):
    """
    This path operation update a new comment

    Parameters:
        - id_comment: str
        - comment: ContributionBasic

    Return the updated comment in a json with a ContributionBasic structure
    """
    with open('data/comments.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())
    
    # id_contribution must be valid
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    if id_comment not in id_comments:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{id_comment}'"
        )
    del id_comments

    comments = list(filter(lambda c: c["id_contribution"] != id_comment, comments))
    comment = comment.dict()
    # Parsing
    comment["id_contribution"] = str(comment["id_contribution"])
    comment["id_user"] = str(comment["id_user"])
    comment["date_publication"] = str(comment["date_publication"])
    comment['kind'] = comment['kind'].value

    # id_contribution must be unique
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    if comment["id_contribution"] in id_comments:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{comment['id_contribution']}'"
        )

    # id_answers must be valid
    for a in comment['id_answers']:
        if a not in id_comments:
            raise HTTPException(
                status_code=404,
                detail=f"HTTP_404_NOT_FOUND: Invalid id answers '{a}'"
            )
    del id_comments
    
    with open('data/users.json', 'r', encoding='utf-8') as f:
        users = json.loads(f.read())

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if comment["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{comment['id_user']}'"
        )
    del id_users

    # kind must be valid
    if comment['kind'] not in ["comment", "question"]:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid comment kind '{comment['kind']}'"
        )

    # Save comments
    comments.append(comment)
    with open('data/comments.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(comments, ensure_ascii=False))
    
    return comment

@comments_routes.delete(
    path="/{id_comment}",
    response_model=ContributionBasic,
    status_code=status.HTTP_200_OK,
    summary="delete a comment",
    tags=["Comments"]
)
def delete_comment(id_comment, kind: Optional[TypeContribution] = Query(default="comment")):
    """
    This path operation delete a comment

    Parameters:
        - id_comment: str

    Return the deleted comment in a json with a ContributionBasic structure
    """
    with open('data/comments.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())

    # id_comment must be valid
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    if id_comment not in id_comments:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id comment '{id_comment}'"
        )
    del id_comments

    comment = list(filter(lambda  c: c["id_contribution"] == id_comment, comments))[0]
    comments = list(filter(lambda  c: c["id_contribution"] != id_comment, comments))
    kind = kind.value

    # delete comment from all files
    if kind in ["tutorial", "blog", "forum"]:
        with open(f'data/{kind}s.json', 'r', encoding='utf-8') as f:
            contributions = json.loads(f.read())

        contributions = list(
            map(
                lambda c: {
                    **c,
                    **{"id_comments": [v for v in c["id_comments"] if v != id_comment]}
                } if c["id_comments"] else c,
                contributions
            )
        )

        with open(f'data/{kind}s.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(contributions, ensure_ascii=False))

    elif kind == "answers":
        comments = list(
            map(
                lambda c: {
                    **c,
                    **{"id_answers": [v for v in c["id_answers"] if v != id_comment]}
                } if "id_answers" in c and c["id_answers"] else c,
                comments
            )
        )
    
    comments = list(filter(lambda c: c["id_contribution"] != id_comment, comments))

    # Save the comment
    with open('data/comments.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(comments, ensure_ascii=False))

    return comment
