from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.connection import get_db
from app.models.task import Task
from app.models.subtask import SubTask
from app.schemas.subtask import SubTask as SubTaskSchema, SubTaskCreate, SubTaskUpdate

router = APIRouter(tags=["subtasks"])

@router.get("/tasks/{task_id}/subtasks", response_model=List[SubTaskSchema])
async def get_subtasks(task_id: UUID, db: Session = Depends(get_db)):
    """特定タスクのサブタスク一覧取得"""
    # タスクの存在確認
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    subtasks = db.query(SubTask).filter(SubTask.task_id == task_id).order_by(SubTask.order_index).all()
    return subtasks

@router.post("/tasks/{task_id}/subtasks", response_model=SubTaskSchema)
async def create_subtask(task_id: UUID, subtask: SubTaskCreate, db: Session = Depends(get_db)):
    """サブタスク作成"""
    # タスクの存在確認
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_subtask = SubTask(task_id=task_id, **subtask.dict())
    db.add(db_subtask)
    db.commit()
    db.refresh(db_subtask)
    return db_subtask

@router.put("/subtasks/{subtask_id}", response_model=SubTaskSchema)
async def update_subtask(subtask_id: UUID, subtask_update: SubTaskUpdate, db: Session = Depends(get_db)):
    """サブタスク更新"""
    subtask = db.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    update_data = subtask_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subtask, field, value)
    
    db.commit()
    db.refresh(subtask)
    return subtask

@router.delete("/subtasks/{subtask_id}")
async def delete_subtask(subtask_id: UUID, db: Session = Depends(get_db)):
    """サブタスク削除"""
    subtask = db.query(SubTask).filter(SubTask.id == subtask_id).first()
    if not subtask:
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    db.delete(subtask)
    db.commit()
    return {"message": "Subtask deleted successfully"}