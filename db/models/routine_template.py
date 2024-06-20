from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, JSON, DateTime, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
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
    
from sqlalchemy.orm import Session

# Create functions
def create_template(db: Session, template: RoutineTemplate):
    """
    Creates a new Routine Template in the database.
    
    Args:
        db (Session): SQLAlchemy session.
        template (RoutineTemplate): Routine Template object to be created.
    
    Returns:
        Routine Template: The created routine template object.
    """
    try:
        db.add(template)
        db.commit()
        db.refresh(template)
        return template
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None
    
# Retrieve functions
def get_template_by_id(db: Session, template_id: int):
    """
    Retrieves the routine template object by ID.
    
    Args:
        db (Session): SQLAlchemy session.
        template_id (int): ID of the template to retrieve.
    
    Returns:
        Template: The retrieved routine template object.
    """
    template = db.query(RoutineTemplate).filter(RoutineTemplate.id == template_id).first()
    return template

# Update functions
def update_routine(db: Session, template: RoutineTemplate):
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

# Delete functions
def delete_routine_template(db: Session, template_id: int):
    """
    Deletes a routine template and all exercises associated with that routine template.
    
    Args:
        db (Session): SQLAlchemy session.
        template_id (int): ID of the routine template to delete.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Retrieve the routine template to ensure it exists
        category = db.query(RoutineTemplate).filter(RoutineTemplate.id == template_id).first()
        if category is None:
            print("Routine Template not found.")
            return False
        
        # Delete all exercises associated with the category
        db.query(RoutineTemplate).filter(RoutineTemplate.id == template_id).delete()

        # Delete the category itself
        db.delete(category)
        
        # Commit the transaction
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting routine template: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected exception: {e}")
        return False