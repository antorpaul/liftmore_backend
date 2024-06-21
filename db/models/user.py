import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from db.session import Base
from core.schemas.common import CreateUpdateUser

class User(Base):
    '''Defines a user object in LiftMore'''
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

from sqlalchemy.orm import Session
# Create Functions
async def create_user(db: Session, user: CreateUpdateUser):
    ''' creates a new user given a defined user object '''    
    user_db_entry = User(**user.model_dump())
    db.add(user_db_entry)
    await db.commit()
    await db.refresh(user_db_entry)
    return user

# Retrieve Functions
def get_user(db: Session, user_id: uuid):
    ''' Retrieves a user with their uuid '''
    return db.query(User).filter(User.id == user_id).first()

# Update Functions
def update_user(db: Session, user: User):
    ''' Updates an existing user '''
    try:
        existing_user = db.query(User).filter(User.id == user.id).first()
        if existing_user is None:
            return None
        else:
            existing_user.name = user.name
            existing_user.email = user.email
            db.commit()
            db.refresh(existing_user)
            return existing_user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Exception: {e}")
        return None

# Delete functions
def delete_user(db: Session, user_id: int):
    """
    Deletes a user.
    
    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user to delete.
    
    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    try:
        # Retrieve the user to ensure it exists
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            print("User does not exist..")
            return False
        
        # Delete the user itself
        db.delete(user)
        
        # Commit the transaction
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error deleting user: {e}")
        return False
    except Exception as e:
        db.rollback()
        print(f"Unexpected exception: {e}")
        return False