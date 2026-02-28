import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, DateTime, ForeignKey, UniqueConstraint, CheckConstraint, Index
)
from sqlalchemy.orm import relationship
from app.database import Base

class Edge(Base):
    __tablename__ = "edges"
    __table_args__ = (
        UniqueConstraint("from_person_id", "to_person_id", name="uix_from_to"),
        CheckConstraint("strength >= 1 AND strength <= 5", name="chk_strength_range"),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_person_id = Column(String, ForeignKey("people.id", ondelete="CASCADE"), nullable=False, index=True)
    to_person_id = Column(String, ForeignKey("people.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String, nullable=True, index=True)
    strength = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    from_person = relationship(
        "Person",
        foreign_keys=[from_person_id],
        back_populates="edges_from"
    )
    to_person = relationship(
        "Person",
        foreign_keys=[to_person_id],
        back_populates="edges_to"
    )

    def __repr__(self):
        return f"<Edge(id={self.id}, from={self.from_person_id}, to={self.to_person_id}, label={self.label}, strength={self.strength})>"
