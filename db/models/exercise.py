from typing import List, Union
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, Session
from core.schemas.common import CreateUpdateExercise, RetrieveExercise
from db.models.exercises_routine_bridge import exercises_routine_bridge
from db.session import Base


class Exercise(Base):
    __tablename__ = 'exercises'

    id = Column(Integer, Sequence('exercises_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))

    category = relationship('Category', back_populates='exercises')
    routine_templates = relationship('RoutineTemplate', secondary=exercises_routine_bridge, back_populates='exercises')

    def __repr__(self):
        return f"<Exercise(id={self.id}, name='{self.name}', description='{self.description}', category_id={self.category_id})>"


# Create functions
async def create_exercise(db: Session, exercise: CreateUpdateExercise):
    """
    Creates an exercise in the database
    
    Args:
        db (Session): SQLAlchemy session.
        exercise (Exercise): Exercise object to add to database
    
    Returns:
        exercise: The exercise that was just created
    """
    try:
        exercise_db_entry = Exercise(**exercise.model_dump())
        db.add(exercise_db_entry)
        await db.commit()
        await db.refresh(exercise_db_entry)
        return exercise_db_entry
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating exercise: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None


# Retrieve functions
async def get_exercise(db: Session, identifier: Union[int, str]) -> Union[RetrieveExercise | None, List[RetrieveExercise]]:
    """
    Retrieves exercise by exercise ID.
    
    Args:
        db (Session): SQLAlchemy session.
        identifier (int | str): ID or name of the exercise to retrieve.
    
    Returns:
        the exercise if found
    """
    if isinstance(identifier, int):
        result = await db.execute(select(Exercise).filter_by(id=identifier))
        exercise = result.scalars().first()
        return exercise

    if isinstance(identifier, str):
        result = await db.execute(
            select(Exercise)
            .filter(Exercise.name.ilike(f"%{identifier}%"))
        )
        exercises = result.scalars().all()
        return [RetrieveExercise.model_validate(exercise) for exercise in exercises]

    print(f"Invalid identifier provided. Unable to find exercise.")
    return None


async def get_all_exercises_query(db: Session, page: int, page_size: int) -> List[RetrieveExercise]:
    """ Retrieves all exercises in the database """
    result = await db.execute(
        select(Exercise)
        .order_by(Exercise.name)
        .limit(page_size)
        .offset(page * page_size))
    exercises = result.scalars().all()
    return exercises


async def get_all_exercises_for_category_id(db: Session, category_id: int, page: int, page_size: int) -> List[Exercise]:
    """
    Retrieves all exercises by category ID.
    
    Args:
        page: page to retrieve
        page_size: size of the page
        db (Session): SQLAlchemy session.
        category_id (int): ID of the category whose exercises to retrieve.
    
    Returns:
        list: List of exercises for the given category ID.
    """
    result = await db.execute(
        select(Exercise)
        .where(Exercise.category_id == category_id)
        .order_by(Exercise.name)
        .limit(page_size)
        .offset(page * page_size))
    exercises = result.scalars().all()
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
