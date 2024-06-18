from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from base import Base

class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, Sequence('exercises_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))

    category = relationship('Category', back_populates='exercises')

    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', description='{self.description}', category_id={self.category_id})>"

from sqlalchemy.orm import Session

# Create functions
def create_exercise(db: Session, exercise: Exercise):
    """
    Creates an exercise
    
    Args:
        db (Session): SQLAlchemy session.
        exercise (Exercise): Exercise object to add to database
    
    Returns:
        exercise: The exercise that was just created
    """
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

# Retrieve functions
def get_exercise_by_id(db: Session, exercise_id: int):
    """
    Retrieves exercise by exercise ID.
    
    Args:
        db (Session): SQLAlchemy session.
        exercise_id (int): ID of the exercise to retrieve.
    
    Returns:
        the exercise if found
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    return exercise

def get_exercise_by_name(db: Session, exercise_name: str):
    """
    Retrieves exercise by exercise name.
    
    Args:
        db (Session): SQLAlchemy session.
        exercise_name (int): name of the exercise to retrieve.
    
    Returns:
        the exercise if found
    """
    exercise = db.query(Exercise).filter(Exercise.name == exercise_name).first()
    return exercise

def get_all_exercises_for_category_id(db: Session, category_id: int) -> List[Exercise]:
    """
    Retrieves all exercises by category ID.
    
    Args:
        db (Session): SQLAlchemy session.
        category_id (int): ID of the category whose exercises to retrieve.
    
    Returns:
        list: List of exercises for the given category ID.
    """
    exercises = db.query(Exercise).filter(Exercise.category_id == category_id).all()
    return exercises

# Update functions
def update_exercise(db: Session, exercise: Exercise):
    """
    Updates an exercise with the current exercise
    
    Args:
        db (Session): SQLAlchemy session.
        exercise (Exercise): Exercise object to add to database
    
    Returns:
        exercise: The exercise that was just updated
    """
    try:
        existing_exercise = db.query(Exercise).filter(exercise.id == exercise.id).first()
        if existing_exercise is None:
            return None
        else:
            existing_exercise.name = exercise.name
            existing_exercise.category = exercise.category
            existing_exercise.category_id = exercise.category_id
            db.commit()
            db.refresh(existing_exercise)
            return existing_exercise
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None
    
# Delete functions
def delete_exercise(db: Session, exercise_id: int):
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
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if exercise is None:
            print("Exercise does not exist..")
            return False
        
        # Delete the exercise itself
        db.delete(exercise)
        
        # Commit the transaction
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting exercise: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected exception: {e}")
        return False