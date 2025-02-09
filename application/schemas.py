from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class Post(BaseModel):
    title: str
    content: str
