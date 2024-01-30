# from openai import OpenAI
# import logging
# import sys
from contextlib import asynccontextmanager
# from dotenv import dotenv_values
from fastapi import FastAPI
import uvicorn
from app.config.settings import settings
from app.config.database import sessionmanager
from app.routers import (
    post,
    rating
)

# logging.basicConfig(
#     stream=sys.stdout,
#     level=(
#         logging.DEBUG
#         if settings.debug_logs
#         else logging.INFO
#     )
# )
# config = dotenv_values('.env')
# client = OpenAI(
#     api_key=config["OPENAI_API_KEY"]
# )


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    docs_url="/docs"
)


@app.get("/")
def root():
    return {
        "message": "Hello World"
    }


app.include_router(post.router)
app.include_router(rating.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True,
        workers=3
    )
