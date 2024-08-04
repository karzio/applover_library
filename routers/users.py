from fastapi import APIRouter

from crud.users import UserCRUD
from schemas.users import UserSchema, CardSchema

users_router = APIRouter()


@users_router.post("/")
async def create_user(user: UserSchema):
    async with UserCRUD() as crud:
        return await crud.create(user)


@users_router.post("/card")
async def create_card(card: CardSchema):
    async with UserCRUD() as crud:
        return await crud.create_card(card)
