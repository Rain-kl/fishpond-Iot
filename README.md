# 鱼塘物联网监控系统 (Fishpond IoT Monitoring System)

这是一个基于Vue前端和Python FastAPI后端的鱼塘监控系统，用于实时监控水质、温度等数据。项目采用Docker容器化部署，方便在各种环境下快速搭建。

## 主要功能

- 实时监控鱼塘水质、温度、pH值等关键数据
- 数据可视化展示和历史趋势分析
- 异常情况自动报警通知
- 设备远程控制管理

## 技术栈

- **前端**：Vue 3 + Element Plus + Axios
- **后端**：Python FastAPI + WebSockets
- **部署**：Docker + Nginx

## 快速开始

### 使用Docker Compose部署

1. 确保已安装Docker和Docker Compose
2. 克隆本仓库
3. 在项目根目录运行：

```bash
docker-compose up -d
```

4. 访问 http://localhost 即可打开监控系统界面

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