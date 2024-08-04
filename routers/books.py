from typing import List

from fastapi import APIRouter

from crud.books import BooksCRUD, BookLoansCRUD
from schemas.books import (
    BookSchema,
    BookLoanCreateSchema,
    BookLoanUpdateSchema,
    BookListSchema,
    BookLoanSchema
)

books_router = APIRouter()


@books_router.post("/", response_model=BookSchema)
async def create_book(book: BookSchema):
    async with BooksCRUD() as crud:
        book_instance = await crud.create(book)
        return book_instance


@books_router.get("/", response_model=List[BookListSchema])
async def get_books():
    async with BooksCRUD() as crud:
        return await crud.fetch_all()


@books_router.delete("/{serial_number}")
async def delete_book(serial_number: int):
    async with BooksCRUD() as crud:
        return await crud.delete(serial_number)


@books_router.post("/loan/", response_model=BookLoanCreateSchema)
async def create_loan_book(book_loan: BookLoanCreateSchema):
    async with BookLoansCRUD() as crud:
        book_loan_instance = await crud.create_book_loan(book_loan)
        return book_loan_instance


@books_router.patch("/loan/{book_loan_id}",
                    response_model=BookLoanSchema,
                    description="Add end date to the book loan object to unmark the book as loaned.")
async def update_loan_book(book_loan_id: int, book_loan: BookLoanUpdateSchema):
    async with BookLoansCRUD() as crud:
        book_loan_instance = await crud.update_book_loan(book_loan_id, book_loan)
        return book_loan_instance


@books_router.get("/{serial_number}/loan")
async def get_book_loan(serial_number: int):
    async with BookLoansCRUD() as crud:
        return await crud.get_book_loans(serial_number)
