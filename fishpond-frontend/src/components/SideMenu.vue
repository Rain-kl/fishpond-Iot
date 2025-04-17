<template>
  <div class="side-menu-container">
    <div class="logo">
      <img :src="fishLogo" alt="Logo"/>
    </div>
    <div class="menu-wrapper">
      <router-link
          v-for="(item, index) in menuItems"
          :key="index"
          :to="item.path"
          class="menu-item"
          :class="{ 'active': $route.path.includes(item.path) }"
      >
        <el-icon class="menu-icon">
          <component :is="item.icon" />
        </el-icon>
        <span class="menu-text">{{ item.title }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Monitor, SetUp, InfoFilled,Histogram } from '@element-plus/icons-vue'
import fishLogo from '../assets/logo.png'

const menuItems = ref([
  {
    title: '实时监测',
    path: '/monitor',
    icon: Monitor
  },
  {
    title: '实时控制',
    path: '/control',
    icon: SetUp
  },
  {
    title: '历史数据',
    path: '/history',
    icon: Histogram
  },
  {
    title: '关于我们',
    path: '/about',
    icon: InfoFilled
  }
])
</script>

<style scoped>
.side-menu-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #F9F9FF;
  padding: 12px;
  width: 56px;
  border-right: 1px solid #EAECF0;
}

.logo {
  padding: 20px 0;
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.logo img {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.menu-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 16px;
}

.menu-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px 0;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
}

.menu-item:hover {
  background-color: rgba(94, 106, 210, 0.04);
}

.menu-item.active {
  background-color: rgba(94, 106, 210, 0.1);
}

.menu-item.active::before {
  content: "";
  position: absolute;
  left: -12px;
  top: 8px;
  bottom: 8px;
  width: 3px;
  background-color: #5E6AD2;
  border-radius: 0 2px 2px 0;
}

.menu-icon {
  font-size: 22px;
  color: #667085;
  margin-bottom: 6px;
  transition: color 0.2s ease;
}

.menu-item:hover .menu-icon {
  color: #5E6AD2;
}

.menu-item.active .menu-icon {
  color: #5E6AD2;
}

.menu-text {
  font-size: 11px;
  font-weight: 500;
  color: #667085;
  text-align: center;
  transition: color 0.2s ease;
}

.menu-item:hover .menu-text {
  color: #5E6AD2;
}

.menu-item.active .menu-text {
  color: #5E6AD2;
  font-weight: 600;
}
</style>
