from sqlalchemy.orm import Session
from models import User
from schemas.user import UserCreate


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new User SQLAlchemy instance from Pydantic schema
    """
    # Convert Pydantic model to dict
    user_data = user_in.model_dump()

    # Create SQLAlchemy model instance
    user = User(**user_data)

    # Add to session
    db.add(user)
    db.flush()
    db.refresh(user)  # refresh to get auto-generated fields like id

    return user
