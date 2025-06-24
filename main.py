#!/usr/bin/env python3
"""
English Learning App
メインエントリーポイント
"""

from backend.app import create_app
from config.settings import settings

def main():
    """アプリケーションを起動"""
    print("English Learning App を起動しています...")
    
    app = create_app()
    server_config = settings.get_server_config()
    
    host = server_config.get('host', '0.0.0.0')
    port = server_config.get('port', 8000)
    debug = server_config.get('debug', True)
    
    print(f"サーバーを起動しました: http://localhost:{port}")
    
    try:
        app.run(debug=debug, host=host, port=port)
    except KeyboardInterrupt:
        print("\nアプリケーションを終了しています...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    main()