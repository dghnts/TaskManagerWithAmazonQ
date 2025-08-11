from pydantic import BaseModel
from datetime import datetime


# ベーススキーマ
class CommentBase(BaseModel):
    content: str

# コメント作成用
class CommentCreate(CommentBase):
    pass

# レスポンス用
class Comment(CommentBase):
    id: str
    task_id: str
    created_at: datetime

    class Config:
        from_attributes = True