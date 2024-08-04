import logging

from fastapi import HTTPException

from db import SessionLocal
from models import User, Card
from schemas.users import UserSchema, CardSchema


class UserCRUD:
    def __init__(self) -> None:
        self.session = SessionLocal

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        error_response = None
        if exc_type is not None:
            error_response = str(exc_val)
            logging.exception(exc_tb)
        if error_response:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=error_response)
        self.session.close()
        return True

    async def create(self, user: UserSchema) -> User:
        user_instance = User(user_id=user.user_id,
                    name=user.name)
        self.session.add(user_instance)
        self.session.commit()
        self.session.refresh(user_instance)
        return user_instance

    async def create_card(self, card: CardSchema) -> Card:
        card_instance = Card(card_id=card.card_id,
                    user_id=card.user_id)
        self.session.add(card_instance)
        self.session.commit()
        self.session.refresh(card_instance)
        return card_instance
