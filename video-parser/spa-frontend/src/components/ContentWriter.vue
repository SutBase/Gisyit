<template>
  <div class="content-writer">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">作品文案写作</h5>
      </div>
      <div class="card-body">
        <!-- 视频信息输入 -->
        <div class="mb-4">
          <label for="videoTitle" class="form-label">视频标题</label>
          <input 
            type="text" 
            class="form-control" 
            id="videoTitle" 
            v-model="videoInfo.title"
            placeholder="输入视频标题"
          >
        </div>

        <div class="mb-4">
          <label for="videoDescription" class="form-label">视频描述</label>
          <textarea 
            class="form-control" 
            id="videoDescription" 
            v-model="videoInfo.description"
            rows="3"
            placeholder="输入视频描述"
          ></textarea>
        </div>

        <div class="mb-4">
          <label for="videoTags" class="form-label">视频标签</label>
          <input 
            type="text" 
            class="form-control" 
            id="videoTags" 
            v-model="videoInfo.tags"
            placeholder="输入视频标签，用逗号分隔"
          >
        </div>

        <div class="mb-4">
          <label for="targetAudience" class="form-label">目标受众</label>
          <textarea 
            class="form-control" 
            id="targetAudience" 
            v-model="videoInfo.targetAudience"
            rows="2"
            placeholder="描述您的目标受众"
          ></textarea>
        </div>

        <!-- 文案类型选择 -->
        <div class="mb-4">
          <label class="form-label">文案类型</label>
          <div class="form-check form-check-inline">
            <input 
              class="form-check-input" 
              type="radio" 
              name="contentType" 
              id="typeTitle" 
              value="title"
              v-model="contentType"
            >
            <label class="form-check-label" for="typeTitle">标题优化</label>
          </div>
          <div class="form-check form-check-inline">
            <input 
              class="form-check-input" 
              type="radio" 
              name="contentType" 
              id="typeDescription" 
              value="description"
              v-model="contentType"
            >
            <label class="form-check-label" for="typeDescription">描述优化</label>
          </div>
          <div class="form-check form-check-inline">
            <input 
              class="form-check-input" 
              type="radio" 
              name="contentType" 
              id="typeTags" 
              value="tags"
              v-model="contentType"
            >
            <label class="form-check-label" for="typeTags">标签推荐</label>
          </div>
          <div class="form-check form-check-inline">
            <input 
              class="form-check-input" 
              type="radio" 
              name="contentType" 
              id="typeFull" 
              value="full"
              v-model="contentType"
            >
            <label class="form-check-label" for="typeFull">完整文案</label>
          </div>
        </div>

        <!-- 平台选择 -->
        <div class="mb-4">
          <label class="form-label">发布平台</label>
          <div class="form-check">
            <input 
              class="form-check-input" 
              type="checkbox" 
              id="platformBilibili" 
              value="bilibili"
              v-model="selectedPlatforms"
            >
            <label class="form-check-label" for="platformBilibili">哔哩哔哩</label>
          </div>
          <div class="form-check">
            <input 
              class="form-check-input" 
              type="checkbox" 
              id="platformDouyin" 
              value="douyin"
              v-model="selectedPlatforms"
            >
            <label class="form-check-label" for="platformDouyin">抖音</label>
          </div>
          <div class="form-check">
            <input 
              class="form-check-input" 
              type="checkbox" 
              id="platformYoutube" 
              value="youtube"
              v-model="selectedPlatforms"
            >
            <label class="form-check-label" for="platformYoutube">YouTube</label>
          </div>
        </div>

        <!-- 生成按钮 -->
        <div class="mb-4">
          <button 
            class="btn btn-primary" 
            @click="generateContent"
            :disabled="loading || !videoInfo.title.trim()"
          >
            <span v-if="!loading"><i class="bi bi-magic"></i> 生成文案</span>
            <span v-else>
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              生成中...
            </span>
          </button>
        </div>

        <!-- 生成结果 -->
        <div v-if="generatedContent" class="generated-content">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6>生成结果</h6>
            <div>
              <button class="btn btn-sm btn-outline-secondary me-2" @click="copyContent">
                <i class="bi bi-clipboard"></i> 复制
              </button>
              <button class="btn btn-sm btn-outline-primary" @click="regenerateContent">
                <i class="bi bi-arrow-clockwise"></i> 重新生成
              </button>
            </div>
          </div>

          <div class="result-container">
            <div v-if="contentType === 'title' || contentType === 'full'">
              <h6>标题建议</h6>
              <ul>
                <li v-for="(title, index) in generatedContent.titles" :key="index">{{ title }}</li>
              </ul>
            </div>

            <div v-if="contentType === 'description' || contentType === 'full'">
              <h6>描述建议</h6>
              <p>{{ generatedContent.description }}</p>
            </div>

            <div v-if="contentType === 'tags' || contentType === 'full'">
              <h6>标签建议</h6>
              <div>
                <span v-for="(tag, index) in generatedContent.tags" :key="index" 
                      class="badge bg-secondary me-1">{{ tag }}</span>
              </div>
            </div>

            <div v-if="contentType === 'full'">
              <h6>完整文案</h6>
              <div class="card">
                <div class="card-body">
                  <h6>{{ generatedContent.fullContent.title }}</h6>
                  <p>{{ generatedContent.fullContent.description }}</p>
                  <div>
                    <span v-for="(tag, index) in generatedContent.fullContent.tags" :key="index" 
                          class="badge bg-secondary me-1">{{ tag }}</span>
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
import { ref } from 'vue';
import { useAIAssistant } from '../composables/useAIAssistant';
import { useToast } from '../composables/useToast';

