<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">历史数据</h2>
      <div class="header-actions">
        <el-select v-model="selectedDuration" class="duration-select" placeholder="选择时间范围">
          <el-option
            v-for="item in durationOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <el-select v-model="selectedDevice" class="device-select" placeholder="选择设备">
          <el-option
            v-for="item in deviceOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        <button class="query-button" @click="queryData">
          <el-icon><Search /></el-icon>
          <span>查询</span>
        </button>
      </div>
    </div>

    <div class="chart-container">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="光照度" name="light">
          <div class="chart-wrapper">
            <LineChart :chartData="lightChartData" :chartOptions="chartOptions" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="溶解氧" name="oxygen">
          <div class="chart-wrapper">
            <LineChart :chartData="oxygenChartData" :chartOptions="chartOptions" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="鱼塘水温" name="temperature">
          <div class="chart-wrapper">
            <LineChart :chartData="temperatureChartData" :chartOptions="chartOptions" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="鱼塘水位" name="waterLevel">
          <div class="chart-wrapper">
            <LineChart :chartData="waterLevelChartData" :chartOptions="chartOptions" />
          </div>
        </el-tab-pane>
        <el-tab-pane label="水质PH" name="ph">
          <div class="chart-wrapper">
            <LineChart :chartData="phChartData" :chartOptions="chartOptions" />
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { historyApi } from '../api'
import LineChart from '../components/LineChart.vue'
import { ElMessage } from 'element-plus'

// 设备选项
const deviceOptions = [
  { value: '1', label: '光照度传感器' },
  { value: '2', label: '溶解氧传感器' },
  { value: '3', label: '水温传感器' },
  { value: '4', label: '水位传感器' },
  { value: '5', label: 'PH传感器' }
]

// 时间范围选项
const durationOptions = [
  { value: '1hour', label: '最近1小时' },
  { value: '6hour', label: '最近6小时' },
  { value: '12hour', label: '最近12小时' },
  { value: '1days', label: '最近1天' },
  { value: '5days', label: '最近5天' },
  { value: '14days', label: '最近14天' },
  { value: '1month', label: '最近1个月' }
]

const activeTab = ref('light')
const selectedDevice = ref('1')
const selectedDuration = ref('12hour')
const historyData = ref([])

// 图表数据
const lightChartData = ref({
  labels: [],
  datasets: [
    {
      label: '光照度 (Lx)',
      data: [],
      borderColor: '#4B9EFA',
      tension: 0.4
    }
  ]
})

const oxygenChartData = ref({
  labels: [],
  datasets: [
    {
      label: '溶解氧 (mg/L)',
      data: [],
      borderColor: '#12B76A',
      tension: 0.4
    }
  ]
})

const temperatureChartData = ref({
  labels: [],
  datasets: [
    {
      label: '水温 (°C)',
      data: [],
      borderColor: '#F79009',
      tension: 0.4
    }
  ]
})

const waterLevelChartData = ref({
  labels: [],
  datasets: [
    {
      label: '水位 (cm)',
      data: [],
      borderColor: '#9E77ED',
      tension: 0.4
    }
  ]
})

const phChartData = ref({
  labels: [],
  datasets: [
    {
      label: 'PH值',
      data: [],
      borderColor: '#F04438',
      tension: 0.4
    }
  ]
})

// 图表配置选项
const chartOptions = {
  // ECharts配置覆盖项（如果需要）
}

// 格式化时间
const formatDateTime = (dateTimeStr) => {
  const date = new Date(dateTimeStr)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${month}-${day} ${hours}:${minutes}`
}

// 查询历史数据
const queryData = async () => {
  try {
    const response = await historyApi.getHistoryData(selectedDevice.value, selectedDuration.value)
    
    // 检查是否有数据点
    if (response.datapoints && response.datapoints.length === 0) {
      // 使用Element Plus的消息提示
      ElMessage({
        message: '当前时间段无数据',
        type: 'info',
        duration: 3000
      })
    }
    
    historyData.value = response.datapoints || []
    if (!historyData.value.length && response.datapoints) {
      historyData.value = response.datapoints
    }
    updateChartData()
  } catch (error) {
    console.error('获取历史数据出错:', error)
  }
}

// 更新图表数据
const updateChartData = () => {
  const times = historyData.value.map(item => formatDateTime(item.at))
  const values = historyData.value.map(item => parseFloat(item.value))
  
  // 根据当前设备类型更新对应图表数据
  switch (selectedDevice.value) {
    case '1': // 光照度
      lightChartData.value = {
        labels: times,
        datasets: [
          {
            label: '光照度 (Lx)',
            data: values,
            borderColor: '#4B9EFA',
            tension: 0.4
          }
        ]
      }
      activeTab.value = 'light'
      break
    case '2': // 溶解氧
      oxygenChartData.value = {
        labels: times,
        datasets: [
          {
            label: '溶解氧 (mg/L)',
            data: values,
            borderColor: '#12B76A',
            tension: 0.4
          }
        ]
      }
      activeTab.value = 'oxygen'
      break
    case '3': // 水温
      temperatureChartData.value = {
        labels: times,
        datasets: [
          {
            label: '水温 (°C)',
            data: values,
            borderColor: '#F79009',
            tension: 0.4
          }
        ]
      }
      activeTab.value = 'temperature'
      break
    case '4': // 水位
      waterLevelChartData.value = {
        labels: times,
        datasets: [
          {
            label: '水位 (cm)',
            data: values,
            borderColor: '#9E77ED',
            tension: 0.4
          }
        ]
      }
      activeTab.value = 'waterLevel'
      break
    case '5': // PH
      phChartData.value = {
        labels: times,
        datasets: [
          {
            label: 'PH值',
            data: values,
            borderColor: '#F04438',
            tension: 0.4
          }
        ]
      }
      activeTab.value = 'ph'
      break
  }
}

// 组件挂载时加载默认数据
onMounted(() => {
  queryData()
})

// 监听标签页变化，确保图表正确显示
watch(activeTab, (newTab) => {
  // 延迟执行以确保DOM已更新
  setTimeout(() => {
    window.dispatchEvent(new Event('resize'));
  }, 100);
});
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.duration-select,
.device-select {
  width: 150px;
}

.query-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background-color: #4B9EFA;
  border: none;
  border-radius: 6px;
  color: white;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.query-button:hover {
  background-color: #3A7FD5;
}

.query-button .el-icon {
  font-size: 16px;
}

.chart-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05);
  padding: 30px;
  min-height: 430px;
}

.chart-wrapper {
  height: 350px;
  margin-top: 5px;
  width: 100%;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
}

/* 确保每个tab面板都是相同大小 */
:deep(.el-tabs__content) {
  height: 450px;
}

:deep(.el-tab-pane) {
  height: 100%;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .header-actions {
    width: 100%;
    flex-direction: column;
  }

  .duration-select,
  .device-select {
    width: 100%;
  }
}
</style> 