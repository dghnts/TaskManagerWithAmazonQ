from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database.connection import Base

class TaskCategory(str, enum.Enum):
    WORK = "work"
    PRIVATE = "private"
    STUDY = "study"
    OTHER = "other"

class TaskPriority(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskUrgency(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(Enum(TaskCategory), nullable=False)
    priority = Column(Enum(TaskPriority), nullable=False)
    urgency = Column(Enum(TaskUrgency), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NOT_STARTED)
    progress = Column(Integer, default=0)
    
    # スケジュール関連
    due_date = Column(DateTime(timezone=True))
    planned_start_date = Column(DateTime(timezone=True))
    planned_end_date = Column(DateTime(timezone=True))
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # 時間管理
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    
    # その他
    notes = Column(Text)
    
    # システム項目
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーション
    subtasks = relationship("SubTask", back_populates="task", cascade="all, delete-orphan")
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")