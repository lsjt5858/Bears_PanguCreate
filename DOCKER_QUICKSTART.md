# 🐳 Docker 快速开始指南

## 📦 方式一：一键部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/lsjt5858/Bears_PanguCreate.git
cd Bears_PanguCreate

# 2. 一键部署
./deploy.sh
```

就这么简单！🎉

---

## 🚀 方式二：手动部署

### 1. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置（重要！）
vim .env
```

**必须修改的配置**：
- `SECRET_KEY` - Flask密钥
- `JWT_SECRET_KEY` - JWT密钥
- `MYSQL_PASSWORD` - MySQL密码

### 2. 启动服务

```bash
# 构建并启动
docker-compose up -d

# 初始化数据库
docker-compose exec backend python database/init_db.py
```

### 3. 访问应用

- 前端: http://localhost
- 后端: http://localhost:5001
- API文档: http://localhost:5001/docs

**默认账户**：
- 用户名: `admin`
- 密码: `admin123`

---

## 📤 方式三：推送到Docker Hub

### 1. 修改配置

编辑 `docker-build.sh`：

```bash
DOCKER_USERNAME="your-dockerhub-username"  # 改成你的用户名
```

### 2. 构建并推送

```bash
# 登录 Docker Hub
docker login

# 构建并推送
./docker-build.sh
```

### 3. 在服务器上拉取

```bash
# 拉取镜像
docker pull your-username/bears-pangudata-backend:latest
docker pull your-username/bears-pangudata-frontend:latest

# 使用 docker-compose 启动
docker-compose up -d
```

---

## 🔧 常用命令

### 查看服务状态

```bash
docker-compose ps
```

### 查看日志

```bash
# 所有服务
docker-compose logs -f

# 特定服务
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mysql
```

### 重启服务

```bash
# 重启所有服务
docker-compose restart

# 重启特定服务
docker-compose restart backend
```

### 停止服务

```bash
docker-compose down
```

### 进入容器

```bash
# 进入后端容器
docker-compose exec backend bash

# 进入MySQL容器
docker-compose exec mysql bash
```

---

## 🗄️ 数据库管理

### 备份数据库

```bash
# 方式1: 使用mysqldump
docker-compose exec mysql mysqldump -u root -pLx123456 pangudata > backup.sql

# 方式2: 使用后端工具
docker-compose exec backend python database/backup_db.py
```

### 恢复数据库

```bash
docker-compose exec -T mysql mysql -u root -pLx123456 pangudata < backup.sql
```

### 重新初始化

```bash
docker-compose exec backend python database/init_db.py --drop
```

---

## 🌐 生产环境部署

### 1. 修改端口（可选）

编辑 `docker-compose.yml`：

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # 改成你想要的端口
```

### 2. 配置域名

如果有域名，修改 `.env`：

```env
CORS_ORIGINS=http://localhost,https://your-domain.com
```

### 3. 使用 HTTPS

推荐使用 Nginx 反向代理 + Let's Encrypt：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
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

---

## 🔍 故障排查

### 问题1: 容器无法启动

```bash
# 查看详细日志
docker-compose logs backend

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

### 问题2: 数据库连接失败

```bash
# 检查MySQL是否启动
docker-compose ps mysql

# 查看MySQL日志
docker-compose logs mysql

# 测试连接
docker-compose exec backend python database/check_db.py
```

### 问题3: 前端无法访问后端

1. 检查 CORS 配置（`.env` 中的 `CORS_ORIGINS`）
2. 检查后端是否启动：`docker-compose ps backend`
3. 查看后端日志：`docker-compose logs backend`

### 问题4: 端口被占用

```bash
# 查看端口占用
lsof -i :80
lsof -i :5001
lsof -i :3306

# 修改 docker-compose.yml 中的端口映射
```

---

## 📊 镜像信息

### 镜像大小

- **后端镜像**: ~500MB
- **前端镜像**: ~25MB
- **MySQL镜像**: ~500MB

### 优化建议

1. **使用多阶段构建**（已实现）
2. **清理缓存**：`docker system prune -a`
3. **使用 .dockerignore**（已配置）

---

## 🔐 安全建议

1. **修改所有默认密码**
   ```bash
   # 编辑 .env
   SECRET_KEY=your-random-secret-key
   JWT_SECRET_KEY=your-random-jwt-key
   MYSQL_PASSWORD=your-strong-password
   ```

2. **使用 HTTPS**
   - 配置 SSL 证书
   - 强制 HTTPS 重定向

3. **限制访问**
   - 配置防火墙
   - 使用 IP 白名单

4. **定期更新**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

---

## 📚 更多文档

- [完整部署文档](README.Docker.md)
- [项目主文档](README.md)
- [数据源使用说明](doc/DATASOURCE_EXPLANATION.md)

---

## 🆘 需要帮助？

1. 查看日志: `docker-compose logs -f`
2. 检查状态: `docker-compose ps`
3. 提交 Issue: [GitHub Issues](https://github.com/lsjt5858/Bears_PanguCreate/issues)

---

**祝你部署顺利！** 🎉
