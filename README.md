# English Learning App

生成AIを活用した英語学習Webアプリケーションです。AIの英語講師とチャットしながら、和訳やライティングフィードバックを受けることができます。

## ✨ 主要機能

### 📚 学習機能
- **AI英語講師との会話**: リアルタイムでの英語会話練習
- **双方向和訳機能**: 学生と先生の両方のメッセージを日本語に翻訳
- **ライティングフィードバック**: 文法や表現の改善提案（文脈を考慮）
- **ヒント機能**: 日本語から英語表現のヒントを取得（💡ボタン）
- **メッセージID対応システム**: 英語テキストと和訳の対応関係を明確表示
- **インテリジェントローディング**: 各処理の進行状況を明確に表示
- **パネル表示切り替え**: 和訳・フィードバックパネルの表示/非表示をトグルスイッチで制御

### ⚙️ カスタマイズ機能
- **複数AI対応**: Claude (Anthropic) / GPT (OpenAI) / GPT (Azure OpenAI) から選択可能
- **レベル設定**: TOEIC 400/600/800点相当のレベル調整
- **テーマ切り替え**: ライト/ダークモード対応
- **システムメッセージ**: エラーや通知の明確な表示
- **会話リセット**: いつでも新しい会話を開始可能
- **インアプリマニュアル**: 📖ボタンで各機能の使い方を確認

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 設定ファイルの作成

`config/config.json` ファイルを作成して各種設定を行います：

```json
{
  "api_keys": {
    "anthropic": "your-anthropic-api-key-here",
    "openai": "your-openai-api-key-here",
    "azure_openai": "your-azure-openai-api-key-here"
  },
  "azure_openai": {
    "endpoint": "https://your-resource.openai.azure.com/",
    "api_version": "2024-02-01"
  },
  "default_provider": "anthropic",
  "models": {
    "anthropic": "claude-3-5-haiku-20241022",
    "openai": "gpt-4o-mini",
    "azure_openai": "gpt-4o-mini"
  },
  "ui": {
    "default_level": "600",
    "theme": "light"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": true
  },
  "proxy": {
    "http": "http://proxy.company.com:8080",
    "https": "http://proxy.company.com:8080", 
    "enabled": false
  },
  "api_endpoints": {
    "anthropic": "https://api.anthropic.com",
    "openai": "https://api.openai.com/v1",
    "azure_openai": ""
  }
}
```

#### 🔧 設定項目の説明

**APIキー設定** - 使用するAIサービスのAPIキーを設定
- `api_keys.anthropic`: Anthropic Claude APIキー
- `api_keys.openai`: OpenAI APIキー  
- `api_keys.azure_openai`: Azure OpenAI APIキー

**プロキシ設定** - 企業環境での使用時に設定
- `proxy.http`: HTTPプロキシURL
- `proxy.https`: HTTPSプロキシURL
- `proxy.enabled`: プロキシ使用の有効/無効

**APIエンドポイント** - カスタムエンドポイント使用時に設定
- `api_endpoints.anthropic`: Anthropic APIエンドポイント
- `api_endpoints.openai`: OpenAI APIエンドポイント
- `api_endpoints.azure_openai`: Azure OpenAI エンドポイント（`azure_openai.endpoint`で設定）

**モデル設定** - 各プロバイダーで使用するモデル名
- `models.anthropic`: Claude使用モデル（例：claude-3-5-haiku-20241022）
- `models.openai`: OpenAI使用モデル（例：gpt-4o-mini）
- `models.azure_openai`: Azure OpenAI使用モデル

#### 🌍 環境変数での設定

設定ファイルの代わりに環境変数でも設定可能です（環境変数が優先されます）：

```bash
# APIキー
export ANTHROPIC_API_KEY='your-anthropic-api-key'
export OPENAI_API_KEY='your-openai-api-key'
export AZURE_OPENAI_API_KEY='your-azure-openai-api-key'
export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'

# プロキシ設定（企業環境）
export HTTP_PROXY='http://proxy.company.com:8080'
export HTTPS_PROXY='http://proxy.company.com:8080'
# または小文字形式
export http_proxy='http://proxy.company.com:8080'
export https_proxy='http://proxy.company.com:8080'
```

#### ⚙️ 最小設定

アプリを動かすために必要な最小限の設定：

```json
{
  "api_keys": {
    "anthropic": "your-anthropic-api-key-here"
  },
  "default_provider": "anthropic"
}
```

他の設定項目は自動的にデフォルト値が使用されます。

### 3. アプリケーションの起動

```bash
python main.py
```

