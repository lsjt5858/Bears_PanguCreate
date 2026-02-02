#!/bin/bash

# Bears PanguCreate 部署脚本

set -e

echo "=========================================="
echo "Bears PanguCreate Docker 部署"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    echo "请先安装 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}错误: Docker Compose 未安装${NC}"
    echo "请先安装 Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${YELLOW}警告: .env 文件不存在${NC}"
    echo "正在从 .env.example 创建 .env 文件..."
    cp .env.example .env
    echo -e "${GREEN}已创建 .env 文件，请修改其中的配置${NC}"
    echo -e "${YELLOW}特别注意修改以下配置：${NC}"
    echo "  - SECRET_KEY"
    echo "  - JWT_SECRET_KEY"
    echo "  - MYSQL_PASSWORD"
    read -p "是否继续部署? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 停止现有容器
echo -e "${YELLOW}停止现有容器...${NC}"
docker-compose down

# 构建镜像
echo -e "${YELLOW}构建 Docker 镜像...${NC}"
docker-compose build --no-cache

# 启动服务
echo -e "${YELLOW}启动服务...${NC}"
docker-compose up -d

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${YELLOW}检查服务状态...${NC}"
docker-compose ps

# 初始化数据库
echo -e "${YELLOW}初始化数据库...${NC}"
docker-compose exec backend python database/init_db.py

# 显示日志
echo ""
echo -e "${GREEN}=========================================="
echo "部署完成！"
echo "==========================================${NC}"
echo ""
echo "服务地址："
echo "  前端: http://localhost"
echo "  后端: http://localhost:5001"
echo "  API文档: http://localhost:5001/docs"
echo ""
echo "默认账户："
echo "  用户名: admin"
echo "  密码: admin123"
echo ""
echo "查看日志："
echo "  docker-compose logs -f"
echo ""
echo "停止服务："
echo "  docker-compose down"
echo ""
echo -e "${GREEN}=========================================${NC}"
