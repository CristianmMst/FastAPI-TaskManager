import jwt
from typing import Annotated, Optional
from fastapi import APIRouter, Cookie, Depends, HTTPException, status, Response
from app.modules.auth.services import create_user, find_user
from app.modules.auth.utils import ALGORITHM, SECRET_KEY, create_access_token, verify_password
from app.modules.auth.schemas import OAuth2EmailRequestForm
from app.modules.users.schemas import User, UserCreate

router = APIRouter()


@router.post("/login")
def login(form_data: Annotated[OAuth2EmailRequestForm, Depends()], response: Response):
    user = find_user(form_data.email)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = User(username=user.username, email=user.email)

    access_token, refresh_token = create_access_token(user.model_dump())
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {"message": "Logged in successfully"}


@router.post("/register")
def register(user: UserCreate):
    db_user = find_user(user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    create_user(user)

    return {"message": "User registered successfully"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.post("/refresh")
def refresh(response: Response, refresh_token: Optional[str] = Cookie(None),):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user = find_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    access_token, refresh_token = create_access_token(user.model_dump())
    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)

    return {"message": "Token refreshed successfully"}
