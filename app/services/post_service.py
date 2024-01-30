from app.services.main import AppService
from app.schema.post import Post
from app.models.post import Post as PostModel
from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from app.services.openai_service import OpenAIService


class PostService(AppService):
    def __init__(self, db):
        self.db = db

    async def get_posts(self, query: str, page: int, size: int):
        # paging = DBUtils.paginate(page, size)
        # .offset(paging.offset)
        # .limit(paging.limit)

        if query:
            q = (
                select(PostModel)
                .where(PostModel.title == query)
                .order_by(PostModel.id.desc()))
        else:
            q = select(PostModel).order_by(PostModel.id.desc())
        # print(q)
        # return {}

        arr = []
        result = await self.db.execute(q)
        for r in result.scalars():
            arr.append({
                "id": r.id,
                "title": r.title,
                "content": r.content,
                "rating": r.rating,
                "created_at": r.created_at,
                "updated_at": r.updated_at
            })

        if query and not len(arr):
            raise HTTPException(status_code=404, detail="Post not found")

        return arr

    async def create_post(self, post: Post, generate_content: bool = False):
        if generate_content:
            client = await self.get_openai_service()
            content = await client.generate_content(post.title)
            post.content = content

        q = insert(PostModel).values(
            title=post.title,
            content=post.content
        ).returning(
            PostModel.id,
            PostModel.title,
            PostModel.content,
            PostModel.rating
        )
        result = await self.db.execute(q)
        result2 = await self.db.commit()
        print(result)
        return True

    async def get_post(self, id: int):
        q = select(PostModel).where(PostModel.id == id)
        result = await self.db.execute(q)
        r = result.scalar()
        return {
            'id': r.id,
            'title': r.title,
            'content': r.content,
            'rating': r.rating,
            'created_at': r.created_at,
            'updated_at': r.updated_at,

        }

    async def update_post(
        self,
        id: int,
        post: Post,
        generate_content: bool = False
    ):
        if generate_content:
            client = await self.get_openai_service()
            content = await client.generate_content(post.title)
            post.content = content

        q = (
            update(PostModel)
            .where(PostModel.id == id)
            .values(title=post.title, content=post.content)
        )
        result = await self.db.execute(q)
        result2 = await self.db.commit()
        print(result)
        return True

    async def delete_post(
            self,
            id: int
    ):
        q = delete(PostModel).where(PostModel.id == id)
        result = await self.db.execute(q)
        result2 = await self.db.commit()
        print(result)
        return True

    async def get_openai_service(self, key=None, model=None):
        client = OpenAIService(key, model)
        return client
