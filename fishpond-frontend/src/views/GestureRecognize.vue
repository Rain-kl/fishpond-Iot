<script setup>
import {ref, onMounted} from 'vue';
import {gestureApi} from '@/api';

// 引用DOM元素
const video = ref(null);
const canvas = ref(null);
const resultDiv = ref(null);
const statusDiv = ref(null);
const startBtn = ref(null);
const captureBtn = ref(null);
const autoCaptureBtn = ref(null);
const stopAutoBtn = ref(null);

// 状态变量
const autoModeActive = ref(false);
let autoModeInterval = null;
const recognitionResult = ref('');
const statusMessage = ref('请启动摄像头');
const isRecognizing = ref(false);

// 启动摄像头
const startCamera = async () => {
  try {
    statusMessage.value = '正在访问摄像头...';
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: 640,
        height: 480,
        facingMode: 'user'
      }
    });
    video.value.srcObject = stream;

    // 启用按钮
    startBtn.value.disabled = true;
    captureBtn.value.disabled = false;
    autoCaptureBtn.value.disabled = false;
    statusMessage.value = '摄像头已启动，可以开始识别';
  } catch (err) {
    console.error('访问摄像头出错:', err);
    statusMessage.value = `无法访问摄像头: ${err.message}`;
  }
};

// 捕获并识别函数
const captureAndRecognize = async () => {
  try {
    isRecognizing.value = true;
    // 设置canvas尺寸
    canvas.value.width = video.value.videoWidth;
    canvas.value.height = video.value.videoHeight;

    // 在canvas上绘制当前视频帧
    const ctx = canvas.value.getContext('2d');
    ctx.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);

    // 将canvas转换为base64图像数据
    const imageData = canvas.value.toDataURL('image/jpeg');

    // 更新状态
    statusMessage.value = '正在识别...';

    // 发送到后端API
    const response = await gestureApi.recognizeGesture(imageData);

    // 显示结果 - response直接包含{gesture: "手势名称"}
    const gestureResult = response.gesture || '未识别';
    recognitionResult.value = gestureResult;

    console.log('手势识别结果:', response); // 调试输出

    statusMessage.value = autoModeActive.value ? '自动模式进行中...' : '识别完成';
    isRecognizing.value = false;
  } catch (err) {
    console.error('识别出错:', err);
    recognitionResult.value = '识别失败';
    statusMessage.value = `错误: ${err.message}`;
    isRecognizing.value = false;

    // 如果在自动模式中出错，停止自动模式
    if (autoModeActive.value) {
      stopAutoMode();
    }
  }
};

// 开始自动模式
const startAutoMode = () => {
  autoModeActive.value = true;
  autoCaptureBtn.value.disabled = true;
  stopAutoBtn.value.disabled = false;
  captureBtn.value.disabled = true;
  statusMessage.value = '自动模式已启动，每2秒识别一次';

  // 立即执行一次
  captureAndRecognize();

  // 设置定时器
  autoModeInterval = setInterval(captureAndRecognize, 2000);
};

// 停止自动模式
const stopAutoMode = () => {
  autoModeActive.value = false;
  clearInterval(autoModeInterval);
  autoCaptureBtn.value.disabled = false;
  stopAutoBtn.value.disabled = true;
  captureBtn.value.disabled = false;
  statusMessage.value = '自动模式已停止';
};

onMounted(() => {
  // 组件挂载后，元素已经可以访问
  video.value = document.getElementById('video');
  canvas.value = document.getElementById('canvas');
  resultDiv.value = document.getElementById('result');
  statusDiv.value = document.getElementById('status');
  startBtn.value = document.getElementById('start-btn');
  captureBtn.value = document.getElementById('capture-btn');
  autoCaptureBtn.value = document.getElementById('auto-capture-btn');
  stopAutoBtn.value = document.getElementById('stop-auto-btn');
});
</script>

