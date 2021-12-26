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


def get_contribution(kind, id):
    """
    get a contribution for a kind in [blogs, forums, tutorials]
    """
    contributions = get_filename_json(f'data/{kind}.json')
    
    # id must be valid
    validate_valid_key(
        id, contributions, 'id_contribution'
        f"Invalid id {kind[:-1]} '{id}'"
    )

    # get contribution
    contribution = list(filter(lambda c: c["id_contribution"] == id, contributions))[0]
    del contributions
    comments = get_filename_json('data/comments.json')
    users = get_filename_json('data/users.json')

    # get comments
    contribution["comments"] = list(
        filter(
            lambda c: c["id_contribution"] in contribution["id_comments"],
            comments
        )
    ) if contribution["id_comments"] else []

    # get user
    contribution["user"] = list(filter(lambda u: u["id_user"] == contribution["id_user"], users))[0]

    # get answers and users
    for c in contribution["comments"]:
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
    
    return contribution


def get_contribution_basic(kind, id):
    """
    get a basic contribution for a kind in [blogs, forums, tutorials]
    """
    contributions = get_filename_json(f'data/{kind}.json')
    
    # id must be valid
    validate_valid_key(
        id, contributions, 'id_contribution',
        f"Invalid id {kind[:-1]} '{id}'"
    )

    # get contribution
    contribution = list(filter(lambda c: c["id_contribution"]==id, contributions))[0]

    return contribution


def post_contribution(kind, contribution):
    """
    post a new contribution for a kind in [blogs, forums, tutorials]
    """
    contribution = contribution.dict()
    contributions = get_filename_json(f'data/{kind}.json')

    # Parsing
    contribution["id_contribution"] = str(contribution["id_contribution"])
    contribution["id_user"] = str(contribution["id_user"])
    contribution["date_publication"] = str(contribution["date_publication"])
    contribution['kind'] = contribution['kind'].value

    # id_contribution must be unique
    validate_unique_key(
        contribution["id_contribution"], contributions, 'id_contribution',
        f"Invalid id contribution '{contribution['id_contribution']}'"
    )
    
    # id_user must be valid
    users = get_filename_json('data/users.json')
    validate_valid_key(
        contribution["id_user"], users, 'id_user',
        f"Invalid id user '{contribution['id_user']}'"
    )
    del users

    # kind must be valid
    if contribution['kind'] != kind[:-1]:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid {kind[:-1]} kind '{contribution['kind']}'"
        )

    # id_answers must be empty
    if 'id_comments' in contribution and contribution['id_comments']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id comments, must be empty"
        )

    # Save contributions
    contributions.append(contribution)
    write_filename_json(f'data/{kind}.json', contributions)
    
    return contribution


def put_contribution(kind, id, contribution):
    """
    put a contribution for a kind in [blogs, forums, tutorials]
    """
    contributions = get_filename_json(f'data/{kind}.json')
    
    # id_contribution must be valid
    validate_valid_key(
        id, contributions, 'id_contribution',
        f"Invalid id contribution '{id}'"
    )

    contributions = list(filter(lambda c: c["id_contribution"] != id, contributions))
    contribution = contribution.dict()
    # Parsing
    contribution["id_contribution"] = str(contribution["id_contribution"])
    contribution["id_user"] = str(contribution["id_user"])
    contribution["date_publication"] = str(contribution["date_publication"])
    contribution['kind'] = contribution['kind'].value

    # id_contribution must be unique
    validate_unique_key(
        contribution["id_contribution"], contributions, 'id_contribution',
        f"Invalid id contribution '{contribution['id_contribution']}'"
    )

    comments = get_filename_json('data/comments.json')
    
    # id_comments must be valid
    for c in contribution['id_comments']:
        validate_valid_key(
            c, comments, 'id_contribution',
            f"Invalid id answers '{c}'"
        )
    del comments
    
    users = get_filename_json('data/users.json')

    # id_user must be valid
    validate_valid_key(
        contribution["id_user"], users, 'id_user',
        f"Invalid id user '{contribution['id_user']}'"
    )
    del users

    # kind must be valid
    if contribution['kind'] != kind[:-1]:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid {kind[:-1]} kind '{contribution['kind']}'"
        )

    # Save contributions
    contributions.append(contribution)
    write_filename_json(f'data/{kind}.json', contributions)

    return contribution


def delete_contribution(kind, id):
    """
    delete a contribution for a kind in [blogs, forums, tutorials]
    """
    contributions = get_filename_json(f'data/{kind}.json')

    # id_blog must be valid
    validate_valid_key(
        id, contributions, f'id_{kind[:-1]}'
        f"Invalid id {kind[:-1]} '{id}'"
    )

    # Save the blog
    contribution = list(filter(lambda  c: c[f'id_{kind[:-1]}'] == id, contributions))[0]
    contributions = list(filter(lambda  c: c[f'id_{kind[:-1]}'] != id, contributions))
    write_filename_json(f'data/{kind}.json', contributions)
    
    return contribution
