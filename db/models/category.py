from sqlalchemy import Column, Integer, String, Sequence, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship
from typing import List

from core.schemas.common import CreateUpdateCategory, RetrieveCategory
from db.session import Base
from db.models.exercise import Exercise

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, Sequence('categories_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))
    type = Column(String(10), nullable=False, default='exercise', name='type')

    exercises = relationship('Exercise', back_populates='category')

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', description='{self.description}', type='{self.type}')>"
    
from sqlalchemy.orm import Session

# Create functions
async def create_category(db: Session, category: CreateUpdateCategory):
    """
    Creates a new category in the database.
    
    Args:
        db (Session): SQLAlchemy session.
        category (Category): Category object to be created.
    
    Returns:
        Category: The created category object.
    """
    try:
        category_db_entry = Category(**category.model_dump())
        db.add(category_db_entry)
        await db.commit()
        await db.refresh(category_db_entry)
        return category_db_entry
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error creating category: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None

# Retrieve Functions
async def get_category_by_id(db: Session, category_id: int):
    """
    Retrieves the category object by ID.
    
    Args:
        db (Session): SQLAlchemy session.
        category_id (int): ID of the category to retrieve.
    
    Returns:
        Category: The retrieved category object.
    """
    result = await db.execute(select(Category).filter_by(id=category_id))
    category = result.scalars().first()
    return category

async def get_category_by_name(db: Session, category_name: int):
    """
    Retrieves the category object by name.
    
    Args:
        db (Session): SQLAlchemy session.
        category_name (str): Name of the category to retrieve.
    
    Returns:
        Category: The retrieved category object.
    """
    result = await db.execute(select(Category).filter_by(id=category_name))
    category = result.scalars().first()
    return category

async def get_all_categories(db: Session) -> List[RetrieveCategory]:
    """
    Retrieves all of the categories from the database.
    
    Args:
        db (Session): SQLAlchemy session
    Returns:
        List[Category]: List of categories
    """
    result = await db.scalars(select(Category).order_by(Category.name))
    categories = result.all()
    return [RetrieveCategory.model_validate(category) for category in categories]


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