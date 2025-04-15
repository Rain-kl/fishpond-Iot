<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">实时监测</h2>
      <div class="header-actions">
        <button class="refresh-button" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          <span>刷新数据</span>
        </button>
      </div>
    </div>

    <div class="status-summary">
      <div class="status-item" :class="getStatusClass(onlineSensorsCount)">
        <div class="status-value">{{ onlineSensorsCount }}/{{ sensors.length }}</div>
        <div class="status-label">传感器在线</div>
      </div>
      <div class="status-item" :class="getAlertClass(alertsCount)">
        <div class="status-value">{{ alertsCount }}</div>
        <div class="status-label">异常指标</div>
      </div>
    </div>

    <div class="monitor-grid">
      <MonitorCard
          v-for="sensor in sensors"
          :key="sensor.id"
          :sensor="sensor"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import MonitorCard from '../components/MonitorCard.vue'
import { monitorApi } from '../api'

const sensors = ref([]);
const updateInterval = ref(null);

// 获取监测数据
const fetchMonitorData = async () => {
  try {
    const response = await monitorApi.getMonitorData();
    // 将数据值格式化为小数点后1位
    sensors.value = response.data.map(sensor => ({
      ...sensor,
      value: Number(sensor.value.toFixed(1))
    }));
  } catch (error) {
    console.error('获取监测数据出错:', error);
  }
};

// 计算在线传感器数量
const onlineSensorsCount = computed(() => {
  return sensors.value.filter(sensor => sensor.status === 'online').length;
});

// 计算异常指标数量
const alertsCount = computed(() => {
  return sensors.value.filter(sensor => {
    const range = sensor.max - sensor.min;
    const dangerThreshold = range * 0.1;
    const warningThreshold = range * 0.15;

    return (sensor.status === 'online') && (
        sensor.value <= sensor.min + dangerThreshold ||
        sensor.value >= sensor.max - dangerThreshold ||
        sensor.value <= sensor.min + warningThreshold ||
        sensor.value >= sensor.max - warningThreshold
    );
  }).length;
});

// 获取传感器状态的CSS类
const getStatusClass = (count) => {
  const percentage = count / sensors.value.length;
  if (percentage >= 0.8) return 'status-good';
  if (percentage >= 0.5) return 'status-warning';
  return 'status-danger';
};

// 获取警报状态的CSS类
const getAlertClass = (count) => {
  if (count === 0) return 'status-good';
  if (count <= 2) return 'status-warning';
  return 'status-danger';
};

// 刷新数据
const refreshData = () => {
  fetchMonitorData();
};

// 设置自动更新
const setupAutoUpdate = () => {
  // 清除之前的定时器
  if (updateInterval.value) {
    clearInterval(updateInterval.value);
  }
  
  // 设置每秒更新一次
  updateInterval.value = setInterval(() => {
    fetchMonitorData();
  }, 1000);
};

// 组件挂载时获取数据并设置自动更新
onMounted(() => {
  fetchMonitorData();
  setupAutoUpdate();
});

// 组件卸载前清除定时器
onBeforeUnmount(() => {
  if (updateInterval.value) {
    clearInterval(updateInterval.value);
    updateInterval.value = null;
  }
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

.refresh-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-button:hover {
  background-color: var(--hover-color);
  border-color: #D0D5DD;
  color: var(--primary-color);
}

.refresh-button .el-icon {
  font-size: 16px;
}

.status-summary {
  display: flex;
  gap: 16px;
}

.status-item {
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 16px;
  min-width: 140px;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05);
}

.status-value {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 4px;
}

.status-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.status-good .status-value {
  color: #12B76A;
}

.status-warning .status-value {
  color: #F79009;
}

.status-danger .status-value {
  color: #F04438;
}

.monitor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

@media (max-width: 768px) {
  .monitor-grid {
    grid-template-columns: 1fr;
  }

  .status-summary {
    flex-direction: column;
  }
}
</style>
