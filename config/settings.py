import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

class Settings:
    """アプリケーション設定を管理するクラス"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / "config.json"
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"設定ファイルの読み込みエラー: {e}")
                return self._default_config()
        else:
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """デフォルト設定を返す"""
        return {
            "api_keys": {
                "anthropic": "",
                "openai": "",
                "azure_openai": ""
            },
            "azure_openai": {
                "endpoint": "",
                "api_version": "2024-02-01"
            },
            "default_provider": "anthropic",
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "debug": True
            },
            "models": {
                "anthropic": "claude-3-haiku-20240307",
                "openai": "gpt-3.5-turbo",
                "azure_openai": "gpt-4o-mini"
            },
            "ui": {
                "default_level": "400",
                "theme": "light"
            },
            "proxy": {
                "http": "",
                "https": "",
                "enabled": False
            },
            "api_endpoints": {
                "anthropic": "https://api.anthropic.com",
                "openai": "https://api.openai.com/v1",
                "azure_openai": ""
            }
        }
    
    def save_config(self) -> None:
        """設定をファイルに保存"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"設定ファイルの保存エラー: {e}")
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """APIキーを取得（環境変数 > 設定ファイルの順）"""
        env_keys = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "azure_openai": "AZURE_OPENAI_API_KEY"
        }
        
        # 環境変数を最優先
        env_key = os.getenv(env_keys.get(provider, ""))
        if env_key:
            return env_key
        
        # 設定ファイルから取得
        return self._config.get("api_keys", {}).get(provider)
    
    def get_server_config(self) -> Dict[str, Any]:
        """サーバー設定を取得"""
        return self._config.get("server", self._default_config()["server"])
    
    def get_model(self, provider: str) -> str:
        """指定されたプロバイダーのモデル名を取得"""
        models = self._config.get("models", self._default_config()["models"])
        return models.get(provider, models["anthropic"])
    
    def get_default_provider(self) -> str:
        """デフォルトプロバイダーを取得"""
        return self._config.get("default_provider", "anthropic")
    
    def get_ui_config(self) -> Dict[str, Any]:
        """UI設定を取得"""
        return self._config.get("ui", self._default_config()["ui"])
    
    def get_azure_openai_endpoint(self) -> Optional[str]:
        """Azure OpenAI エンドポイントを取得（環境変数 > 設定ファイルの順）"""
        # 環境変数を最優先
        env_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if env_endpoint:
            return env_endpoint
        
        # 設定ファイルから取得
        return self._config.get("azure_openai", {}).get("endpoint")
    
    def get_azure_openai_api_version(self) -> str:
        """Azure OpenAI API バージョンを取得"""
        return self._config.get("azure_openai", {}).get("api_version", "2024-02-01")
    
    def get_proxy_config(self) -> Dict[str, str]:
        """プロキシ設定を取得"""
        proxy_config = self._config.get("proxy", {})
        
        # 環境変数も確認
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy") or proxy_config.get("http", "")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy") or proxy_config.get("https", "")
        
        return {
            "http": http_proxy,
            "https": https_proxy,
            "enabled": proxy_config.get("enabled", False) or bool(http_proxy or https_proxy)
        }
    
    def get_api_endpoint(self, provider: str) -> str:
        """指定されたプロバイダーのAPIエンドポイントを取得"""
        endpoints = self._config.get("api_endpoints", {})
        default_endpoints = self._default_config()["api_endpoints"]
        return endpoints.get(provider, default_endpoints.get(provider, ""))

# グローバル設定インスタンス
settings = Settings()