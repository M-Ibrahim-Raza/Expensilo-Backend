from sqlalchemy.orm import Session
from models import User
from schemas.user import UserCreateRequest, UserReadResponse, UserUpdateRequest
from fastapi import HTTPException, status


def read_user(db: Session, user_id: int) -> UserReadResponse:

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserReadResponse.model_validate(user)


def create_user(db: Session, user: UserCreateRequest) -> UserReadResponse:
    """
    Create a new User SQLAlchemy instance from Pydantic schema
    """
    # Convert Pydantic model to dict
    user_data = user.model_dump()

    # Create SQLAlchemy model instance
    user = User(**user_data)

    # Add to session
    db.add(user)
    db.commit()
    db.refresh(user)  # refresh to get auto-generated fields like id

    return UserReadResponse.model_validate(user)


def update_user(
    db: Session, user_id: int, user_update_request: UserUpdateRequest
) -> UserReadResponse:

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    print(user_update_request)
    update_data = user_update_request.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return UserReadResponse.model_validate(user)
