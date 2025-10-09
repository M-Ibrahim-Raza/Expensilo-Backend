from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from db import get_db_session
from schemas.user import UserResponse
from schemas.auth import SignUpRequest
from services.user import create_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Sign up a new user",
    response_description="The newly sign up user",
)
def signup(sign_up_request: SignUpRequest, db: Session = Depends(get_db_session)):
    sign_up_user: UserResponse = create_user(db=db, user_create_request=sign_up_request)
    return sign_up_user
