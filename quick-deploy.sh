#!/bin/bash

# Bears PanguCreate 一键部署脚本 - 阿里云 Linux 3
# 使用方法: bash quick-deploy.sh

set -e

echo "=========================================="
echo "Bears PanguCreate 一键部署"
echo "=========================================="

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 安装 Git
echo -e "${YELLOW}[1/7] 安装 Git...${NC}"
if ! command -v git &> /dev/null; then
    sudo yum install git -y
fi
echo -e "${GREEN}✓ Git 已安装${NC}"

# 2. 安装 Docker
echo -e "${YELLOW}[2/7] 安装 Docker...${NC}"
if ! command -v docker &> /dev/null; then
    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install -y docker-ce docker-ce-cli containerd.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi
echo -e "${GREEN}✓ Docker 已安装${NC}"

# 3. 安装 Docker Compose
echo -e "${YELLOW}[3/7] 安装 Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi
echo -e "${GREEN}✓ Docker Compose 已安装${NC}"

# 4. 克隆项目
echo -e "${YELLOW}[4/7] 克隆项目...${NC}"
if [ ! -d "Bears_PanguCreate" ]; then
    git clone https://github.com/lsjt5858/Bears_PanguCreate.git
fi
cd Bears_PanguCreate
git pull
echo -e "${GREEN}✓ 项目已克隆${NC}"

# 5. 配置环境变量
echo -e "${YELLOW}[5/7] 配置环境变量...${NC}"
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}请编辑 .env 文件修改密钥和密码${NC}"
    echo -e "${YELLOW}按任意键继续...${NC}"
    read -n 1
fi
echo -e "${GREEN}✓ 环境变量已配置${NC}"

# 6. 开放防火墙端口
echo -e "${YELLOW}[6/7] 配置防火墙...${NC}"
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-port=80/tcp 2>/dev/null || true
    sudo firewall-cmd --permanent --add-port=5001/tcp 2>/dev/null || true
    sudo firewall-cmd --reload 2>/dev/null || true
fi
echo -e "${GREEN}✓ 防火墙已配置${NC}"

# 7. 部署项目
echo -e "${YELLOW}[7/7] 部署项目...${NC}"
chmod +x deploy.sh
sudo ./deploy.sh

echo ""
echo -e "${GREEN}=========================================="
echo "部署完成！"
echo "==========================================${NC}"
echo ""
echo "访问地址："
echo "  前端: http://$(curl -s ifconfig.me)"
echo "  后端: http://$(curl -s ifconfig.me):5001"
echo ""
echo "管理命令："
echo "  查看状态: sudo docker-compose ps"
echo "  查看日志: sudo docker-compose logs -f"
echo "  停止服务: sudo docker-compose down"
echo "  重启服务: sudo docker-compose restart"
echo ""
