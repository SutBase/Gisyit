// -*- coding: utf-8 -*-
/**
 * API 请求模块
 */

// API 基础URL，生产环境应该修改为实际的API地址
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com' 
  : 'http://localhost:8000';

/**
 * 解析视频URL
 * @param {string} url - 视频URL
 * @returns {Promise} - 解析结果
 */
export const parseVideoUrl = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/parse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || '解析视频失败');
    }

    return await response.json();
  } catch (error) {
    console.error('解析视频API请求失败:', error);
    throw error;
  }
};

/**
 * 获取支持的平台列表
 * @returns {Promise} - 平台列表
 */
export const getSupportedPlatforms = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/platforms`);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || '获取平台列表失败');
    }

    return await response.json();
  } catch (error) {
    console.error('获取平台列表API请求失败:', error);
    throw error;
  }
};

/**
 * 健康检查
 * @returns {Promise} - 健康状态
 */
export const healthCheck = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error('健康检查失败');
    }

    return await response.json();
  } catch (error) {
    console.error('健康检查API请求失败:', error);
    throw error;
  }
};
