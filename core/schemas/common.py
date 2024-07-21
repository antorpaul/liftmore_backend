import json

from pydantic import BaseModel, UUID4
from typing import Dict, Optional, List, Union
from datetime import datetime


# USER
class CreateUpdateUser(BaseModel):
    """
    Schema defining attributes to create user
    """
    first_name: str
    last_name: str
    username: str
    phone_number: str
    email: str
    password: str

    class Config:
        from_attributes = True


class RetrieveUser(BaseModel):
    """
    Schema defining attributes to get a user
    """
    id: UUID4
    first_name: str
    last_name: str
    username: str
    phone_number: str
    email: str

    class Config:
        from_attributes = True


class UserLoginWithEmail(BaseModel):
    """
    Schema defining attributes to login as a user
    """
    email: str
    password: str

    class Config:
        from_attributes = True


class UserLoginWithPhone(BaseModel):
    """
    Schema defining attributes to login as a user
    """
    phone_number: str
    password: str

    class Config:
        from_attributes = True


class DeleteUser(BaseModel):
    """
    Schema defining necessary properties to delete user
    """
    id: UUID4

    class Config:
        from_attributes = True


# CATEGORY
class CreateUpdateCategory(BaseModel):
    name: str
    description: str
    type: str

    class Config:
        from_attributes = True


class RetrieveCategory(BaseModel):
    id: int
    name: str
    description: str
    type: str

    class Config:
        from_attributes = True


# EXERCISE
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
    category_id: int

    class Config:
        from_attributes = True


# ROUTINE TEMPLATE
class CreateUpdateRoutineTemplate(BaseModel):
    name: str
    description: Optional[str] = None
    sets: Optional[Dict] = None
    exercises: Optional[List[int]] = None  # List of exercise IDs

    class Config:
        from_attributes = True

    def validate(self) -> Union[Dict, None]:
        """ Basic checks to validate this routine session before trying to create entity in db. """
        issues = {}
        for key, val in self.sets.items():
            if int(key) not in self.exercises:
                issues[f"exercise-{key}"] = f"Set for exercise (id#{key}) not in exercise list."
        return issues


class RetrieveRoutineTemplate(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    sets: Optional[Dict] = None
    exercises: Optional[List[RetrieveExercise]] = None

    class Config:
        from_attributes = True


# ROUTINE SESSION
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
