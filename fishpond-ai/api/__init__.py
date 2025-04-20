# api/__init__.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .router import router


def create_app() -> FastAPI:
    app = FastAPI(title="手势识别API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源，生产环境中应该限制为你的前端域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the API router
    app.include_router(router, prefix="/ai")

    @app.get("/", response_class=HTMLResponse)
    async def camera_demo():
        """
        提供一个HTML页面用于测试摄像头手势识别
        """
        html_content = """
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>摄像头手势识别演示</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    text-align: center;
                }
                .container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                #video-container {
                    margin-bottom: 20px;
                    position: relative;
                    width: 640px;
                    height: 480px;
                }
                #video {
                    width: 100%;
                    height: 100%;
                    background-color: #000;
                }
                #canvas {
                    display: none;
                }
                #result {
                    font-size: 24px;
                    font-weight: bold;
                    margin-top: 20px;
                    min-height: 40px;
                }
                .controls {
                    margin: 20px 0;
                }
                button {
                    padding: 10px 20px;
                    margin: 0 10px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                button:hover {
                    background-color: #45a049;
                }
                button:disabled {
                    background-color: #cccccc;
                    cursor: not-allowed;
                }
                .status {
                    color: #666;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <h1>摄像头手势识别演示</h1>
            <div class="container">
                <div id="video-container">
                    <video id="video" autoplay playsinline></video>
                    <canvas id="canvas"></canvas>
                </div>

                <div class="controls">
                    <button id="start-btn">启动摄像头</button>
                    <button id="capture-btn" disabled>捕获并识别</button>
                    <button id="auto-capture-btn" disabled>自动模式</button>
                    <button id="stop-auto-btn" disabled>停止自动</button>
                </div>

                <div id="status" class="status">请启动摄像头</div>
                <div id="result"></div>
            </div>

            <script>
                // DOM元素
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const resultDiv = document.getElementById('result');
                const startBtn = document.getElementById('start-btn');
                const captureBtn = document.getElementById('capture-btn');
                const autoCaptureBtn = document.getElementById('auto-capture-btn');
                const stopAutoBtn = document.getElementById('stop-auto-btn');
                const statusDiv = document.getElementById('status');

                // 自动模式变量
                let autoModeActive = false;
                let autoModeInterval;

                // 启动摄像头
                startBtn.addEventListener('click', async () => {
                    try {
                        statusDiv.textContent = '正在访问摄像头...';
                        const stream = await navigator.mediaDevices.getUserMedia({ 
                            video: { 
                                width: 640, 
                                height: 480,
                                facingMode: 'user' 
                            } 
                        });
                        video.srcObject = stream;

                        // 启用按钮
                        startBtn.disabled = true;
                        captureBtn.disabled = false;
                        autoCaptureBtn.disabled = false;
                        statusDiv.textContent = '摄像头已启动，可以开始识别';
                    } catch (err) {
                        console.error('访问摄像头出错:', err);
                        statusDiv.textContent = `无法访问摄像头: ${err.message}`;
                    }
                });

                // 捕获图像并识别
                captureBtn.addEventListener('click', captureAndRecognize);

                // 自动模式
                autoCaptureBtn.addEventListener('click', () => {
                    autoModeActive = true;
                    autoCaptureBtn.disabled = true;
                    stopAutoBtn.disabled = false;
                    captureBtn.disabled = true;
                    statusDiv.textContent = '自动模式已启动，每2秒识别一次';

                    // 立即执行一次
                    captureAndRecognize();

                    // 设置定时器
                    autoModeInterval = setInterval(captureAndRecognize, 2000);
                });

                // 停止自动模式
                stopAutoBtn.addEventListener('click', () => {
                    autoModeActive = false;
                    clearInterval(autoModeInterval);
                    autoCaptureBtn.disabled = false;
                    stopAutoBtn.disabled = true;
                    captureBtn.disabled = false;
                    statusDiv.textContent = '自动模式已停止';
                });

                // 捕获并识别函数
                async function captureAndRecognize() {
                    try {
                        // 设置canvas尺寸
                        canvas.width = video.videoWidth;
                        canvas.height = video.videoHeight;

                        // 在canvas上绘制当前视频帧
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                        // 将canvas转换为base64图像数据
                        const imageData = canvas.toDataURL('image/jpeg');

                        // 更新状态
                        statusDiv.textContent = '正在识别...';

                        // 发送到后端API
                        const response = await fetch('/ai/process-camera-gesture/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ image: imageData }),
                        });

                        if (!response.ok) {
                            throw new Error(`HTTP error: ${response.status}`);
                        }

                        const data = await response.json();

                        // 显示结果
                        resultDiv.textContent = `识别结果: ${data.gesture || '未识别'}`;
                        statusDiv.textContent = autoModeActive ? '自动模式进行中...' : '识别完成';
                    } catch (err) {
                        console.error('识别出错:', err);
                        resultDiv.textContent = '识别失败';
                        statusDiv.textContent = `错误: ${err.message}`;

                        // 如果在自动模式中出错，停止自动模式
                        if (autoModeActive) {
                            stopAutoBtn.click();
                        }
                    }
                }
            </script>
        </body>
        </html>
        """
        return html_content

    return app


app = create_app()
