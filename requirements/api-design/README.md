# API設計書

タスク管理アプリのAPI設計に関するドキュメントです。

## ファイル構成

- `api_specification.md` - API設計仕様書（詳細なエンドポイント定義）
- `openapi.yaml` - OpenAPI 3.0仕様書（Swagger UI対応）
- `README.md` - このファイル

## API概要

### 技術仕様
- **フレームワーク**: FastAPI
- **データ形式**: JSON
- **認証**: なし（個人利用想定）
- **ベースURL**: `http://localhost:8000/api/v1`

### 主要エンドポイント

#### タスク管理
- `GET /tasks` - タスク一覧取得（フィルター・ページング対応）
- `POST /tasks` - タスク作成
- `GET /tasks/{task_id}` - タスク詳細取得
- `PUT /tasks/{task_id}` - タスク更新
- `DELETE /tasks/{task_id}` - タスク削除

#### 特殊表示
- `GET /tasks/matrix` - マトリックス表示用データ
- `GET /tasks/calendar` - カレンダー表示用データ

#### サブタスク管理
- `GET /tasks/{task_id}/subtasks` - サブタスク一覧
- `POST /tasks/{task_id}/subtasks` - サブタスク作成
- `PUT /subtasks/{subtask_id}` - サブタスク更新
- `DELETE /subtasks/{subtask_id}` - サブタスク削除

#### コメント管理
- `GET /tasks/{task_id}/comments` - コメント一覧
- `POST /tasks/{task_id}/comments` - コメント作成
- `DELETE /comments/{comment_id}` - コメント削除

## 開発・テスト用ツール

### Swagger UI
OpenAPI仕様書を使用してSwagger UIでAPIドキュメントを確認できます。

```bash
# FastAPIサーバー起動後
http://localhost:8000/docs
```

### API仕様書の確認
```bash
# Swagger Editorでopenapi.yamlを開く
# または、オンラインエディタを使用
https://editor.swagger.io/
```

## 実装時の考慮事項

### パフォーマンス
- **ページング**: 大量データ対応のため必須実装
- **フィルタリング**: データベースレベルでの効率的な絞り込み
- **インデックス**: 検索頻度の高いカラムに適切なインデックス

### データ整合性
- **バリデーション**: Pydanticモデルでの入力検証
- **制約チェック**: 進捗率（0-100）、時間（>= 0）等の妥当性
- **外部キー**: 関連データの整合性保証

### エラーハンドリング
- **統一形式**: 全エンドポイントで一貫したエラーレスポンス
- **適切なHTTPステータス**: RESTful原則に従った状態コード
- **詳細情報**: バリデーションエラー時の具体的なフィールド情報

### セキュリティ
- **入力サニタイゼーション**: XSS対策
- **SQLインジェクション対策**: ORMの適切な使用
- **CORS設定**: フロントエンドからのアクセス許可

## 実装順序の推奨

### Phase 1: 基本CRUD
1. タスクの基本CRUD操作
2. バリデーションとエラーハンドリング
3. ページング機能

### Phase 2: 関連データ
1. サブタスクのCRUD操作
2. コメントのCRUD操作
3. タスク詳細取得（関連データ含む）

### Phase 3: 特殊機能
1. フィルタリング機能
2. マトリックス表示API
3. カレンダー表示API

### Phase 4: 最適化
1. パフォーマンス改善
2. キャッシュ機能
3. ログ機能

## テストケース例

### タスク作成API
```python
# 正常ケース
{
    "title": "テストタスク",
    "category": "work",
    "priority": "high",
    "urgency": "medium"
}

# バリデーションエラーケース
{
    "title": "",  # 空文字
    "category": "invalid",  # 無効な値
    "priority": "high",
    "urgency": "medium"
}
```

### フィルタリングAPI
```
GET /tasks?category=work&priority=high&page=1&limit=10
```

## 今後の拡張予定

- **認証機能**: JWT認証の追加
- **ファイルアップロード**: 添付ファイル機能
- **通知機能**: リマインダー・期限通知
- **統計機能**: タスク完了率・時間分析
- **エクスポート機能**: CSV・PDF出力

---

**作成日**: 2024年12月
**バージョン**: 1.0