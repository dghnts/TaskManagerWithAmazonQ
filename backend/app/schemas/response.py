from pydantic import BaseModel
from typing import List, Dict, Any

# ページング用レスポンス
class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int

# タスク一覧レスポンス
class TaskListResponse(BaseModel):
    tasks: List[Dict[str, Any]]
    pagination: PaginationResponse

# マトリックス表示レスポンス
class MatrixResponse(BaseModel):
    matrix: Dict[str, List[Dict[str, Any]]]
    summary: Dict[str, Any]

# カレンダー表示レスポンス
class CalendarResponse(BaseModel):
    calendar_data: Dict[str, List[Dict[str, Any]]]
    summary: Dict[str, int]

# エラーレスポンス
class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    error: Dict[str, Any]