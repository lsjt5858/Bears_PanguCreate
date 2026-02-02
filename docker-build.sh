#!/bin/bash

# Bears PanguCreate Docker 镜像构建和推送脚本

set -e

# 配置
DOCKER_USERNAME="${DOCKER_USERNAME:-your-dockerhub-username}"
IMAGE_NAME="bears-pangudata"
VERSION="${VERSION:-latest}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Bears PanguCreate Docker 镜像构建"
echo "=========================================="

# 检查Docker登录状态
echo -e "${YELLOW}检查 Docker 登录状态...${NC}"
if ! docker info | grep -q "Username"; then
    echo -e "${YELLOW}请先登录 Docker Hub:${NC}"
    docker login
fi

# 构建后端镜像
echo -e "${YELLOW}构建后端镜像...${NC}"
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}-backend:${VERSION} \
    -t ${DOCKER_USERNAME}/${IMAGE_NAME}-backend:latest \
    -f backend/Dockerfile \
    backend/

# 构建前端镜像
echo -e "${YELLOW}构建前端镜像...${NC}"
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}-frontend:${VERSION} \
    -t ${DOCKER_USERNAME}/${IMAGE_NAME}-frontend:latest \
    -f frontend/Dockerfile \
    frontend/

# 显示镜像信息
echo -e "${GREEN}镜像构建完成！${NC}"
echo ""
docker images | grep ${IMAGE_NAME}

# 询问是否推送
echo ""
read -p "是否推送镜像到 Docker Hub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}推送后端镜像...${NC}"
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}-backend:${VERSION}
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}-backend:latest
    
    echo -e "${YELLOW}推送前端镜像...${NC}"
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}-frontend:${VERSION}
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}-frontend:latest
    
    echo -e "${GREEN}镜像推送完成！${NC}"
    echo ""
    echo "拉取命令："
    echo "  docker pull ${DOCKER_USERNAME}/${IMAGE_NAME}-backend:${VERSION}"
    echo "  docker pull ${DOCKER_USERNAME}/${IMAGE_NAME}-frontend:${VERSION}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "完成！"
echo "==========================================${NC}"
