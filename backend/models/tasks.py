# models/tasks.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
from enum import Enum

class TaskStatus(str, Enum):
    not_started = "not started"
    in_progress = "in progress"
    blocked = "blocked"
    done = "done"

class Task(BaseModel):
    id: int
    title: str
    description: str
    tags: List[str] = []
    dependencies: List[int] = []
    assigned_to: List[int] = []
    status: TaskStatus = TaskStatus.not_started
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[date] = None