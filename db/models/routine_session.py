from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from base import Base

class RoutineSession(Base):
    __tablename__ = 'routine_sessions'

    id = Column(Integer, Sequence('routine_sessions_id_seq'), primary_key=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    routine_template_id = Column(Integer, ForeignKey('routine_templates.id', ondelete='CASCADE'))
    breakdown = Column(JSON)

    # Define a relationship to the RoutineTemplate model
    routine_template = relationship('RoutineTemplate', back_populates='routine_sessions')

    def __repr__(self):
        return f"<RoutineSession(id={self.id}, start_time='{self.start_time}', end_time='{self.end_time}', routine_template_id={self.routine_template_id}, breakdown={self.breakdown})>"