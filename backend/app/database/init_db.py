from app.database.connection import engine, Base
from app.models.task import Task
from app.models.subtask import SubTask
from app.models.comment import TaskComment

def create_tables():
    """データベーステーブルを作成"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def drop_tables():
    """データベーステーブルを削除"""
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped successfully!")

if __name__ == "__main__":
    create_tables()