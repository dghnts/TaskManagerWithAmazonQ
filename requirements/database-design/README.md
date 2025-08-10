# データベース設計書

タスク管理アプリのデータベース設計に関するドキュメントです。

## ファイル構成

- `database_design.html` - 視覚的なデータベース設計書（ER図・テーブル定義）
- `create_tables.sql` - PostgreSQL用テーブル作成スクリプト
- `README.md` - このファイル

## データベース概要

### 使用技術
- **データベース**: PostgreSQL 14+
- **主要機能**: UUID主キー、ENUM型、トリガー、インデックス

### テーブル構成
1. **tasks** - メインのタスク情報
2. **subtasks** - サブタスク・チェックリスト
3. **task_comments** - タスクに対するコメント

## 設計のポイント

### 1. 正規化
- 第3正規形まで正規化
- 適切な外部キー制約でデータ整合性を保証

### 2. パフォーマンス
- 検索頻度の高いカラムにインデックス設定
- 複合インデックスでマトリックス表示を最適化

### 3. 拡張性
- UUID使用で分散環境対応
- ENUM型で値の制約とパフォーマンス両立
- トリガーによる自動更新機能

### 4. データ整合性
- CHECK制約で進捗率や時間の妥当性チェック
- CASCADE削除でデータの一貫性保証

## セットアップ手順

1. PostgreSQLサーバーの準備
2. `create_tables.sql`を実行
3. サンプルデータが自動挿入される

```bash
psql -U postgres -f create_tables.sql
```

## 主要クエリ例

### タスク一覧取得（フィルター付き）
```sql
SELECT * FROM tasks 
WHERE category = 'work' 
  AND status != 'completed'
ORDER BY priority DESC, urgency DESC, due_date ASC;
```

### マトリックス表示用データ取得
```sql
SELECT priority, urgency, COUNT(*) as task_count
FROM tasks 
WHERE status != 'completed'
GROUP BY priority, urgency;
```

### タスク詳細（サブタスク・コメント含む）
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

## 今後の拡張予定

- ユーザー管理テーブルの追加
- タスク間の依存関係テーブル
- 添付ファイル管理テーブル
- 通知設定テーブル

---

**作成日**: 2024年12月
**バージョン**: 1.0