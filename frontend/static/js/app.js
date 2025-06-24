/**
 * English Learning App
 * メインアプリケーションクラス
 */

class EnglishLearningApp {
    constructor() {
        this.conversationHistory = [];
        this.translationHistory = [];
        this.currentLevel = '400';
        this.currentProvider = 'anthropic';
        this.isDarkMode = false;
        this.userMessageCounter = 0;
        this.teacherMessageCounter = 0;
        this.lastUserMessageId = null;
        this.isTranslationVisible = true;
        this.isFeedbackVisible = true;
        
        this.initializeElements();
        this.bindEvents();
        this.loadTheme();
        this.loadConfig();
    }

    initializeElements() {
        this.elements = {
            aiProviderSelect: document.getElementById('aiProvider'),
            englishLevelSelect: document.getElementById('englishLevel'),
            resetButton: document.getElementById('resetConversation'),
            themeToggle: document.getElementById('themeToggle'),
            userInput: document.getElementById('userInput'),
            sendButton: document.getElementById('sendMessage'),
            conversationContent: document.getElementById('conversationContent'),
            translationContent: document.getElementById('translationContent'),
            feedbackContent: document.getElementById('feedbackContent'),
            translationPanel: document.getElementById('translationPanel'),
            feedbackPanel: document.getElementById('feedbackPanel'),
            translationToggle: document.getElementById('translationToggle'),
            feedbackToggle: document.getElementById('feedbackToggle'),
            hintButton: document.getElementById('hintButton'),
            hintPopup: document.getElementById('hintPopup'),
            hintInput: document.getElementById('hintInput'),
            getHintButton: document.getElementById('getHint'),
            closeHintButton: document.getElementById('closeHintPopup'),
            hintResult: document.getElementById('hintResult'),
            hintText: document.getElementById('hintText'),
            manualButton: document.getElementById('manualButton'),
            manualPopup: document.getElementById('manualPopup'),
            closeManualButton: document.getElementById('closeManualPopup')
        };
    }

