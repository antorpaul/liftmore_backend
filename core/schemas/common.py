from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class User(BaseModel):
  name: str
  email: str

  class Config:
    orm_mode = True

class Category(BaseModel):
  name: str
  description: str
  _type: str

  class Config:
    orm_mode = True

class Exercise(BaseModel):
  name: str
  description: str
  category_id: int
  
  class Config:
    orm_mode = True

class RoutineSessionBase(BaseModel):
  start_time: datetime
  end_time: datetime
  routine_template_id: Optional[int] = None
  breakdown: Optional[dict] = None
  
  class Config:
    orm_mode = True

class RoutineTemplateBase(BaseModel):
  name: str
  description: Optional[str] = None
  sets: Optional[Dict] = None
  
  class Config:
    orm_mode = True