from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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

from sqlalchemy.orm import Session

# Create functions
def create_routine_session(db: Session, session: Session):
    """
    Creates a new routine session in the database.
    
    Args:
        db (Session): SQLAlchemy session.
        session (RoutineSession): RoutineSession object to be created.
    
    Returns:
        RoutineSession: The created RoutineSession object.
    """
    try:
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None

# Retrieve functions
def get_session_by_id(db: Session, session_id: int):
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
def update_session(db: Session, session: RoutineSession) -> RoutineSession | None:
    """
    Updates the session object with the specified session.
    
    Args:
        db (Session): SQLAlchemy session.
        session (RoutineSession): Session object with updated values.
    
    Returns:
        session: The updated routine session object, or None if not found or on error.
    """
    try:
        existing_session = db.query(RoutineSession).filter(RoutineSession.id == session.id).first()
        if existing_session is None:
            return None
        else:
            existing_session.start_time = session.start_time
            existing_session.end_time = session.end_time
            existing_session.breakdown = session.breakdown

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
def delete_exercise(db: Session, session_id: int):
    """
    Deletes an exercise.
    
    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the exercise to delete.
    
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