<template>
  <div class="container">
    <div class="card-container">
      <!-- 左侧卡片 - 摄像头区域 -->
      <div class="gesture-card camera-card">
        <div class="card-header">
          <h2>摄像头</h2>
          <div class="status-indicator" v-if="video && video.srcObject">
            <div class="status-dot online"></div>
            <span class="status-text">已连接</span>
          </div>
        </div>

        <div class="card-body">
          <div class="video-container">
            <video id="video" autoplay playsinline></video>
            <canvas id="canvas"></canvas>
            <div class="loading-overlay" v-if="isRecognizing">
              <div class="spinner"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧卡片 - 控制和结果区域 -->
      <div class="gesture-card control-card">
        <div class="card-header">
          <h2>手势识别</h2>
        </div>

        <div class="card-body">
          <div class="result-display" v-if="recognitionResult">
            <div class="result-label">识别结果</div>
            <div class="result-value">{{ recognitionResult }}</div>
          </div>
          
          <div class="status-message" id="status">{{ statusMessage }}</div>
          
          <div class="controls-group">
            <button id="start-btn" @click="startCamera" class="primary-btn">
              <i class="icon-camera"></i>
              启动摄像头
            </button>
            <button id="capture-btn" @click="captureAndRecognize" disabled class="action-btn">
              <i class="icon-capture"></i>
              捕获并识别
            </button>
            <button id="auto-capture-btn" @click="startAutoMode" disabled class="action-btn">
              <i class="icon-auto"></i>
              自动模式
            </button>
            <button id="stop-auto-btn" @click="stopAutoMode" disabled class="action-btn stop-btn">
              <i class="icon-stop"></i>
              停止自动
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  max-width: 1200px;
  margin: 24px auto;
  padding: 0 20px;
}

.card-container {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
}

.gesture-card {
  background-color: #FFFFFF;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  flex: 1;
  min-width: 300px;
}

.camera-card {
  flex: 1.2;
}

.control-card {
  flex: 0.8;
  display: flex;
  flex-direction: column;
}

.gesture-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.card-header {
  padding: 20px 24px;
  background-color: #F9F9FF;
  border-bottom: 1px solid #EAECF0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #101828;
  margin: 0;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background-color: rgba(18, 183, 106, 0.1);
  border-radius: 16px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.online {
  background-color: #12B76A;
}

.status-text {
  font-size: 14px;
  color: #12B76A;
  font-weight: 500;
}

.card-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: calc(100% - 70px); /* 70px is approximate header height */
}

.control-card .card-body {
  justify-content: center;
}

.video-container {
  position: relative;
  width: 100%;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #000;
}

#video {
  width: 100%;
  display: block;
  border-radius: 12px;
  background-color: #000;
}

#canvas {
  display: none;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 12px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #5E6AD2;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.result-display {
  background-color: #F9F9FF;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  border: 1px solid #EAECF0;
}

.result-label {
  font-size: 14px;
  color: #667085;
  margin-bottom: 6px;
}

.result-value {
  font-size: 32px;
  font-weight: 600;
  color: #5E6AD2;
}

.status-message {
  font-size: 14px;
  color: #667085;
  text-align: center;
  min-height: 20px;
  padding: 8px 0;
}

.controls-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

button {
  font-family: inherit;
  font-size: 15px;
  padding: 12px 20px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  flex: 1;
  justify-content: center;
  min-width: 140px;
}

.primary-btn {
  background-color: #5E6AD2;
  color: white;
}

.primary-btn:hover {
  background-color: #4C56B9;
  transform: translateY(-1px);
}

.action-btn {
  background-color: #F5F5FF;
  color: #5E6AD2;
  border: 1px solid #E4E7FB;
}

.action-btn:hover {
  background-color: #EBEDF9;
  transform: translateY(-1px);
}

.stop-btn {
  background-color: #FFF1F0;
  color: #F04438;
  border: 1px solid #FEDFDC;
}

.stop-btn:hover {
  background-color: #FEEAE8;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

[class^="icon-"] {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.icon-camera {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23ffffff'%3E%3Cpath d='M12 15a3 3 0 100-6 3 3 0 000 6z'/%3E%3Cpath fill-rule='evenodd' d='M20 4h-3.17l-1.24-1.35A1.99 1.99 0 0014.12 2H9.88c-.56 0-1.1.24-1.47.65L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-8 13c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z'/%3E%3C/svg%3E");
}

.icon-capture {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%235E6AD2'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-12h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E");
}

.icon-auto {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%235E6AD2'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-2-5.5l6-4.5-6-4.5v9z'/%3E%3C/svg%3E");
}

.icon-stop {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23F04438'%3E%3Cpath d='M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z'/%3E%3C/svg%3E");
}

/* 响应式样式 */
@media (max-width: 900px) {
  .card-container {
    flex-direction: column;
  }
  
  .gesture-card {
    flex: none;
    width: 100%;
  }
  
  .camera-card, .control-card {
    flex: none;
  }
  
  .card-body {
    padding: 16px;
  }
  
  .result-value {
    font-size: 24px;
  }
  
  button {
    padding: 10px 16px;
  }
}

@media (max-width: 500px) {
  .container {
    padding: 0 12px;
    margin: 12px auto;
  }
  
  .card-header {
    padding: 16px;
  }
  
  .controls-group {
    flex-direction: column;
  }
  
  button {
    width: 100%;
  }
  
  .result-value {
    font-size: 20px;
  }
}
</style>
