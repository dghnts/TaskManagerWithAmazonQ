#!/usr/bin/env python3
"""
データベース接続確認スクリプト
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def check_database_connection():
    """データベース接続をテスト"""
    try:
        # 環境変数から接続情報を取得
        db_url = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/task_management_app")
        print(f"接続URL: {db_url}")
        
        # URLをパース
        if db_url.startswith("postgresql://"):
            # postgresql://user:password@host:port/database の形式
            parts = db_url.replace("postgresql://", "").split("/")
            db_name = parts[1] if len(parts) > 1 else "task_management_app"
            user_host = parts[0].split("@")
            host_port = user_host[1].split(":")
            user_pass = user_host[0].split(":")
            
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 5432
            user = user_pass[0]
            password = user_pass[1] if len(user_pass) > 1 else ""
        else:
            # デフォルト値
            host = "localhost"
            port = 5432
            user = "postgres"
            password = ""
            db_name = "task_management_app"
        
        print(f"接続先: {host}:{port}")
        print(f"ユーザー: {user}")
        print(f"データベース: {db_name}")
        
        # PostgreSQLサーバーに接続テスト（デフォルトDBに接続）
        print("\n1. PostgreSQLサーバー接続テスト...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="postgres"  # デフォルトDB
        )
        print("✓ PostgreSQLサーバーに接続成功")
        
        # データベース存在確認
        print(f"\n2. データベース '{db_name}' 存在確認...")
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cur.fetchone()
        
        if exists:
            print(f"✓ データベース '{db_name}' が存在します")
        else:
            print(f"✗ データベース '{db_name}' が存在しません")
            print(f"\n以下のSQLを実行してデータベースを作成してください:")
            print(f"CREATE DATABASE {db_name};")
            
            # データベースを自動作成
            print(f"\n自動でデータベースを作成しますか? (y/n): ", end="")
            response = input().lower()
            if response == 'y':
                cur.execute(f"CREATE DATABASE {db_name}")
                conn.commit()
                print(f"✓ データベース '{db_name}' を作成しました")
        
        cur.close()
        conn.close()
        
        # 作成したデータベースに接続テスト
        print(f"\n3. データベース '{db_name}' 接続テスト...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name
        )
        print(f"✓ データベース '{db_name}' に接続成功")
        conn.close()
        
        print("\n✓ データベース接続確認完了!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ データベース接続エラー: {e}")
        print("\n確認事項:")
        print("1. PostgreSQLサービスが起動していますか?")
        print("2. 接続情報（ホスト、ポート、ユーザー、パスワード）は正しいですか?")
        print("3. .envファイルのDATABASE_URLは正しく設定されていますか?")
        return False
    except Exception as e:
        print(f"\n✗ エラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    check_database_connection()