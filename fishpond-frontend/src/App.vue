<template>
  <div class="app-container">
    <div class="side-menu">
      <SideMenu/>
    </div>
    <div class="main-content">
      <div class="header">
        <div class="header-left">
          <h1 class="app-title">水产养殖智能监控系统</h1>
        </div>
        <div class="header-right">
          <div class="time-display">
            <div class="time-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="time">{{ currentTime }}</div>
          </div>
        </div>
      </div>

      <div class="page-container">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue'
import { Clock } from '@element-plus/icons-vue'
import SideMenu from './components/SideMenu.vue'

const currentTime = ref('00:00')

const updateTime = () => {
  const now = new Date()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  currentTime.value = `${hours}:${minutes}`
}

let timer

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 60000) // 每分钟更新一次
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style>
:root {
  --primary-color: #5E6AD2;
  --background-color: #F8F9FC;
  --card-background: #FFFFFF;
  --text-primary: #101828;
  --text-secondary: #667085;
  --border-color: #EAECF0;
  --hover-color: rgba(94, 106, 210, 0.04);
}

body {
  margin: 0;
  font-family: 'Inter', 'Microsoft YaHei', sans-serif;
  color: var(--text-primary);
  background-color: var(--background-color);
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: var(--background-color);
}

.side-menu {
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: 80px;
  background-color: var(--card-background);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}

.header-left {
  display: flex;
  align-items: center;
}

.app-title {
  font-size: 26px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  background-color: var(--background-color);
}

.time-icon {
  color: var(--primary-color);
  display: flex;
  align-items: center;
}

.time {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
}

.page-container {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .control-grid, .monitor-grid {
    grid-template-columns: 1fr;
  }

  .header {
    padding: 0 16px;
  }

  .page-container {
    padding: 16px;
  }
}
</style>
