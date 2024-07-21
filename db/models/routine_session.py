from typing import Union

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, Session
from db.session import Base


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


# Create functions
def create_routine_session(db: Session, routine_session: RoutineSession) -> Union[RoutineSession, None]:
    """
    Creates a new routine session in the database.
    
    Args:
        db (Session): SQLAlchemy session.
        routine_session (RoutineSession): RoutineSession object to be created.
    
    Returns:
        RoutineSession: The created RoutineSession object.
    """
    try:
        db.add(routine_session)
        db.commit()
        db.refresh(routine_session)
        return routine_session
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating routine session: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None


# Retrieve functions
def get_session_by_id(db: Session, session_id: int) -> RoutineSession:
    """
    Retrieves the routine session object by ID.
    
    Args:
        db (Session): SQLAlchemy session.
        session_id (int): ID of the RoutineSession to retrieve.
    
    Returns:
        Category: The retrieved category object.
    """
    session = db.query(RoutineSession).filter(RoutineSession.id == session_id).first()
    return session


# Update functions
def update_session(db: Session, routine_session: RoutineSession) -> Union[RoutineSession, None]:
    """
    Updates the session object with the specified session.
    
    Args:
        db (Session): SQLAlchemy session.
        routine_session (RoutineSession): Session object with updated values.
    
    Returns:
        session: The updated routine session object, or None if not found or on error.
    """
    try:
        existing_session = db.query(RoutineSession).filter(RoutineSession.id == routine_session.id).first()
        if existing_session is None:
            return None
        else:
            existing_session.start_time = routine_session.start_time
            existing_session.end_time = routine_session.end_time
            existing_session.breakdown = routine_session.breakdown

            db.commit()
            db.refresh(existing_session)
            return existing_session
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None


# Delete functions
def delete_exercise(db: Session, session_id: int) -> bool:
    """
    Deletes an exercise.
    
    Args:
        db (Session): SQLAlchemy session.
        session_id (int): ID of the routine session to delete.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Retrieve the user to ensure it exists
        session = db.query(RoutineSession).filter(RoutineSession.id == session_id).first()
        if session is None:
            print("RoutineSession does not exist..")
            return False
        
        # Delete the exercise itself
        db.delete(session)
        
        # Commit the transaction
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting routine session: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected routine session: {e}")
        return False
