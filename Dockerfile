FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装Node.js、npm和nginx
RUN apt-get update && \
    apt-get install -y nodejs npm nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 复制并安装后端依赖
COPY fishpond-backend/pyproject.toml /app/backend/
WORKDIR /app/backend
RUN pip install --no-cache-dir .

# 复制后端代码
COPY fishpond-backend/ /app/backend/

# 切换到前端目录
WORKDIR /app/frontend

# 复制前端依赖文件
COPY fishpond-frontend/package*.json fishpond-frontend/pnpm-lock.yaml ./

# 安装前端依赖
RUN npm install -g pnpm && \
    pnpm install

# 复制前端代码（排除node_modules目录）
COPY fishpond-frontend/src ./src
COPY fishpond-frontend/public ./public
COPY fishpond-frontend/index.html ./
COPY fishpond-frontend/vite.config.js ./

# 构建前端
RUN pnpm build

# 配置nginx
RUN rm -rf /var/www/html && \
    mkdir -p /var/www/html
# 移动构建好的前端文件到Nginx目录
RUN cp -r /app/frontend/dist/* /var/www/html/

# 创建nginx配置文件
RUN echo 'server {\n\
    listen 80;\n\
    server_name localhost;\n\
    root /var/www/html;\n\
    index index.html;\n\
    \n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
    \n\
    location /api/ {\n\
        proxy_pass http://localhost:10086;\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
    }\n\
}' > /etc/nginx/sites-available/default

# 暴露端口
EXPOSE 80 10086

# 创建启动脚本
RUN echo '#!/bin/bash\n\
service nginx start\n\
cd /app/backend\n\
python run_server.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# 启动命令
CMD ["/app/start.sh"]