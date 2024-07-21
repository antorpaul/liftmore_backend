from typing import Union, List

from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, JSON, DateTime, Table, select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, Session, selectinload

from core.schemas import CreateUpdateRoutineTemplate
from db.models import Exercise
from db.models.exercises_routine_bridge import exercises_routine_bridge
from db.session import Base


class RoutineTemplate(Base):
    __tablename__ = 'routine_templates'

    id = Column(Integer, Sequence('routine_templates_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300))
    sets = Column(JSON)

    routine_sessions = relationship('RoutineSession', back_populates='routine_template')
    exercises = relationship('Exercise', secondary=exercises_routine_bridge, back_populates='routine_templates')

    def __repr__(self):
        return f"<RoutineTemplate(id={self.id}, name='{self.name}', description='{self.description}', sets={self.sets})>"


# Create functions
async def create_template(db: Session, template: CreateUpdateRoutineTemplate) -> Union[RoutineTemplate, None]:
    """
    Creates a new Routine Template in the database.
    
    Args:
        db (Session): SQLAlchemy session.
        template (RoutineTemplate): Routine Template object to be created.
    
    Returns:
        Routine Template: The created routine template object.
    """
    try:
        # print("Template Info:")
        # print(template.name)
        # print(template.description)
        # print(template.sets)
        # print(template.exercises)
        # print("\n")
        # Get the exercises first
        get_exercises_query = await db.execute(select(Exercise).filter(Exercise.id.in_(template.exercises)))
        exercises = get_exercises_query.scalars().all()
        template_db_entry = RoutineTemplate(
            name=template.name,
            description=template.description,
            sets=template.sets)
        template_db_entry.exercises = exercises
        db.add(template_db_entry)
        await db.commit()
        await db.refresh(template_db_entry)
        return template_db_entry
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None


# Retrieve functions
async def get_template_by_id(db: Session, template_id: int) -> Union[RoutineTemplate, None]:
    """
    Retrieves the routine template object by ID.
    
    Args:
        db (Session): SQLAlchemy session.
        template_id (int): ID of the template to retrieve.
    
    Returns:
        Template: The retrieved routine template object.
    """
    result = await db.execute(
        select(RoutineTemplate)
        .where(RoutineTemplate.id == template_id)
        .options(selectinload(RoutineTemplate.exercises), selectinload(RoutineTemplate.routine_sessions)))
    template = result.scalars().first()
    if template is None:
        return {}
    return template


# Update functions
def update_routine(db: Session, template: RoutineTemplate) -> Union[RoutineTemplate, None]:
    """
    Updates the routine template object with the specified template.
    
    Args:
        db (Session): SQLAlchemy session.
        template (RoutineTemplate): Routine Template object with updated values.
    
    Returns:
        RoutineTemplate: The updated routine template object, or None if not found or on error.
    """
    try:
        existing_template = db.query(RoutineTemplate).filter(RoutineTemplate.id == template.id).first()
        if existing_template is None:
            return None
        else:
            existing_template.name = template.name
            existing_template.description = template.description
            existing_template.exercises = template.exercises
            db.commit()
            db.refresh(existing_template)
            return existing_template
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating routine template: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None


async def get_exercises_from_routine(db: Session, template_id: int) -> List[Exercise]:
    """ Gets all the exercises in a routine template """
    try:
        exercises = await db.execute(
            select(exercises_routine_bridge)
            .where(exercises_routine_bridge.routine_template_id == template_id)
        ).scalars().all()
        return exercises
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error getting exercises from routine template: {e}")
    except Exception as e:
        db.rollback()
        print(f"Unexpected Exception: {e}")


# Delete functions
async def delete_routine_template(db: Session, template_id: int) -> bool:
    """
    Deletes a routine template and all exercises associated with that routine template.
    
    Args:
        db (Session): SQLAlchemy session.
        template_id (int): ID of the routine template to delete.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        print("hello")
        # Retrieve the routine template to ensure it exists
        template = await get_template_by_id(db, template_id)
        if template is None:
            print("Routine Template not found.")
            return False
        delete_template_by_id = (
            delete(RoutineTemplate)
            .where(RoutineTemplate.id == template_id)
        )
        result = await db.execute(delete_template_by_id)
        await db.commit()
        if result.rowcount == 1:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting routine template: {e}")
        return False
    except Exception as e:
        await db.rollback()
        print(f"Unexpected exception: {e}")
        return False
