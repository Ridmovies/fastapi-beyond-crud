from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.books.router import router as book_router
from src.config import settings
from src.dev.router import router as dev_router

from src.database import init_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield




version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix =f"/api/{version}"


app = FastAPI(
    lifespan=lifespan,
    title="Bookly",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    # contact={
    #     "name": "Ssali Jonathan",
    #     "url": "https://github.com/jod35",
    #     "email": "ssalijonathank@gmail.com",
    # },
)

app.include_router(book_router, prefix=f"{version_prefix}/books", tags=["books"])
if settings.MODE == "DEV":
    app.include_router(dev_router, prefix=f"{version_prefix}/dev", tags=["dev"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
