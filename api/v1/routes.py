from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.connection import get_db
from app.schemas.user import UserCreate, UserRead
from app.db.queries.user_queries import create_user, get_user

router = APIRouter()

@router.post("/users", response_model=UserRead)
async def create_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user(db, user_id)