
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, JSON, DateTime, Table
from sqlalchemy.orm import relationship
from base import Base


# Define the bridge table for many-to-many relationship between RoutineTemplate and Exercise
exercises_routine_bridge = Table(
    'exercises_routine_bridge',
    Base.metadata,
    Column('routine_template_id', Integer, ForeignKey('routine_templates.id', ondelete='CASCADE'), primary_key=True),
    Column('exercises_id', Integer, ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True)
)