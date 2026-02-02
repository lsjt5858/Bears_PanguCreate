# Bears PanguCreate Docker 部署指南

## 📦 快速开始

### 1. 使用 Docker Compose（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/Bears_PanguCreate.git
cd Bears_PanguCreate

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，修改必要的配置

# 3. 一键部署
chmod +x deploy.sh
./deploy.sh
```

### 2. 手动部署

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 初始化数据库
docker-compose exec backend python database/init_db.py

# 查看日志
docker-compose logs -f
```

## 🚀 访问应用

- **前端**: http://localhost
- **后端API**: http://localhost:5001
- **API文档**: http://localhost:5001/docs

**默认账户**:
- 用户名: `admin`
- 密码: `admin123`

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置以下变量：

```env
# Flask配置
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# 数据库配置
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_USER=pangudata
MYSQL_PASSWORD=your-password-here
MYSQL_DATABASE=pangudata

# CORS配置
CORS_ORIGINS=http://localhost,http://your-domain.com
```

### 端口配置

默认端口映射：
- 前端: `80:80`
- 后端: `5001:5001`
- MySQL: `3306:3306`

修改端口请编辑 `docker-compose.yml`：

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # 修改为 8080
```

## 📊 服务管理

### 启动服务

```bash
docker-compose up -d
```

### 停止服务

```bash
docker-compose down
```

### 重启服务

```bash
docker-compose restart
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql
```

### 查看服务状态

```bash
docker-compose ps
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 进入MySQL容器
docker-compose exec mysql bash
```

## 🗄️ 数据库管理

### 备份数据库

```bash
# 备份到文件
docker-compose exec mysql mysqldump -u root -p pangudata > backup.sql

# 或使用后端备份工具
docker-compose exec backend python database/backup_db.py
```

### 恢复数据库

```bash
# 从备份文件恢复
docker-compose exec -T mysql mysql -u root -p pangudata < backup.sql
```

### 重新初始化数据库

```bash
docker-compose exec backend python database/init_db.py --drop
```

## 🔨 构建和推送镜像

### 构建镜像

```bash
# 使用脚本构建
chmod +x docker-build.sh
./docker-build.sh

# 或手动构建
docker build -t your-username/bears-pangudata-backend:latest -f backend/Dockerfile backend/
docker build -t your-username/bears-pangudata-frontend:latest -f frontend/Dockerfile frontend/
```

### 推送到 Docker Hub

```bash
# 登录 Docker Hub
docker login

# 推送镜像
docker push your-username/bears-pangudata-backend:latest
docker push your-username/bears-pangudata-frontend:latest
```

### 从 Docker Hub 拉取

```bash
docker pull your-username/bears-pangudata-backend:latest
docker pull your-username/bears-pangudata-frontend:latest
```

## 🌐 生产环境部署

### 1. 使用反向代理（Nginx）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 使用 HTTPS

```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

### 3. 配置防火墙

```bash
# 允许 HTTP 和 HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 🔍 故障排查

### 服务无法启动

```bash
# 查看详细日志
docker-compose logs backend
docker-compose logs frontend

# 检查容器状态
docker-compose ps

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

### 数据库连接失败

```bash
# 检查MySQL是否启动
docker-compose ps mysql

# 查看MySQL日志
docker-compose logs mysql

# 测试连接
docker-compose exec backend python database/check_db.py
```

### 前端无法访问后端

1. 检查 CORS 配置
2. 检查网络连接
3. 查看后端日志

```bash
docker-compose logs backend
```

## 📈 性能优化

### 1. 调整资源限制

编辑 `docker-compose.yml`：

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### 2. 使用生产级数据库

```yaml
services:
  mysql:
    command: >
      --max_connections=1000
      --innodb_buffer_pool_size=2G
      --innodb_log_file_size=512M
```

### 3. 启用缓存

前端已配置 Nginx 缓存，后端可以添加 Redis：

```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

## 🔐 安全建议

1. **修改默认密码**
   - 修改 `.env` 中的所有密码
   - 修改默认管理员密码

2. **使用 HTTPS**
   - 配置 SSL 证书
   - 强制 HTTPS 重定向

3. **限制访问**
   - 配置防火墙
   - 使用 IP 白名单

4. **定期备份**
   - 设置自动备份
   - 异地存储备份

## 📚 相关文档

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Compose 文档](https://docs.docker.com/compose/)
- [项目主文档](README.md)

## 🆘 获取帮助

如有问题，请：
1. 查看日志: `docker-compose logs -f`
2. 检查配置: `.env` 和 `docker-compose.yml`
3. 提交 Issue: [GitHub Issues](https://github.com/your-repo/issues)

---

**祝部署顺利！** 🎉
