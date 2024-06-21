from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import *
from db.connection import get_db
from db.models.user import create_user, get_user
from db.models.category import create_category, get_category_by_id
from db.models.exercise import create_exercise, get_exercise_by_id

router = APIRouter()

@router.post("/users", response_model=RetrieveUser)
async def create_new_user(user: CreateUpdateUser, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)

@router.get("/users/{user_id}", response_model=RetrieveUser)
async def read_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await get_user(db, user_id)

@router.post("/category", response_model=RetrieveCategory)
async def create_new_category(category: CreateUpdateCategory, db: AsyncSession = Depends(get_db)):
    return await create_category(db, category)

@router.get("/category/{category_id}", response_model=RetrieveCategory)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await get_category_by_id(db, category_id)

@router.post("/exercise", response_model=RetrieveExercise)
async def create_new_category(exercise: CreateUpdateExercise, db: AsyncSession = Depends(get_db)):
    return await create_exercise(db, exercise)

@router.get("/exercise/{exercise_id}", response_model=RetrieveExercise)
async def get_category(exercise_id: int, db: AsyncSession = Depends(get_db)):
    return await get_exercise_by_id(db, exercise_id)