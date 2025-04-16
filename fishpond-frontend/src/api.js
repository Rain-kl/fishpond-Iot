import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '/api', // 使用相对路径，会被代理转发
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 响应拦截器，统一处理响应
api.interceptors.response.use(
  response => {
    // 对于返回ok字段的标准格式响应
    if (response.data && response.data.ok) {
      return response.data;
    }
    // 对于没有ok字段但直接返回数据的响应（如历史数据接口）
    if (response.data) {
      return response.data;
    }
    return Promise.reject(new Error(response.data?.message || '请求失败'));
  },
  error => {
    console.error('接口请求错误:', error);
    return Promise.reject(error);
  }
);

/**
 * 监测数据相关API
 */
export const monitorApi = {
  // 获取监测数据
  getMonitorData() {
    return api.get('/status/monitor');
  }
};

/**
 * 控制器相关API
 */
export const controllerApi = {
  // 获取控制器数据
  getControllerData() {
    return api.get('/status/controller');
  },
  
  // 控制设备开关
  toggleDevice(deviceId, command) {
    // 根据curl请求的格式调整
    return api.post('/controller/command', {
      device: deviceId,
      command: command
    });
  }
};

/**
 * 历史数据相关API
 */
export const historyApi = {
  // 获取历史数据
  getHistoryData(deviceId, duration) {
    return api.get(`/history`, {
      params: {
        device: deviceId,
        duration: duration
      }
    });
  }
}; 