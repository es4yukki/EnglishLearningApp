"""Flask アプリケーション"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from config.settings import settings
from .ai_service import AIService

def create_app() -> Flask:
    """Flask アプリケーションを作成"""
    app = Flask(__name__, 
                static_folder='../frontend/static',
                template_folder='../frontend')
    CORS(app)
    
    # AI サービス初期化
    ai_service = AIService()
    
    @app.route('/')
    def index():
        """メインページを返す"""
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/api/chat', methods=['POST'])
    async def chat():
        """チャットAPIエンドポイント"""
        try:
            data = request.get_json()
            message = data.get('message', '')
            level = data.get('level', '400')
            history = data.get('history', [])
            
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            response = await ai_service.get_ai_response(message, level, history)
            return jsonify({'response': response})
        except Exception as e:
            print(f"Chat API error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/translate', methods=['POST'])
    async def translate():
        """翻訳APIエンドポイント"""
        try:
            data = request.get_json()
            text = data.get('text', '')
            target_language = data.get('target_language', 'japanese')
            
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            
            translation = await ai_service.get_translation(text, target_language)
            return jsonify({'translation': translation})
        except Exception as e:
            print(f"Translation API error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/feedback', methods=['POST'])
    async def feedback():
        """フィードバックAPIエンドポイント"""
        try:
            data = request.get_json()
            text = data.get('text', '')
            teacher_text = data.get('teacher_text', '')
            level = data.get('level', '400')
            
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            
            feedback_result = await ai_service.get_feedback(text, level, teacher_text)
            return jsonify({'feedback': feedback_result})
        except Exception as e:
            print(f"Feedback API error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/hint', methods=['POST'])
    async def hint():
        """ヒントAPIエンドポイント"""
        try:
            data = request.get_json()
            japanese_text = data.get('japanese_text', '')
            level = data.get('level', '400')
            
            if not japanese_text:
                return jsonify({'error': 'Japanese text is required'}), 400
            
            hint_result = await ai_service.get_hint(japanese_text, level)
            return jsonify({'hint': hint_result})
        except Exception as e:
            print(f"Hint API error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/switch-provider', methods=['POST'])
    def switch_provider():
        """AI プロバイダーを切り替える"""
        try:
            data = request.get_json()
            provider = data.get('provider', 'anthropic')
            
            if ai_service.switch_provider(provider):
                return jsonify({'success': True, 'provider': provider})
            else:
                return jsonify({'error': 'Invalid provider'}), 400
        except Exception as e:
            print(f"Provider switch error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/config', methods=['GET'])
    def get_config():
        """UI設定を取得"""
        try:
            ui_config = settings.get_ui_config()
            return jsonify(ui_config)
        except Exception as e:
            print(f"Config API error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    return app