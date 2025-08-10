-- タスク管理アプリ データベース作成スクリプト
-- PostgreSQL用

-- データベース作成
CREATE DATABASE task_management_app;

-- データベースに接続
\c task_management_app;

-- UUID拡張を有効化
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ENUMタイプの定義
CREATE TYPE task_category AS ENUM ('work', 'private', 'study', 'other');
CREATE TYPE task_priority AS ENUM ('high', 'medium', 'low');
CREATE TYPE task_urgency AS ENUM ('high', 'medium', 'low');
CREATE TYPE task_status AS ENUM ('not_started', 'in_progress', 'completed', 'on_hold');

-- tasksテーブル作成
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category task_category NOT NULL,
    priority task_priority NOT NULL,
    urgency task_urgency NOT NULL,
    status task_status NOT NULL DEFAULT 'not_started',
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    
    -- スケジュール関連
    due_date TIMESTAMP,
    planned_start_date TIMESTAMP,
    planned_end_date TIMESTAMP,
    actual_start_date TIMESTAMP,
    actual_end_date TIMESTAMP,
    
    -- 時間管理
    estimated_hours FLOAT CHECK (estimated_hours >= 0),
    actual_hours FLOAT CHECK (actual_hours >= 0),
    
    -- その他
    notes TEXT,
    
    -- システム項目
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- subtasksテーブル作成
CREATE TABLE subtasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- task_commentsテーブル作成
CREATE TABLE task_comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- インデックス作成
CREATE INDEX idx_tasks_category ON tasks(category);
CREATE INDEX idx_tasks_priority_urgency ON tasks(priority, urgency);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

CREATE INDEX idx_subtasks_task_id ON subtasks(task_id);
CREATE INDEX idx_subtasks_order ON subtasks(task_id, order_index);

CREATE INDEX idx_comments_task_id ON task_comments(task_id);
CREATE INDEX idx_comments_created_at ON task_comments(created_at);

-- updated_at自動更新のトリガー関数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- tasksテーブルにupdated_at自動更新トリガーを設定
CREATE TRIGGER update_tasks_updated_at 
    BEFORE UPDATE ON tasks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- サンプルデータ挿入
INSERT INTO tasks (title, description, category, priority, urgency, status, progress, due_date, estimated_hours, notes) VALUES
('プロジェクト企画書作成', '新規プロジェクトの企画書を作成する。市場調査と競合分析を含む包括的な内容で作成予定。', 'work', 'high', 'high', 'in_progress', 60, '2024-12-25 23:59:59', 8.0, '重要なプロジェクトのため優先的に進める'),
('会議資料準備', '来週の定例会議用の資料を準備する。前回の議事録確認と今回のアジェンダ作成。', 'work', 'medium', 'low', 'not_started', 0, '2024-12-30 17:00:00', 2.0, NULL),
('React学習', 'React.jsの基礎から応用まで学習する。オンライン教材とハンズオン実習を組み合わせて進める。', 'study', 'low', 'medium', 'not_started', 0, NULL, 20.0, '継続的に学習を進める'),
('システム設計書作成', '新システムの設計書を作成する。アーキテクチャとデータベース設計を含む。', 'work', 'high', 'low', 'not_started', 0, '2025-01-15 23:59:59', 16.0, '計画的に進める重要タスク'),
('緊急バグ修正', '本番環境で発生した緊急バグの修正対応。', 'work', 'high', 'high', 'completed', 100, '2024-12-20 18:00:00', 4.0, '緊急対応完了');

-- サブタスクのサンプルデータ
INSERT INTO subtasks (task_id, title, completed, order_index) VALUES
((SELECT id FROM tasks WHERE title = 'プロジェクト企画書作成'), '市場調査', TRUE, 1),
((SELECT id FROM tasks WHERE title = 'プロジェクト企画書作成'), '競合分析', TRUE, 2),
((SELECT id FROM tasks WHERE title = 'プロジェクト企画書作成'), '企画書執筆', FALSE, 3),
((SELECT id FROM tasks WHERE title = 'プロジェクト企画書作成'), '資料作成', FALSE, 4),
((SELECT id FROM tasks WHERE title = 'React学習'), 'React基礎学習', FALSE, 1),
((SELECT id FROM tasks WHERE title = 'React学習'), 'コンポーネント作成練習', FALSE, 2),
((SELECT id FROM tasks WHERE title = 'React学習'), 'Hooks学習', FALSE, 3);

-- コメントのサンプルデータ
INSERT INTO task_comments (task_id, content) VALUES
((SELECT id FROM tasks WHERE title = 'プロジェクト企画書作成'), '市場調査完了。想定より時間がかかった。競合他社の動向も詳しく調べることができた。'),
((SELECT id FROM tasks WHERE title = 'プロジェクト企画書作成'), 'タスク開始。まずは市場調査から着手する。'),
((SELECT id FROM tasks WHERE title = '緊急バグ修正'), 'バグの原因を特定。データベースのインデックス不備が原因だった。'),
((SELECT id FROM tasks WHERE title = '緊急バグ修正'), '修正完了。本番環境にデプロイ済み。');

-- データ確認用クエリ
-- SELECT t.title, t.category, t.priority, t.urgency, t.status, t.progress, 
--        COUNT(s.id) as subtask_count, COUNT(c.id) as comment_count
-- FROM tasks t
-- LEFT JOIN subtasks s ON t.id = s.task_id
-- LEFT JOIN task_comments c ON t.id = c.task_id
-- GROUP BY t.id, t.title, t.category, t.priority, t.urgency, t.status, t.progress
-- ORDER BY t.created_at;