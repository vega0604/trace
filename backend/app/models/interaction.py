import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    person_id = Column(String, ForeignKey("people.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(String, nullable=False, index=True)
    notes = Column(Text, nullable=False)
    tags_json = Column(Text, nullable=True)
    occurred_at = Column(DateTime, nullable=False, index=True)
    follow_up_at = Column(DateTime, nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    person = relationship("Person", back_populates="interactions")

    def __repr__(self):
        return f"<Interaction(id={self.id}, type={self.type}, person_id={self.person_id})>"
