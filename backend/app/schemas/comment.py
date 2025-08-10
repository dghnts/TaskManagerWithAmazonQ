from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

# ベーススキーマ
class CommentBase(BaseModel):
    content: str

# コメント作成用
class CommentCreate(CommentBase):
    pass

# レスポンス用
class Comment(CommentBase):
    id: UUID
    task_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True