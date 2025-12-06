# Bears_PanguCreate

🚀 **企业级测试数据生成平台** - 快速构造高质量模拟数据

## ✨ 核心功能

### 数据生成
- 🎯 **30+ 数据类型** - 个人信息、地址、日期时间、金融、互联网、企业等
- ⚡ **实时预览** - 字段配置即时预览，所见即所得
- 📦 **批量生成** - 支持 1-10000 条数据一键生成
- 💾 **多格式导出** - JSON / CSV / SQL 三种格式复制与下载

### 企业级功能
- 📊 **仪表盘** - 数据统计概览、生成趋势、热门模板、活动日志
- 🔗 **关联数据生成** - 可视化表关系配置，生成符合外键约束的多表数据
- 🛒 **模板市场** - 团队共享模板库，支持评分、下载统计、收藏
- 📜 **历史记录** - 完整的生成历史，支持搜索、筛选、配置复用
- 🗄️ **数据源管理** - MySQL/PostgreSQL/MongoDB/REST API 多种数据源连接
- 🔑 **API 管理** - API 密钥管理、调用统计、权限配置
- ⏰ **定时任务** - Cron 配置、自动化数据生成
- 👥 **项目空间** - 多项目隔离、成员管理

## 🛠 技术栈

| 类型 | 技术 |
|------|------|
| 前端 | React 18 + Vite + TypeScript |
| 样式 | Tailwind CSS |
| 后端 | Python 3 + Flask |
| 图标 | Lucide React |
| 图表 | Recharts |

## 📁 项目结构

```
├── frontend/                    # React 前端
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/          # 通用 UI 组件 (Button, Input, Modal, Card, etc.)
│   │   │   ├── layout/          # 布局组件 (Header, Sidebar, UserMenu, ProjectSwitcher)
│   │   │   ├── generator/       # 数据生成组件
│   │   │   └── ...
│   │   ├── pages/               # 页面组件
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── HistoryPage.tsx
│   │   │   ├── TemplateMarketPage.tsx
│   │   │   ├── DataSourcePage.tsx
│   │   │   ├── ApiPage.tsx
│   │   │   └── RelationPage.tsx
│   │   ├── lib/
│   │   │   ├── api.ts           # API 调用
│   │   │   ├── types.ts         # TypeScript 类型定义
│   │   │   └── utils.ts
│   │   └── App.tsx
│   └── package.json
│
├── backend/                     # Flask 后端
│   ├── models/                  # 数据模型
│   ├── services/                # 业务服务
│   │   ├── data_generator_service.py
│   │   ├── data_type_service.py
│   │   ├── template_service.py
│   │   └── export_service.py
│   ├── routes/                  # API 路由
│   │   ├── types_routes.py
│   │   ├── generate_routes.py
│   │   ├── templates_routes.py
│   │   └── export_routes.py
│   ├── app.py
│   └── requirements.txt
│
├── IMPLEMENTATION_PLAN.md       # 实施计划
└── README.md
```

## ⚙️ 环境要求

- Node >= 18
- Python >= 3.9
- macOS (Apple Silicon M2) 需安装 `Xcode Command Line Tools`

## 🚀 快速开始

```bash
# 1. 后端 - 创建虚拟环境并安装依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. 启动后端 (端口 5001)
python app.py

# 3. 新终端，安装前端依赖
cd frontend
npm install

# 4. 启动前端 (端口 5173)
npm run dev

# 访问 http://localhost:5173
```

## 🔌 API 端点

### 核心 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/types` | 获取所有数据类型 |
| POST | `/api/generate` | 生成测试数据 |
| GET | `/api/templates` | 获取模板列表 |
| POST | `/api/templates` | 创建模板 |
| POST | `/api/export/json` | 导出 JSON |
| POST | `/api/export/csv` | 导出 CSV |
| POST | `/api/export/sql` | 导出 SQL |

### 生成数据示例

```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "fields": [
      {"name": "id", "type": "uuid"},
      {"name": "name", "type": "chineseName"},
      {"name": "email", "type": "email"},
      {"name": "phone", "type": "chinesePhone"}
    ],
    "count": 100
  }'
```

## 📖 页面导航

| 页面 | 功能 |
|------|------|
| **仪表盘** | 数据统计、生成趋势图、热门模板、最近活动 |
| **数据生成** | 配置字段、生成数据、预览和导出 |
| **关联数据** | 多表关系配置、外键约束数据生成 |
| **模板市场** | 浏览、收藏、使用团队共享模板 |
| **历史记录** | 查看生成历史、复用配置 |
| **数据源** | 管理数据库和 API 连接 |
| **API** | API 密钥管理、定时任务、API 文档 |

## 🎨 UI 特性

- 🌙 深色主题，护眼设计
- 📱 响应式布局，支持移动端
- ✨ 流畅动画和过渡效果
- 🎯 企业级组件库

## 📝 License

本项目采用专有许可证，源码仅供学习参考。商业使用请联系授权。

详见 [LICENSE](./LICENSE)
