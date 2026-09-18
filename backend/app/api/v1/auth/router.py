from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.v1.auth.schemas import (
    CurrentUserResponse,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
)

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User

from app.api.v1.auth.dependencies import get_current_user


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)



@auth_router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@auth_router.post(
    "/login",
    response_model = LoginResponse,
    status_code = status.HTTP_200_OK,
)
def login(data: LoginRequest, 
        db: Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return LoginResponse(access_token=access_token, token_type = "bearer")



@auth_router.get("/me", response_model = CurrentUserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user



