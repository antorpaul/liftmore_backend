from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.exc import SQLAlchemyError
from db.session import Base
from db.models.exercise import Exercise

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence('categories_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))
    _type = Column(String(10), nullable=False, default='exercise', name='type')

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', description='{self.description}', type='{self.type}')>"
    
from sqlalchemy.orm import Session

# Create functions
def create_category(db: Session, category: Category):
    """
    Creates a new category in the database.
    
    Args:
        db (Session): SQLAlchemy session.
        category (Category): Category object to be created.
    
    Returns:
        Category: The created category object.
    """
    try:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None

# Retrieve Functions
def get_category_by_id(db: Session, category_id: int):
    """
    Retrieves the category object by ID.
    
    Args:
        db (Session): SQLAlchemy session.
        category_id (int): ID of the category to retrieve.
    
    Returns:
        Category: The retrieved category object.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    return category

def get_category_by_name(db: Session, category_name: int):
    """
    Retrieves the category object by name.
    
    Args:
        db (Session): SQLAlchemy session.
        category_name (str): Name of the category to retrieve.
    
    Returns:
        Category: The retrieved category object.
    """
    category = db.query(Category).filter(Category.name == category_name).first()
    return category

# Update functions
def update_category(db: Session, category: Category):
    """
    Updates the category object with the specified category.
    
    Args:
        db (Session): SQLAlchemy session.
        category (Category): Category object with updated values.
    
    Returns:
        Category: The updated category object, or None if not found or on error.
    """
    try:
        existing_category = db.query(Category).filter(Category.id == category.id).first()
        if existing_category is None:
            return None
        else:
            existing_category.name = category.name
            existing_category.description = category.description
            existing_category.type = category.type
            db.commit()
            db.refresh(existing_category)
            return existing_category
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None

# Delete functions
def delete_category(db: Session, category_id: int):
    """
    Deletes a category and all exercises associated with that category.
    
    Args:
        db (Session): SQLAlchemy session.
        category_id (int): ID of the category to delete.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Retrieve the category to ensure it exists
        category = db.query(Category).filter(Category.id == category_id).first()
        if category is None:
            print("Category not found.")
            return False
        
        # Delete all exercises associated with the category
        db.query(Exercise).filter(Exercise.category_id == category_id).delete()

        # Delete the category itself
        db.delete(category)
        
        # Commit the transaction
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting category and its exercises: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected exception: {e}")
        return False