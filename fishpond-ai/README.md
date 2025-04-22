# 手势识别API

这是一个基于FastAPI的手势识别服务，可以通过API接口上传图片进行手势识别，支持识别伸出的手指数量（0-5）。

## 功能特点

- 基于MediaPipe的手势识别
- 支持不同严格度级别的手势检测
- 手掌朝向检测
- 手势稳定性检测
- 实时和静态图像处理
- 支持Docker容器化部署

## 项目依赖

- Python 3.8+
- FastAPI
- OpenCV
- MediaPipe
- 其他依赖请查看 pyproject.toml

## 安装

```bash
pip install -r requirements.txt
```

或使用uv管理依赖:

```bash
uv pip install -e .
```

## 运行服务

```bash
python run_server.py
```

服务将在 http://0.0.0.0:10099 上启动

## API文档

启动服务后，访问 http://localhost:10099/docs 可以查看交互式API文档。

### API端点

#### 1. 上传图片识别

- **URL**: `/recognize-gesture/`
- **方法**: POST
- **描述**: 上传图片进行手势识别
- **请求**:
  - 请求体: `multipart/form-data`
  - 参数:
    - `file`: 图片文件

- **响应**:
  - 成功: `{"gesture": "数字"}`（数字表示识别出的手指数量，"null"表示未识别出有效手势）
  - 失败: `{"detail": "处理失败: 错误信息"}`

#### 2. 处理摄像头图像

- **URL**: `/process-camera-gesture/`
- **方法**: POST
- **描述**: 处理从前端摄像头捕获的Base64编码图像数据
- **请求**:
  - 请求体: JSON
  - 参数:
    - `image`: Base64编码的图像数据

- **响应**:
  - 成功: `{"gesture": "数字"}`
  - 失败: `{"gesture": "错误", "error": "错误信息"}`

## 使用示例

### Python 客户端示例

```python
import requests

url = "http://localhost:10099/recognize-gesture/"
files = {"file": open("path/to/your/image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### curl 示例

```bash
curl -X POST "http://localhost:10099/recognize-gesture/" -F "file=@path/to/your/image.jpg"
```

### Base64图像示例

```python
import requests
import base64

url = "http://localhost:10099/process-camera-gesture/"
with open("path/to/your/image.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
response = requests.post(url, json={"image": encoded_image})
print(response.json())
```

## Docker 部署

本项目提供了优化的Dockerfile (Dockerfile.ai)，支持通过Docker容器化部署。

### 构建镜像

```bash
docker build -t fishpond-ai -f Dockerfile.ai .
```

### 运行容器

```bash
docker run -d -p 10099:10099 --name fishpond-ai-container fishpond-ai
```
