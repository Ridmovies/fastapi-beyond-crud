from fastapi import APIRouter
from sqlmodel import select

from src.database import SessionDep
from src.hero.models import Hero

router = APIRouter()


@router.get("/", response_model=list[Hero])
async def get_all_hero(session: SessionDep):
    stmt = select(Hero)
    result = await session.scalars(stmt)
    return result.all()


@router.post("/")
async def create_hero(hero_data: Hero, session: SessionDep):
    hero = Hero(**hero_data.model_dump())
    session.add(hero)
    await session.commit()
