"""AI サービスモジュール"""

import anthropic
from openai import AzureOpenAI
from typing import Dict, List, Optional
from config.settings import settings
from .prompts import prompt_manager

class AIService:
    """AI サービスを管理するクラス"""
    
    def __init__(self):
        self.anthropic_client = None
        self.azure_openai_client = None
        self.current_provider = settings.get_default_provider()
        self._initialize_clients()
    
    def _initialize_clients(self) -> None:
        """APIクライアントを初期化"""
        anthropic_key = settings.get_api_key('anthropic')
        azure_openai_key = settings.get_api_key('azure_openai')
        azure_openai_endpoint = settings.get_azure_openai_endpoint()
        
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            print("Anthropic Claude API が利用可能です")
        
        if azure_openai_key and azure_openai_endpoint:
            self.azure_openai_client = AzureOpenAI(
                api_key=azure_openai_key,
                azure_endpoint=azure_openai_endpoint,
                api_version=settings.get_azure_openai_api_version()
            )
            print("Azure OpenAI API が利用可能です")
        elif azure_openai_key or azure_openai_endpoint:
            print("Warning: Azure OpenAI の設定が不完全です。APIキーとエンドポイントの両方を設定してください。")
            
        if not self.anthropic_client and not self.azure_openai_client:
            print("Warning: APIキーが設定されていません。config/config.json ファイルでAPIキーを設定してください。")
    
    async def get_ai_response(self, message: str, level: str, history: List[Dict]) -> str:
        """AI からの回答を取得"""
        system_prompt = prompt_manager.get_system_prompt(level)
        
        try:
            if self.anthropic_client and self.current_provider == "anthropic":
                return await self._get_anthropic_response(message, system_prompt, history)
            elif self.azure_openai_client and self.current_provider == "azure_openai":
                return await self._get_azure_openai_response(message, system_prompt, history)
            else:
                return "I'm sorry, but the AI service is not available. Please check the API configuration."
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return "I apologize, but I'm having trouble responding right now. Please try again."
    
    async def _get_anthropic_response(self, message: str, system_prompt: str, history: List[Dict]) -> str:
        """Anthropic Claude API からの回答を取得"""
        messages = []
        for msg in history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        messages.append({"role": "user", "content": message})
        
        model = settings.get_model("anthropic")
        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=1000,
            system=system_prompt,
            messages=messages
        )
        
        return response.content[0].text
    
    async def _get_azure_openai_response(self, message: str, system_prompt: str, history: List[Dict]) -> str:
        """Azure OpenAI API からの回答を取得"""
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        messages.append({"role": "user", "content": message})
        
        deployment_name = settings.get_azure_openai_deployment_name()
        if not deployment_name:
            # フォールバックとしてモデル名を使用（互換性のため）
            deployment_name = settings.get_model("azure_openai")
        
        response = self.azure_openai_client.chat.completions.create(
            model=deployment_name,
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
            top_p=0.95
        )
        
        return response.choices[0].message.content
    
    async def get_translation(self, text: str, target_language: str = "japanese") -> str:
        """テキストを翻訳"""
        prompt = prompt_manager.get_translation_prompt(text, target_language)
        
        try:
            if self.anthropic_client and self.current_provider == "anthropic":
                model = settings.get_model("anthropic")
                response = self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.azure_openai_client and self.current_provider == "azure_openai":
                deployment_name = settings.get_azure_openai_deployment_name()
                if not deployment_name:
                    deployment_name = settings.get_model("azure_openai")
                
                response = self.azure_openai_client.chat.completions.create(
                    model=deployment_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                return response.choices[0].message.content
            else:
                return "Translation service not available"
        except Exception as e:
            print(f"Error getting translation: {e}")
            return "Translation failed"
    
    async def get_feedback(self, text: str, level: str, teacher_text: Optional[str] = None) -> str:
        """テキストに対するフィードバックを取得"""
        prompt = prompt_manager.get_feedback_prompt(text, level, teacher_text)
        
        try:
            if self.anthropic_client and self.current_provider == "anthropic":
                model = settings.get_model("anthropic")
                response = self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=800,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.azure_openai_client and self.current_provider == "azure_openai":
                deployment_name = settings.get_azure_openai_deployment_name()
                if not deployment_name:
                    deployment_name = settings.get_model("azure_openai")
                
                response = self.azure_openai_client.chat.completions.create(
                    model=deployment_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )
                return response.choices[0].message.content
            else:
                return "Feedback service not available"
        except Exception as e:
            print(f"Error getting feedback: {e}")
            return "Feedback failed"
    
    async def get_hint(self, japanese_text: str, level: str) -> str:
        """日本語テキストから英語表現のヒントを取得"""
        prompt = prompt_manager.get_hint_prompt(japanese_text, level)
        
        try:
            if self.anthropic_client and self.current_provider == "anthropic":
                model = settings.get_model("anthropic")
                response = self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.azure_openai_client and self.current_provider == "azure_openai":
                deployment_name = settings.get_azure_openai_deployment_name()
                if not deployment_name:
                    deployment_name = settings.get_model("azure_openai")
                
                response = self.azure_openai_client.chat.completions.create(
                    model=deployment_name,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                return response.choices[0].message.content
            else:
                return "Hint service not available"
        except Exception as e:
            print(f"Error getting hint: {e}")
            return "Hint request failed"
    
    def switch_provider(self, provider: str) -> bool:
        """AI プロバイダーを切り替え"""
        if provider in ['anthropic', 'azure_openai']:
            self.current_provider = provider
            return True
        return False