from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, JSON, DateTime, Table
from sqlalchemy.orm import relationship, declarative_base
from base import Base

class RoutineTemplate(Base):
    __tablename__ = 'routine_templates'

    id = Column(Integer, Sequence('routine_templates_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    sets = Column(JSON)

    # Define a relationship to the RoutineSession model
    routine_sessions = relationship('RoutineSession', back_populates='routine_template')

    # Define a relationship to the Exercise model through the bridge table
    exercises = relationship('Exercise', secondary=exercises_routine_bridge, back_populates='routine_templates')

    def __repr__(self):
        return f"<RoutineTemplate(id={self.id}, name='{self.name}', description='{self.description}', sets={self.sets})>"