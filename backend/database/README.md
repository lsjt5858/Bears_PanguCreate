# 数据库管理工具

这个目录包含所有数据库相关的管理脚本和工具。

## 📁 目录结构

```
database/
├── __init__.py          # 模块初始化
├── init_db.py           # 数据库初始化脚本
├── check_db.py          # 数据库连接检查
├── backup_db.py         # 数据库备份工具
├── backups/             # 备份文件存储目录（自动创建）
└── README.md            # 本文档
```

## 🚀 使用指南

### 1. 初始化数据库

首次使用或需要重置数据库时运行：

```bash
# 进入后端目录
cd backend

# 激活虚拟环境
source venv/bin/activate

# 初始化数据库（创建表和初始数据）
python database/init_db.py

# 如果需要删除现有表并重新创建（⚠️ 会清空所有数据）
python database/init_db.py --drop
```

**默认账户：**
- 管理员：`admin` / `admin123`
- 测试用户：`testuser` / `test123`

### 2. 检查数据库连接

测试数据库连接是否正常：

```bash
python database/check_db.py
```

这个脚本会：
- 测试数据库连接
- 显示数据库配置信息
- 列出所有表
- 显示数据统计

### 3. 备份数据库

定期备份数据库：

```bash
python database/backup_db.py
```

**支持的数据库：**
- MySQL：使用 `mysqldump` 命令
- SQLite：直接复制数据库文件

**备份文件位置：**
- `database/backups/`
- 自动保留最近10个备份文件

## ⚙️ 数据库配置

数据库配置在 `backend/.env` 文件中：

### MySQL 配置示例

```env
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=pangudata
```

### SQLite 配置示例

```env
DB_TYPE=sqlite
SQLITE_PATH=data/app.db
```

### PostgreSQL 配置示例

```env
DB_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DATABASE=pangudata
```

## 📝 注意事项

### 首次配置

1. **复制配置文件**
   ```bash
   cp .env.example .env
   ```

2. **修改数据库配置**
   编辑 `.env` 文件，设置你的数据库连接信息

3. **初始化数据库**
   ```bash
   python database/init_db.py
   ```

### MySQL 注意事项

- 确保 MySQL 服务已启动
- 确保用户有创建数据库的权限
- 脚本会自动创建数据库（如果不存在）
- 备份需要安装 MySQL 客户端工具

### SQLite 注意事项

- 数据库文件会自动创建
- 适合开发和测试环境
- 不推荐用于生产环境

### 生产环境建议

1. **使用强密码**
   - 修改默认管理员密码
   - 使用复杂的数据库密码

2. **定期备份**
   - 设置定时任务自动备份
   - 将备份文件存储到安全位置

3. **使用专业数据库**
   - 推荐使用 MySQL 或 PostgreSQL
   - 不要在生产环境使用 SQLite

## 🔧 故障排除

### 连接失败

如果数据库连接失败，检查：

1. 数据库服务是否启动
2. `.env` 配置是否正确
3. 数据库用户权限是否足够
4. 防火墙是否阻止连接

### 初始化失败

如果初始化失败，尝试：

1. 检查数据库连接
2. 确保数据库用户有创建表的权限
3. 查看错误日志定位问题

### 备份失败

如果备份失败，检查：

1. MySQL：是否安装了 `mysqldump` 命令
2. 磁盘空间是否充足
3. 文件写入权限是否正确

## 📚 相关文档

- [配置文件说明](../config.py)
- [环境变量配置](../.env.example)
- [API 文档](http://localhost:5001/docs)

## 🆘 获取帮助

如有问题，请查看：
- 项目文档：`doc/` 目录
- 错误日志：控制台输出
- 联系开发团队
