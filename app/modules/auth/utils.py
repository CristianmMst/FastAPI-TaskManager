import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.modules.users.schemas import UserRead


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
SECRET_KEY = "secret"


def get_jwt_from_cookies(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_token


def get_current_user(token: Annotated[str, Depends(get_jwt_from_cookies)]):
    from app.modules.auth.services import find_user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception

    except jwt.PyJWTError:
        raise credentials_exception

    user = find_user(email)
    if user is None:
        raise credentials_exception
    return UserRead(id=user.id, username=user.username, email=user.email)


def create_access_token(payload: dict):
    to_encode = payload.copy()
    to_encode.update({"exp": datetime.now(
        timezone.utc) + timedelta(minutes=1), "type": "access"})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    to_encode.update({"exp": datetime.now(timezone.utc) +
                     timedelta(minutes=2), "type": "refresh"})
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
