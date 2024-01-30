from fastapi import APIRouter, Response, HTTPException, status
from app.dependencies.core import DBSessionDep
from app.services.rating_service import RatingService

router = APIRouter(
    prefix="/rating",
    responses={
        404: {"description": "Not found."}
    }
)


@router.put('/{id}')
async def update_rating(
    db: DBSessionDep,
    id: int,
    rating: int = 5,
    generate_rating: bool = False
):
    return await RatingService(db).update_rating(id, rating, generate_rating)
