from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .db import Base
import datetime


class NewMemoryNode(Base):
    __tablename__ = "memory_nodes"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("memory_nodes.id", ondelete="CASCADE"), nullable=True)
    depth = Column(Integer, nullable=False, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    children = relationship("NewMemoryNode", cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "response": self.response,
            "summary": self.summary,
            "parent_id": self.parent_id,
            "depth": self.depth,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }
