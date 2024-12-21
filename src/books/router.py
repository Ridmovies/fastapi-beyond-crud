from fastapi import APIRouter
from sqlalchemy import text

from src.database import SessionDep

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/check-db-connection")
async def check_db_connection(session: SessionDep):
    """Check if the database connection is successful"""
    result = await session.execute(text("SELECT 1"))
    return {"message": "Connection to the database successful"}
