# 鱼塘物联网监控系统 (Fishpond IoT Monitoring System)

这是一个基于Vue前端和Python FastAPI后端的鱼塘监控系统，用于实时监控水质、温度等数据。项目采用Docker容器化部署，方便在各种环境下快速搭建。

## 主要功能

- 实时监控鱼塘水质、温度、pH值等关键数据
- 数据可视化展示和历史趋势分析
- 异常情况自动报警通知
- 设备远程控制管理
- 手势识别控制（AI模块）

## 技术栈

- **前端**：Vue 3 + Element Plus + Axios
- **后端**：Python FastAPI + WebSockets
- **AI服务**：MediaPipe + OpenCV + FastAPI
- **部署**：Docker + Nginx

## 项目结构

项目由三个主要组件构成：

- `fishpond-frontend`：Vue 3前端
- `fishpond-backend`：FastAPI后端服务
- `fishpond-ai`：手势识别AI服务

## 快速开始

### 使用Docker Compose部署

1. 确保已安装Docker和Docker Compose
2. 克隆本仓库

```bash
git clone https://github.com/Rain-kl/fishpond-Iot
```

3. 在项目根目录运行：

注意：如果需要使用手势识别等需要调用摄像头权限的功能时，必须配置 ssl，一键脚本和 ssl 证书生成需要在 linux环境下执行，Windows用户请手动生成证书存放在 ./certs 目录下，然后使用 docker-compose 启动服务。

```bash
./setup-ssl.sh  # 生成SSL证书
docker-compose build  # 构建Docker镜像
docker-compose up -d  # 启动服务
```

或者使用一键脚本

```bash
./deploy.sh
```

4.  访问 <https://localhost:8086> 即可打开监控系统界面

### 开发环境设置

#### 前端开发

```bash
cd fishpond-frontend
pnpm install
pnpm dev
```

#### 后端开发

```bash
cd fishpond-backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python run_server.py
```

```bash
# using uv
cd fishpond-backend
uv sync
uv run run_server.py
```

#### AI服务开发

```bash
cd fishpond-ai
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
python run_server.py
```

```bash
# using uv
cd fishpond-ai
uv sync
uv run run_server.py
```

## 服务端口

- 前端服务：80/443 (Docker)，5173 (开发模式)
- 后端服务：10086
- AI服务：10099

## AI功能 - 手势识别

系统集成了基于MediaPipe的手势识别功能，可以识别用户手势并转换为控制命令：

- 支持识别0-5的手指数量
- 可通过图片上传或摄像头实时捕获进行识别
- API端点：
  - `/recognize-gesture/`：图片上传识别
  - `/process-camera-gesture/`：摄像头数据识别

详细功能请参考 [fishpond-ai/README.md](fishpond-ai/README.md)

## SSL安全访问

本项目已配置HTTPS安全访问支持

1. 首先生成自签证书：

```bash
./setup-ssl.sh
```

2. 然后启动服务：

```bash
docker-compose up -d
```

- HTTPS访问端口：8086
- HTTP访问端口：8085

详细配置说明请参考 [deploy-with-ssl.md](deploy-with-ssl.md)
