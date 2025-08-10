from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # アプリケーション起動時の処理
    print("Starting Task Management API...")
    yield
    # アプリケーション終了時の処理
    print("Shutting down Task Management API...")

# FastAPIアプリケーションの作成
app = FastAPI(
    title="タスク管理アプリ API",
    description="個人用タスク管理アプリケーションのRESTful API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS設定
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "Task Management API", "version": "1.0.0"}

# ヘルスチェック
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )