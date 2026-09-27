from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema.book import Book, BookCreate
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

books = []
with open("data.json", "r", encoding="utf-8") as file:
    books = json.load(file)

@app.get("/books")
def get_books(
    page: int = 1,
    limit: int = 5,
    search: str = ""
):
    # Validasi page dan limit
    if page < 1:
        page = 1

    if limit < 1:
        limit = 5

    # Filter search
    filtered_books = books

    if search:
        keyword = search.lower()

        filtered_books = [
            book for book in books
            if keyword in book["isbn"].lower()
            or keyword in book["judul"].lower()
            or keyword in str(book["tahun_terbit"])
        ]

    # Pagination
    total = len(filtered_books)

    start = (page - 1) * limit
    end = start + limit

    data = filtered_books[start:end]

    total_pages = (total + limit - 1) // limit

    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages
    }

@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):

    for book in books:
        if book["id"] == book_id:
            return book

    return "Buku tidak ditemukan"

@app.post("/books")
def post_books(book: BookCreate):

    for book_id in books:
        if book.isbn == book_id["isbn"]:
            return "data dengan isbn tersebut sudah ada"

    new_id = len(books) + 1

    new_book = {
        "id": new_id,
        "isbn": book.isbn,
        "judul": book.judul,
        "tahun_terbit": book.tahun_terbit
    }

    books.append(new_book)

    return new_book


@app.put("/books/{book_id}")
def edit_book(book_id: int, book: BookCreate):

    for index, old_book in enumerate(books):
        if old_book["id"] == book_id:

            books[index] = {
                "id": book_id,
                "isbn": book.isbn,
                "judul": book.judul,
                "tahun_terbit": book.tahun_terbit
            }

            return books[index]

    return "Buku tidak ditemukan"


@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    for index, book in enumerate(books):
        if book["id"] == book_id:

            deleted_book = books.pop(index)

            return deleted_book

    return "Buku tidak ditemukan"