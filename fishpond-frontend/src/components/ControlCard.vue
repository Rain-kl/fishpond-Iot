<template>
  <div class="control-card" :class="cardStatusClass">
    <div class="card-header" :class="headerStatusClass">
      <span class="device-name">{{ device.name }}</span>
      <div class="status-indicator">
        <div class="status-dot" :class="device.status"></div>
        <span class="status-text">{{ statusText }}</span>
      </div>
    </div>
    <div class="card-content">
      <div class="device-icon" :class="{ 'inactive': isInactive, 'active': !isInactive }">
        <img :src="getIconPath(device.icon)" :alt="device.name"/>
      </div>
    </div>
    <div class="card-footer">
      <el-switch
          v-model="deviceOn"
          size="large"
          :disabled="device.status === 'offline'"
          :active-color="'#5E6AD2'"
          :inactive-color="'#e0e0e0'"
          @change="handleToggle"
      />
      <span class="switch-label">{{ deviceOn ? '已开启' : '已关闭' }}</span>
    </div>
  </div>
</template>

<script setup>
import {defineProps, defineEmits, computed, ref, watch} from 'vue'

const props = defineProps({
  device: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['toggle'])

const deviceOn = ref(props.device.isOn)

watch(() => props.device.isOn, (newValue) => {
  deviceOn.value = newValue
})

const isInactive = computed(() => {
  return props.device.status === 'offline' || !deviceOn.value
})

// 计算卡片状态类
const cardStatusClass = computed(() => {
  if (props.device.status === 'offline') return 'offline'
  return deviceOn.value ? 'online-on' : 'online-off'
})

// 计算头部状态类
const headerStatusClass = computed(() => {
  if (props.device.status === 'offline') return 'header-offline'
  return deviceOn.value ? 'header-online-on' : 'header-online-off'
})

// 计算状态文本
const statusText = computed(() => {
  if (props.device.status === 'offline') return '离线'
  // return deviceOn.value ? '运行中' : '已停止'
  return ''
})

const handleToggle = (value) => {
  emit('toggle', props.device.id, value ? 'on' : 'off')
}

const getIconPath = (iconName) => {
  return new URL(`../assets/${iconName}`, import.meta.url).href
}
</script>

<style scoped>
.control-card {
  background-color: #FFFFFF;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(16, 24, 40, 0.1);
  border: 1px solid #F2F4F7;
  transition: all 0.2s ease;
}

.control-card:hover {
  box-shadow: 0 4px 8px rgba(16, 24, 40, 0.08);
  transform: translateY(-1px);
}

/* 离线卡片样式 */
.control-card.offline {
  background-color: #FAFAFA;
  border: 1px solid #EFEFEF;
}

/* 在线但关闭的卡片样式 */
.control-card.online-off {
  border: 1px solid #FFFFFF;
}

/* 在线且开启的卡片样式 */
.control-card.online-on {
  border: 1px solid #C8E6C9;
}

.card-header {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #F2F4F7;
  transition: all 0.3s ease;
}

/* 离线头部样式 - 灰色 */
.card-header.header-offline {
  background-color: #d8d8d8;
  border-bottom: 1px solid #d8d8d8;
}

/* 在线但关闭头部样式 - 红色 */
.card-header.header-online-off {
  background-color: #ffe5e8;
  border-bottom: 1px solid #ffe5e8;
}

/* 在线且开启头部样式 - 绿色 */
.card-header.header-online-on {
  background-color: #E8F5E9;
  border-bottom: 1px solid #C8E6C9;
}

.device-name {
  font-weight: 500;
  font-size: 15px;
  color: #101828;
}

.status-indicator {
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
  color: #667085;
}

.card-content {
  padding: 32px 20px;
  display: flex;
  justify-content: center;
  background-color: #FCFCFD;
}

.device-icon img {
  width: 64px;
  height: 64px;
  transition: all 0.3s ease;
}

.device-icon.inactive img {
  filter: grayscale(100%) brightness(1.1) opacity(0.7);
}

.device-icon.active img {
  filter: none;
}

.card-footer {
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background-color: #FFFFFF;
  border-top: 1px solid #F2F4F7;
}

.switch-label {
  font-size: 13px;
  color: #667085;
}

/* 覆盖 element-plus 的开关样式 */
:deep(.el-switch.is-checked .el-switch__core) {
  background-color: #5E6AD2 !important;
  border-color: #5E6AD2 !important;
}

:deep(.el-switch__core) {
  border-radius: 12px;
}
</style>
