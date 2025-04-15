<template>
  <div class="monitor-card">
    <div class="card-header">
      <div class="sensor-name">{{ sensor.name }}</div>
      <div class="sensor-status">
        <div class="status-dot" :class="sensor.status"></div>
        <span class="status-text">{{ sensor.status === 'online' ? '在线' : '离线' }}</span>
      </div>
    </div>

    <div class="card-body">
      <div class="gauge-container">
        <el-progress
            type="dashboard"
            :percentage="calculatePercentage"
            :color="dynamicColor"
            :stroke-width="10"
            :width="130"
            :format="() => ''"
            :status="progressStatus"
        />
        <div class="gauge-value">
          <span class="value-text">{{ sensor.value }}</span>
          <span class="value-unit">{{ sensor.unit }}</span>
        </div>
      </div>

      <div class="sensor-range">
        <div class="range-item">
          <div class="range-label">最小值</div>
          <div class="range-value">{{ sensor.min }} {{ sensor.unit }}</div>
        </div>
        <div class="range-separator"></div>
        <div class="range-item">
          <div class="range-label">最大值</div>
          <div class="range-value">{{ sensor.max }} {{ sensor.unit }}</div>
        </div>
      </div>
    </div>

    <div class="card-footer">
      <div class="sensor-type-tag" :class="sensor.type">{{ sensorTypeLabel }}</div>
      <div class="sensor-status-text" :class="sensorValueStatus">
        {{ sensorValueStatusText }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  sensor: {
    type: Object,
    required: true
  }
});

// 计算进度条百分比
const calculatePercentage = computed(() => {
  const range = props.sensor.max - props.sensor.min;
  const value = props.sensor.value - props.sensor.min;
  return Math.round((value / range) * 100);
});

// 获取传感器值状态
const sensorValueStatus = computed(() => {
  if (props.sensor.status === 'offline') return 'offline';

  const range = props.sensor.max - props.sensor.min;
  const warningThreshold = range * 0.15;
  const dangerThreshold = range * 0.1;

  if (props.sensor.value <= props.sensor.min + dangerThreshold ||
      props.sensor.value >= props.sensor.max - dangerThreshold) {
    return 'danger';
  }

  if (props.sensor.value <= props.sensor.min + warningThreshold ||
      props.sensor.value >= props.sensor.max - warningThreshold) {
    return 'warning';
  }

  return 'normal';
});

// 获取动态颜色
const dynamicColor = computed(() => {
  if (sensorValueStatus.value === 'warning') return '#F79009';
  if (sensorValueStatus.value === 'danger') return '#F04438';
  return '#5E6AD2';
});

// 获取进度条状态
const progressStatus = computed(() => {
  if (props.sensor.status === 'offline') return 'exception';
  if (sensorValueStatus.value === 'warning') return 'warning';
  if (sensorValueStatus.value === 'danger') return 'exception';
  return 'success';
});

// 获取传感器值状态文本
const sensorValueStatusText = computed(() => {
  if (sensorValueStatus.value === 'offline') return '设备离线';
  if (sensorValueStatus.value === 'danger') return '数值异常';
  if (sensorValueStatus.value === 'warning') return '接近临界值';
  return '数值正常';
});

// 获取传感器类型标签
const sensorTypeLabel = computed(() => {
  const labels = {
    'temperature': '温度',
    'ph': '酸碱度',
    'oxygen': '溶解氧',
    'light': '光照',
    // 'water-level': '水位',
    'humidity': '湿度',
  };
  return labels[props.sensor.type] || props.sensor.type;
});
</script>

<style scoped>
.monitor-card {
  background-color: white;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05);
  display: flex;
  flex-direction: column;
  transition: all 0.2s ease;
}

.monitor-card:hover {
  box-shadow: 0 4px 8px rgba(16, 24, 40, 0.08);
  transform: translateY(-1px);
}

.card-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
}

.sensor-name {
  font-weight: 500;
  font-size: 15px;
  color: var(--text-primary);
}

.sensor-status {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.online {
  background-color: #12B76A;
}

.status-dot.offline {
  background-color: #F04438;
}

.status-text {
  font-size: 13px;
  color: var(--text-secondary);
}

.card-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background-color: #FCFCFD;
}

.gauge-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.gauge-value {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.value-text {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

.value-unit {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: -2px;
}

.sensor-range {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
}

.range-item {
  text-align: center;
}

.range-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 2px;
}

.range-value {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.range-separator {
  height: 1px;
  flex-grow: 1;
  background-color: var(--border-color);
  margin: 0 8px;
}

.card-footer {
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid var(--border-color);
}

.sensor-type-tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 16px;
  font-weight: 500;
}

.sensor-type-tag.temperature {
  background-color: rgba(217, 119, 6, 0.1);
  color: #D97706;
}

.sensor-type-tag.ph {
  background-color: rgba(147, 51, 234, 0.1);
  color: #9333EA;
}

.sensor-type-tag.oxygen {
  background-color: rgba(6, 182, 212, 0.1);
  color: #06B6D4;
}
.sensor-type-tag.humidity {
  background-color: rgba(6, 182, 212, 0.1);
  color: #065fd4;
}
.sensor-type-tag.light {
  background-color: rgba(245, 158, 11, 0.1);
  color: #F59E0B;
}

.sensor-type-tag.water-level {
  background-color: rgba(37, 99, 235, 0.1);
  color: #2563EB;
}

.sensor-status-text {
  font-size: 13px;
  font-weight: 500;
}

.sensor-status-text.normal {
  color: #12B76A;
}

.sensor-status-text.warning {
  color: #F79009;
}

.sensor-status-text.danger {
  color: #F04438;
}

.sensor-status-text.offline {
  color: var(--text-secondary);
}

/* 自定义 el-progress 样式 */
:deep(.el-progress__text) {
  font-size: 18px !important;
  font-weight: 600;
}

:deep(.el-progress-dashboard__inner) {
  transition: all 0.3s ease;
}

:deep(.el-progress__text .el-icon) {
  display: none !important;
}

:deep(.el-progress__text) {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
</style>
