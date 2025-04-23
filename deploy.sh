#!/bin/bash

# 鱼塘物联网监控系统一键部署脚本
# 用于从git仓库拉取最新代码并部署

# 显示彩色输出的函数
print_green() {
    echo -e "\033[32m$1\033[0m"
}

print_yellow() {
    echo -e "\033[33m$1\033[0m"
}

print_red() {
    echo -e "\033[31m$1\033[0m"
}

# 显示脚本标题
print_green "=============================================="
print_green "    鱼塘物联网监控系统 - 一键部署脚本"
print_green "=============================================="
echo ""

# 检查是否安装了Docker和Docker Compose
if ! command -v docker &> /dev/null; then
    print_red "错误: 未安装Docker，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_red "错误: 未安装Docker Compose，请先安装Docker Compose"
    exit 1
fi

# 获取脚本所在目录(项目根目录)
PROJECT_DIR=$(pwd)
print_yellow "项目目录: $PROJECT_DIR"

# 1. 拉取最新代码
print_yellow "正在从Git仓库拉取最新代码..."
git pull
if [ $? -ne 0 ]; then
    print_red "Git拉取失败，请检查网络或仓库权限"
    exit 1
fi
print_green "√ 代码拉取成功"

# 2. 配置SSL
print_yellow "正在配置SSL证书..."
# 检查证书目录
if [ ! -d "./certs" ]; then
    mkdir -p ./certs
fi

# 检查证书是否存在，如果不存在则生成
if [ ! -f "./certs/cert.pem" ] || [ ! -f "./certs/key.pem" ]; then
    # 运行SSL配置脚本
    bash ./setup-ssl.sh
    if [ $? -ne 0 ]; then
        print_red "SSL证书生成失败"
        exit 1
    fi
else
    print_yellow "SSL证书已存在，跳过生成步骤"
fi

# 使用带SSL的配置启动
print_yellow "将使用HTTPS(8086端口)和HTTP(8085端口)部署服务"
COMPOSE_FILE="docker-compose.yaml"
print_green "√ SSL配置完成"

# 3. 停止并移除现有容器
print_yellow "停止并移除现有容器..."
docker-compose down
print_green "√ 旧容器已停止"

# 4. 构建并启动容器
print_yellow "正在构建并启动Docker容器..."
docker-compose -f $COMPOSE_FILE up -d --build
if [ $? -ne 0 ]; then
    print_red "Docker容器启动失败"
    exit 1
fi
print_green "√ Docker容器启动成功"

# 5. 检查容器状态
print_yellow "正在检查容器运行状态..."
sleep 5  # 等待容器完全启动

# 获取所有相关容器的状态
containers=$(docker-compose ps --services)
all_running=true

for container in $containers; do
    status=$(docker-compose ps $container | grep -i "up" | wc -l)
    if [ $status -eq 0 ]; then
        print_red "× 容器 $container 未正常运行"
        all_running=false
    else
        print_green "√ 容器 $container 运行正常"
    fi
done

# 6. 显示访问信息
echo ""
if [ "$all_running" = true ]; then
    print_green "=============================================="
    print_green "    部署成功! 系统已成功启动"
    print_green "=============================================="
    echo ""
    
    # 获取服务器IP
    SERVER_IP=$(hostname -I | awk '{print $1}')
    
    if [[ "$need_ssl" =~ ^[Yy]$ ]]; then
        print_green "您可以通过以下地址访问系统:"
        print_green "HTTPS: https://$SERVER_IP:8086"
        print_green "HTTP:  http://$SERVER_IP:8085"
    else
        print_green "您可以通过以下地址访问系统:"
        print_green "HTTP: http://$SERVER_IP:80"
    fi
    
    echo ""
    print_yellow "前端服务: 80/443 (Docker)"
    print_yellow "后端服务: 10086"
    print_yellow "AI服务: 10099"
else
    print_red "=============================================="
    print_red "    警告: 部分容器未能正常启动"
    print_red "=============================================="
    print_yellow "请使用 'docker-compose logs' 查看详细日志"
fi

echo ""
print_yellow "部署完成!"