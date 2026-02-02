# MySQL 数据库配置指南

## ✅ 已完成的工作

1. ✅ 数据库配置系统已完善
2. ✅ 支持 MySQL、PostgreSQL、SQLite 三种数据库
3. ✅ 数据库管理脚本已创建
4. ✅ MySQL 数据库已成功初始化
5. ✅ 所有表已创建（19个表）
6. ✅ 默认用户和模板已创建

## 📊 当前数据库状态

**数据库类型**: MySQL  
**数据库名称**: pangudata  
**连接地址**: localhost:3306  
**字符集**: utf8mb4  

**数据统计**:
- 用户数量: 2 (admin + testuser)
- 模板数量: 6 (默认模板)
- 数据表: 19个

## 🔑 默认账户

### 管理员账户
- 用户名: `admin`
- 密码: `admin123`
- 权限: 管理员
- ⚠️ **生产环境请务必修改密码！**

### 测试账户
- 用户名: `testuser`
- 密码: `test123`
- 权限: 普通用户

## 📁 数据库文件位置

```
backend/
├── .env                    # 数据库配置文件（已创建，包含你的MySQL密码）
├── .env.example            # 配置文件模板
├── config.py               # 配置管理（已更新）
├── database/               # 数据库管理目录
│   ├── init_db.py         # 初始化脚本
│   ├── check_db.py        # 连接检查脚本
│   ├── backup_db.py       # 备份脚本
│   ├── backups/           # 备份文件目录（自动创建）
│   └── README.md          # 使用文档
└── extensions.py          # 扩展初始化（已更新）
```

## 🚀 快速开始

### 1. 启动后端服务

```bash
cd backend
source venv/bin/activate
python app.py
```

服务将在 http://localhost:5001 启动

### 2. 访问 API 文档

打开浏览器访问: http://localhost:5001/docs

### 3. 测试登录

使用 Postman 或 curl 测试：

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

## 🔧 数据库管理命令

### 检查数据库连接

```bash
python database/check_db.py
```

### 重新初始化数据库（⚠️ 会清空所有数据）

```bash
python database/init_db.py --drop
```

### 备份数据库

```bash
python database/backup_db.py
```

备份文件保存在 `database/backups/` 目录

## 📝 配置说明

### 当前配置 (.env)

```env
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=Lx123456
MYSQL_DATABASE=pangudata
```

### 切换到其他数据库

#### 切换到 SQLite

```env
DB_TYPE=sqlite
SQLITE_PATH=data/app.db
```

#### 切换到 PostgreSQL

```env
DB_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=pangudata
```

修改配置后，需要重新初始化数据库：

```bash
python database/init_db.py
```

## 🗄️ 数据库表结构

已创建的19个表：

1. **users** - 用户表
2. **projects** - 项目表
3. **project_members** - 项目成员表
4. **generation_history** - 生成历史表
5. **templates** - 模板表
6. **tags** - 标签表
7. **template_tags** - 模板标签关联表
8. **template_ratings** - 模板评分表
9. **template_favorites** - 模板收藏表
10. **template_downloads** - 模板下载记录表
11. **api_keys** - API密钥表
12. **api_key_usage_logs** - API使用日志表
13. **scheduled_tasks** - 定时任务表
14. **task_execution_logs** - 任务执行日志表
15. **datasources** - 数据源表
16. **notifications** - 通知表
17. **webhooks** - Webhook表
18. **audit_logs** - 审计日志表
19. **system_settings** - 系统设置表

## 🔒 安全建议

### 开发环境

- ✅ 当前配置适合开发环境
- ✅ 密码已配置在 `.env` 文件中
- ✅ `.env` 文件已加入 `.gitignore`

### 生产环境

1. **修改默认密码**
   ```bash
   # 登录后修改 admin 密码
   ```

2. **使用强密码**
   - 数据库密码至少12位
   - 包含大小写字母、数字、特殊字符

3. **限制数据库访问**
   - 只允许应用服务器IP访问
   - 不要暴露数据库端口到公网

4. **定期备份**
   - 设置自动备份任务
   - 备份文件加密存储

## 📊 监控和维护

### 查看数据库状态

```bash
# 连接到 MySQL
mysql -u root -p

# 查看数据库
SHOW DATABASES;
USE pangudata;

# 查看表
SHOW TABLES;

# 查看用户
SELECT * FROM users;

# 查看模板
SELECT * FROM templates;
```

### 性能优化

1. **添加索引**（已自动创建）
   - users: username, email
   - templates: author_id, category
   - 等等

2. **连接池配置**（已配置）
   - pool_size: 10
   - pool_recycle: 3600
   - pool_pre_ping: True

## 🐛 故障排除

### 连接失败

**问题**: `(1049, "Unknown database 'pangudata'")`

**解决**: 运行初始化脚本
```bash
python database/init_db.py
```

### 权限不足

**问题**: `Access denied for user 'root'@'localhost'`

**解决**: 检查 `.env` 文件中的密码是否正确

### 表不存在

**问题**: `Table 'pangudata.users' doesn't exist`

**解决**: 重新初始化数据库
```bash
python database/init_db.py --drop
```

## 📞 获取帮助

如有问题，请查看：
- [数据库管理文档](./README.md)
- [配置文件说明](../config.py)
- [API 文档](http://localhost:5001/docs)

---

**配置完成时间**: 2026-02-02  
**数据库版本**: MySQL 8.0+  
**状态**: ✅ 已完成并测试通过
