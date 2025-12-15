<template>
  <div class="ai-assistant">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">AI助手</h5>
      </div>
      <div class="card-body">
        <!-- 模型选择 -->
        <div class="mb-3">
          <label for="modelSelect" class="form-label">选择AI模型</label>
          <select class="form-select" id="modelSelect" v-model="selectedModel">
            <option value="deepseek-chat">DeepSeek Chat</option>
            <option value="deepseek-reasoner">DeepSeek Reasoner</option>
          </select>
        </div>

        <!-- API密钥设置 -->
        <div class="mb-3">
          <label for="apiKey" class="form-label">API密钥</label>
          <div class="input-group">
            <input 
              :type="showApiKey ? 'text' : 'password'" 
              class="form-control" 
              id="apiKey" 
              v-model="apiKey"
              placeholder="输入DeepSeek API密钥"
            >
            <button class="btn btn-outline-secondary" type="button" @click="showApiKey = !showApiKey">
              <i :class="showApiKey ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
          <div class="form-text">API密钥将保存在本地浏览器中</div>
        </div>

        <!-- 聊天界面 -->
        <div class="chat-container">
          <div class="chat-messages" ref="chatMessages">
            <div v-for="(message, index) in messages" :key="index" 
                 :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
              <div class="message-content">
                <div v-if="message.role === 'assistant'" class="avatar">
                  <i class="bi bi-robot"></i>
                </div>
                <div v-else class="avatar">
                  <i class="bi bi-person"></i>
                </div>
                <div class="text">{{ message.content }}</div>
              </div>
            </div>
          </div>

          <div v-if="loading" class="message assistant-message">
            <div class="message-content">
              <div class="avatar">
                <i class="bi bi-robot"></i>
              </div>
              <div class="text">
                <div class="spinner-border spinner-border-sm" role="status">
                  <span class="visually-hidden">思考中...</span>
                </div>
                正在思考...
              </div>
            </div>
          </div>

          <div class="chat-input">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="userInput"
                placeholder="输入您的问题..."
                @keyup.enter="sendMessage"
                :disabled="loading || !apiKey"
              >
              <button class="btn btn-primary" type="button" @click="sendMessage" 
                      :disabled="loading || !apiKey || !userInput.trim()">
                <i class="bi bi-send"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- 预设问题 -->
        <div class="mt-3">
          <h6>预设问题</h6>
          <div class="preset-questions">
            <button v-for="(question, index) in presetQuestions" :key="index"
                    class="btn btn-sm btn-outline-secondary me-2 mb-2"
                    @click="askPresetQuestion(question)">
              {{ question }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick, watch } from 'vue';
import { useAIAssistant } from '../composables/useAIAssistant';

export default {
  name: 'AIAssistant',
  props: {
    initialPrompt: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const { 
      messages, 
      loading, 
      sendMessage: sendAIMessage, 
      apiKey, 
      selectedModel,
      saveApiKey,
      saveModel
    } = useAIAssistant();

    const userInput = ref('');
    const showApiKey = ref(false);
    const chatMessages = ref(null);

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
      if (!userInput.value.trim() || loading.value || !apiKey.value) return;

      const message = userInput.value.trim();
      userInput.value = '';

      await sendAIMessage(message);

      // 滚动到底部
      await nextTick();
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      }
    };

    // 询问预设问题
    const askPresetQuestion = (question) => {
      userInput.value = question;
      sendMessage();
    };

    // 监听API密钥变化
    watch(apiKey, (newKey) => {
      if (newKey) {
        saveApiKey(newKey);
      }
    });

    // 监听模型变化
    watch(selectedModel, (newModel) => {
      if (newModel) {
        saveModel(newModel);
      }
    });

    // 监听初始提示
    watch(() => props.initialPrompt, (newPrompt) => {
      if (newPrompt && newPrompt.trim()) {
        userInput.value = newPrompt;
        sendMessage();
      }
    }, { immediate: true });

    onMounted(() => {
      // 滚动到底部
      if (chatMessages.value) {
        chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
      }
    });

    return {
      messages,
      loading,
      userInput,
      apiKey,
      selectedModel,
      showApiKey,
      chatMessages,
      presetQuestions,
      sendMessage,
      askPresetQuestion
    };
  }
};
</script>

<style scoped>
.ai-assistant {
  margin-bottom: 1.5rem;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 400px;
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background-color: #f8f9fa;
}

.message {
  margin-bottom: 1rem;
}

.message-content {
  display: flex;
  align-items: flex-start;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

.user-message .avatar {
  background-color: #0d6efd;
  color: white;
}

.assistant-message .avatar {
  background-color: #6c757d;
  color: white;
}

.text {
  flex: 1;
  background-color: white;
  padding: 0.75rem;
  border-radius: 0.375rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chat-input {
  padding: 1rem;
  border-top: 1px solid #dee2e6;
  background-color: white;
}

.preset-questions {
  display: flex;
  flex-wrap: wrap;
}
</style>
