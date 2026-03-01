# models/people.py
from pydantic import BaseModel
from typing import List

class Person(BaseModel):
    id: int
    email: str
    name: str
    tags: List[str] = []
    proficiencies: List[str] = []