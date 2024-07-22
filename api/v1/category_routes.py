from typing import Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import *
from db.connection import get_db
from db.models.user import create_user, get_user
from db.models.category import create_category, get_category_by_id, get_all_categories
from db.models.exercise import create_exercise, get_exercise

category_router = APIRouter()


@category_router.post("/category", response_model=RetrieveCategory)
async def create_new_category(category: CreateUpdateCategory, db: AsyncSession = Depends(get_db)):
    return await create_category(db, category)


@category_router.get("/category/{category_id}", response_model=RetrieveCategory | Dict)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    category = await get_category_by_id(db, category_id)
    if category is None:
        return {}
    return category


@category_router.get("/categories/all", response_model=List[RetrieveCategory] | List)
async def get_categories(db: AsyncSession = Depends(get_db)):
    categories = await get_all_categories(db)
    if categories is None:
        return []
    return categories