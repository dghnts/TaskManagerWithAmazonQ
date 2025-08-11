#!/usr/bin/env python3
"""
サンプルデータの優先度・緊急度確認
"""
from app.database.connection import SessionLocal
from app.models.task import Task

def check_sample_data():
    db = SessionLocal()
    
    tasks = db.query(Task).all()
    print(f"Total tasks: {len(tasks)}")
    print()
    
    for task in tasks:
        print(f"Task: {task.title}")
        print(f"  Priority: {task.priority.value}")
        print(f"  Urgency: {task.urgency.value}")
        print(f"  Status: {task.status.value}")
        print(f"  Matrix Key: {task.priority.value}_{task.urgency.value}")
        print()
    
    db.close()

if __name__ == "__main__":
    check_sample_data()