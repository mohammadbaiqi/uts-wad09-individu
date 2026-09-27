from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int
    isbn: str = Field(min_length=13, max_length=13)
    judul: str
    tahun_terbit: int = Field(ge=1900, le=2026)


class BookCreate(BaseModel):
    isbn: str = Field(min_length=13, max_length=13)
    judul: str
    tahun_terbit: int = Field(ge=1900, le=2026)