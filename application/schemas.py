from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostIn(BaseModel):
    title: str
    content: str


class Post(BaseModel):
    title: str
    content: str
    user_id: int
    user: UserOut


class PostList(BaseModel):
    data: list[Post]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[int] = None