### 4. ブラウザでアクセス

http://localhost:8000 にアクセスしてアプリケーションを使用できます。

## 📖 使用方法

1. **AI プロバイダー選択**: Claude、OpenAI、または Azure OpenAI から選択
2. **レベル設定**: TOEIC点数相当のレベルを選択
3. **メッセージ送信**: テキストボックスに英文を入力して✈️ボタンで送信
4. **リアルタイム表示**: 
   - 中央パネル: AI講師との会話
   - 左パネル: 双方向和訳（学生・講師両方）
   - 右パネル: ライティングフィードバック
5. **ヒント機能**: 💡ボタンで日本語から英語表現のヒントを取得
6. **メッセージ対応**: ID表示で英文と和訳の対応関係を確認
7. **パネル制御**: 各パネルのトグルスイッチで和訳・フィードバックの表示切り替え
8. **テーマ切り替え**: 🌙ボタンでライト/ダークモードを切り替え
9. **マニュアル**: 📖ボタンで各機能の使い方を確認
10. **会話リセット**: 「Reset Chat」ボタンで会話履歴をクリア

## 🏗️ プロジェクト構造

```
EnglishLearning/
├── main.py                 # アプリケーションエントリーポイント
├── requirements.txt        # Python依存関係
├── .gitignore             # Git除外設定
├── README.md              # プロジェクト説明書
├── CLAUDE.md              # 開発指針とプロジェクト要件
├── config/
│   ├── __init__.py
│   ├── settings.py         # 設定管理クラス
│   └── config.json         # 設定ファイル（要作成）
├── backend/
│   ├── __init__.py
│   ├── app.py             # Flaskアプリケーション
│   ├── ai_service.py      # AI API統合クラス
│   └── prompts.py         # プロンプト管理クラス
├── frontend/
│   ├── index.html         # メインHTML
│   └── static/
│       ├── css/
│       │   └── style.css  # スタイルシート
│       └── js/
│           └── app.js     # フロントエンドJavaScript
└── data/                  # 将来的なデータ保存用
```

## 🔧 技術仕様

### バックエンド
- **Python 3.8+**
- **Flask 3.1.0** (非同期対応)
- **Flask-CORS 5.0.0** (CORS対応)
- **Anthropic 0.40.0** (Claude API)
- **OpenAI 1.54.0** (OpenAI & Azure OpenAI API)

### フロントエンド
- **HTML5 / CSS3 / JavaScript (ES6+)**
- **レスポンシブデザイン** (デスクトップ・モバイル対応)
- **CSS Variables** (テーマ切り替え対応)
- **モダンUI** (トグルスイッチ、ポップアップ等)

## 🔐 セキュリティ注意事項

- このアプリケーションはローカル環境での使用を想定しています
- APIキーは設定ファイル（`config/config.json`）で管理されます
- `config/config.json` ファイルを他人と共有しないよう注意してください
- `.gitignore`により設定ファイルは自動的にGit管理対象外になります
- インターネット接続が必要です（AI APIにアクセスするため）

## 🆕 最新の機能追加

### ヒント機能 (2024年12月)
- 💡ボタンで日本語から英語表現のヒントを取得
- レベル別対応（TOEIC 400/600/800）
- 複数表現提案と使い方の解説
- モダンなポップアップUI

### インアプリマニュアル (2024年12月)
- 📖ボタンで各機能の使い方を確認
- 簡潔で分かりやすい説明
- レスポンシブデザイン対応

### Azure OpenAI 対応 (2024年12月)
- 3つのAIプロバイダーから選択可能
- 統一されたインターフェース
- エラーハンドリングの改善

### パネル表示切り替え機能
- 和訳・フィードバックパネルにトグルスイッチを追加
- 不要なパネルを非表示にして画面を効率的に使用
- 非表示時はモザイク効果で内容を隠し、「Hidden」表示で状態を明確化
- 内部処理は継続するため、表示切り替え時に即座に結果を確認可能

### ローディング表示の最適化
- チャット画面のLoading表示は先生の回答が表示されたタイミングで終了
- 和訳・フィードバックパネルに独立したLoading表示を追加
- ユーザー体験の向上により、会話がよりスムーズに

### 双方向翻訳機能
- 学生のメッセージに加えて、AI講師のメッセージも翻訳
- メッセージIDによる対応関係の明確化
- 初期挨拶メッセージも翻訳対象に含める

### フィードバック品質向上
- 先生の直前のメッセージを文脈として含める
- より適切で文脈に沿ったフィードバックを提供

## 📝 ライセンス

このプロジェクトは個人使用を目的としています。