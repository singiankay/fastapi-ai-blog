from fastapi import APIRouter, Response, HTTPException, status
from app.schema.post import Post
from app.services.post_service import PostService
from typing import Union
from app.dependencies.core import DBSessionDep

router = APIRouter(
    prefix="/posts",
    responses={
        404: {"description": "Not found."}
    }
)


@router.get('/')
async def get_posts(
        db: DBSessionDep,
        query: Union[str, None] = None,
        page: int = 1,
        size: int = 10
):
    result = await PostService(db).get_posts(query, page, size)
    return result


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_posts(
    db: DBSessionDep,
    post: Post,
    generate_content: bool = False
):
    result = await PostService(db).create_post(post, generate_content)
    return result


@router.get("/{id}")
async def get_post_by_id(db: DBSessionDep, id: int):
    if not id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post {id} not found.')
    return await PostService(db).get_post(id)


@router.put("/{id}")
async def update_post_by_id(
    db: DBSessionDep,
    post: Post,
    id: int,
    generate_content: bool = False
):
    return await PostService(db).update_post(id, post, generate_content)


@router.delete('/{id}')
async def delete_post_by_id(
    db: DBSessionDep,
    id: int
):
    return await PostService(db).delete_post(id)
