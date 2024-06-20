from pydantic import BaseModel, UUID4
from typing import Dict, Optional
from datetime import datetime

class CreateUser(BaseModel):
  """
  Schema defining attributes to create user
  """
  name: str
  email: str

  class Config:
    from_attributes = True

class RetrieveUser(BaseModel):
  """
  Schema defining attributes to create user
  """
  id: UUID4
  name: str
  email: str

  class Config:
    from_attributes = True

class Category(BaseModel):
  name: str
  description: str
  _type: str

  class Config:
    from_attributes = True

class Exercise(BaseModel):
  name: str
  description: str
  category_id: int
  
  class Config:
    from_attributes = True

class RoutineSessionBase(BaseModel):
  start_time: datetime
  end_time: datetime
  routine_template_id: Optional[int] = None
  breakdown: Optional[dict] = None
  
  class Config:
    from_attributes = True

class RoutineTemplateBase(BaseModel):
  name: str
  description: Optional[str] = None
  sets: Optional[Dict] = None
  
  class Config:
    from_attributes = True