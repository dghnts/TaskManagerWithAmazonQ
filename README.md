# タスク管理アプリ

個人のタスクを優先度や緊急度で分類し、効率的なタスク管理を行うことができるアプリケーション

## 機能

- タスクのCRUD機能
- タスクごとの優先度管理機能
- タスクごとの緊急度管理機能
- タスクの緊急度と優先度に基づいたマトリックス表示
- タスクの種別・優先度・緊急度に応じたフィルタリング

## 技術スタック

### フロントエンド
- **React.js** - UIライブラリ
- **Material-UI** - UIコンポーネントライブラリ
- **React Router** - ルーティング
- **Axios** - HTTP通信

### バックエンド
- **FastAPI** - Webフレームワーク
- **SQLAlchemy** - ORM
- **PostgreSQL** - データベース
- **Alembic** - データベースマイグレーション

## プロジェクト構成

```
TaskManager/
├── backend/                # FastAPI バックエンド
│   ├── app/
│   │   ├── api/           # APIエンドポイント
│   │   ├── models/        # データベースモデル
│   │   ├── schemas/       # Pydanticスキーマ
│   │   └── database/      # データベース設定
│   ├── main.py            # FastAPIアプリケーション
│   └── requirements.txt   # Python依存関係
├── frontend/              # React フロントエンド
│   ├── src/
│   │   ├── components/    # Reactコンポーネント
│   │   ├── pages/         # ページコンポーネント
│   │   └── services/      # API通信
│   └── package.json       # Node.js依存関係
└── requirements/          # 要件定義関連
    ├── database-design/   # データベース設計書
    ├── api-design/        # API設計書
    ├── layout-design/     # 画面設計・モックアップ
    └── 要件定義書_タスク管理アプリ.md
```

## セットアップ

### 前提条件
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+

### バックエンドセットアップ

1. 仮想環境の作成と有効化
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

3. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集してデータベース接続情報を設定
```

4. データベースの作成
```bash
# PostgreSQLでデータベースを作成
createdb task_management_app
```

5. サーバー起動
```bash
python main.py
```

### フロントエンドセットアップ

1. 依存関係のインストール
```bash
cd frontend
npm install
```

2. 開発サーバー起動
```bash
npm start
```

## 開発状況

- ✅ 要件定義
- ✅ 画面設計（HTMLモックアップ）
- ✅ データベース設計
- ✅ API設計
- ✅ プロジェクト初期化
- 🚧 バックエンド実装
- 🚧 フロントエンド実装

## ドキュメント

- [要件定義書](requirements/要件定義書_タスク管理アプリ.md)
- [データベース設計書](requirements/database-design/)
- [API設計書](requirements/api-design/)
- [画面設計書](requirements/layout-design/)

## API ドキュメント

バックエンドサーバー起動後、以下のURLでSwagger UIを確認できます：
- http://localhost:8000/docs

## 開発・テスト

### バックエンドテスト
```bash
cd backend
pytest
```

### フロントエンドテスト
```bash
cd frontend
npm test
```

## ライセンス

このプロジェクトは個人利用目的で作成されています。