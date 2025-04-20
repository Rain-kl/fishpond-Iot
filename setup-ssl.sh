#!/bin/bash

# 创建证书存储目录
mkdir -p ./certs

# 确保certs目录权限正确
chmod 755 ./certs

echo "开始生成SSL证书..."

# 检查是否已存在证书
if [ ! -f ./certs/fishpond.crt ]; then
  # 生成自签证书
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout ./certs/fishpond.key \
    -out ./certs/fishpond.crt \
    -subj "/C=CN/ST=State/L=City/O=Organization/CN=fishpond-local" \
    -addext "subjectAltName = DNS:localhost,IP:127.0.0.1"
  
  # 设置正确的证书权限
  chmod 644 ./certs/fishpond.crt ./certs/fishpond.key
  
  echo "证书已成功生成！"
else
  echo "证书已存在，无需重新生成。"
fi

echo "证书准备就绪，现在可以启动Docker服务。" 