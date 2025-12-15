<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1>多平台视频链接解析与下载引擎</h1>
        <p>合规、可扩展、可维护的视频链接解析与下载系统</p>
      </div>
    </header>

    <main class="main">
      <div class="container">
        <!-- 导航标签 -->
        <ul class="nav nav-tabs mb-4" id="mainTabs" role="tablist">
          <li class="nav-item" role="presentation">
            <button class="nav-link active" id="parser-tab" data-bs-toggle="tab" data-bs-target="#parser" type="button" role="tab" aria-controls="parser" aria-selected="true">
              <i class="bi bi-search"></i> 视频解析
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="history-tab" data-bs-toggle="tab" data-bs-target="#history" type="button" role="tab" aria-controls="history" aria-selected="false">
              <i class="bi bi-clock-history"></i> 下载历史
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="analytics-tab" data-bs-toggle="tab" data-bs-target="#analytics" type="button" role="tab" aria-controls="analytics" aria-selected="false">
              <i class="bi bi-graph-up"></i> 数据分析
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="content-tab" data-bs-toggle="tab" data-bs-target="#content" type="button" role="tab" aria-controls="content" aria-selected="false">
              <i class="bi bi-pencil-square"></i> 文案写作
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="correlation-tab" data-bs-toggle="tab" data-bs-target="#correlation" type="button" role="tab" aria-controls="correlation" aria-selected="false">
              <i class="bi bi-diagram-3"></i> 相关性分析
            </button>
          </li>
          <li class="nav-item" role="presentation">
            <button class="nav-link" id="ai-tab" data-bs-toggle="tab" data-bs-target="#ai" type="button" role="tab" aria-controls="ai" aria-selected="false">
              <i class="bi bi-robot"></i> AI助手
            </button>
          </li>
        </ul>

        <!-- 标签内容 -->
        <div class="tab-content" id="mainTabsContent">
          <!-- 视频解析标签页 -->
          <div class="tab-pane fade show active" id="parser" role="tabpanel" aria-labelledby="parser-tab">
            <VideoParser @video-parsed="handleVideoParsed" />
          </div>

          <!-- 下载历史标签页 -->
          <div class="tab-pane fade" id="history" role="tabpanel" aria-labelledby="history-tab">
            <DownloadHistory @generate-content="handleGenerateContent" />
          </div>

          <!-- 数据分析标签页 -->
          <div class="tab-pane fade" id="analytics" role="tabpanel" aria-labelledby="analytics-tab">
            <DataAnalytics />
          </div>

          <!-- 文案写作标签页 -->
          <div class="tab-pane fade" id="content" role="tabpanel" aria-labelledby="content-tab">
            <ContentWriter :videoData="currentVideoData" />
          </div>

          <!-- 相关性分析标签页 -->
          <div class="tab-pane fade" id="correlation" role="tabpanel" aria-labelledby="correlation-tab">
            <CorrelationAnalysis :videoData="currentVideoData" />
          </div>

          <!-- AI助手标签页 -->
          <div class="tab-pane fade" id="ai" role="tabpanel" aria-labelledby="ai-tab">
            <AIAssistant :initialPrompt="aiPrompt" />
          </div>
        </div>
      </div>
    </main>

    <!-- Toast提示容器 -->
    <div class="toast-container position-fixed bottom-0 end-0 p-3">
      <div v-for="toast in toasts" :key="toast.id" 
           class="toast" :class="`toast-${toast.type}`" 
           role="alert" aria-live="assertive" aria-atomic="true"
           :class="{ show: toast.visible }">
        <div class="toast-header">
          <strong class="me-auto">
            <i :class="getToastIcon(toast.type)"></i>
            {{ getToastTitle(toast.type) }}
          </strong>
          <button type="button" class="btn-close" @click="hideToast(toast.id)" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          {{ toast.message }}
        </div>
      </div>
    </div>

    <footer class="footer">
      <div class="container">
        <p>本工具仅解析平台允许下载的公开视频内容，请遵守原平台版权与使用协议</p>
        <p>© 2023 多平台视频链接解析与下载引擎</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref } from 'vue';
import VideoParser from './components/VideoParser.vue';
import DownloadHistory from './components/DownloadHistory.vue';
import DataAnalytics from './components/DataAnalytics.vue';
import ContentWriter from './components/ContentWriter.vue';
import CorrelationAnalysis from './components/CorrelationAnalysis.vue';
import AIAssistant from './components/AIAssistant.vue';
import { useToast } from './composables/useToast';

export default {
  name: 'App',
  components: {
    VideoParser,
    DownloadHistory,
    DataAnalytics,
    ContentWriter,
    CorrelationAnalysis,
    AIAssistant
  },
  setup() {
    const { toasts, hideToast } = useToast();
    const currentVideoData = ref({});
    const aiPrompt = ref('');

    // 处理视频解析完成
    const handleVideoParsed = (videoData) => {
      currentVideoData.value = videoData;
    };

    // 处理生成内容请求
    const handleGenerateContent = (historyItem) => {
      // 切换到文案写作标签页
      const contentTab = document.getElementById('content-tab');
      if (contentTab) {
        contentTab.click();
      }

      // 设置当前视频数据
      currentVideoData.value = historyItem;
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

    return {
      toasts,
      currentVideoData,
      aiPrompt,
      hideToast,
      handleVideoParsed,
      handleGenerateContent,
      getToastIcon,
      getToastTitle
    };
  }
};
</script>

<style>
body {
  background-color: #f8f9fa;
  font-family: 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
  margin: 0;
  padding: 0;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 15px;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 0;
  text-align: center;
}

.main {
  flex: 1;
  padding: 2rem 0;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.card-header {
  border-radius: 15px 15px 0 0 !important;
}

.platform-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  margin-right: 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.8rem;
  background-color: #e9ecef;
}

.video-result {
  margin-top: 1.5rem;
}

.stream-item {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.alert-disclaimer {
  font-size: 0.85rem;
}

.loading {
  text-align: center;
  padding: 2rem;
}

.footer {
  text-align: center;
  color: #6c757d;
  font-size: 0.9rem;
  padding: 1.5rem 0;
}

.platform-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
}

.platform-item {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

.platform-item.enabled {
  background-color: #d4edda;
  border-color: #c3e6cb;
}

/* 标签页样式 */
.nav-tabs .nav-link {
  color: #495057;
  font-weight: 500;
  border-top-left-radius: 0.5rem;
  border-top-right-radius: 0.5rem;
  padding: 0.75rem 1rem;
}

.nav-tabs .nav-link.active {
  color: #667eea;
  font-weight: 600;
  background-color: transparent;
  border-color: #dee2e6 #dee2e6 #fff;
}

.nav-tabs .nav-link:hover:not(.active) {
  color: #667eea;
  background-color: rgba(102, 126, 234, 0.05);
}

.tab-content {
  padding-top: 1.5rem;
}

/* Toast样式 */
.toast-container {
  z-index: 1050;
}

.toast {
  min-width: 250px;
  max-width: 350px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.toast.show {
  opacity: 1;
}

.toast-success {
  border-left: 4px solid #198754;
}

.toast-danger {
  border-left: 4px solid #dc3545;
}

.toast-warning {
  border-left: 4px solid #ffc107;
}

.toast-info {
  border-left: 4px solid #0dcaf0;
}
</style>
