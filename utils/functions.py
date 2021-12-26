# Python
import json

# FastAPI
from fastapi import HTTPException


def get_filename_json(path):
    """
    get the data from a file in a json format
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.loads(f.read())


def write_filename_json(path, content):
    """
    write a file in a json format
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False))


def validate_unique_key(value, values_dict, key, err):
    """
    valide if a value in a key is unique
    """
    keys = list(map(lambda v: v[key], values_dict))
    if value in keys:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: {err}'"
        )


def validate_valid_key(value, values_dict, key, err):
    """
    valide if a value in a key is valid
    """
    keys = list(map(lambda v: v[key], values_dict))
    if value not in keys:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: {err}"
        )


# Contributions
def get_all_contributions(kind):
    """
    get all contributions for a kind in [blogs, forums, tutorials]
    """
    contributions = get_filename_json(f'data/{kind}.json')
    comments = get_filename_json('data/comments.json')
    users = get_filename_json('data/users.json')

    # get comments and user for each blog
    contributions = list(
        map(
            lambda ct: {
                **ct,
                **[{"comments": list(
                    filter(
                        lambda c: c["id_contribution"] in ct["id_comments"],
                        comments
                    )
                )} if ct["id_comments"] else {"comments": []}][0],
                **{"user": list(
                    filter(
                        lambda u: u["id_user"] == ct["id_user"],
                        users
                    )
                )[0]}
            },
            contributions
        )
    )

    # get users and answers for all contributions
    for ct in contributions:
        for c in ct["comments"]:
            # get user for each contribution's comment
            c["user"] = list(filter(lambda u: u["id_user"] == c["id_user"], users))[0]
    
            # get answers for each contribution's comment
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
    
    return contributions

def get_contribution():
    """
    get a contributions for a kind in [blog, forum, tutorial]
    """
    pass

def get_contribution_basic():
    """
    get all contributions for a kind in [blogs, forums, tutorials]
    """
    pass

def post_contribution():
    """
    get all contributions for a kind in [blogs, forums, tutorials]
    """
    pass

def put_contribution():
    """
    get all contributions for a kind in [blogs, forums, tutorials]
    """
    pass

def delete_contribution():
    """
    get all contributions for a kind in [blogs, forums, tutorials]
    """
    pass