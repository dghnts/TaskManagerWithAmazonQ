#!/usr/bin/env python3
"""
シンプルなAPIテスト
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    """APIテストを実行"""
    print("API テスト開始")
    
    try:
        # 1. ヘルスチェック
        print("\n1. ヘルスチェック...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("OK: サーバーが起動しています")
        
        # 2. タスク一覧取得
        print("\n2. タスク一覧取得...")
        response = requests.get(f"{BASE_URL}/api/v1/tasks")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"取得タスク数: {len(data['tasks'])}")
            if data['tasks']:
                print(f"最初のタスク: {data['tasks'][0]['title']}")
        
        # 3. タスク作成
        print("\n3. タスク作成...")
        new_task = {
            "title": "APIテスト用タスク",
            "description": "テスト用のタスクです",
            "category": "work",
            "priority": "medium",
            "urgency": "low",
            "estimated_hours": 1.0
        }
        response = requests.post(f"{BASE_URL}/api/v1/tasks", json=new_task)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"作成されたタスク: {task['title']}")
            task_id = task['id']
            
            # 4. タスク詳細取得
            print(f"\n4. タスク詳細取得 (ID: {task_id})...")
            response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("OK: タスク詳細取得成功")
            
            # 5. サブタスク作成
            print(f"\n5. サブタスク作成...")
            subtask = {"title": "テスト用サブタスク", "order_index": 1}
            response = requests.post(f"{BASE_URL}/api/v1/tasks/{task_id}/subtasks", json=subtask)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("OK: サブタスク作成成功")
            
            # 6. コメント作成
            print(f"\n6. コメント作成...")
            comment = {"content": "テスト用コメントです"}
            response = requests.post(f"{BASE_URL}/api/v1/tasks/{task_id}/comments", json=comment)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("OK: コメント作成成功")
        
        # 7. マトリックス表示
        print("\n7. マトリックス表示データ...")
        response = requests.get(f"{BASE_URL}/api/v1/tasks/matrix")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"総タスク数: {data['summary']['total_tasks']}")
        
        # 8. カレンダー表示
        print("\n8. カレンダー表示データ...")
        from datetime import datetime
        now = datetime.now()
        response = requests.get(f"{BASE_URL}/api/v1/tasks/calendar?year={now.year}&month={now.month}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"総イベント数: {data['summary']['total_events']}")
        
        print("\n全テスト完了!")
        
    except requests.exceptions.ConnectionError:
        print("エラー: サーバーに接続できません")
        print("FastAPIサーバーが起動していることを確認してください")
        print("起動コマンド: python main.py")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    test_api()