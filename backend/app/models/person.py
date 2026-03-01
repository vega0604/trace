import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.database import Base

class Person(Base):
    __tablename__ = "people"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False, index=True)
    company = Column(String, nullable=True, index=True)
    role = Column(String, nullable=True)
    phone = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True, index=True)
    tags_json = Column(Text, nullable=True)
    last_contacted_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    interactions = relationship(
        "Interaction",
        back_populates="person",
        cascade="all, delete-orphan"
    )
    edges_from = relationship(
        "Edge",
        foreign_keys="[Edge.from_person_id]",
        back_populates="from_person",
        cascade="all, delete-orphan"
    )
    edges_to = relationship(
        "Edge",
        foreign_keys="[Edge.to_person_id]",
        back_populates="to_person",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Person(id={self.id}, full_name={self.full_name})>"
