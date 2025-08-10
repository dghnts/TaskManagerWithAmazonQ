# タスク管理アプリ API設計書

## 概要

FastAPIを使用したRESTful APIの設計仕様書。

### 基本情報
- **ベースURL**: `http://localhost:8000/api/v1`
- **認証**: なし（個人利用想定）
- **データ形式**: JSON
- **HTTPステータスコード**: 標準的なRESTful API仕様に準拠

## エンドポイント一覧

### タスク関連

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| GET | `/tasks` | タスク一覧取得（フィルター・ページング対応） |
| POST | `/tasks` | 新規タスク作成 |
| GET | `/tasks/{task_id}` | 特定タスクの詳細取得 |
| PUT | `/tasks/{task_id}` | タスク情報更新 |
| DELETE | `/tasks/{task_id}` | タスク削除 |
| GET | `/tasks/matrix` | マトリックス表示用データ取得 |
| GET | `/tasks/calendar` | カレンダー表示用データ取得 |

### サブタスク関連

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| GET | `/tasks/{task_id}/subtasks` | 特定タスクのサブタスク一覧取得 |
| POST | `/tasks/{task_id}/subtasks` | サブタスク作成 |
| PUT | `/subtasks/{subtask_id}` | サブタスク更新 |
| DELETE | `/subtasks/{subtask_id}` | サブタスク削除 |

### コメント関連

| メソッド | エンドポイント | 説明 |
|---------|---------------|------|
| GET | `/tasks/{task_id}/comments` | 特定タスクのコメント一覧取得 |
| POST | `/tasks/{task_id}/comments` | コメント作成 |
| DELETE | `/comments/{comment_id}` | コメント削除 |

## 詳細仕様

### GET /tasks

タスク一覧を取得する。フィルタリングとページングに対応。

#### クエリパラメータ

| パラメータ | 型 | 必須 | 説明 | デフォルト |
|-----------|---|------|------|----------|
| category | string | No | カテゴリフィルター (work, private, study, other) | - |
| priority | string | No | 優先度フィルター (high, medium, low) | - |
| urgency | string | No | 緊急度フィルター (high, medium, low) | - |
| status | string | No | ステータスフィルター (not_started, in_progress, completed, on_hold) | - |
| search | string | No | タスク名・説明での検索 | - |
| page | integer | No | ページ番号 | 1 |
| limit | integer | No | 1ページあたりの件数 | 20 |
| sort_by | string | No | ソート項目 (created_at, due_date, priority, urgency) | created_at |
| sort_order | string | No | ソート順 (asc, desc) | desc |

#### レスポンス例

```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "プロジェクト企画書作成",
      "description": "新規プロジェクトの企画書を作成する",
      "category": "work",
      "priority": "high",
      "urgency": "high",
      "status": "in_progress",
      "progress": 60,
      "due_date": "2024-12-25T23:59:59Z",
      "planned_start_date": "2024-12-20T09:00:00Z",
      "planned_end_date": "2024-12-25T18:00:00Z",
      "actual_start_date": "2024-12-21T10:00:00Z",
      "actual_end_date": null,
      "estimated_hours": 8.0,
      "actual_hours": 5.0,
      "notes": "重要なプロジェクトのため優先的に進める",
      "created_at": "2024-12-20T09:00:00Z",
      "updated_at": "2024-12-21T15:30:00Z",
      "subtask_count": 4,
      "completed_subtasks": 2,
      "comment_count": 2
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5,
    "total_pages": 1
  }
}
```

### POST /tasks

新規タスクを作成する。

#### リクエストボディ

```json
{
  "title": "新しいタスク",
  "description": "タスクの詳細説明",
  "category": "work",
  "priority": "high",
  "urgency": "medium",
  "due_date": "2024-12-30T23:59:59Z",
  "planned_start_date": "2024-12-25T09:00:00Z",
  "planned_end_date": "2024-12-30T18:00:00Z",
  "estimated_hours": 10.0,
  "notes": "メモ"
}
```

#### レスポンス例

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174001",
  "title": "新しいタスク",
  "description": "タスクの詳細説明",
  "category": "work",
  "priority": "high",
  "urgency": "medium",
  "status": "not_started",
  "progress": 0,
  "due_date": "2024-12-30T23:59:59Z",
  "planned_start_date": "2024-12-25T09:00:00Z",
  "planned_end_date": "2024-12-30T18:00:00Z",
  "actual_start_date": null,
  "actual_end_date": null,
  "estimated_hours": 10.0,
  "actual_hours": 0.0,
  "notes": "メモ",
  "created_at": "2024-12-21T10:00:00Z",
  "updated_at": "2024-12-21T10:00:00Z"
}
```

### GET /tasks/{task_id}

特定タスクの詳細情報を取得する。

#### レスポンス例

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "プロジェクト企画書作成",
  "description": "新規プロジェクトの企画書を作成する",
  "category": "work",
  "priority": "high",
  "urgency": "high",
  "status": "in_progress",
  "progress": 60,
  "due_date": "2024-12-25T23:59:59Z",
  "planned_start_date": "2024-12-20T09:00:00Z",
  "planned_end_date": "2024-12-25T18:00:00Z",
  "actual_start_date": "2024-12-21T10:00:00Z",
  "actual_end_date": null,
  "estimated_hours": 8.0,
  "actual_hours": 5.0,
  "notes": "重要なプロジェクトのため優先的に進める",
  "created_at": "2024-12-20T09:00:00Z",
  "updated_at": "2024-12-21T15:30:00Z",
  "subtasks": [
    {
      "id": "subtask-1",
      "title": "市場調査",
      "completed": true,
      "order_index": 1,
      "created_at": "2024-12-20T09:00:00Z"
    },
    {
      "id": "subtask-2",
      "title": "競合分析",
      "completed": true,
      "order_index": 2,
      "created_at": "2024-12-20T09:00:00Z"
    }
  ],
  "comments": [
    {
      "id": "comment-1",
      "content": "市場調査完了。想定より時間がかかった。",
      "created_at": "2024-12-21T15:30:00Z"
    }
  ]
}
```

