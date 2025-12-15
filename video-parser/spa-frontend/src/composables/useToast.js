// -*- coding: utf-8 -*-
/**
 * Toast提示功能
 */

import { ref } from 'vue';

const toasts = ref([]);

// 显示Toast提示
const showToast = (message, type = 'info', duration = 3000) => {
  const id = Date.now().toString();

  toasts.value.push({
    id,
    message,
    type,
    visible: true
  });

  // 自动隐藏
  setTimeout(() => {
    hideToast(id);
  }, duration);
};

// 隐藏Toast提示
const hideToast = (id) => {
  const toast = toasts.value.find(t => t.id === id);
  if (toast) {
    toast.visible = false;

    // 延迟移除，让过渡动画完成
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id);
    }, 300);
  }
};

// 显示成功提示
const showSuccess = (message, duration) => {
  showToast(message, 'success', duration);
};

// 显示错误提示
const showError = (message, duration) => {
  showToast(message, 'danger', duration);
};

// 显示警告提示
const showWarning = (message, duration) => {
  showToast(message, 'warning', duration);
};

export function useToast() {
  return {
    toasts,
    showToast,
    hideToast,
    showSuccess,
    showError,
    showWarning
  };
}
