@echo off
echo データベースセットアップとAPIテストを実行します...
echo.

echo 1. データベースセットアップ
python setup_db.py
if %errorlevel% neq 0 (
    echo データベースセットアップに失敗しました
    pause
    exit /b 1
)

echo.
echo 2. FastAPIサーバー起動確認
echo サーバーが起動していない場合は、別のターミナルで以下を実行してください:
echo python main.py
echo.

echo 3. APIテスト実行
python test_api.py

echo.
echo テスト完了
pause