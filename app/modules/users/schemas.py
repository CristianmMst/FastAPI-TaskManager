from pydantic import EmailStr, BaseModel


class User(BaseModel):
    username: str
    email: EmailStr


class UserCreate(User):
    password: str


class UserRead(User):
    id: int
