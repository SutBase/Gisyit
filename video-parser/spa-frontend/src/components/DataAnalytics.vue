<template>
  <div class="data-analytics">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">数据分析与统计</h5>
      </div>
      <div class="card-body">
        <div class="row">
          <!-- 平台分布饼图 -->
          <div class="col-md-6 mb-4">
            <div class="chart-container">
              <h6>平台分布</h6>
              <div ref="platformChart" class="chart"></div>
            </div>
          </div>

          <!-- 质量分布柱状图 -->
          <div class="col-md-6 mb-4">
            <div class="chart-container">
              <h6>质量分布</h6>
              <div ref="qualityChart" class="chart"></div>
            </div>
          </div>

          <!-- 下载趋势折线图 -->
          <div class="col-12 mb-4">
            <div class="chart-container">
              <h6>下载趋势</h6>
              <div ref="trendChart" class="chart"></div>
            </div>
          </div>

          <!-- 统计数据表格 -->
          <div class="col-12">
            <h6>详细统计</h6>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>平台</th>
                    <th>下载数量</th>
                    <th>最常下载质量</th>
                    <th>最常下载格式</th>
                    <th>最近下载时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(stat, index) in platformStats" :key="index">
                    <td>{{ stat.platform }}</td>
                    <td>{{ stat.count }}</td>
                    <td>{{ stat.topQuality }}</td>
                    <td>{{ stat.topFormat }}</td>
                    <td>{{ formatDateTime(stat.lastDownload) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useDownloadHistory } from '../composables/useDownloadHistory';
import * as echarts from 'echarts';

export default {
  name: 'DataAnalytics',
  setup() {
    const { history } = useDownloadHistory();
    const platformChart = ref(null);
    const qualityChart = ref(null);
    const trendChart = ref(null);
    const platformStats = ref([]);

    // 平台统计
    const calculatePlatformStats = () => {
      const stats = {};

      history.value.forEach(item => {
        if (!stats[item.platform]) {
          stats[item.platform] = {
            platform: item.platform,
            count: 0,
            qualities: {},
            formats: {},
            lastDownload: null
          };
        }

        const stat = stats[item.platform];
        stat.count++;

        // 统计质量
        if (!stat.qualities[item.quality]) {
          stat.qualities[item.quality] = 0;
        }
        stat.qualities[item.quality]++;

        // 统计格式
        if (!stat.formats[item.format]) {
          stat.formats[item.format] = 0;
        }
        stat.formats[item.format]++;

        // 更新最近下载时间
        if (!stat.lastDownload || new Date(item.timestamp) > new Date(stat.lastDownload)) {
          stat.lastDownload = item.timestamp;
        }
      });

      // 转换为数组并计算最常下载的质量和格式
      const result = Object.values(stats).map(stat => {
        const topQuality = Object.entries(stat.qualities)
          .sort((a, b) => b[1] - a[1])[0][0];

        const topFormat = Object.entries(stat.formats)
          .sort((a, b) => b[1] - a[1])[0][0];

        return {
          platform: stat.platform,
          count: stat.count,
          topQuality,
          topFormat,
          lastDownload: stat.lastDownload
        };
      });

      platformStats.value = result;
      return result;
    };

    // 初始化平台分布饼图
    const initPlatformChart = (stats) => {
      if (!platformChart.value) return;

      const chart = echarts.init(platformChart.value);
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: stats.map(item => item.platform)
        },
        series: [
          {
            name: '平台分布',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: stats.map(item => ({
              value: item.count,
              name: item.platform
            }))
          }
        ]
      };

      chart.setOption(option);

      // 响应式调整
      window.addEventListener('resize', () => {
        chart.resize();
      });
    };

    // 初始化质量分布柱状图
    const initQualityChart = () => {
      if (!qualityChart.value) return;

      const qualityStats = {};
      history.value.forEach(item => {
        if (!qualityStats[item.quality]) {
          qualityStats[item.quality] = 0;
        }
        qualityStats[item.quality]++;
      });

      const chart = echarts.init(qualityChart.value);
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: Object.keys(qualityStats)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '下载数量',
            type: 'bar',
            data: Object.values(qualityStats)
          }
        ]
      };

      chart.setOption(option);

      // 响应式调整
      window.addEventListener('resize', () => {
        chart.resize();
      });
    };

    // 初始化下载趋势折线图
    const initTrendChart = () => {
      if (!trendChart.value) return;

      // 按日期统计下载数量
      const dateStats = {};
      history.value.forEach(item => {
        const date = new Date(item.timestamp).toLocaleDateString('zh-CN');
        if (!dateStats[date]) {
          dateStats[date] = 0;
        }
        dateStats[date]++;
      });

      // 排序日期
      const sortedDates = Object.keys(dateStats).sort((a, b) => {
        return new Date(a) - new Date(b);
      });

      const chart = echarts.init(trendChart.value);
      const option = {
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: sortedDates
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '下载数量',
            type: 'line',
            stack: 'Total',
            areaStyle: {},
            emphasis: {
              focus: 'series'
            },
            data: sortedDates.map(date => dateStats[date])
          }
        ]
      };

      chart.setOption(option);

      // 响应式调整
      window.addEventListener('resize', () => {
        chart.resize();
      });
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

    // 初始化所有图表
    const initCharts = () => {
      const stats = calculatePlatformStats();
      initPlatformChart(stats);
      initQualityChart();
      initTrendChart();
    };

    onMounted(() => {
      initCharts();
    });

    // 监听历史数据变化，更新图表
    watch(history, () => {
      initCharts();
    }, { deep: true });

    return {
      platformChart,
      qualityChart,
      trendChart,
      platformStats,
      formatDateTime
    };
  }
};
</script>

<style scoped>
.data-analytics {
  margin-bottom: 1.5rem;
}

.chart-container {
  height: 300px;
}

.chart {
  width: 100%;
  height: 100%;
}
</style>
