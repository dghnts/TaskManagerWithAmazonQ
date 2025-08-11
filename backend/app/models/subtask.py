from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database.connection import Base

class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String(36), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    completed = Column(Boolean, nullable=False, default=False)
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    task = relationship("Task", back_populates="subtasks")