### PUT /tasks/{task_id}

タスク情報を更新する。

#### リクエストボディ

```json
{
  "title": "更新されたタスク名",
  "description": "更新された説明",
  "category": "work",
  "priority": "medium",
  "urgency": "high",
  "status": "in_progress",
  "progress": 75,
  "due_date": "2024-12-26T23:59:59Z",
  "actual_start_date": "2024-12-21T10:00:00Z",
  "actual_hours": 6.0,
  "notes": "更新されたメモ"
}
```

### GET /tasks/matrix

マトリックス表示用のデータを取得する。

#### レスポンス例

```json
{
  "matrix": {
    "high_high": [
      {
        "id": "task-1",
        "title": "緊急バグ修正",
        "priority": "high",
        "urgency": "high",
        "status": "in_progress",
        "progress": 80
      }
    ],
    "high_medium": [],
    "high_low": [
      {
        "id": "task-2",
        "title": "システム設計書作成",
        "priority": "high",
        "urgency": "low",
        "status": "not_started",
        "progress": 0
      }
    ],
    "medium_high": [],
    "medium_medium": [],
    "medium_low": [],
    "low_high": [
      {
        "id": "task-3",
        "title": "会議資料準備",
        "priority": "low",
        "urgency": "high",
        "status": "not_started",
        "progress": 0
      }
    ],
    "low_medium": [],
    "low_low": []
  },
  "summary": {
    "total_tasks": 3,
    "by_quadrant": {
      "quadrant_1": 1,
      "quadrant_2": 1,
      "quadrant_3": 1,
      "quadrant_4": 0
    }
  }
}
```

### GET /tasks/calendar

カレンダー表示用のデータを取得する。

#### クエリパラメータ

| パラメータ | 型 | 必須 | 説明 |
|-----------|---|------|------|
| year | integer | Yes | 年 |
| month | integer | Yes | 月 |

#### レスポンス例

```json
{
  "calendar_data": {
    "2024-12-20": [
      {
        "id": "task-1",
        "title": "プロジェクト企画書作成",
        "type": "start",
        "priority": "high",
        "urgency": "high"
      }
    ],
    "2024-12-25": [
      {
        "id": "task-1",
        "title": "プロジェクト企画書作成",
        "type": "due",
        "priority": "high",
        "urgency": "high"
      },
      {
        "id": "task-2",
        "title": "会議資料準備",
        "type": "start",
        "priority": "medium",
        "urgency": "low"
      }
    ]
  },
  "summary": {
    "total_events": 3,
    "due_dates": 1,
    "start_dates": 2,
    "milestones": 0
  }
}
```

### POST /tasks/{task_id}/subtasks

サブタスクを作成する。

#### リクエストボディ

```json
{
  "title": "新しいサブタスク",
  "order_index": 3
}
```

#### レスポンス例

```json
{
  "id": "subtask-3",
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "新しいサブタスク",
  "completed": false,
  "order_index": 3,
  "created_at": "2024-12-21T16:00:00Z"
}
```

### PUT /subtasks/{subtask_id}

サブタスクを更新する。

#### リクエストボディ

```json
{
  "title": "更新されたサブタスク",
  "completed": true,
  "order_index": 2
}
```

### POST /tasks/{task_id}/comments

コメントを作成する。

#### リクエストボディ

```json
{
  "content": "新しいコメント内容"
}
```

#### レスポンス例

```json
{
  "id": "comment-2",
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "content": "新しいコメント内容",
  "created_at": "2024-12-21T16:30:00Z"
}
```

## エラーレスポンス

### 標準エラー形式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力データが無効です",
    "details": [
      {
        "field": "title",
        "message": "タスク名は必須です"
      }
    ]
  }
}
```

### HTTPステータスコード

| コード | 説明 | 使用場面 |
|-------|------|----------|
| 200 | OK | 正常な取得・更新 |
| 201 | Created | 正常な作成 |
| 400 | Bad Request | リクエストデータの不正 |
| 404 | Not Found | リソースが見つからない |
| 422 | Unprocessable Entity | バリデーションエラー |
| 500 | Internal Server Error | サーバー内部エラー |

## データモデル

### Task

```json
{
  "id": "string (UUID)",
  "title": "string (max: 100)",
  "description": "string (optional)",
  "category": "enum (work, private, study, other)",
  "priority": "enum (high, medium, low)",
  "urgency": "enum (high, medium, low)",
  "status": "enum (not_started, in_progress, completed, on_hold)",
  "progress": "integer (0-100)",
  "due_date": "string (ISO 8601, optional)",
  "planned_start_date": "string (ISO 8601, optional)",
  "planned_end_date": "string (ISO 8601, optional)",
  "actual_start_date": "string (ISO 8601, optional)",
  "actual_end_date": "string (ISO 8601, optional)",
  "estimated_hours": "number (optional)",
  "actual_hours": "number (optional)",
  "notes": "string (optional)",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)"
}
```

### SubTask

```json
{
  "id": "string (UUID)",
  "task_id": "string (UUID)",
  "title": "string (max: 200)",
  "completed": "boolean",
  "order_index": "integer",
  "created_at": "string (ISO 8601)"
}
```

### Comment

```json
{
  "id": "string (UUID)",
  "task_id": "string (UUID)",
  "content": "string",
  "created_at": "string (ISO 8601)"
}
```

---

**最終更新**: 2024年12月
**バージョン**: 1.0