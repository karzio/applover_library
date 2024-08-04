from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    user_id: int
    name: str


class CardSchema(BaseModel):
    card_id: int = Field(gt=99999, lt=1000000)
    user_id: int
