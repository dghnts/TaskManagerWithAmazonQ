#!/usr/bin/env python3
"""
シンプルなデータベースセットアップ
"""
import os
import sys
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

def setup_database():
    """データベースのセットアップ"""
    try:
        # データベーステーブル作成
        from app.database.init_db import create_tables
        create_tables()
        
        # サンプルデータ挿入
        from app.database.connection import SessionLocal
        from app.models.task import Task, TaskCategory, TaskPriority, TaskUrgency, TaskStatus
        from app.models.subtask import SubTask
        from app.models.comment import TaskComment
        from datetime import datetime, timedelta
        
        db = SessionLocal()
        
        # 既存データをクリア（開発環境のみ）
        db.query(TaskComment).delete()
        db.query(SubTask).delete()
        db.query(Task).delete()
        
        # サンプルタスクを作成
        sample_tasks = [
            Task(
                title="プロジェクト企画書作成",
                description="新規プロジェクトの企画書を作成する",
                category=TaskCategory.WORK,
                priority=TaskPriority.HIGH,
                urgency=TaskUrgency.HIGH,
                status=TaskStatus.IN_PROGRESS,
                progress=60,
                due_date=datetime.now() + timedelta(days=4),
                estimated_hours=8.0,
                actual_hours=5.0,
                notes="重要なプロジェクト"
            ),
            Task(
                title="会議資料準備",
                description="定例会議用の資料を準備する",
                category=TaskCategory.WORK,
                priority=TaskPriority.MEDIUM,
                urgency=TaskUrgency.LOW,
                status=TaskStatus.NOT_STARTED,
                progress=0,
                due_date=datetime.now() + timedelta(days=9),
                estimated_hours=2.0
            ),
            Task(
                title="React学習",
                description="React.jsの基礎学習",
                category=TaskCategory.STUDY,
                priority=TaskPriority.LOW,
                urgency=TaskUrgency.MEDIUM,
                status=TaskStatus.NOT_STARTED,
                progress=0,
                estimated_hours=20.0
            )
        ]
        
        for task in sample_tasks:
            db.add(task)
        
        db.commit()
        
        # 最初のタスクのIDを取得してサブタスクを作成
        first_task = db.query(Task).first()
        if first_task:
            subtasks = [
                SubTask(task_id=first_task.id, title="市場調査", completed=True, order_index=1),
                SubTask(task_id=first_task.id, title="企画書執筆", completed=False, order_index=2)
            ]
            for subtask in subtasks:
                db.add(subtask)
            
            # コメントも追加
            comment = TaskComment(task_id=first_task.id, content="作業開始しました")
            db.add(comment)
        
        db.commit()
        db.close()
        
        print("OK: データベースセットアップ完了!")
        print("OK: サンプルデータ挿入完了!")
        
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()