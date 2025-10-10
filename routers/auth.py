from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db import get_db_session
from auth import create_access_token, get_current_user_id
from schemas.user import UserResponse
from schemas.auth import SignUpRequest, Token
from services.user import create_user, authenticate_user

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


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    user = authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token", response_model=dict)
async def verify_token_endpoint(
    user_id: int = Depends(get_current_user_id),
):
    return {"user_id": user_id}
