from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db.db_setup import get_db_session
from schemas.user import UserCreate, UserRead
from services.user import create_user


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    response_description="The newly created user",
)
def create_user_endpoint(
    user_in: UserCreate,
    db: Session = Depends(get_db_session),
):
    user = create_user(db=db, user_in=user_in)
    return user
