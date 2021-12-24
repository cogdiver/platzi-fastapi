# Python
from typing import List
import json

# FastAPI
from fastapi import APIRouter
from fastapi import Body
from fastapi import status

# Models
from models import *

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
    with open('data/blogs.json', 'r') as f:
        blogs = json.loads(f.read())

    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())

    # get comments and user for each blog
    blogs = list(
        map(
            lambda b: {
                **b,
                **[{"comments": list(
                    filter(
                        lambda c: c["id_contribution"] in b["id_comments"],
                        comments
                    )
                )} if b["id_comments"] else {"comments": []}][0],
                **{"user": list(
                    filter(
                        lambda u: u["id_user"] == b["id_user"],
                        users
                    )
                )[0]}
            },
            blogs
        )
    )

    # get users and answers for all blogs
    for b in blogs:
        for c in b["comments"]:
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
    with open('data/blogs.json', 'r') as f:
        blogs = json.loads(f.read())
    
    # id_blog must be valid
    id_blogs = list(map(lambda b: b["id_contribution"], blogs))
    if id_blog not in id_blogs:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id blog '{id_blog}'"
        )
    del id_blogs

    # get blog
    blog = list(filter(lambda b: b["id_contribution"] == id_blog, blogs))[0]
    del blogs

    with open('data/comments.json', 'r') as f:
        comments = json.loads(f.read())

    with open('data/users.json', 'r') as f:
        users = json.loads(f.read())

    # get comments
    blog["comments"] = list(
        filter(
            lambda c: c["id_contribution"] in blog["id_comments"],
            comments
        )
    ) if blog["id_comments"] else []

    # get user
    blog["user"] = list(filter(lambda u: u["id_user"] == blog["id_user"], users))[0]


    # get answers and users
    for c in blog["comments"]:
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
    with open('data/blogs.json', 'r') as f:
        blogs = json.loads(f.read())
    
    id_blogs = list(map(lambda c: c["id_contribution"], blogs))

    # id_blog must be valid
    if id_blog not in id_blogs:
        raise HTTPException(
            status_code = 404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id blog '{id_blog}'"
        )
    del id_blogs

    # get blog
    blog = list(filter(lambda c: c["id_contribution"]==id_blog, blogs))[0]

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
    blog = blog.dict()
    with open('data/blogs.json', 'r', encoding='utf-8') as f:
        blogs = json.loads(f.read())

    # Parsing
    blog["id_contribution"] = str(blog["id_contribution"])
    blog["id_user"] = str(blog["id_user"])
    blog["date_publication"] = str(blog["date_publication"])
    blog['kind'] = blog['kind'].value

    # id_contribution must be unique
    id_blogs = list(map(lambda b: b['id_contribution'], blogs))
    if blog["id_contribution"] in id_blogs:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{blog['id_contribution']}'"
        )
    del id_blogs
    
    with open('data/users.json', 'r', encoding='utf-8') as f:
        users = json.loads(f.read())

    # id_user must be valid
    id_users = list(map(lambda u: u['id_user'], users))
    del users
    if blog["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{blog['id_user']}'"
        )
    del id_users

    # kind must be valid
    if blog['kind'] != "blog":
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid blog kind '{blog['kind']}'"
        )

    # id_answers must be empty
    if 'id_comments' in blog and blog['id_comments']:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id comments, must be empty"
        )

    # Save blogs
    blogs.append(blog)
    with open('data/blogs.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(blogs, ensure_ascii=False))
    
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
    with open('data/blogs.json', 'r', encoding='utf-8') as f:
        blogs = json.loads(f.read())
    
    # id_contribution must be valid
    id_blogs = list(map(lambda c: c['id_contribution'], blogs))
    if id_blog not in id_blogs:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{id_blog}'"
        )
    del id_blogs

    blogs = list(filter(lambda c: c["id_contribution"] != id_blog, blogs))
    blog = blog.dict()
    # Parsing
    blog["id_contribution"] = str(blog["id_contribution"])
    blog["id_user"] = str(blog["id_user"])
    blog["date_publication"] = str(blog["date_publication"])
    blog['kind'] = blog['kind'].value

    # id_contribution must be unique
    id_blogs = list(map(lambda c: c['id_contribution'], blogs))
    if blog["id_contribution"] in id_blogs:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id contribution '{blog['id_contribution']}'"
        )
    del id_blogs

    with open('data/comments.json', 'r', encoding='utf-8') as f:
        comments = json.loads(f.read())
    
    # id_comments must be valid
    id_comments = list(map(lambda c: c['id_contribution'], comments))
    del comments
    for c in blog['id_comments']:
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
    if blog["id_user"] not in id_users:
        raise HTTPException(
            status_code=404,
            detail=f"HTTP_404_NOT_FOUND: Invalid id user '{blog['id_user']}'"
        )
    del id_users

    # kind must be valid
    if blog['kind'] != "blog":
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid blog kind '{blog['kind']}'"
        )

    # Save blogs
    blogs.append(blog)
    with open('data/blogs.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(blogs, ensure_ascii=False))
    
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
    with open('data/blogs.json', 'r', encoding='utf-8') as f:
        blogs = json.loads(f.read())

    # id_blog must be valid
    id_blogs = list(map(lambda c: c['id_blog'], blogs))
    if id_blog not in id_blogs:
        raise HTTPException(
            status_code=406,
            detail=f"HTTP_406_NOT_ACCEPTABLE: Invalid id blog '{id_blog}'"
        )
    del id_blogs

    # Save the blog
    blog = list(filter(lambda  c: c["id_blog"] == id_blog, blogs))[0]
    blogs = list(filter(lambda  c: c["id_blog"] != id_blog, blogs))
    with open('data/blogs.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(blogs, ensure_ascii=False))
    
    return blog
