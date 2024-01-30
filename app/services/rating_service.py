from app.services.main import AppService
from app.services.post_service import PostService
from app.services.openai_service import OpenAIService
from app.models.post import Post as PostModel
from app.schema.post import Post
from sqlalchemy import select, update


class RatingService(AppService):
    def __init__(self, db):
        self.db = db

    async def update_rating(
        self,
        id: int,
        rating: int,
        generate_rating: bool = False
    ):

        if generate_rating:
            post = await PostService(self.db).get_post(id)
            client = await self.get_openai_service()
            rating = await client.rate_content(post["title"], post["content"])

        q = (
            update(PostModel)
            .where(PostModel.id == id)
            .values(rating=rating)
        )

        result = await self.db.execute(q)
        result2 = await self.db.commit()
        print(result)
        return True

    async def get_openai_service(self, key=None, model=None):
        client = OpenAIService(key, model)
        return client
