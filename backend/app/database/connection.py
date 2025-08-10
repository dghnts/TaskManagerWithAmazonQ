from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# データベースURL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/task_management_app")

# SQLAlchemyエンジンの作成
engine = create_engine(DATABASE_URL)

# セッションローカルクラス
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス
Base = declarative_base()

# データベースセッションの依存性注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()