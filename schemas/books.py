from datetime import datetime
from pydantic import BaseModel, Field


class BookSchema(BaseModel):
    serial_number: int = Field(gt=99999, lt=1000000)
    title: str
    author: str


class BookListSchema(BookSchema):
    is_loaned: bool


class BookLoanCreateSchema(BaseModel):
    book_id: int
    start_date: datetime
    loaned_by_id: int


class BookLoanUpdateSchema(BaseModel):
    end_date: datetime


class BookLoanSchema(BookLoanUpdateSchema, BookLoanCreateSchema):
    ...