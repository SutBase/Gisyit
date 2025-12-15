// -*- coding: utf-8 -*-
/**
 * React版本的主应用组件
 */

import React, { useState, useEffect } from 'react';
import VideoParser from './VideoParser';
import DownloadHistory from './DownloadHistory';
import DataAnalytics from './DataAnalytics';
import ContentWriter from './ContentWriter';
import CorrelationAnalysis from './CorrelationAnalysis';
import AIAssistant from './AIAssistant';
import { useToast } from '../../composables/useToast';

const App = () => {
  const { toasts, hideToast } = useToast();
  const [currentVideoData, setCurrentVideoData] = useState({});
  const [aiPrompt, setAiPrompt] = useState('');
  const [activeTab, setActiveTab] = useState('parser');

  // 处理视频解析完成
  const handleVideoParsed = (videoData) => {
    setCurrentVideoData(videoData);
  };

  // 处理生成内容请求
  const handleGenerateContent = (historyItem) => {
    // 切换到文案写作标签页
    setActiveTab('content');

    // 设置当前视频数据
    setCurrentVideoData(historyItem);
  };

  // 获取Toast图标
  const getToastIcon = (type) => {
    switch (type) {
      case 'success':
        return 'bi bi-check-circle-fill';
      case 'danger':
        return 'bi bi-exclamation-triangle-fill';
      case 'warning':
        return 'bi bi-exclamation-triangle-fill';
      default:
        return 'bi bi-info-circle-fill';
    }
  };

  // 获取Toast标题
  const getToastTitle = (type) => {
    switch (type) {
      case 'success':
        return '成功';
      case 'danger':
        return '错误';
      case 'warning':
        return '警告';
      default:
        return '提示';
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>多平台视频链接解析与下载引擎</h1>
          <p>合规、可扩展、可维护的视频链接解析与下载系统</p>
        </div>
      </header>

      <main className="main">
        <div className="container">
          {/* 导航标签 */}
          <ul className="nav nav-tabs mb-4" id="mainTabs" role="tablist">
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'parser' ? 'active' : ''}`} 
                id="parser-tab" 
                type="button" 
                role="tab" 
                aria-controls="parser" 
                aria-selected={activeTab === 'parser'}
                onClick={() => setActiveTab('parser')}
              >
                <i className="bi bi-search"></i> 视频解析
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'history' ? 'active' : ''}`} 
                id="history-tab" 
                type="button" 
                role="tab" 
                aria-controls="history" 
                aria-selected={activeTab === 'history'}
                onClick={() => setActiveTab('history')}
              >
                <i className="bi bi-clock-history"></i> 下载历史
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'analytics' ? 'active' : ''}`} 
                id="analytics-tab" 
                type="button" 
                role="tab" 
                aria-controls="analytics" 
                aria-selected={activeTab === 'analytics'}
                onClick={() => setActiveTab('analytics')}
              >
                <i className="bi bi-graph-up"></i> 数据分析
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'content' ? 'active' : ''}`} 
                id="content-tab" 
                type="button" 
                role="tab" 
                aria-controls="content" 
                aria-selected={activeTab === 'content'}
                onClick={() => setActiveTab('content')}
              >
                <i className="bi bi-pencil-square"></i> 文案写作
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'correlation' ? 'active' : ''}`} 
                id="correlation-tab" 
                type="button" 
                role="tab" 
                aria-controls="correlation" 
                aria-selected={activeTab === 'correlation'}
                onClick={() => setActiveTab('correlation')}
              >
                <i className="bi bi-diagram-3"></i> 相关性分析
              </button>
            </li>
            <li className="nav-item" role="presentation">
              <button 
                className={`nav-link ${activeTab === 'ai' ? 'active' : ''}`} 
                id="ai-tab" 
                type="button" 
                role="tab" 
                aria-controls="ai" 
                aria-selected={activeTab === 'ai'}
                onClick={() => setActiveTab('ai')}
              >
                <i className="bi bi-robot"></i> AI助手
              </button>
            </li>
          </ul>

          {/* 标签内容 */}
          <div className="tab-content" id="mainTabsContent">
            {/* 视频解析标签页 */}
            {activeTab === 'parser' && (
              <div className="tab-pane fade show active" id="parser" role="tabpanel" aria-labelledby="parser-tab">
                <VideoParser onVideoParsed={handleVideoParsed} />
              </div>
            )}

            {/* 下载历史标签页 */}
            {activeTab === 'history' && (
              <div className="tab-pane fade show active" id="history" role="tabpanel" aria-labelledby="history-tab">
                <DownloadHistory onGenerateContent={handleGenerateContent} />
              </div>
            )}

            {/* 数据分析标签页 */}
            {activeTab === 'analytics' && (
              <div className="tab-pane fade show active" id="analytics" role="tabpanel" aria-labelledby="analytics-tab">
                <DataAnalytics />
              </div>
            )}

            {/* 文案写作标签页 */}
            {activeTab === 'content' && (
              <div className="tab-pane fade show active" id="content" role="tabpanel" aria-labelledby="content-tab">
                <ContentWriter videoData={currentVideoData} />
              </div>
            )}

            {/* 相关性分析标签页 */}
            {activeTab === 'correlation' && (
              <div className="tab-pane fade show active" id="correlation" role="tabpanel" aria-labelledby="correlation-tab">
                <CorrelationAnalysis videoData={currentVideoData} />
              </div>
            )}

            {/* AI助手标签页 */}
            {activeTab === 'ai' && (
              <div className="tab-pane fade show active" id="ai" role="tabpanel" aria-labelledby="ai-tab">
                <AIAssistant initialPrompt={aiPrompt} />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Toast提示容器 */}
      <div className="toast-container position-fixed bottom-0 end-0 p-3">
        {toasts.map(toast => (
          <div key={toast.id} 
               className={`toast toast-${toast.type}`} 
               role="alert" 
               aria-live="assertive" 
               aria-atomic="true"
               style={{ opacity: toast.visible ? 1 : 0 }}>
            <div className="toast-header">
              <strong className="me-auto">
                <i className={getToastIcon(toast.type)}></i>
                {getToastTitle(toast.type)}
              </strong>
              <button type="button" className="btn-close" onClick={() => hideToast(toast.id)} aria-label="Close"></button>
            </div>
            <div className="toast-body">
              {toast.message}
            </div>
          </div>
        ))}
      </div>

      <footer className="footer">
        <div className="container">
          <p>本工具仅解析平台允许下载的公开视频内容，请遵守原平台版权与使用协议</p>
          <p>© 2023 多平台视频链接解析与下载引擎</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