export default {
  name: 'ContentWriter',
  props: {
    videoData: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const { generateText } = useAIAssistant();
    const { showToast } = useToast();

    const videoInfo = ref({
      title: '',
      description: '',
      tags: '',
      targetAudience: ''
    });

    const contentType = ref('full');
    const selectedPlatforms = ref(['bilibili']);
    const loading = ref(false);
    const generatedContent = ref(null);

    // 监听视频数据变化
    watch(() => props.videoData, (newData) => {
      if (newData && newData.title) {
        videoInfo.value.title = newData.title;
      }
    }, { immediate: true, deep: true });

    // 生成文案
    const generateContent = async () => {
      if (!videoInfo.value.title.trim()) {
        showToast('请输入视频标题', 'warning');
        return;
      }

      loading.value = true;

      try {
        const prompt = buildPrompt();
        const response = await generateText(prompt);

        // 解析响应
        generatedContent.value = parseResponse(response);
      } catch (error) {
        showToast('生成文案失败: ' + error.message, 'danger');
      } finally {
        loading.value = false;
      }
    };

    // 构建提示词
    const buildPrompt = () => {
      const platformText = selectedPlatforms.value.join('、');

      let prompt = `请为以下视频生成适合${platformText}平台的${getContentTypeText()}：

`;
      prompt += `视频标题：${videoInfo.value.title}
`;

      if (videoInfo.value.description) {
        prompt += `视频描述：${videoInfo.value.description}
`;
      }

      if (videoInfo.value.tags) {
        prompt += `视频标签：${videoInfo.value.tags}
`;
      }

      if (videoInfo.value.targetAudience) {
        prompt += `目标受众：${videoInfo.value.targetAudience}
`;
      }

      // 根据内容类型添加特定要求
      if (contentType.value === 'title') {
        prompt += '
请生成5个吸引人的标题建议，每个标题不超过30字。';
      } else if (contentType.value === 'description') {
        prompt += '
请生成一段吸引人的视频描述，不超过200字。';
      } else if (contentType.value === 'tags') {
        prompt += '
请推荐10个相关的标签，每个标签不超过10字。';
      } else {
        prompt += '
请生成完整的视频文案，包括：
';
        prompt += '1. 3个吸引人的标题建议（每个不超过30字）
';
        prompt += '2. 一段吸引人的视频描述（不超过200字）
';
        prompt += '3. 10个相关的标签（每个不超过10字）
';
        prompt += '4. 一个整合以上内容的完整文案示例';
      }

      return prompt;
    };

    // 获取内容类型文本
    const getContentTypeText = () => {
      switch (contentType.value) {
        case 'title':
          return '标题';
        case 'description':
          return '描述';
        case 'tags':
          return '标签';
        case 'full':
          return '完整文案';
        default:
          return '内容';
      }
    };

    // 解析AI响应
    const parseResponse = (response) => {
      try {
        // 简单解析，实际应用中可能需要更复杂的解析逻辑
        const lines = response.split('
').filter(line => line.trim());

        if (contentType.value === 'title') {
          // 提取标题
          const titles = lines.filter(line => 
            line.match(/^\d+\./) || line.match(/^[-*]/)
          ).map(line => 
            line.replace(/^\d+\.\s*/, '').replace(/^[-*]\s*/, '')
          );

          return { titles };
        } else if (contentType.value === 'description') {
          // 提取描述
          const description = lines.join('
');
          return { description };
        } else if (contentType.value === 'tags') {
          // 提取标签
          const tags = lines.flatMap(line => 
            line.split(/[,，\s]/).filter(tag => tag.trim())
          );
          return { tags };
        } else {
          // 提取完整内容
          // 这里是简化版，实际应用中需要更复杂的解析
          return {
            titles: ['示例标题1', '示例标题2', '示例标题3'],
            description: '这是一段示例描述，展示了AI如何根据视频信息生成吸引人的文案。',
            tags: ['示例', '标签1', '标签2', '标签3'],
            fullContent: {
              title: '示例完整标题',
              description: '这是一段完整的示例描述，展示了AI如何根据视频信息生成吸引人的文案。',
              tags: ['示例', '标签1', '标签2', '标签3']
            }
          };
        }
      } catch (error) {
        console.error('解析AI响应失败:', error);
        throw new Error('解析生成内容失败');
      }
    };

    // 复制内容
    const copyContent = () => {
      let textToCopy = '';

      if (contentType.value === 'title' || contentType.value === 'full') {
        textToCopy += '标题建议：
';
        generatedContent.value.titles.forEach((title, index) => {
          textToCopy += `${index + 1}. ${title}
`;
        });
      }

      if (contentType.value === 'description' || contentType.value === 'full') {
        textToCopy += '
描述建议：
';
        textToCopy += generatedContent.value.description + '
';
      }

      if (contentType.value === 'tags' || contentType.value === 'full') {
        textToCopy += '
标签建议：
';
        textToCopy += generatedContent.value.tags.join(', ') + '
';
      }

      if (contentType.value === 'full') {
        textToCopy += '
完整文案：
';
        textToCopy += `标题：${generatedContent.value.fullContent.title}
`;
        textToCopy += `描述：${generatedContent.value.fullContent.description}
`;
        textToCopy += `标签：${generatedContent.value.fullContent.tags.join(', ')}
`;
      }

      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          showToast('内容已复制到剪贴板', 'success');
        })
        .catch(() => {
          showToast('复制失败，请手动复制', 'danger');
        });
    };

    // 重新生成内容
    const regenerateContent = () => {
      generateContent();
    };

    return {
      videoInfo,
      contentType,
      selectedPlatforms,
      loading,
      generatedContent,
      generateContent,
      copyContent,
      regenerateContent
    };
  }
};
</script>

<style scoped>
.content-writer {
  margin-bottom: 1.5rem;
}

.generated-content {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.375rem;
}

.result-container {
  background-color: white;
  padding: 1rem;
  border-radius: 0.375rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.result-container h6 {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: #495057;
}

.result-container h6:first-child {
  margin-top: 0;
}
</style>
