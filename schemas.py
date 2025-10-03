from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    login: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    authorId: int
    createdAt: datetime
    updatedAt: datetime
