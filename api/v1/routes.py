from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import CreateUser, RetrieveUser, Category
from db.connection import get_db
from db.models.user import create_user, get_user
from db.models.category import create_category, get_category_by_id

router = APIRouter()

@router.post("/users", response_model=CreateUser)
async def create_new_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/users/{user_id}", response_model=RetrieveUser)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user(db, user_id)

@router.post("/category", response_model=Category)
async def create_new_category(category: Category, db: AsyncSession = Depends(get_db)):
    return await create_category(db, category)

@router.get("/category/{category_id}", response_model=Category)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await get_category_by_id(db, category_id)