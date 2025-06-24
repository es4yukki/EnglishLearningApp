"""プロンプト管理モジュール"""

from typing import Dict, Optional


class PromptManager:
    """プロンプトテンプレートを管理するクラス"""

    def __init__(self):
        self.level_descriptions = {
            "400": "初級レベル（TOEICで400点相当の簡単な語彙と文法を使用する）",
            "600": "中級レベル（TOEICで600点相当の語彙と文法を使用する）",
            "800": "上級レベル（TOEICで800点相当の語彙と文法を使用する）",
        }

        self.system_prompt_template = (
            "あなたはフレンドリーな英語教師です。{level}の生徒を想定し、"
            "英会話の先生として英語で受け答えしてください。"
            "なお、あなたのテキスト量と生徒のテキスト量はだいたい同じになるように調整してください。"
            "生徒の投稿が長いならあなたの英文も長く、生徒の投稿が短いなら、あなたの投稿も短くしてください。"
        )

    def get_system_prompt(self, level: str) -> str:
        """指定されたレベルに応じたシステムプロンプトを生成"""
        level_desc = self.level_descriptions.get(level, self.level_descriptions["400"])
        return self.system_prompt_template.format(level=level_desc)

    def get_translation_prompt(
        self, text: str, target_language: str = "japanese"
    ) -> str:
        """翻訳用プロンプトを生成"""
        language_map = {"japanese": "Japanese", "english": "English"}
        target = language_map.get(target_language.lower(), "Japanese")
        return f"Translate the following English text to {target}. Provide only the translation:\n\n{text}"

    def get_feedback_prompt(
        self, text: str, level: str, teacher_text: Optional[str] = None
    ) -> str:
        """フィードバック用プロンプトを生成"""
        level_desc = self.level_descriptions.get(level, self.level_descriptions["400"])

        context_part = ""
        if teacher_text:
            context_part = (
                f"\n\n# 直前の先生からのメッセージ（文脈参考用）\n{teacher_text}"
            )

        return f"""私の以下の英文をネイティブスピーカーの目線で評価してください。
私は英語の練習中で、英会話の先生とチャットで会話をしています。
この英文は、そのチャットの一部を抜粋したものです。
文法や単語の誤りを指摘したり、より自然な表現があれば提案してください。{context_part}

# Note
- 私の英語は{level_desc}レベルを目標にしていると想定してください。
- フィードバックは日本語でお願いします。
- "わかりました"のような返事やあいさつなどは不要です。本題から始めてください。
- フィードバックは短く簡潔な内容にしてください。長くても200文字程度が上限です。例えば誤りが多い場合は全て指摘する必要はなく、より基本的なものを1〜2つピックすればよいです。

# 私の英文
{text}"""

    def get_hint_prompt(self, japanese_text: str, level: str) -> str:
        """ヒント機能用プロンプトを生成"""
        level_desc = self.level_descriptions.get(level, self.level_descriptions["400"])

        return f"""私は英語学習者で、英会話の先生とチャットで会話をしています。
以下の内容を英語で伝えたいのですが、適切な英語表現を教えてください。

# 伝えたい内容（日本語）
{japanese_text}

# 要求事項
- 私の英語レベルは{level_desc}です。このレベルに適した語彙と文法を使用してください。
- 会話で使えるナチュラルな表現を提案してください。
- 出力は、対応する英語表現だけでよいです。下記のoutput_sampleを参考にしてください。
- 複数の表現方法がある場合は、最大で3つまで提示してください。また、違いがわかるように、和訳に続いて短い説明を追記してください。
- もし提供された日本語が英語学習のヒントとして不適切な内容（挨拶以外の日本語の質問、意味不明な文章など）の場合は、「申し訳ございませんが、英語表現のヒントとしてお答えできない内容です。伝えたい内容を具体的にお書きください。」と日本語で回答してください。

# input_sample
〜が不安だ

# output_sample
- I'm worried about... ：〜について心配している （最もよく使われる一般的な表現）
- I'm a bit nervous about... : 〜について少し不安だ(やや柔らかい、カジュアルな表現)
- I'm concerned that...：〜ということに懸念を感じている(やや慎重で、フォーマルな印象の表現)
"""


# グローバルインスタンス
prompt_manager = PromptManager()
