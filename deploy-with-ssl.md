# 启用HTTPS的Fishpond部署指南

本指南将帮助你使用自签证书在本地部署Fishpond系统，启用HTTPS安全访问。

## 前提条件

- 已安装Docker和Docker Compose
- 基本的命令行操作知识

## 部署步骤

### 1. 生成自签证书

首先，运行提供的脚本生成自签SSL证书：

```bash
./setup-ssl.sh
```

这个脚本会：
- 创建必要的`certs`目录
- 生成自签SSL证书
- 设置正确的文件权限

> **重要**：必须先执行此步骤，然后再启动Docker服务，否则HTTPS将无法正常工作。

### 2. 启动容器

证书生成完成后，运行以下命令启动服务：

```bash
docker-compose up -d
```

这将：
- 构建并启动前端和AI服务容器
- 配置HTTPS安全访问
- 将网站访问端口映射到8086（HTTPS）

### 3. 访问系统

现在可以通过浏览器访问系统：

```
https://localhost:8086
```

> **注意**：由于使用的是自签证书，浏览器可能会显示安全警告。这在本地开发环境中是正常的，你可以选择"继续访问"。

如果HTTPS服务出现问题，系统也提供HTTP访问作为备选：

```
http://localhost:8085
```

### 4. 停止服务

要停止服务，运行：

```bash
docker-compose down
```

## 端口说明

- `8086`: HTTPS前端入口（映射到容器的443端口）
- `8085`: HTTP前端入口（可用作备选访问方式）
- `10086`: 后端API端口
- `10099`: AI服务API端口

## 证书管理

### 重新生成证书

如需重新生成证书，可以删除现有证书文件并重新运行脚本：

```bash
rm -f certs/fishpond.crt certs/fishpond.key
./setup-ssl.sh
```

之后需要重启服务以应用新证书：

```bash
docker-compose restart fishpond-app
```

### 使用自定义证书

如果您有自己的SSL证书，可以将其命名为`fishpond.crt`和`fishpond.key`，并放置在`certs`目录中，系统将自动使用它们。

## 故障排查

如果遇到证书问题，请检查：

1. 确认已执行`setup-ssl.sh`脚本并成功生成证书
2. `certs`目录中是否包含`fishpond.crt`和`fishpond.key`文件
3. 证书文件权限是否正确（应为644）

查看容器日志以获取更多信息：

```bash
docker logs fishpond-app
```

如果仍然遇到问题，可以尝试完全重建证书和服务：

```bash
docker-compose down
rm -rf certs
./setup-ssl.sh
docker-compose up -d
``` 