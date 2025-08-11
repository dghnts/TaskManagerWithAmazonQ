#!/usr/bin/env python3
"""
マトリックスAPI直接テスト
"""
import requests

def test_matrix_api():
    try:
        print("Testing matrix API...")
        response = requests.get("http://localhost:8000/api/v1/tasks/matrix")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Matrix data keys: {data.keys()}")
            if 'matrix' in data:
                print(f"Matrix keys: {data['matrix'].keys()}")
                for key, tasks in data['matrix'].items():
                    print(f"  {key}: {len(tasks)} tasks")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_matrix_api()