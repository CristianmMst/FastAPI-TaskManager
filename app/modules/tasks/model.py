import enum
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.modules.users.model import UserDB


class TaskStatus(enum.Enum):
    DONE = "DONE"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"


class TaskDB(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(primary_key=True)
    title: str = Field(nullable=False, max_length=128)
    description: str = Field(nullable=False, max_length=256)
    status: TaskStatus = Field(nullable=False)

    user_id: int = Field(nullable=False, foreign_key="users.id")
    user: "UserDB" = Relationship(back_populates="tasks")
