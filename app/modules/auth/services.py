from sqlmodel import Session, select

from app.core.database import engine
from app.modules.users.model import UserDB
from app.modules.auth.utils import hash_password
from app.modules.users.schemas import UserCreate


def find_user(email: str):
    with Session(engine) as session:
        user = session.exec(select(UserDB).where(
            UserDB.email == email)).first()
        return user


def create_user(user: UserCreate):
    hashed_password = hash_password(user.password)

    create_user = UserDB(
        email=user.email, username=user.username, password=hashed_password)

    with Session(engine) as session:
        session.add(create_user)
        session.commit()
