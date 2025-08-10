#!/usr/bin/env python3
"""
データベースセットアップスクリプト
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
                description="新規プロジェクトの企画書を作成する。市場調査と競合分析を含む包括的な内容で作成予定。",
                category=TaskCategory.WORK,
                priority=TaskPriority.HIGH,
                urgency=TaskUrgency.HIGH,
                status=TaskStatus.IN_PROGRESS,
                progress=60,
                due_date=datetime.now() + timedelta(days=4),
                planned_start_date=datetime.now() - timedelta(days=1),
                estimated_hours=8.0,
                actual_hours=5.0,
                notes="重要なプロジェクトのため優先的に進める"
            ),
            Task(
                title="会議資料準備",
                description="来週の定例会議用の資料を準備する。前回の議事録確認と今回のアジェンダ作成。",
                category=TaskCategory.WORK,
                priority=TaskPriority.MEDIUM,
                urgency=TaskUrgency.LOW,
                status=TaskStatus.NOT_STARTED,
                progress=0,
                due_date=datetime.now() + timedelta(days=9),
                estimated_hours=2.0,
                notes=None
            ),
            Task(
                title="React学習",
                description="React.jsの基礎から応用まで学習する。オンライン教材とハンズオン実習を組み合わせて進める。",
                category=TaskCategory.STUDY,
                priority=TaskPriority.LOW,
                urgency=TaskUrgency.MEDIUM,
                status=TaskStatus.NOT_STARTED,
                progress=0,
                estimated_hours=20.0,
                notes="継続的に学習を進める"
            ),
            Task(
                title="システム設計書作成",
                description="新システムの設計書を作成する。アーキテクチャとデータベース設計を含む。",
                category=TaskCategory.WORK,
                priority=TaskPriority.HIGH,
                urgency=TaskUrgency.LOW,
                status=TaskStatus.NOT_STARTED,
                progress=0,
                due_date=datetime.now() + timedelta(days=25),
                estimated_hours=16.0,
                notes="計画的に進める重要タスク"
            ),
            Task(
                title="緊急バグ修正",
                description="本番環境で発生した緊急バグの修正対応。",
                category=TaskCategory.WORK,
                priority=TaskPriority.HIGH,
                urgency=TaskUrgency.HIGH,
                status=TaskStatus.COMPLETED,
                progress=100,
                due_date=datetime.now() - timedelta(days=1),
                actual_start_date=datetime.now() - timedelta(days=2),
                actual_end_date=datetime.now() - timedelta(days=1),
                estimated_hours=4.0,
                actual_hours=3.5,
                notes="緊急対応完了"
            )
        ]
        
        for task in sample_tasks:
            db.add(task)
        
        db.commit()
        
        # サンプルサブタスクを作成
        task1 = db.query(Task).filter(Task.title == "プロジェクト企画書作成").first()
        if task1:
            subtasks = [
                SubTask(task_id=task1.id, title="市場調査", completed=True, order_index=1),
                SubTask(task_id=task1.id, title="競合分析", completed=True, order_index=2),
                SubTask(task_id=task1.id, title="企画書執筆", completed=False, order_index=3),
                SubTask(task_id=task1.id, title="資料作成", completed=False, order_index=4)
            ]
            for subtask in subtasks:
                db.add(subtask)
        
        task3 = db.query(Task).filter(Task.title == "React学習").first()
        if task3:
            subtasks = [
                SubTask(task_id=task3.id, title="React基礎学習", completed=False, order_index=1),
                SubTask(task_id=task3.id, title="コンポーネント作成練習", completed=False, order_index=2),
                SubTask(task_id=task3.id, title="Hooks学習", completed=False, order_index=3)
            ]
            for subtask in subtasks:
                db.add(subtask)
        
        # サンプルコメントを作成
        if task1:
            comments = [
                TaskComment(task_id=task1.id, content="市場調査完了。想定より時間がかかった。競合他社の動向も詳しく調べることができた。"),
                TaskComment(task_id=task1.id, content="タスク開始。まずは市場調査から着手する。")
            ]
            for comment in comments:
                db.add(comment)
        
        task5 = db.query(Task).filter(Task.title == "緊急バグ修正").first()
        if task5:
            comments = [
                TaskComment(task_id=task5.id, content="バグの原因を特定。データベースのインデックス不備が原因だった。"),
                TaskComment(task_id=task5.id, content="修正完了。本番環境にデプロイ済み。")
            ]
            for comment in comments:
                db.add(comment)
        
        db.commit()
        db.close()
        
        print("✅ データベースセットアップ完了!")
        print("✅ サンプルデータ挿入完了!")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()