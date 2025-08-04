# データベーススキーマ定義書

## 概要

タスク管理アプリのデータベーススキーマ定義。PostgreSQLを使用し、3つのメインテーブルで構成。

## テーブル一覧

| テーブル名 | 説明 | 関連 |
|-----------|------|------|
| tasks | メインのタスク情報 | 1:N → subtasks, task_comments |
| subtasks | サブタスク・チェックリスト | N:1 ← tasks |
| task_comments | タスクに対するコメント | N:1 ← tasks |

## ENUM型定義

### task_category
```sql
CREATE TYPE task_category AS ENUM ('work', 'private', 'study', 'other');
```
- `work` - 仕事
- `private` - プライベート  
- `study` - 学習
- `other` - その他

### task_priority
```sql
CREATE TYPE task_priority AS ENUM ('high', 'medium', 'low');
```
- `high` - 高
- `medium` - 中
- `low` - 低

### task_urgency
```sql
CREATE TYPE task_urgency AS ENUM ('high', 'medium', 'low');
```
- `high` - 高（⚡）
- `medium` - 中（⏰）
- `low` - 低（📅）

### task_status
```sql
CREATE TYPE task_status AS ENUM ('not_started', 'in_progress', 'completed', 'on_hold');
```
- `not_started` - 未着手
- `in_progress` - 進行中
- `completed` - 完了
- `on_hold` - 保留

## テーブル定義

### tasks テーブル

メインのタスク情報を格納するテーブル。

| カラム名 | データ型 | 制約 | デフォルト値 | 説明 |
|---------|---------|------|-------------|------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid_generate_v4() | タスクの一意識別子 |
| title | VARCHAR(100) | NOT NULL | - | タスク名 |
| description | TEXT | - | - | タスクの詳細説明 |
| category | task_category | NOT NULL | - | タスクの種別 |
| priority | task_priority | NOT NULL | - | 優先度 |
| urgency | task_urgency | NOT NULL | - | 緊急度 |
| status | task_status | NOT NULL | 'not_started' | タスクのステータス |
| progress | INTEGER | CHECK (0-100) | 0 | 進捗率（0-100） |
| due_date | TIMESTAMP | - | - | 期限日時 |
| planned_start_date | TIMESTAMP | - | - | 開始予定日時 |
| planned_end_date | TIMESTAMP | - | - | 終了予定日時 |
| actual_start_date | TIMESTAMP | - | - | 実際の開始日時 |
| actual_end_date | TIMESTAMP | - | - | 実際の終了日時 |
| estimated_hours | FLOAT | CHECK (>= 0) | - | 見積時間 |
| actual_hours | FLOAT | CHECK (>= 0) | - | 実績時間 |
| notes | TEXT | - | - | メモ・備考 |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | 更新日時 |

#### インデックス
- `idx_tasks_category` - category
- `idx_tasks_priority_urgency` - priority, urgency
- `idx_tasks_status` - status
- `idx_tasks_due_date` - due_date
- `idx_tasks_created_at` - created_at

#### トリガー
- `update_tasks_updated_at` - updated_at自動更新

### subtasks テーブル

サブタスク・チェックリスト情報を格納するテーブル。

| カラム名 | データ型 | 制約 | デフォルト値 | 説明 |
|---------|---------|------|-------------|------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid_generate_v4() | サブタスクの一意識別子 |
| task_id | UUID | FOREIGN KEY, NOT NULL | - | 親タスクのID |
| title | VARCHAR(200) | NOT NULL | - | サブタスク名 |
| completed | BOOLEAN | NOT NULL | FALSE | 完了フラグ |
| order_index | INTEGER | NOT NULL | - | 表示順序 |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | 作成日時 |

#### 外部キー制約
- `task_id` REFERENCES `tasks(id)` ON DELETE CASCADE

#### インデックス
- `idx_subtasks_task_id` - task_id
- `idx_subtasks_order` - task_id, order_index

### task_comments テーブル

タスクに対するコメント情報を格納するテーブル。

| カラム名 | データ型 | 制約 | デフォルト値 | 説明 |
|---------|---------|------|-------------|------|
| id | UUID | PRIMARY KEY, NOT NULL | uuid_generate_v4() | コメントの一意識別子 |
| task_id | UUID | FOREIGN KEY, NOT NULL | - | 対象タスクのID |
| content | TEXT | NOT NULL | - | コメント内容 |
| created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | 作成日時 |

#### 外部キー制約
- `task_id` REFERENCES `tasks(id)` ON DELETE CASCADE

#### インデックス
- `idx_comments_task_id` - task_id
- `idx_comments_created_at` - created_at

## リレーション

```
tasks (1) ----< subtasks (N)
  |
  +----------< task_comments (N)
```

- 1つのタスクは複数のサブタスクを持つ（1:N）
- 1つのタスクは複数のコメントを持つ（1:N）
- タスク削除時、関連するサブタスクとコメントも削除される（CASCADE）

## 主要クエリパターン

### タスク一覧取得（フィルター付き）
```sql
SELECT * FROM tasks 
WHERE category = $1 
  AND status != 'completed'
ORDER BY priority DESC, urgency DESC, due_date ASC;
```

### マトリックス表示用データ
```sql
SELECT priority, urgency, COUNT(*) as task_count
FROM tasks 
WHERE status != 'completed'
GROUP BY priority, urgency;
```

### タスク詳細（関連データ含む）
```sql
SELECT t.*, 
       COALESCE(s.subtask_count, 0) as subtask_count,
       COALESCE(s.completed_count, 0) as completed_subtasks,
       COALESCE(c.comment_count, 0) as comment_count
FROM tasks t
LEFT JOIN (
    SELECT task_id, 
           COUNT(*) as subtask_count,
           COUNT(CASE WHEN completed THEN 1 END) as completed_count
    FROM subtasks 
    GROUP BY task_id
) s ON t.id = s.task_id
LEFT JOIN (
    SELECT task_id, COUNT(*) as comment_count
    FROM task_comments 
    GROUP BY task_id
) c ON t.id = c.task_id
WHERE t.id = $1;
```

### サブタスク一覧取得
```sql
SELECT * FROM subtasks 
WHERE task_id = $1 
ORDER BY order_index;
```

### コメント一覧取得
```sql
SELECT * FROM task_comments 
WHERE task_id = $1 
ORDER BY created_at DESC;
```

## パフォーマンス考慮事項

### インデックス戦略
- **category**: フィルタリング頻度が高い
- **priority, urgency**: マトリックス表示で複合検索
- **status**: ステータス別表示で使用
- **due_date**: 期限順ソートで使用
- **task_id**: 外部キーでJOIN頻度が高い

### クエリ最適化
- サブタスク・コメント数の集計はサブクエリで事前計算
- 大量データ対応のためページネーション実装
- 不要なカラムは SELECT で除外

## データ整合性

### 制約
- **CHECK制約**: progress (0-100), estimated_hours/actual_hours (>= 0)
- **外部キー制約**: CASCADE削除でデータ一貫性保証
- **NOT NULL制約**: 必須項目の保証

### トリガー
- **updated_at自動更新**: データ更新時に自動でタイムスタンプ更新

## 拡張予定

### 将来追加予定のテーブル
- **users** - ユーザー管理
- **task_dependencies** - タスク間依存関係
- **task_attachments** - 添付ファイル
- **notifications** - 通知設定

### 追加予定のカラム
- **tasks.assigned_user_id** - 担当者
- **tasks.estimated_completion_date** - 完了予定日
- **subtasks.assigned_user_id** - サブタスク担当者

---

**最終更新**: 2024年12月
**バージョン**: 1.0