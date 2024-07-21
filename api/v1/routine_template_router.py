from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas import *
from db.connection import get_db
from db.models.routine_template import create_template, delete_routine_template, get_template_by_id

routine_template_router = APIRouter()


@routine_template_router.get("/routineTemplates/{template_id}", response_model=Union[RetrieveRoutineTemplate, Dict])
async def get_routine_template(template_id: int, db: AsyncSession = Depends(get_db)):
    template = await get_template_by_id(db=db, template_id=template_id)
    if template is None:
        return {}
    return template


@routine_template_router.post("/routineTemplates", response_model=Union[RetrieveRoutineTemplate, Dict])
async def create_routine_template(template: CreateUpdateRoutineTemplate, db: AsyncSession = Depends(get_db)):
    template_issues = template.validate()
    if len(template_issues) > 0:
        return template_issues

    template = await create_template(template=template, db=db)
    if template is None:
        return {}
    return template


@routine_template_router.delete("/routineTemplates/{template_id}", response_model=bool)
async def delete_template(template_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_routine_template(db, template_id)
