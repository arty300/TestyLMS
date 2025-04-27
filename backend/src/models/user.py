from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str = "student"
    groups: List[str] = []

class UserUpdate(BaseModel):
    groups: List[str]

class User(UserBase):
    id: str | None = None
    points: int = 0
    role: str = "student"
    groups: List[str] = []
    unlockedSections: dict = {}  # Формат: {"course_id": [index1, index2, ...]}

    class Config:
        from_attributes = True

class Group(BaseModel):
    id: str | None = None
    name: str
    users: List[str] = []
    allowedCourses: List[str] = []

    class Config:
        from_attributes = True