    bindEvents() {
        this.elements.aiProviderSelect.addEventListener('change', (e) => {
            this.currentProvider = e.target.value;
            this.switchProvider(e.target.value);
        });

        this.elements.englishLevelSelect.addEventListener('change', (e) => {
            this.currentLevel = e.target.value;
            this.addSystemMessage(`レベルが変更されました: TOEIC ${this.currentLevel}`);
        });

        this.elements.resetButton.addEventListener('click', () => {
            this.resetConversation();
        });

        this.elements.themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        this.elements.translationToggle.addEventListener('change', (e) => {
            this.toggleTranslationPanel(e.target.checked);
        });

        this.elements.feedbackToggle.addEventListener('change', (e) => {
            this.toggleFeedbackPanel(e.target.checked);
        });

        this.elements.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });

        this.elements.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // ヒント機能のイベントリスナー
        this.elements.hintButton.addEventListener('click', () => {
            this.showHintPopup();
        });

        this.elements.closeHintButton.addEventListener('click', () => {
            this.hideHintPopup();
        });

        this.elements.getHintButton.addEventListener('click', () => {
            this.getHint();
        });

        this.elements.hintInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.getHint();
            }
        });

        // ポップアップの背景クリックで閉じる
        this.elements.hintPopup.addEventListener('click', (e) => {
            if (e.target === this.elements.hintPopup) {
                this.hideHintPopup();
            }
        });

        // マニュアル機能のイベントリスナー
        this.elements.manualButton.addEventListener('click', () => {
            this.showManualPopup();
        });

        this.elements.closeManualButton.addEventListener('click', () => {
            this.hideManualPopup();
        });

        this.elements.manualPopup.addEventListener('click', (e) => {
            if (e.target === this.elements.manualPopup) {
                this.hideManualPopup();
            }
        });
    }

    async loadConfig() {
        try {
            const response = await fetch('/api/config');
            if (response.ok) {
                const config = await response.json();
                this.currentLevel = config.default_level || '400';
                this.elements.englishLevelSelect.value = this.currentLevel;
            }
        } catch (error) {
            console.error('設定の読み込みに失敗しました:', error);
        }
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            this.isDarkMode = true;
            document.body.setAttribute('data-theme', 'dark');
            this.elements.themeToggle.textContent = '☀️';
        }
    }

    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        if (this.isDarkMode) {
            document.body.setAttribute('data-theme', 'dark');
            this.elements.themeToggle.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.removeAttribute('data-theme');
            this.elements.themeToggle.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    }

    async sendMessage() {
        const message = this.elements.userInput.value.trim();
        if (!message) return;

        this.elements.userInput.value = '';
        this.elements.sendButton.disabled = true;

        this.lastUserMessageId = this.addMessageToConversation(message, 'user');
        
        try {
            await this.processUserMessage(message);
        } catch (error) {
            console.error('Error processing message:', error);
            this.addSystemMessage('エラーが発生しました。もう一度お試しください。');
        } finally {
            this.elements.sendButton.disabled = false;
        }
    }

    addMessageToConversation(message, sender, messageId = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        let displayId;
        if (sender === 'user') {
            this.userMessageCounter++;
            displayId = `User-${String(this.userMessageCounter).padStart(2, '0')}`;
        } else if (sender === 'ai') {
            this.teacherMessageCounter++;
            displayId = `Teacher-${String(this.teacherMessageCounter).padStart(2, '0')}`;
        }

        const messageContent = `
            <div class="message-header">
                <span class="message-id">${displayId}</span>
            </div>
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;
        
        messageDiv.innerHTML = messageContent;
        this.elements.conversationContent.appendChild(messageDiv);
        this.scrollToBottom(this.elements.conversationContent);
        
        return displayId;
    }

    addSystemMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';
        messageDiv.innerHTML = `<p>${this.escapeHtml(message)}</p>`;
        this.elements.conversationContent.appendChild(messageDiv);
        this.scrollToBottom(this.elements.conversationContent);
    }

    async processUserMessage(message) {
        this.showLoading();
        
        // 会話履歴を更新
        this.conversationHistory.push({ role: 'user', content: message });
        
        try {
            // まずAI回答を取得して表示
            const aiResponse = await this.getAIResponse(message);
            const teacherMessageId = this.addMessageToConversation(aiResponse, 'ai');
            this.conversationHistory.push({ role: 'assistant', content: aiResponse });
            
            // AI回答が表示されたらLoadingを終了
            this.hideLoading();

            // 翻訳とフィードバックを背景で並列処理
            this.showPanelLoading();
            this.processTranslationAndFeedback(message, aiResponse, this.lastUserMessageId, teacherMessageId);

        } catch (error) {
            console.error('AI response error:', error);
            this.addSystemMessage('AI回答の取得中にエラーが発生しました。');
            this.hideLoading();
        }
    }

    async processTranslationAndFeedback(userMessage, aiResponse, userMessageId, teacherMessageId) {
        try {
            // 並列処理で翻訳とフィードバックを取得
            const [userTranslation, teacherTranslation, feedback] = await Promise.all([
                this.getTranslation(userMessage),
                this.getTranslation(aiResponse),
                this.getFeedback(userMessage)
            ]);

            // 翻訳とフィードバックを更新
            this.updateTranslation(userMessage, userTranslation, userMessageId);
            this.updateTranslation(aiResponse, teacherTranslation, teacherMessageId);
            this.updateFeedback(feedback);

        } catch (error) {
            console.error('Translation/Feedback error:', error);
            this.addSystemMessage('翻訳またはフィードバックの取得中にエラーが発生しました。');
        } finally {
            this.hidePanelLoading();
        }
    }

    async getAIResponse(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                level: this.currentLevel,
                history: this.conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error(`AI API Error: ${response.status}`);
        }

        const data = await response.json();
        return data.response;
    }

    async getTranslation(text) {
        const response = await fetch('/api/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                target_language: 'japanese'
            })
        });

        if (!response.ok) {
            throw new Error(`Translation API Error: ${response.status}`);
        }

        const data = await response.json();
        return data.translation;
    }

    async getFeedback(text) {
        const teacherText = this.getLastTeacherMessage();
        
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                level: this.currentLevel,
                teacher_text: teacherText
            })
        });

        if (!response.ok) {
            throw new Error(`Feedback API Error: ${response.status}`);
        }

        const data = await response.json();
        return data.feedback;
    }

    getLastTeacherMessage() {
        for (let i = this.conversationHistory.length - 1; i >= 0; i--) {
            if (this.conversationHistory[i].role === 'assistant') {
                return this.conversationHistory[i].content;
            }
        }
        return null;
    }

    updateTranslation(originalText, translation, messageId) {
        if (!translation) return;

        const translationItem = document.createElement('div');
        translationItem.className = 'translation-item';
        translationItem.innerHTML = `
            <div class="translation-header">
                <span class="message-id">${messageId}</span>
            </div>
            <div class="translation-content">
                <div class="translated-text">${this.escapeHtml(translation)}</div>
            </div>
        `;

        // プレースホルダーを削除
        const placeholder = this.elements.translationContent.querySelector('.placeholder');
        if (placeholder) {
            placeholder.remove();
        }

        // ローディング表示があれば削除
        const loading = this.elements.translationContent.querySelector('#translationLoading');
        if (loading) {
            loading.remove();
        }

        this.elements.translationContent.appendChild(translationItem);
        this.scrollToBottom(this.elements.translationContent);
    }

    updateFeedback(feedback) {
        if (!feedback) return;

        const feedbackItem = document.createElement('div');
        feedbackItem.className = 'feedback-item';
        feedbackItem.innerHTML = `
            <div class="feedback-content">
                <p>${this.escapeHtml(feedback)}</p>
            </div>
        `;

        // プレースホルダーを削除
        const placeholder = this.elements.feedbackContent.querySelector('.placeholder');
        if (placeholder) {
            placeholder.remove();
        }

        // ローディング表示があれば削除
        const loading = this.elements.feedbackContent.querySelector('#feedbackLoading');
        if (loading) {
            loading.remove();
        }

        this.elements.feedbackContent.innerHTML = '';
        this.elements.feedbackContent.appendChild(feedbackItem);
        this.scrollToBottom(this.elements.feedbackContent);
    }

    async resetConversation() {
        // 会話履歴をクリア
        this.conversationHistory = [];
        this.translationHistory = [];
        this.userMessageCounter = 0;
        this.teacherMessageCounter = 0;

        // 画面を完全に初期状態に戻す
        this.elements.conversationContent.innerHTML = '';
        this.elements.translationContent.innerHTML = '<p class="placeholder">和訳がここに表示されます</p>';
        this.elements.feedbackContent.innerHTML = '<p class="placeholder">フィードバックがここに表示されます</p>';
        
        // ローディング表示をクリア
        this.hideLoading();
        this.hidePanelLoading();

        // 初期メッセージを表示
        const initialMessage = "Hello! I'm your English teacher. How can I help you practice English today?";
        const teacherMessageId = this.addMessageToConversation(initialMessage, 'ai');
        
        // 初期メッセージの翻訳を取得して表示（エラーが発生しても無視する）
        try {
            const initialTranslation = await this.getTranslation(initialMessage);
            this.updateTranslation(initialMessage, initialTranslation, teacherMessageId);
        } catch (error) {
            console.error('初期メッセージの翻訳に失敗しました:', error);
        }
    }

    showLoading() {
        const loading = document.createElement('div');
        loading.className = 'loading-message';
        loading.id = 'loadingMessage';
        loading.innerHTML = '<p>Loading...</p>';
        this.elements.conversationContent.appendChild(loading);
        this.scrollToBottom(this.elements.conversationContent);
    }

    hideLoading() {
        const loading = document.getElementById('loadingMessage');
        if (loading) {
            loading.remove();
        }
    }

    showPanelLoading() {
        // 和訳パネルのローディング表示
        const translationLoading = document.createElement('div');
        translationLoading.className = 'panel-loading-message translation-loading';
        translationLoading.id = 'translationLoading';
        translationLoading.innerHTML = '<p>Loading...</p>';
        
        // 既存のプレースホルダーを一時的に隠す
        const translationPlaceholder = this.elements.translationContent.querySelector('.placeholder');
        if (translationPlaceholder) {
            translationPlaceholder.style.display = 'none';
        }
        
        this.elements.translationContent.appendChild(translationLoading);

        // フィードバックパネルのローディング表示
        const feedbackLoading = document.createElement('div');
        feedbackLoading.className = 'panel-loading-message feedback-loading';
        feedbackLoading.id = 'feedbackLoading';
        feedbackLoading.innerHTML = '<p>Loading...</p>';
        
        // 既存のプレースホルダーを一時的に隠す
        const feedbackPlaceholder = this.elements.feedbackContent.querySelector('.placeholder');
        if (feedbackPlaceholder) {
            feedbackPlaceholder.style.display = 'none';
        }
        
        this.elements.feedbackContent.appendChild(feedbackLoading);
    }

    hidePanelLoading() {
        // 和訳ローディングを削除
        const translationLoading = document.getElementById('translationLoading');
        if (translationLoading) {
            translationLoading.remove();
        }

        // フィードバックローディングを削除
        const feedbackLoading = document.getElementById('feedbackLoading');
        if (feedbackLoading) {
            feedbackLoading.remove();
        }
    }

    scrollToBottom(element) {
        setTimeout(() => {
            element.scrollTop = element.scrollHeight;
        }, 100);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    toggleTranslationPanel(isVisible) {
        this.isTranslationVisible = isVisible;
        
        if (this.isTranslationVisible) {
            this.elements.translationPanel.classList.remove('hidden');
        } else {
            this.elements.translationPanel.classList.add('hidden');
        }
    }

    toggleFeedbackPanel(isVisible) {
        this.isFeedbackVisible = isVisible;
        
        if (this.isFeedbackVisible) {
            this.elements.feedbackPanel.classList.remove('hidden');
        } else {
            this.elements.feedbackPanel.classList.add('hidden');
        }
    }

    // ヒント機能関連メソッド
    showHintPopup() {
        this.elements.hintPopup.style.display = 'block';
        this.elements.hintInput.focus();
        // 前回の結果をクリア
        this.elements.hintResult.style.display = 'none';
        this.elements.hintInput.value = '';
    }

    hideHintPopup() {
        this.elements.hintPopup.style.display = 'none';
    }

    async getHint() {
        const japaneseText = this.elements.hintInput.value.trim();
        if (!japaneseText) return;

        this.elements.getHintButton.disabled = true;
        this.showHintLoading();

        try {
            const response = await fetch('/api/hint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    japanese_text: japaneseText,
                    level: this.currentLevel
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.displayHintResult(data.hint);
        } catch (error) {
            console.error('Hint API error:', error);
            this.displayHintResult('ヒントの取得中にエラーが発生しました。もう一度お試しください。');
        } finally {
            this.elements.getHintButton.disabled = false;
            this.hideHintLoading();
        }
    }

    showHintLoading() {
        this.elements.hintText.innerHTML = '<div class="hint-loading">Getting hint...</div>';
        this.elements.hintResult.style.display = 'block';
    }

    hideHintLoading() {
        const loading = this.elements.hintText.querySelector('.hint-loading');
        if (loading) {
            loading.remove();
        }
    }

    displayHintResult(hint) {
        this.elements.hintText.textContent = hint;
        this.elements.hintResult.style.display = 'block';
    }

    showManualPopup() {
        this.elements.manualPopup.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    hideManualPopup() {
        this.elements.manualPopup.style.display = 'none';
        document.body.style.overflow = '';
    }

    async switchProvider(provider) {
        try {
            const response = await fetch('/api/switch-provider', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ provider: provider })
            });

            if (!response.ok) {
                throw new Error(`Switch provider API Error: ${response.status}`);
            }

            const data = await response.json();
            if (data.success) {
                const providerNames = {
                    'anthropic': 'Claude (Anthropic)',
                    'azure_openai': 'GPT (Azure OpenAI)'
                };
                this.addSystemMessage(`AI provider switched to ${providerNames[provider]}`);
            } else {
                this.addSystemMessage(`Failed to switch provider: ${data.message || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Switch provider error:', error);
            this.addSystemMessage('プロバイダーの切り替え中にエラーが発生しました。');
        }
    }
}

// アプリケーション初期化
document.addEventListener('DOMContentLoaded', () => {
    new EnglishLearningApp();
});