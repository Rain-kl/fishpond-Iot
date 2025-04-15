<template>
  <div class="page-container">
    <div class="page-header">
      <h2>实时控制</h2>
    </div>
    <div class="control-grid">
      <ControlCard
          v-for="device in devices"
          :key="device.id"
          :device="device"
          @toggle="toggleDevice"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import ControlCard from '../components/ControlCard.vue'
import { controllerApi } from '../api'

const devices = ref([]);
const updateInterval = ref(null);

// 获取控制器数据
const fetchControllerData = async () => {
  try {
    const response = await controllerApi.getControllerData();
    devices.value = response.data;
  } catch (error) {
    console.error('获取控制器数据出错:', error);
  }
};

const toggleDevice = async (deviceId, action) => {
  const device = devices.value.find(d => d.id === deviceId);
  if (device) {
    try {
      // 在实际应用中，可以取消注释以下代码，实现真实API调用
      // await controllerApi.toggleDevice(deviceId, action);
      
      // 暂时直接修改本地状态
      if (action === 'on') {
        device.isOn = true;
      } else if (action === 'off') {
        device.isOn = false;
      }
      
      console.log(`设备 ${device.name} ${action === 'on' ? '开启' : '关闭'}`);
    } catch (error) {
      console.error(`控制设备出错:`, error);
    }
  }
};

// 设置自动更新
const setupAutoUpdate = () => {
  // 清除之前的定时器
  if (updateInterval.value) {
    clearInterval(updateInterval.value);
  }
  
  // 设置每秒更新一次
  updateInterval.value = setInterval(() => {
    fetchControllerData();
  }, 1000);
};

// 组件挂载时获取数据并设置自动更新
onMounted(() => {
  fetchControllerData();
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
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.page-header {
  color: black;
  margin-bottom: 20px;
}

.control-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>
