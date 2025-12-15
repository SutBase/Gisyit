// -*- coding: utf-8 -*-
/**
 * AI助手功能
 */

import { ref } from 'vue';

const API_KEY_STORAGE_KEY = 'video_parser_api_key';
const MODEL_STORAGE_KEY = 'video_parser_model';

const messages = ref([]);
const loading = ref(false);
const apiKey = ref('');
const selectedModel = ref('deepseek-chat');

// 从本地存储加载API密钥和模型
const loadSettings = () => {
  try {
    const savedApiKey = localStorage.getItem(API_KEY_STORAGE_KEY);
    if (savedApiKey) {
      apiKey.value = savedApiKey;
    }

    const savedModel = localStorage.getItem(MODEL_STORAGE_KEY);
    if (savedModel) {
      selectedModel.value = savedModel;
    }
  } catch (error) {
    console.error('加载AI设置失败:', error);
  }
};

// 保存API密钥
const saveApiKey = (key) => {
  try {
    localStorage.setItem(API_KEY_STORAGE_KEY, key);
  } catch (error) {
    console.error('保存API密钥失败:', error);
  }
};

// 保存模型选择
const saveModel = (model) => {
  try {
    localStorage.setItem(MODEL_STORAGE_KEY, model);
  } catch (error) {
    console.error('保存模型设置失败:', error);
  }
};

// 发送消息给AI
const sendMessage = async (content) => {
  if (!content.trim() || !apiKey.value) return;

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: content.trim(),
    timestamp: new Date().toISOString()
  });

  loading.value = true;

  try {
    const response = await callDeepSeekAPI(content);

    // 添加AI回复
    messages.value.push({
      role: 'assistant',
      content: response,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('AI回复失败:', error);

    // 添加错误消息
    messages.value.push({
      role: 'assistant',
      content: `抱歉，处理您的请求时出错: ${error.message}`,
      timestamp: new Date().toISOString()
    });
  } finally {
    loading.value = false;
  }
};

// 生成文本
const generateText = async (prompt) => {
  if (!apiKey.value) {
    throw new Error('请先设置API密钥');
  }

  try {
    return await callDeepSeekAPI(prompt);
  } catch (error) {
    console.error('生成文本失败:', error);
    throw error;
  }
};

// 调用DeepSeek API
const callDeepSeekAPI = async (prompt) => {
  const url = 'https://api.deepseek.com/v1/chat/completions';

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey.value}`
    },
    body: JSON.stringify({
      model: selectedModel.value,
      messages: [
        {
          role: 'system',
          content: '你是一个专业的视频内容分析师和文案写作助手，擅长分析视频内容、撰写吸引人的文案和提供有价值的建议。'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      temperature: 0.7,
      max_tokens: 2000
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error?.message || 'API请求失败');
  }

  const data = await response.json();
  return data.choices[0].message.content;
};

// 初始化设置
loadSettings();

export function useAIAssistant() {
  return {
    messages,
    loading,
    apiKey,
    selectedModel,
    sendMessage,
    generateText,
    saveApiKey,
    saveModel
  };
}
