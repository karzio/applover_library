from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    """
    Simple user model just to have something to fill out for the task.
    """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String)

    cards = relationship("Card", back_populates="user")

class Card(Base):
    __tablename__ = 'user_cards'

    card_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    book_loans = relationship("BookLoan")
    user = relationship("User")
