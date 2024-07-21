import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, select, delete
from db.session import Base
from core.schemas.common import CreateUpdateUser, RetrieveUser
from passlib.context import CryptContext


class User(Base):
    """Defines a user object in LiftMore"""
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True)
    phone_number = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Create Functions
async def create_user(db: Session, user: CreateUpdateUser):
    """ creates a new user given a defined user object """
    user_db_entry = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        phone_number=user.phone_number,
        email=user.email,
        password=get_password_hash(user.password))

    db.add(user_db_entry)
    await db.commit()
    await db.refresh(user_db_entry)

    return RetrieveUser(
        id=user_db_entry.id,
        first_name=user_db_entry.first_name,
        last_name=user_db_entry.last_name,
        username=user_db_entry.username,
        phone_number=user_db_entry.phone_number,
        email=user_db_entry.email)


# Retrieve Functions
async def get_user(db: Session, user_id: uuid):
    """ Retrieves a user with their uuid """
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()
    return user


# Update Functions
def update_user(db: Session, user: User):
    """ Updates an existing user """
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
async def delete_user_from_db(db: Session, user_id: uuid) -> bool:
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
        user = await get_user(db, user_id)
        if user is None:
            return False
        # Delete the user itself
        result = await db.execute(
            delete(User)
            .where(User.id == user.id)
        )
        await db.commit()
        if result.rowcount == 1:
            return True
        else:
            return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting user: {e}")
        return False
    except Exception as e:
        await db.rollback()
        print(f"Unexpected exception: {e}")
        return False
