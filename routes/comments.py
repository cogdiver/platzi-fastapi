# Python
from typing import Optional
from typing import List

# FastAPI
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Body
from fastapi import Query
from fastapi import status

# Models
from schemas.contributions import ContributionAnswer
from schemas.contributions import ContributionBasic
from schemas.enums import TypeContribution

# Utils
from utils.functions import get_filename_json
from utils.functions import write_filename_json
from utils.functions import validate_valid_key
from utils.functions import validate_unique_key

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
    comments = get_filename_json('data/comments.json')
    users = get_filename_json('data/users.json')
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
    comments = get_filename_json('data/comments.json')

    # id_comment must be valid
    validate_valid_key(
        id_comment, comments, 'id_contribution',
        f"Invalid id comment '{id_comment}'"
    )
    
    # get comment
    comment = list(filter(lambda c: c["id_contribution"]==id_comment, comments))[0]

    # get user for comment
    users = get_filename_json('data/users.json')
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
    comments = get_filename_json('data/comments.json')

    # id_comment must be valid
    validate_valid_key(
        id_comment, comments, 'id_contribution',
        f"Invalid id comment '{id_comment}'"
    )

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
    comments = get_filename_json('data/comments.json')

    # Parsing
    comment["id_contribution"] = str(comment["id_contribution"])
    comment["id_user"] = str(comment["id_user"])
    comment["date_publication"] = str(comment["date_publication"])
    comment['kind'] = comment['kind'].value

    # id_contribution must be unique
    validate_unique_key(
        comment["id_contribution"], comments, 'id_contribution',
        f"Invalid id contribution '{comment['id_contribution']}'"
    )
    
    # id_user must be valid
    users = get_filename_json('data/users.json')
    validate_valid_key(
        comment["id_user"], users, 'id_user',
        f"Invalid id user '{comment['id_user']}'"
    )
    del users

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
    write_filename_json('data/comments.json', comments)
    
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
    comments = get_filename_json('data/comments.json')
    
    # id_contribution must be valid
    validate_valid_key(
        id_comment, comments , 'id_contribution',
        f"Invalid id contribution '{id_comment}'"
    )

    comments = list(filter(lambda c: c["id_contribution"] != id_comment, comments))
    comment = comment.dict()
    # Parsing
    comment["id_contribution"] = str(comment["id_contribution"])
    comment["id_user"] = str(comment["id_user"])
    comment["date_publication"] = str(comment["date_publication"])
    comment['kind'] = comment['kind'].value

    # id_contribution must be unique
    validate_unique_key(
        comment["id_contribution"], comments, 'id_contribution',
        f"Invalid id contribution '{comment['id_contribution']}'"
    )

    # id_answers must be valid
    for a in comment['id_answers']:
        validate_valid_key(
            a, comments, 'id_contribution',
            f"Invalid id answers '{a}'"
        )

    # id_user must be valid
    users = get_filename_json('data/users.json')
    validate_valid_key(
        comment["id_user"], users, 'id_user',
        f"Invalid id user '{comment['id_user']}'"
    )
    del users

    # kind must be valid
    if comment['kind'] not in ["comment", "question"]:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid comment kind '{comment['kind']}'"
        )

    # Save comments
    comments.append(comment)
    write_filename_json('data/comments.json', comments)
    
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
    comments = get_filename_json('data/comments.json')

    # id_comment must be valid
    validate_valid_key(
        id_comment, comments, 'id_contribution',
        f"Invalid id comment '{id_comment}'"
    )

    comment = list(filter(lambda  c: c["id_contribution"] == id_comment, comments))[0]
    comments = list(filter(lambda  c: c["id_contribution"] != id_comment, comments))
    kind = kind.value

    # delete comment from all files
    if kind in ["tutorial", "blog", "forum"]:
        contributions = get_filename_json(f'data/{kind}s.json')

        contributions = list(
            map(
                lambda c: {
                    **c,
                    **{"id_comments": [v for v in c["id_comments"] if v != id_comment]}
                } if c["id_comments"] else c,
                contributions
            )
        )

        write_filename_json(f'data/{kind}s.json', contributions)

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
    write_filename_json('data/comments.json', comments)

    return comment
