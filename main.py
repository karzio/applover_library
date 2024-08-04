import logging

from fastapi import FastAPI

from db import engine
from models import base
from routers import books, users


def create_app() -> FastAPI:
    base.Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.include_router(books.books_router, prefix="/books", tags=["books"])
    app.include_router(users.users_router, prefix="/users", tags=["users"])
    return app


app = create_app()

logger = logging.getLogger(__name__)
