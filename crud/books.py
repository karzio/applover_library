import logging
from typing import List
import pytz

from fastapi import HTTPException
from sqlalchemy import select, case, null, delete
from sqlalchemy.exc import IntegrityError

from db import SessionLocal
from models.books import Book, BookLoan
from schemas.books import BookSchema, BookLoanCreateSchema, BookLoanUpdateSchema


class BooksCRUD:
    def __init__(self) -> None:
        self.session = SessionLocal

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        error_response = None
        if isinstance(exc_type, type(IntegrityError)):
            if "already exists" in str(exc_val):
                error_response = "Book with that serial number already exists"
            else:
                error_response = str(exc_val)
        elif exc_type is not None:
            error_response = str(exc_val)
            logging.exception(exc_tb)
        if error_response:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=error_response)
        self.session.close()
        return True

    async def create(self, book: BookSchema) -> Book:
        book = Book(serial_number=book.serial_number,
                    title=book.title,
                    author=book.author)
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)
        return book

    async def delete(self, book_id: int) -> None:
        book_loans_delete_stmt = (
            delete(BookLoan)
            .where(BookLoan.book_id == book_id)
        )
        self.session.execute(book_loans_delete_stmt)
        stmt = (
            delete(Book)
            .where(Book.serial_number == book_id)
        )
        self.session.execute(stmt)
        self.session.commit()

    async def fetch_all(self) -> List[type[Book]]:
        loaned_subquery = (
            select(BookLoan.book_id)
            .where(BookLoan.end_date == null())
            .distinct()
            .subquery()
        )

        # Get books and decide, based on BookLoan.end_date fields
        # if each book is loaned or not
        stmt = (
            select(
                Book.serial_number,
                Book.title,
                Book.author,
                case(
                    (loaned_subquery.c.book_id != null(), True),
                    else_=False
                ).label('is_loaned')
            ).outerjoin(loaned_subquery, Book.serial_number == loaned_subquery.c.book_id)
        )

        results = self.session.execute(stmt).all()
        return results


class BookLoansCRUD:
    def __init__(self) -> None:
        self.session = SessionLocal

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        error_response = None
        if isinstance(exc_type, type(IntegrityError)):
            error_response = str(exc_val)
        elif isinstance(exc_type, type(ValueError)):
            error_response = str(exc_val)

        if error_response:
            self.session.rollback()
            raise HTTPException(status_code=400, detail=error_response)
        self.session.close()
        return True

    async def get_book_loans(self, book_id: int) -> List[BookLoan]:
        book_loan_instances = self.session.query(
            BookLoan
        ).where(BookLoan.book_id == book_id).order_by(BookLoan.start_date).all()
        return book_loan_instances

    async def create_book_loan(self, book_loan: BookLoanCreateSchema) -> BookLoan:
        book_loan_instance = BookLoan(
            book_id=book_loan.book_id,
            start_date=book_loan.start_date,
            loaned_by_id=book_loan.loaned_by_id,
            end_date=None
        )
        self.session.add(book_loan_instance)
        self.session.commit()
        self.session.refresh(book_loan_instance)
        return book_loan_instance

    async def update_book_loan(self, book_loan_id: int, book_loan: BookLoanUpdateSchema) -> BookLoan:
        book_loan_instance = self.session.query(BookLoan).where(BookLoan.book_loan_id==book_loan_id).first()
        end_date = book_loan.end_date.replace(tzinfo=pytz.utc)
        start_date = book_loan_instance.start_date.replace(tzinfo=pytz.utc)
        if start_date > end_date:
            raise ValueError("End date must be greater than start date")
        book_loan_instance.end_date = end_date
        self.session.add(book_loan_instance)
        self.session.commit()
        self.session.refresh(book_loan_instance)
        return book_loan_instance
