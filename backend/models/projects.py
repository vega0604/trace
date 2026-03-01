# models/projects.py
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    active = "active"
    archived = "archived"

class Project(BaseModel):
    id: int
    title: str
    description: str
    status: ProjectStatus = ProjectStatus.active
    tasks: List[int] = []
    people: List[int] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)