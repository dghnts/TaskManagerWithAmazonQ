#!/usr/bin/env python3
"""
API テストスクリプト
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """ヘルスチェックテスト"""
    print("🔍 ヘルスチェックテスト...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_tasks_list():
    """タスク一覧取得テスト"""
    print("🔍 タスク一覧取得テスト...")
    response = requests.get(f"{BASE_URL}/api/v1/tasks")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"取得タスク数: {len(data['tasks'])}")
        print(f"ページング: {data['pagination']}")
        if data['tasks']:
            print(f"最初のタスク: {data['tasks'][0]['title']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_task_create():
    """タスク作成テスト"""
    print("🔍 タスク作成テスト...")
    new_task = {
        "title": "APIテスト用タスク",
        "description": "APIテストで作成されたタスク",
        "category": "work",
        "priority": "medium",
        "urgency": "low",
        "estimated_hours": 1.0,
        "notes": "テスト用"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/tasks", json=new_task)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        task = response.json()
        print(f"作成されたタスク ID: {task['id']}")
        print(f"タスク名: {task['title']}")
        return task['id']
    else:
        print(f"Error: {response.text}")
        return None
    print()

def test_task_detail(task_id):
    """タスク詳細取得テスト"""
    print(f"🔍 タスク詳細取得テスト (ID: {task_id})...")
    response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        task = response.json()
        print(f"タスク名: {task['title']}")
        print(f"サブタスク数: {len(task.get('subtasks', []))}")
        print(f"コメント数: {len(task.get('comments', []))}")
    else:
        print(f"Error: {response.text}")
    print()

def test_subtask_create(task_id):
    """サブタスク作成テスト"""
    print(f"🔍 サブタスク作成テスト (Task ID: {task_id})...")
    new_subtask = {
        "title": "テスト用サブタスク",
        "order_index": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/tasks/{task_id}/subtasks", json=new_subtask)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        subtask = response.json()
        print(f"作成されたサブタスク ID: {subtask['id']}")
        print(f"サブタスク名: {subtask['title']}")
        return subtask['id']
    else:
        print(f"Error: {response.text}")
        return None
    print()

def test_comment_create(task_id):
    """コメント作成テスト"""
    print(f"🔍 コメント作成テスト (Task ID: {task_id})...")
    new_comment = {
        "content": "APIテストで作成されたコメントです。"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/tasks/{task_id}/comments", json=new_comment)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        comment = response.json()
        print(f"作成されたコメント ID: {comment['id']}")
        print(f"コメント内容: {comment['content']}")
        return comment['id']
    else:
        print(f"Error: {response.text}")
        return None
    print()

def test_matrix_data():
    """マトリックス表示データテスト"""
    print("🔍 マトリックス表示データテスト...")
    response = requests.get(f"{BASE_URL}/api/v1/tasks/matrix")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"総タスク数: {data['summary']['total_tasks']}")
        print(f"象限別タスク数: {data['summary']['by_quadrant']}")
        print(f"第1象限タスク数: {len(data['matrix']['high_high'])}")
    else:
        print(f"Error: {response.text}")
    print()

def test_calendar_data():
    """カレンダー表示データテスト"""
    print("🔍 カレンダー表示データテスト...")
    now = datetime.now()
    response = requests.get(f"{BASE_URL}/api/v1/tasks/calendar?year={now.year}&month={now.month}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"総イベント数: {data['summary']['total_events']}")
        print(f"期限数: {data['summary']['due_dates']}")
        print(f"開始予定数: {data['summary']['start_dates']}")
        print(f"カレンダーデータ日数: {len(data['calendar_data'])}")
    else:
        print(f"Error: {response.text}")
    print()

def test_filters():
    """フィルタリングテスト"""
    print("🔍 フィルタリングテスト...")
    
    # カテゴリフィルター
    response = requests.get(f"{BASE_URL}/api/v1/tasks?category=work")
    print(f"仕事カテゴリ: {response.status_code} - {len(response.json()['tasks']) if response.status_code == 200 else 'Error'} tasks")
    
    # 優先度フィルター
    response = requests.get(f"{BASE_URL}/api/v1/tasks?priority=high")
    print(f"高優先度: {response.status_code} - {len(response.json()['tasks']) if response.status_code == 200 else 'Error'} tasks")
    
    # 検索フィルター
    response = requests.get(f"{BASE_URL}/api/v1/tasks?search=プロジェクト")
    print(f"検索(プロジェクト): {response.status_code} - {len(response.json()['tasks']) if response.status_code == 200 else 'Error'} tasks")
    print()

def run_all_tests():
    """全テストを実行"""
    print("🚀 API テスト開始\n")
    
    try:
        # 基本テスト
        test_health()
        test_tasks_list()
        
        # CRUD テスト
        task_id = test_task_create()
        if task_id:
            test_task_detail(task_id)
            subtask_id = test_subtask_create(task_id)
            comment_id = test_comment_create(task_id)
        
        # 特殊機能テスト
        test_matrix_data()
        test_calendar_data()
        test_filters()
        
        print("✅ 全テスト完了!")
        
    except requests.exceptions.ConnectionError:
        print("❌ サーバーに接続できません。FastAPIサーバーが起動していることを確認してください。")
        print("   起動コマンド: python main.py")
    except Exception as e:
        print(f"❌ テスト中にエラーが発生しました: {e}")

if __name__ == "__main__":
    run_all_tests()