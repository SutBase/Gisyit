// -*- coding: utf-8 -*-
/**
 * React版本的AI助手组件
 */

import React, { useState, useEffect, useRef } from 'react';
import { useAIAssistant } from '../../composables/useAIAssistant';

const AIAssistant = ({ initialPrompt }) => {
  const { 
    messages, 
    loading, 
    sendMessage: sendAIMessage, 
    apiKey, 
    selectedModel,
    saveApiKey,
    saveModel
  } = useAIAssistant();

  const [userInput, setUserInput] = useState('');
  const [showApiKey, setShowApiKey] = useState(false);
  const chatMessagesRef = useRef(null);

  // 预设问题
  const presetQuestions = [
    '如何优化视频标题？',
    '如何写视频描述？',
    '如何选择合适的标签？',
    '分析这个视频的受众',
    '如何提高视频的观看量？'
  ];

  // 发送消息
  const sendMessage = async () => {
    if (!userInput.trim() || loading || !apiKey) return;

    const message = userInput.trim();
    setUserInput('');

    await sendAIMessage(message);

    // 滚动到底部
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  };

  // 询问预设问题
  const askPresetQuestion = (question) => {
    setUserInput(question);
    sendMessage();
  };

  // 监听API密钥变化
  useEffect(() => {
    if (apiKey) {
      saveApiKey(apiKey);
    }
  }, [apiKey, saveApiKey]);

  // 监听模型变化
  useEffect(() => {
    if (selectedModel) {
      saveModel(selectedModel);
    }
  }, [selectedModel, saveModel]);

  // 监听初始提示
  useEffect(() => {
    if (initialPrompt && initialPrompt.trim()) {
      setUserInput(initialPrompt);
      sendMessage();
    }
  }, [initialPrompt]);

  useEffect(() => {
    // 滚动到底部
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div className="ai-assistant">
      <div className="card">
        <div className="card-header">
          <h5 className="mb-0">AI助手</h5>
        </div>
        <div className="card-body">
          {/* 模型选择 */}
          <div className="mb-3">
            <label htmlFor="modelSelect" className="form-label">选择AI模型</label>
            <select className="form-select" id="modelSelect" value={selectedModel} onChange={(e) => saveModel(e.target.value)}>
              <option value="deepseek-chat">DeepSeek Chat</option>
              <option value="deepseek-reasoner">DeepSeek Reasoner</option>
            </select>
          </div>

          {/* API密钥设置 */}
          <div className="mb-3">
            <label htmlFor="apiKey" className="form-label">API密钥</label>
            <div className="input-group">
              <input 
                type={showApiKey ? "text" : "password"} 
                className="form-control" 
                id="apiKey" 
                value={apiKey}
                onChange={(e) => saveApiKey(e.target.value)}
                placeholder="输入DeepSeek API密钥"
              />
              <button className="btn btn-outline-secondary" type="button" onClick={() => setShowApiKey(!showApiKey)}>
                <i className={showApiKey ? "bi bi-eye-slash" : "bi bi-eye"}></i>
              </button>
            </div>
            <div className="form-text">API密钥将保存在本地浏览器中</div>
          </div>

          {/* 聊天界面 */}
          <div className="chat-container">
            <div className="chat-messages" ref={chatMessagesRef}>
              {messages.map((message, index) => (
                <div key={index} className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}>
                  <div className="message-content">
                    <div className="avatar">
                      <i className={message.role === 'user' ? "bi bi-person" : "bi bi-robot"}></i>
                    </div>
                    <div className="text">{message.content}</div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message assistant-message">
                  <div className="message-content">
                    <div className="avatar">
                      <i className="bi bi-robot"></i>
                    </div>
                    <div className="text">
                      <div className="spinner-border spinner-border-sm" role="status">
                        <span className="visually-hidden">思考中...</span>
                      </div>
                      正在思考...
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="chat-input">
              <div className="input-group">
                <input 
                  type="text" 
                  className="form-control" 
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  placeholder="输入您的问题..."
                  onKeyUp={(e) => e.key === 'Enter' && sendMessage()}
                  disabled={loading || !apiKey}
                />
                <button className="btn btn-primary" type="button" onClick={sendMessage} 
                        disabled={loading || !apiKey || !userInput.trim()}>
                  <i className="bi bi-send"></i>
                </button>
              </div>
            </div>
          </div>

          {/* 预设问题 */}
          <div className="mt-3">
            <h6>预设问题</h6>
            <div className="preset-questions">
              {presetQuestions.map((question, index) => (
                <button key={index}
                        className="btn btn-sm btn-outline-secondary me-2 mb-2"
                        onClick={() => askPresetQuestion(question)}>
                  {question}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
