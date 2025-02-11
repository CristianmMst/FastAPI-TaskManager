from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.tasks.model import TaskDB


class UserDB(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(primary_key=True)
    username: str = Field(nullable=False, max_length=30)
    email: str = Field(nullable=False, unique=True, max_length=128)
    password: str = Field(nullable=False, max_length=128)
    tasks: list["TaskDB"] = Relationship(back_populates="user")
