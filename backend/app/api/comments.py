from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.connection import get_db
from app.models.task import Task
from app.models.comment import TaskComment
from app.schemas.comment import Comment as CommentSchema, CommentCreate

router = APIRouter(tags=["comments"])

@router.get("/tasks/{task_id}/comments", response_model=List[CommentSchema])
async def get_comments(task_id: UUID, db: Session = Depends(get_db)):
    """特定タスクのコメント一覧取得"""
    # タスクの存在確認
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    comments = db.query(TaskComment).filter(TaskComment.task_id == task_id).order_by(TaskComment.created_at.desc()).all()
    return comments

@router.post("/tasks/{task_id}/comments", response_model=CommentSchema)
async def create_comment(task_id: UUID, comment: CommentCreate, db: Session = Depends(get_db)):
    """コメント作成"""
    # タスクの存在確認
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_comment = TaskComment(task_id=task_id, **comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: UUID, db: Session = Depends(get_db)):
    """コメント削除"""
    comment = db.query(TaskComment).filter(TaskComment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}