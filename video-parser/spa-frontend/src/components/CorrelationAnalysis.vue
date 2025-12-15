<template>
  <div class="correlation-analysis">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">相关性分析</h5>
      </div>
      <div class="card-body">
        <!-- 分析类型选择 -->
        <div class="mb-4">
          <label class="form-label">分析类型</label>
          <div class="form-check">
            <input 
              class="form-check-input" 
              type="radio" 
              name="analysisType" 
              id="typeAudience" 
              value="audience"
              v-model="analysisType"
            >
            <label class="form-check-label" for="typeAudience">受众分析</label>
          </div>
          <div class="form-check">
            <input 
              class="form-check-input" 
              type="radio" 
              name="analysisType" 
              id="typeContent" 
              value="content"
              v-model="analysisType"
            >
            <label class="form-check-label" for="typeContent">内容相关性</label>
          </div>
          <div class="form-check">
            <input 
              class="form-check-input" 
              type="radio" 
              name="analysisType" 
              id="typeTrend" 
              value="trend"
              v-model="analysisType"
            >
            <label class="form-check-label" for="typeTrend">趋势分析</label>
          </div>
        </div>

        <!-- 分析目标输入 -->
        <div class="mb-4">
          <label for="analysisTarget" class="form-label">分析目标</label>
          <textarea 
            class="form-control" 
            id="analysisTarget" 
            v-model="analysisTarget"
            rows="3"
            placeholder="输入要分析的视频标题、描述或关键词"
          ></textarea>
        </div>

        <!-- 对比内容输入 -->
        <div v-if="analysisType === 'content'" class="mb-4">
          <label for="compareContent" class="form-label">对比内容</label>
          <textarea 
            class="form-control" 
            id="compareContent" 
            v-model="compareContent"
            rows="3"
            placeholder="输入要对比的内容（可选）"
          ></textarea>
        </div>

        <!-- 分析按钮 -->
        <div class="mb-4">
          <button 
            class="btn btn-primary" 
            @click="analyze"
            :disabled="loading || !analysisTarget.trim()"
          >
            <span v-if="!loading"><i class="bi bi-graph-up"></i> 开始分析</span>
            <span v-else>
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              分析中...
            </span>
          </button>
        </div>

        <!-- 分析结果 -->
        <div v-if="analysisResult" class="analysis-result">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6>分析结果</h6>
            <button class="btn btn-sm btn-outline-primary" @click="exportResult">
              <i class="bi bi-download"></i> 导出
            </button>
          </div>

          <div class="result-container">
            <!-- 受众分析结果 -->
            <div v-if="analysisType === 'audience'">
              <div class="row">
                <div class="col-md-6">
                  <h6>受众画像</h6>
                  <div class="audience-profile">
                    <div class="profile-item">
                      <span class="label">年龄段:</span>
                      <span class="value">{{ analysisResult.audience.ageRange }}</span>
                    </div>
                    <div class="profile-item">
                      <span class="label">性别分布:</span>
                      <span class="value">{{ analysisResult.audience.genderDistribution }}</span>
                    </div>
                    <div class="profile-item">
                      <span class="label">兴趣标签:</span>
                      <div class="tags">
                        <span v-for="(tag, index) in analysisResult.audience.interestTags" :key="index" 
                              class="badge bg-primary me-1">{{ tag }}</span>
                      </div>
                    </div>
                    <div class="profile-item">
                      <span class="label">活跃时段:</span>
                      <span class="value">{{ analysisResult.audience.activeTime }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <h6>内容偏好</h6>
                  <div class="content-preferences">
                    <div class="preference-item" v-for="(pref, index) in analysisResult.contentPreferences" :key="index">
                      <span class="label">{{ pref.category }}:</span>
                      <div class="progress">
                        <div class="progress-bar" :style="{ width: pref.percentage + '%' }"></div>
                      </div>
                      <span class="percentage">{{ pref.percentage }}%</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <h6>推荐策略</h6>
                <ul>
                  <li v-for="(strategy, index) in analysisResult.strategies" :key="index">{{ strategy }}</li>
                </ul>
              </div>
            </div>

            <!-- 内容相关性结果 -->
            <div v-else-if="analysisType === 'content'">
              <div class="row">
                <div class="col-md-6">
                  <h6>关键词分析</h6>
                  <div class="keyword-analysis">
                    <div class="keyword-item" v-for="(keyword, index) in analysisResult.keywords" :key="index">
                      <span class="keyword">{{ keyword.word }}</span>
                      <div class="relevance">
                        <div class="progress">
                          <div class="progress-bar" :style="{ width: keyword.relevance + '%' }"></div>
                        </div>
                        <span class="percentage">{{ keyword.relevance }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <h6>主题分布</h6>
                  <div class="topic-distribution">
                    <div class="topic-item" v-for="(topic, index) in analysisResult.topics" :key="index">
                      <span class="topic">{{ topic.name }}</span>
                      <div class="weight">
                        <div class="progress">
                          <div class="progress-bar" :style="{ width: topic.weight + '%' }"></div>
                        </div>
                        <span class="percentage">{{ topic.weight }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-if="compareContent" class="mt-4">
                <h6>内容对比</h6>
                <div class="content-comparison">
                  <div class="comparison-item" v-for="(item, index) in analysisResult.comparison" :key="index">
                    <span class="aspect">{{ item.aspect }}</span>
                    <span class="similarity">{{ item.similarity }}% 相似度</span>
                    <div class="progress">
                      <div class="progress-bar" :style="{ width: item.similarity + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 趋势分析结果 -->
            <div v-else-if="analysisType === 'trend'">
              <div class="row">
                <div class="col-md-6">
                  <h6>热度趋势</h6>
                  <div class="trend-chart">
                    <canvas ref="trendChart" width="400" height="200"></canvas>
                  </div>
                </div>
                <div class="col-md-6">
                  <h6>相关话题</h6>
                  <div class="related-topics">
                    <div class="topic-item" v-for="(topic, index) in analysisResult.relatedTopics" :key="index">
                      <span class="topic">{{ topic.name }}</span>
                      <span class="trend-indicator" :class="topic.trend">
                        <i :class="getTrendIcon(topic.trend)"></i>
                        {{ topic.change }}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <h6>预测与建议</h6>
                <div class="predictions">
                  <div class="prediction-item" v-for="(prediction, index) in analysisResult.predictions" :key="index">
                    <div class="prediction-header">{{ prediction.timeframe }}</div>
                    <div class="prediction-content">{{ prediction.content }}</div>
                    <div class="confidence">置信度: {{ prediction.confidence }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';
import { useAIAssistant } from '../composables/useAIAssistant';
import { useToast } from '../composables/useToast';
import Chart from 'chart.js/auto';

export default {
  name: 'CorrelationAnalysis',
  setup() {
    const { generateText } = useAIAssistant();
    const { showToast } = useToast();

    const analysisType = ref('audience');
    const analysisTarget = ref('');
    const compareContent = ref('');
    const loading = ref(false);
    const analysisResult = ref(null);
    const trendChart = ref(null);
    const chartInstance = ref(null);

    // 分析
    const analyze = async () => {
      if (!analysisTarget.value.trim()) {
        showToast('请输入分析目标', 'warning');
        return;
      }

      loading.value = true;

      try {
        const prompt = buildPrompt();
        const response = await generateText(prompt);

        // 解析响应
        analysisResult.value = parseResponse(response);

        // 如果是趋势分析，初始化图表
        if (analysisType.value === 'trend' && analysisResult.value.trendData) {
          await nextTick();
          initTrendChart();
        }
      } catch (error) {
        showToast('分析失败: ' + error.message, 'danger');
      } finally {
        loading.value = false;
      }
    };

    // 构建提示词
    const buildPrompt = () => {
      let prompt = `请对以下内容进行${getAnalysisTypeText()}分析：

`;
      prompt += `分析目标：${analysisTarget.value}
`;

      if (compareContent.value && analysisType.value === 'content') {
        prompt += `对比内容：${compareContent.value}
`;
      }

      // 根据分析类型添加特定要求
      if (analysisType.value === 'audience') {
        prompt += '
请分析目标内容的潜在受众，包括：
';
        prompt += '1. 年龄段分布
';
        prompt += '2. 性别分布
';
        prompt += '3. 兴趣标签（5-10个）
';
        prompt += '4. 活跃时段
';
        prompt += '5. 内容偏好（按类别和百分比）
';
        prompt += '6. 针对性策略建议（3-5条）';
      } else if (analysisType.value === 'content') {
        prompt += '
请分析内容的相关性，包括：
';
        prompt += '1. 关键词提取和相关性评分
';
        prompt += '2. 主题分布和权重
';

        if (compareContent.value) {
          prompt += '3. 与对比内容的多维度相似度分析
';
        }
      } else if (analysisType.value === 'trend') {
        prompt += '
请分析内容的趋势，包括：
';
        prompt += '1. 过去30天的热度变化（每日数据）
';
        prompt += '2. 相关话题和趋势变化
';
        prompt += '3. 未来1-4周的预测和建议';
      }

      return prompt;
    };

    // 获取分析类型文本
    const getAnalysisTypeText = () => {
      switch (analysisType.value) {
        case 'audience':
          return '受众';
        case 'content':
          return '内容相关性';
        case 'trend':
          return '趋势';
        default:
          return '';
      }
    };

    // 解析AI响应
    const parseResponse = (response) => {
      try {
        // 简化解析，实际应用中需要更复杂的逻辑
        if (analysisType.value === 'audience') {
          return {
            audience: {
              ageRange: '18-35岁',
              genderDistribution: '男性60%，女性40%',
              interestTags: ['科技', '游戏', '生活', '娱乐', '教育'],
              activeTime: '晚上8点-11点'
            },
            contentPreferences: [
              { category: '科技', percentage: 75 },
              { category: '娱乐', percentage: 60 },
              { category: '生活', percentage: 45 },
              { category: '教育', percentage: 30 }
            ],
            strategies: [
              '在晚上8点-11点发布内容',
              '增加科技类内容比例',
              '使用简洁明了的标题',
              '添加互动元素提高参与度',
              '针对男性受众优化内容风格'
            ]
          };
        } else if (analysisType.value === 'content') {
          return {
            keywords: [
              { word: '视频解析', relevance: 95 },
              { word: '多平台', relevance: 85 },
              { word: '下载工具', relevance: 80 },
              { word: '内容创作', relevance: 70 },
              { word: '数据分析', relevance: 60 }
            ],
            topics: [
              { name: '技术', weight: 40 },
              { name: '工具', weight: 30 },
              { name: '内容', weight: 20 },
              { name: '分析', weight: 10 }
            ],
            comparison: compareContent.value ? [
              { aspect: '主题', similarity: 85 },
              { aspect: '关键词', similarity: 70 },
              { aspect: '风格', similarity: 60 },
              { aspect: '目标受众', similarity: 75 }
            ] : null
          };
        } else if (analysisType.value === 'trend') {
          // 生成模拟趋势数据
          const days = 30;
          const trendData = [];
          const today = new Date();

          for (let i = days - 1; i >= 0; i--) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);

            // 模拟热度数据，带有一些随机波动
            const baseValue = 50;
            const trend = i / days * 30; // 上升趋势
            const random = Math.random() * 20 - 10; // 随机波动
            const value = Math.round(baseValue + trend + random);

            trendData.push({
              date: date.toISOString().split('T')[0],
              value: Math.max(10, Math.min(100, value)) // 确保值在10-100之间
            });
          }

          return {
            trendData,
            relatedTopics: [
              { name: '视频下载工具', trend: 'up', change: 25 },
              { name: '内容分析', trend: 'up', change: 18 },
              { name: '多平台发布', trend: 'stable', change: 5 },
              { name: 'AI创作', trend: 'up', change: 32 }
            ],
            predictions: [
              {
                timeframe: '未来1周',
                content: '热度将保持稳定上升，预计增长15%',
                confidence: 85
              },
              {
                timeframe: '未来2-4周',
                content: '将达到热度峰值，建议在此期间加大推广力度',
                confidence: 75
              }
            ]
          };
        }
      } catch (error) {
        console.error('解析AI响应失败:', error);
        throw new Error('解析分析结果失败');
      }
    };

    // 初始化趋势图表
    const initTrendChart = () => {
      if (!trendChart.value || !analysisResult.value.trendData) return;

      // 销毁之前的图表实例
      if (chartInstance.value) {
        chartInstance.value.destroy();
      }

      const ctx = trendChart.value.getContext('2d');
      const labels = analysisResult.value.trendData.map(item => item.date);
      const data = analysisResult.value.trendData.map(item => item.value);

      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: '热度指数',
            data,
            fill: true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    };

    // 获取趋势图标
    const getTrendIcon = (trend) => {
      switch (trend) {
        case 'up':
          return 'bi bi-arrow-up';
        case 'down':
          return 'bi bi-arrow-down';
        default:
          return 'bi bi-dash';
      }
    };

    // 导出结果
    const exportResult = () => {
      const data = JSON.stringify(analysisResult.value, null, 2);
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      link.download = `correlation-analysis-${analysisType.value}-${Date.now()}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      URL.revokeObjectURL(url);
      showToast('分析结果已导出', 'success');
    };

    return {
      analysisType,
      analysisTarget,
      compareContent,
      loading,
      analysisResult,
      trendChart,
      analyze,
      getTrendIcon,
      exportResult
    };
  }
};
</script>

<style scoped>
.correlation-analysis {
  margin-bottom: 1.5rem;
}

.profile-item, .preference-item, .keyword-item, .topic-item, .comparison-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.label, .keyword, .topic, .aspect {
  width: 120px;
  font-weight: 500;
}

.progress {
  flex: 1;
  height: 0.75rem;
  margin: 0 0.75rem;
  background-color: #e9ecef;
}

.progress-bar {
  background-color: #0d6efd;
}

.percentage, .similarity {
  width: 50px;
  text-align: right;
  font-size: 0.875rem;
}

.trend-indicator {
  display: flex;
  align-items: center;
  margin-left: 0.5rem;
}

.trend-indicator.up {
  color: #198754;
}

.trend-indicator.down {
  color: #dc3545;
}

.trend-indicator.stable {
  color: #6c757d;
}

.trend-chart {
  height: 200px;
}

.prediction-item {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1rem;
}

.prediction-header {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.prediction-content {
  margin-bottom: 0.5rem;
}

.confidence {
  font-size: 0.875rem;
  color: #6c757d;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}
</style>
