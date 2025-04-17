from pydantic import BaseModel
from typing import List

class HiddenSection(BaseModel):
    content: str
    cost: int
    isUnlocked: bool = False

class CourseBase(BaseModel):
    title: str
    description: str
    instructor: str

class CourseCreate(CourseBase):
    content: str = ""
    hiddenSections: List[HiddenSection] = []
    allowedGroups: List[str] = []

class Course(CourseBase):
    id: str | None = None
    content: str = ""
    hiddenSections: List[HiddenSection] = []
    allowedGroups: List[str] = []

    class Config:
        from_attributes = True