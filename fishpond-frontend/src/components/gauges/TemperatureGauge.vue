<!-- components/gauges/TemperatureGauge.vue -->
<template>
  <div class="temperature-gauge">
    <div class="gauge-body">
      <div class="mercury-container">
        <div class="mercury" :style="{ height: mercuryHeight + '%' }"></div>
      </div>
      <div class="scale">
        <div v-for="n in 5" :key="n" class="mark">
          <span>{{ max - (n-1) * step }}</span>
        </div>
      </div>
    </div>
    <div class="gauge-value">{{ value }}{{ unit }}</div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 40
  },
  unit: {
    type: String,
    default: '°C'
  }
})

const step = computed(() => (props.max - props.min) / 4)
const mercuryHeight = computed(() => {
  const percentage = ((props.value - props.min) / (props.max - props.min)) * 100
  return Math.min(Math.max(percentage, 0), 100)
})
</script>

<style scoped>
.temperature-gauge {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.gauge-body {
  display: flex;
  height: 150px;
  margin-bottom: 10px;
}

.mercury-container {
  width: 20px;
  height: 100%;
  background-color: #e0e0e0;
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.mercury {
  position: absolute;
  bottom: 0;
  width: 100%;
  background-color: #ff4d4f;
  transition: height 0.5s;
}

.scale {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  margin-left: 5px;
}

.mark {
  font-size: 12px;
  color: #666;
}

.gauge-value {
  font-size: 16px;
  font-weight: bold;
}
</style>
