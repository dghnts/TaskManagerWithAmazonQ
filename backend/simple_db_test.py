#!/usr/bin/env python3
"""
シンプルなデータベース接続テスト
"""
import psycopg2

def test_connection():
    try:
        # PostgreSQLのデフォルト設定で接続
        print("PostgreSQL接続テスト...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="postgres",  # デフォルトパスワード
            database="postgres"  # デフォルトDB
        )
        print("OK: PostgreSQLサーバーに接続成功")
        
        # データベース作成
        conn.autocommit = True
        cur = conn.cursor()
        
        # 既存のデータベースを確認
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'task_management_app'")
        if cur.fetchone():
            print("OK: task_management_app データベースが存在します")
        else:
            print("データベースを作成中...")
            cur.execute("CREATE DATABASE task_management_app")
            print("OK: task_management_app データベースを作成しました")
        
        cur.close()
        conn.close()
        
        # 作成したデータベースに接続テスト
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="postgres",
            database="task_management_app"
        )
        print("OK: task_management_app データベースに接続成功")
        conn.close()
        
        print("\nデータベース接続テスト完了!")
        return True
        
    except Exception as e:
        print(f"エラー: {e}")
        print("\n確認事項:")
        print("1. PostgreSQLサービスが起動していますか?")
        print("2. postgresユーザーでパスワードなしで接続できますか?")
        return False

if __name__ == "__main__":
    test_connection()