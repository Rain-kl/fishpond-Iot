<template>
  <div class="chart-container" ref="chartContainer"></div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartOptions: {
    type: Object,
    default: () => ({})
  }
})

const chartContainer = ref(null)
let chartInstance = null

// 初始化图表
const initChart = () => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  // 确保DOM已经渲染
  if (!chartContainer.value) return
  
  // 初始化ECharts实例
  chartInstance = echarts.init(chartContainer.value, null, {
    renderer: 'canvas',
    useDirtyRect: true
  })
  
  // 设置图表配置项
  updateChart()
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', resizeChart)
}

// 更新图表数据和配置
const updateChart = () => {
  if (!chartInstance) return
  
  // 准备数据
  const { labels = [], datasets = [] } = props.chartData
  const series = datasets.map(dataset => ({
    name: dataset.label,
    type: 'line',
    data: dataset.data,
    smooth: true,
    symbol: 'emptyCircle',
    symbolSize: 3,
    showSymbol: false,
    lineStyle: {
      width: 2,
      color: dataset.borderColor
    },
    itemStyle: {
      color: dataset.borderColor,
      borderWidth: 2
    },
    emphasis: {
      itemStyle: {
        color: '#fff',
        borderColor: dataset.borderColor,
        borderWidth: 3,
        shadowColor: 'rgba(0, 0, 0, 0.3)',
        shadowBlur: 8
      }
    },
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        {
          offset: 0,
          color: echarts.color.modifyAlpha(dataset.borderColor, 0.3)
        },
        {
          offset: 1,
          color: echarts.color.modifyAlpha(dataset.borderColor, 0.05)
        }
      ])
    }
  }))
  
  // 基础配置
  const option = {
    animation: true,
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#eee',
      borderWidth: 1,
      textStyle: {
        color: '#333'
      },
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        },
        lineStyle: {
          color: 'rgba(0, 0, 0, 0.2)',
          width: 1
        }
      },
      formatter: function(params) {
        let result = `<div style="font-weight:bold;margin-bottom:5px;">${params[0].axisValue}</div>`;
        params.forEach(param => {
          result += `<div style="margin: 3px 0; display:flex; align-items:center;">
            <span style="display:inline-block;width:10px;height:10px;background-color:${param.color};margin-right:5px;border-radius:50%;"></span>
            <span>${param.seriesName}: <strong>${param.value}</strong></span>
          </div>`;
        });
        return result;
      },
      confine: true
    },
    legend: {
      data: datasets.map(d => d.label),
      top: '10px',
      textStyle: {
        fontSize: 11,
        color: '#666'
      },
      icon: 'circle',
      itemWidth: 8,
      itemHeight: 8,
      itemGap: 12
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '8%',
      top: '60px',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: labels,
      axisLine: {
        lineStyle: {
          color: '#eee'
        }
      },
      axisLabel: {
        color: '#666',
        fontSize: 11,
        margin: 12,
        rotate: labels.length > 20 ? 45 : 0,
        formatter: function (value) {
          // 如果标签太多，截断显示
          if (labels.length > 30) {
            return value.slice(6); // 只显示时间部分
          }
          return value;
        }
      },
      axisTick: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed',
          color: '#eee'
        }
      },
      axisLabel: {
        color: '#666',
        fontSize: 11,
        margin: 12
      },
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      }
    },
    series: series
  }
  
  // 合并自定义选项
  const mergedOption = { ...option, ...props.chartOptions }
  
  // 设置图表选项
  chartInstance.setOption(mergedOption, true)
}

// 响应窗口大小变化
const resizeChart = () => {
  if (chartInstance) {
    // 延迟调整大小，以确保容器已经调整完毕
    setTimeout(() => {
      chartInstance.resize()
    }, 100)
  }
}

// 监听数据变化
watch(() => props.chartData, () => {
  updateChart()
}, { deep: true })

// 监听配置变化
watch(() => props.chartOptions, () => {
  updateChart()
}, { deep: true })

// 组件挂载后初始化图表
onMounted(() => {
  // 延迟初始化，确保DOM已渲染
  setTimeout(initChart, 100)
})

// 组件卸载前清理资源
onBeforeUnmount(() => {
  if (chartInstance) {
    window.removeEventListener('resize', resizeChart)
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  position: relative;
}
</style> 