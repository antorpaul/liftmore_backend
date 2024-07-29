from typing import Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import *
from db.connection import get_db
from db.models.user import create_user, get_user
from db.models.category import create_category, get_category_by_id, get_all_categories
from db.models.exercise import create_exercise, get_exercise, get_all_exercises_query, get_all_exercises_for_category_id

exercise_router = APIRouter()


@exercise_router.post("/exercise", response_model=RetrieveExercise)
async def create_new_exercise(exercise: CreateUpdateExercise, db: AsyncSession = Depends(get_db)):
    return await create_exercise(db, exercise)


@exercise_router.get("/exercise/{exercise_id}", response_model=RetrieveExercise | None)
async def get_exercise_by_id(exercise_id: int, db: AsyncSession = Depends(get_db)):
    return await get_exercise(db, exercise_id)


@exercise_router.get("/exercises/all", response_model=List[RetrieveExercise] | None)
async def get_all_exercises(db: AsyncSession = Depends(get_db),
                            page: int = Query(0, description="page of results"),
                            page_size: int = Query(10, description="size of page"),
                            category_id: int = Query(-1, description="id of the category to get")):
    if category_id == -1:
        return await get_all_exercises_query(db, page, page_size)
    else:
        return await get_all_exercises_for_category_id(db, category_id, page, page_size)


@exercise_router.get("/exercise/search", response_model=Union[List[RetrieveExercise], List])
async def search_exercise_by_name(query: str = Query(..., description="Term to search exercises by name"), db: AsyncSession = Depends(get_db)):
    print(f"[search_exercise_by_name] searching for {query}")
    exercises = await get_exercise(db, query)
    if exercises is None:
        return []
    return exercises