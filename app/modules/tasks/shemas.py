from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    status: str
    description: str
    user_id: Optional[int] = None


class TaskRead(TaskCreate):
    id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
