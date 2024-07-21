from typing import Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import *
from db.connection import get_db
from db.models.user import create_user, get_user, delete_user_from_db


user_router = APIRouter()


@user_router.post("/users", response_model=RetrieveUser)
async def create_new_user(user: CreateUpdateUser, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@user_router.get("/users/{user_id}", response_model=RetrieveUser | Dict)
async def read_user_by_id(user_id: UUID4, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if user is None:
        return {}
    return user


@user_router.delete("/users/{user_id}", response_model=bool)
async def delete_user(user_id: UUID4, db: AsyncSession = Depends(get_db)):
    success = await delete_user_from_db(db, user_id)
    return success
