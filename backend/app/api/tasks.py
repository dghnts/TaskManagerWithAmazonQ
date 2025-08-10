from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from uuid import UUID
from datetime import datetime

from app.database.connection import get_db
from app.models.task import Task, TaskCategory, TaskPriority, TaskUrgency, TaskStatus
from app.models.subtask import SubTask
from app.models.comment import TaskComment
from app.schemas.task import (
    Task as TaskSchema, TaskCreate, TaskUpdate, TaskDetail, 
    TaskWithCounts, MatrixTask, CalendarEvent
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=dict)
async def get_tasks(
    category: Optional[TaskCategory] = None,
    priority: Optional[TaskPriority] = None,
    urgency: Optional[TaskUrgency] = None,
    status: Optional[TaskStatus] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    """タスク一覧取得"""
    query = db.query(Task)
    
    # フィルタリング
    if category:
        query = query.filter(Task.category == category)
    if priority:
        query = query.filter(Task.priority == priority)
    if urgency:
        query = query.filter(Task.urgency == urgency)
    if status:
        query = query.filter(Task.status == status)
    if search:
        query = query.filter(Task.title.contains(search))
    
    # ソート
    if sort_order == "desc":
        query = query.order_by(getattr(Task, sort_by).desc())
    else:
        query = query.order_by(getattr(Task, sort_by))
    
    # ページング
    total = query.count()
    tasks = query.offset((page - 1) * limit).limit(limit).all()
    
    # 集計情報を追加
    tasks_with_counts = []
    for task in tasks:
        subtask_count = db.query(SubTask).filter(SubTask.task_id == task.id).count()
        completed_subtasks = db.query(SubTask).filter(
            SubTask.task_id == task.id, SubTask.completed == True
        ).count()
        comment_count = db.query(TaskComment).filter(TaskComment.task_id == task.id).count()
        
        task_dict = TaskSchema.from_orm(task).dict()
        task_dict.update({
            "subtask_count": subtask_count,
            "completed_subtasks": completed_subtasks,
            "comment_count": comment_count
        })
        tasks_with_counts.append(task_dict)
    
    return {
        "tasks": tasks_with_counts,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    }

@router.post("/", response_model=TaskSchema)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """タスク作成"""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskDetail)
async def get_task(task_id: UUID, db: Session = Depends(get_db)):
    """タスク詳細取得"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """タスク更新"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    """タスク削除"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.get("/matrix", response_model=dict)
async def get_matrix_data(db: Session = Depends(get_db)):
    """マトリックス表示データ取得"""
    tasks = db.query(Task).filter(Task.status != TaskStatus.COMPLETED).all()
    
    matrix = {
        "high_high": [],
        "high_medium": [],
        "high_low": [],
        "medium_high": [],
        "medium_medium": [],
        "medium_low": [],
        "low_high": [],
        "low_medium": [],
        "low_low": []
    }
    
    for task in tasks:
        key = f"{task.priority.value}_{task.urgency.value}"
        matrix[key].append(MatrixTask.from_orm(task))
    
    # 象限別の集計
    quadrant_counts = {
        "quadrant_1": len(matrix["high_high"]),
        "quadrant_2": len(matrix["high_low"]),
        "quadrant_3": len(matrix["low_high"]),
        "quadrant_4": len(matrix["low_low"])
    }
    
    return {
        "matrix": matrix,
        "summary": {
            "total_tasks": len(tasks),
            "by_quadrant": quadrant_counts
        }
    }

@router.get("/calendar", response_model=dict)
async def get_calendar_data(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db)
):
    """カレンダー表示データ取得"""
    # 指定月のタスクを取得
    from datetime import datetime, timedelta
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    tasks = db.query(Task).filter(
        (Task.due_date.between(start_date, end_date)) |
        (Task.planned_start_date.between(start_date, end_date)) |
        (Task.actual_start_date.between(start_date, end_date))
    ).all()
    
    calendar_data: Dict[str, List[dict]] = {}
    due_count = start_count = milestone_count = 0
    
    for task in tasks:
        # 期限
        if task.due_date and start_date <= task.due_date <= end_date:
            date_key = task.due_date.strftime("%Y-%m-%d")
            if date_key not in calendar_data:
                calendar_data[date_key] = []
            calendar_data[date_key].append({
                "id": task.id,
                "title": task.title,
                "type": "due",
                "priority": task.priority,
                "urgency": task.urgency
            })
            due_count += 1
        
        # 開始予定
        if task.planned_start_date and start_date <= task.planned_start_date <= end_date:
            date_key = task.planned_start_date.strftime("%Y-%m-%d")
            if date_key not in calendar_data:
                calendar_data[date_key] = []
            calendar_data[date_key].append({
                "id": task.id,
                "title": task.title,
                "type": "start",
                "priority": task.priority,
                "urgency": task.urgency
            })
            start_count += 1
    
    return {
        "calendar_data": calendar_data,
        "summary": {
            "total_events": due_count + start_count + milestone_count,
            "due_dates": due_count,
            "start_dates": start_count,
            "milestones": milestone_count
        }
    }