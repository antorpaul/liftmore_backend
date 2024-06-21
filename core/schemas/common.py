from pydantic import BaseModel, UUID4
from typing import Dict, Optional, List
from datetime import datetime

### USER
class CreateUpdateUser(BaseModel):
  """
  Schema defining attributes to create user
  """
  name: str
  email: str

  class Config:
    from_attributes = True

class RetrieveUser(BaseModel):
  """
  Schema defining attributes to get a user
  """
  id: UUID4

  class Config:
    from_attributes = True

class DeleteUser(BaseModel):
  """
  Schema defining necessary properties to delete user
  """
  id: UUID4

  class Config:
    from_attributes = True

### CATEGORY
class CreateUpdateCategory(BaseModel):
  name: str
  description: str
  _type: str

  class Config:
    from_attributes = True

class RetrieveCategory(BaseModel):
  id: int
  name: str
  description: str
  _type: str

  class Config:
    from_attributes = True

### EXERCISE
class CreateUpdateExercise(BaseModel):
  name: str
  description: str
  category_id: int
  
  class Config:
    from_attributes = True

class RetrieveExercise(BaseModel):
  id: int
  name: str
  description: str
  _type: str

  class Config:
    from_attributes = True

### ROUTINE TEMPLATE
class CreateUpdateRoutineTemplate(BaseModel):
  name: str
  description: Optional[str] = None
  sets: Optional[Dict] = None
  exercises: Optional[List[int]] = None  # List of exercise IDs

  class Config:
      from_attributes = True

class RetrieveRoutineTemplate(BaseModel):
  id: int
  name: str
  description: Optional[str] = None
  sets: Optional[Dict] = None
  exercises: Optional[List[RetrieveExercise]] = None

  class Config:
      from_attributes = True
    
### ROUTINE SESSION
class CreateUpdateRoutineSession(BaseModel):
  start_time: datetime
  end_time: datetime
  routine_template_id: Optional[int] = None
  breakdown: Optional[dict] = None
  routine_template: RetrieveRoutineTemplate
  
  class Config:
    from_attributes = True

class RetrieveRoutineSession(BaseModel):
  start_time: datetime
  end_time: datetime
  routine_template_id: Optional[int] = None
  breakdown: Optional[dict] = None
  routine_template: RetrieveRoutineTemplate
  
  class Config:
    from_attributes = True