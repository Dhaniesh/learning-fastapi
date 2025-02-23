from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Annotated, Optional, List
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
    id: int
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


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True
