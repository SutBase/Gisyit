// -*- coding: utf-8 -*-
/**
 * 下载历史管理
 */

import { ref, watch } from 'vue';

const STORAGE_KEY = 'video_parser_download_history';
const history = ref([]);
const MAX_HISTORY = 100; // 最大保存100条记录

// 从本地存储加载历史记录
const loadHistory = () => {
  try {
    const savedHistory = localStorage.getItem(STORAGE_KEY);
    if (savedHistory) {
      history.value = JSON.parse(savedHistory);
    }
  } catch (error) {
    console.error('加载下载历史失败:', error);
    history.value = [];
  }
};

// 保存历史记录到本地存储
const saveHistory = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history.value));
  } catch (error) {
    console.error('保存下载历史失败:', error);
  }
};

// 添加到历史记录
const addToHistory = (item) => {
  history.value.unshift({
    ...item,
    id: Date.now().toString()
  });

  // 限制历史记录数量
  if (history.value.length > MAX_HISTORY) {
    history.value = history.value.slice(0, MAX_HISTORY);
  }

  saveHistory();
};

// 清空历史记录
const clearHistory = () => {
  history.value = [];
  saveHistory();
};

// 初始化时加载历史记录
loadHistory();

// 监听历史记录变化，自动保存
watch(history, saveHistory, { deep: true });

export function useDownloadHistory() {
  return {
    history,
    addToHistory,
    clearHistory
  };
}
