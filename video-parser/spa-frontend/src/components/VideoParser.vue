<template>
  <div class="video-parser">
    <div class="card">
      <div class="card-body">
        <div class="mb-4">
          <label for="videoUrl" class="form-label">视频链接</label>
          <div class="input-group">
            <input 
              type="text" 
              class="form-control" 
              id="videoUrl" 
              v-model="videoUrl"
              placeholder="粘贴视频链接..."
              @keyup.enter="parseVideo"
            >
            <button class="btn btn-primary" type="button" @click="parseVideo" :disabled="loading">
              <span v-if="!loading"><i class="bi bi-search"></i> 解析</span>
              <span v-else>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                解析中...
              </span>
            </button>
          </div>
          <div class="form-text">支持哔哩哔哩、抖音、YouTube等主流视频平台</div>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">解析中...</span>
          </div>
          <p class="mt-2">正在解析视频，请稍候...</p>
        </div>

        <div v-if="videoResult" class="video-result">
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <span class="platform-badge">{{ videoResult.platform }}</span>
                {{ videoResult.title }}
              </h5>
            </div>
            <div class="card-body">
              <div v-if="videoResult.cover" class="row">
                <div class="col-md-4">
                  <img :src="videoResult.cover" class="img-fluid rounded" alt="视频封面">
                </div>
                <div class="col-md-8">
                  <p><strong>时长:</strong> {{ formatDuration(videoResult.duration) }}</p>
                </div>
              </div>
              <div v-else>
                <p><strong>时长:</strong> {{ formatDuration(videoResult.duration) }}</p>
              </div>

              <div v-if="videoResult.downloadable && videoResult.streams && videoResult.streams.length > 0">
                <h6>可用下载选项:</h6>
                <div class="streams-container">
                  <div v-for="(stream, index) in videoResult.streams" :key="index" class="stream-item">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <span class="badge bg-primary">{{ stream.quality }}</span>
                        <span class="badge bg-secondary">{{ stream.format }}</span>
                        <span v-if="stream.has_watermark" class="badge bg-warning">含水印</span>
                        <span v-else class="badge bg-success">无水印</span>
                      </div>
                      <a :href="stream.url" class="btn btn-sm btn-success" @click="downloadVideo(stream, videoResult)">
                        <i class="bi bi-download"></i> 下载
                      </a>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="alert alert-warning">
                <i class="bi bi-exclamation-triangle-fill"></i> {{ videoResult.reason || '此视频无法下载' }}
              </div>
            </div>
          </div>

          <div v-if="videoResult.disclaimer" class="alert alert-info alert-disclaimer mt-3">
            <i class="bi bi-info-circle-fill"></i> {{ videoResult.disclaimer }}
          </div>
        </div>

        <div v-if="error" class="alert alert-danger">
          <i class="bi bi-exclamation-triangle-fill"></i> {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { parseVideoUrl } from '../api/api';
import { useDownloadHistory } from '../composables/useDownloadHistory';

export default {
  name: 'VideoParser',
  emits: ['video-parsed'],
  setup(props, { emit }) {
    const videoUrl = ref('');
    const loading = ref(false);
    const videoResult = ref(null);
    const error = ref('');
    const { addToHistory } = useDownloadHistory();

    // 解析视频
    const parseVideo = async () => {
      const url = videoUrl.value.trim();
      if (!url) {
        error.value = '请输入视频链接';
        return;
      }

      loading.value = true;
      error.value = '';
      videoResult.value = null;

      try {
        const result = await parseVideoUrl(url);
        videoResult.value = result;
        emit('video-parsed', result);
      } catch (err) {
        error.value = err.message || '解析视频时发生错误';
      } finally {
        loading.value = false;
      }
    };

    // 下载视频
    const downloadVideo = (stream, video) => {
      // 添加到下载历史
      addToHistory({
        title: video.title,
        platform: video.platform,
        quality: stream.quality,
        format: stream.format,
        timestamp: new Date().toISOString()
      });

      // 触发下载
      const link = document.createElement('a');
      link.href = stream.url;
      link.download = `${video.title}_${stream.quality}.${stream.format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    // 格式化时长
    const formatDuration = (seconds) => {
      if (!seconds || seconds <= 0) return '未知';

      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);

      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
      } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
      }
    };

    return {
      videoUrl,
      loading,
      videoResult,
      error,
      parseVideo,
      downloadVideo,
      formatDuration
    };
  }
};
</script>

<style scoped>
.video-parser {
  margin-bottom: 1.5rem;
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
</style>
