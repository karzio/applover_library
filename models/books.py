from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, exists
from sqlalchemy.orm import mapped_column, relationship, validates

from db import SessionLocal
from models.base import Base


class Book(Base):
    __tablename__ = 'books'

    serial_number = Column(Integer, primary_key=True, index=True, autoincrement=False)
    title = Column(String)
    author = Column(String)

    book_loans = relationship("BookLoan", back_populates="book")

    @validates("serial_number")
    def validate_serial_number(self, key, value):
        if 100000 > value or value > 1000000:
            raise ValueError("Serial number must have six digits")
        return value


class BookLoan(Base):
    __tablename__ = 'book_loans'

    book_loan_id = Column(Integer, primary_key=True, index=True)
    book_id = mapped_column(ForeignKey("books.serial_number"))
    start_date = Column(DateTime, default=datetime.now)
    end_date = Column(DateTime, nullable=True, default=None)
    loaned_by_id = mapped_column(ForeignKey("user_cards.card_id"))

    book = relationship("Book", back_populates="book_loans")
    loaned_by = relationship("Card", back_populates="book_loans")

    @validates("loaned_by_id")
    def validate_loaned_by_id(self, key, value):
        from models import Card
        session = SessionLocal
        user_card_exists = session.scalar(
            exists()
            .where(Card.card_id == value)
            .select()
        )
        if not user_card_exists:
            raise ValueError(f"User Card with id {value} does not exist")
        return value

    @validates("book_id")
    def validate_book_id(self, key, value):
        session = SessionLocal
        book_exists = session.scalar(
            exists()
            .where(Book.serial_number == value)
            .select()
        )
        if not book_exists:
            raise ValueError(f"Book with serial number {value} does not exist")
        return value
