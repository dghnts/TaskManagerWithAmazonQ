from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ベーススキーマ
class SubTaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    order_index: int

# サブタスク作成用
class SubTaskCreate(SubTaskBase):
    pass

# サブタスク更新用
class SubTaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    completed: Optional[bool] = None
    order_index: Optional[int] = None

# レスポンス用
class SubTask(SubTaskBase):
    id: str
    task_id: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True