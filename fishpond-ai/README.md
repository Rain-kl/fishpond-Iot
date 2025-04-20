# 手势识别API

这是一个基于FastAPI的手势识别服务，可以通过API接口上传图片进行手势识别。

## 项目依赖

- Python 3.8+
- FastAPI
- OpenCV
- MediaPipe
- 其他依赖请查看 requirements.txt

## 安装

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python api.py
```

服务将在 http://0.0.0.0:8000 上启动

## API文档

启动服务后，访问 http://localhost:8000/docs 可以查看交互式API文档。

### 手势识别端点

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

## 使用示例

### Python 客户端示例

```python
import requests

url = "http://localhost:8000/recognize-gesture/"
files = {"file": open("path/to/your/image.jpg", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### curl 示例

```bash
curl -X POST "http://localhost:8000/recognize-gesture/" -F "file=@path/to/your/image.jpg"
```
