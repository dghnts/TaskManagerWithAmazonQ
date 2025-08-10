# バックエンドセットアップガイド

## 前提条件

- Python 3.9+
- PostgreSQL 14+

## セットアップ手順

### 1. 仮想環境の有効化

```bash
# プロジェクトルートから
venv\Scripts\activate  # Windows
```

### 2. 依存関係のインストール

```bash
cd backend
pip install -r requirements.txt
```

### 3. PostgreSQLデータベースの作成

```sql
-- PostgreSQLに接続して実行
CREATE DATABASE task_management_app;
CREATE USER taskuser WITH PASSWORD 'taskpass';
GRANT ALL PRIVILEGES ON DATABASE task_management_app TO taskuser;
```

### 4. 環境変数の設定

`.env`ファイルを編集してデータベース接続情報を設定:

```env
DATABASE_URL=postgresql://taskuser:taskpass@localhost:5432/task_management_app
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
CORS_ORIGINS=http://localhost:3000
```

### 5. データベースセットアップ

```bash
python setup_db.py
```

### 6. FastAPIサーバー起動

```bash
python main.py
```

サーバーが起動したら以下のURLでアクセス可能:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 7. APIテスト実行

別のターミナルで:

```bash
python test_api.py
```

または Windows の場合:

```bash
run_tests.bat
```

## トラブルシューティング

### データベース接続エラー

1. PostgreSQLサービスが起動していることを確認
2. データベースとユーザーが作成されていることを確認
3. `.env`ファイルの接続情報が正しいことを確認

### モジュールインポートエラー

```bash
# Pythonパスの設定
set PYTHONPATH=%PYTHONPATH%;.  # Windows
export PYTHONPATH=$PYTHONPATH:.  # Linux/Mac
```

### ポート使用中エラー

```bash
# ポート8000が使用中の場合、別のポートを使用
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## API エンドポイント一覧

### タスク管理
- `GET /api/v1/tasks` - タスク一覧
- `POST /api/v1/tasks` - タスク作成
- `GET /api/v1/tasks/{id}` - タスク詳細
- `PUT /api/v1/tasks/{id}` - タスク更新
- `DELETE /api/v1/tasks/{id}` - タスク削除

### 特殊表示
- `GET /api/v1/tasks/matrix` - マトリックス表示
- `GET /api/v1/tasks/calendar` - カレンダー表示

### サブタスク
- `GET /api/v1/tasks/{id}/subtasks` - サブタスク一覧
- `POST /api/v1/tasks/{id}/subtasks` - サブタスク作成
- `PUT /api/v1/subtasks/{id}` - サブタスク更新
- `DELETE /api/v1/subtasks/{id}` - サブタスク削除

### コメント
- `GET /api/v1/tasks/{id}/comments` - コメント一覧
- `POST /api/v1/tasks/{id}/comments` - コメント作成
- `DELETE /api/v1/comments/{id}` - コメント削除