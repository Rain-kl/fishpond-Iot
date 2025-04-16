# 构建阶段 - 前端
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY fishpond-frontend/package*.json fishpond-frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY fishpond-frontend/src ./src
COPY fishpond-frontend/public ./public
COPY fishpond-frontend/index.html ./
COPY fishpond-frontend/vite.config.js ./
RUN pnpm build

# 构建阶段 - 后端
FROM python:3.12-alpine AS backend-builder
WORKDIR /app/backend
# 更换 Alpine 源为清华镜像源
RUN sed -i 's#https\?://dl-cdn.alpinelinux.org/alpine#https://mirrors.tuna.tsinghua.edu.cn/alpine#g' /etc/apk/repositories
# 安装构建依赖
RUN apk add --no-cache gcc musl-dev python3-dev
COPY fishpond-backend/pyproject.toml ./
RUN pip install --no-cache-dir build && python -m build

# 最终阶段
FROM python:3.12-alpine
WORKDIR /app

# 更换 Alpine 源为清华镜像源
RUN sed -i 's#https\?://dl-cdn.alpinelinux.org/alpine#https://mirrors.tuna.tsinghua.edu.cn/alpine#g' /etc/apk/repositories
# 安装nginx和运行时依赖
RUN apk add --no-cache nginx supervisor bash && \
    mkdir -p /run/nginx

# 复制后端构建结果并安装
COPY --from=backend-builder /app/backend/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

# 复制后端代码
COPY fishpond-backend/ /app/backend/

# 配置nginx
RUN mkdir -p /var/www/html
COPY --from=frontend-builder /app/frontend/dist /var/www/html/

# 创建nginx配置文件
COPY nginx.conf /etc/nginx/http.d/default.conf

# 创建supervisor配置
RUN mkdir -p /etc/supervisor.d/
COPY supervisord.conf /etc/supervisor.d/supervisord.ini

# 暴露端口
EXPOSE 80 10086

# 启动命令
CMD ["supervisord", "-c", "/etc/supervisor.d/supervisord.ini"]