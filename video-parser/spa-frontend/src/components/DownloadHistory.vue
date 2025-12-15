<template>
  <div class="download-history">
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">下载历史</h5>
        <button class="btn btn-sm btn-outline-danger" @click="clearHistory">
          <i class="bi bi-trash"></i> 清空历史
        </button>
      </div>
      <div class="card-body">
        <div v-if="history.length === 0" class="text-center py-3 text-muted">
          <i class="bi bi-clock-history" style="font-size: 2rem;"></i>
          <p class="mt-2">暂无下载历史</p>
        </div>
        <div v-else>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>标题</th>
                  <th>平台</th>
                  <th>质量</th>
                  <th>格式</th>
                  <th>下载时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in history" :key="index">
                  <td>{{ item.title }}</td>
                  <td>{{ item.platform }}</td>
                  <td>{{ item.quality }}</td>
                  <td>{{ item.format }}</td>
                  <td>{{ formatDateTime(item.timestamp) }}</td>
                  <td>
                    <button class="btn btn-sm btn-outline-primary" @click="generateContent(item)">
                      <i class="bi bi-pencil-square"></i> 生成文案
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 分页 -->
          <nav v-if="totalPages > 1" aria-label="历史记录分页">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">上一页</a>
              </li>
              <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: currentPage === page }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">下一页</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useDownloadHistory } from '../composables/useDownloadHistory';

export default {
  name: 'DownloadHistory',
  emits: ['generate-content'],
  setup(props, { emit }) {
    const { history, clearHistory } = useDownloadHistory();
    const currentPage = ref(1);
    const itemsPerPage = 10;

    // 计算总页数
    const totalPages = computed(() => {
      return Math.ceil(history.value.length / itemsPerPage);
    });

    // 获取当前页的数据
    const paginatedHistory = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage;
      const end = start + itemsPerPage;
      return history.value.slice(start, end);
    });

    // 切换页面
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
      }
    };

    // 格式化日期时间
    const formatDateTime = (timestamp) => {
      if (!timestamp) return '';

      const date = new Date(timestamp);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    // 生成内容
    const generateContent = (item) => {
      emit('generate-content', item);
    };

    return {
      history: paginatedHistory,
      currentPage,
      totalPages,
      clearHistory,
      changePage,
      formatDateTime,
      generateContent
    };
  }
};
</script>

<style scoped>
.download-history {
  margin-bottom: 1.5rem;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.pagination {
  margin-top: 1rem;
}
</style>
