from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List

app = FastAPI()

# ✅ CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define the Book model
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str

# ✅ Create SQLite engine
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Create tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}

# ✅ Get all books
@app.get("/books", response_model=List[Book])
def get_books():
    with Session(engine) as session:
        result = session.exec(select(Book))
        return result.all()

# ✅ Add a new book
@app.post("/books", response_model=Book)
def add_book(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book
