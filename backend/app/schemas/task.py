from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.task import TaskCategory, TaskPriority, TaskUrgency, TaskStatus

# ベーススキーマ
class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    category: TaskCategory
    priority: TaskPriority
    urgency: TaskUrgency
    due_date: Optional[datetime] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

# タスク作成用
class TaskCreate(TaskBase):
    pass

# タスク更新用
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    category: Optional[TaskCategory] = None
    priority: Optional[TaskPriority] = None
    urgency: Optional[TaskUrgency] = None
    status: Optional[TaskStatus] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    due_date: Optional[datetime] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = Field(None, ge=0)
    actual_hours: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None

# レスポンス用（基本）
class Task(TaskBase):
    id: UUID
    status: TaskStatus
    progress: int
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    actual_hours: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# サブタスク・コメント用の簡易スキーマ
class SubTaskSimple(BaseModel):
    id: UUID
    title: str
    completed: bool
    order_index: int
    created_at: datetime

    class Config:
        from_attributes = True

class CommentSimple(BaseModel):
    id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

# タスク詳細用（関連データ含む）
class TaskDetail(Task):
    subtasks: List[SubTaskSimple] = []
    comments: List[CommentSimple] = []

# タスク一覧用（集計情報含む）
class TaskWithCounts(Task):
    subtask_count: int = 0
    completed_subtasks: int = 0
    comment_count: int = 0

# マトリックス表示用
class MatrixTask(BaseModel):
    id: UUID
    title: str
    priority: TaskPriority
    urgency: TaskUrgency
    status: TaskStatus
    progress: int

    class Config:
        from_attributes = True

# カレンダー表示用
class CalendarEvent(BaseModel):
    id: UUID
    title: str
    type: str  # "start", "due", "milestone"
    priority: TaskPriority
    urgency: TaskUrgency

    class Config:
        from_attributes = True