# Bears_PanguCreate

企业级测试数据生成平台 - 快速构造高质量模拟数据

## ✨ 功能特性

- 🎯 **多数据类型** - 个人信息、地址、日期时间、金融、互联网、企业等 30+ 种数据类型
- ⚡ **实时预览** - 字段配置即时预览，所见即所得
- 📦 **批量生成** - 支持 1-10000 条数据一键生成
- 💾 **多格式导出** - JSON / CSV / SQL 三种格式复制与下载
- 📋 **模板管理** - 保存、复用、分类管理常用数据模板
- 🎨 **现代 UI** - 深色主题，响应式设计

## 🛠 技术栈

| 类型 | 技术 |
|------|------|
| 前端 | React 18 + Vite + TypeScript |
| 样式 | Tailwind CSS |
| 后端 | Python 3 + Flask |
| 图标 | Lucide React |

## ⚙️ 环境要求

- Node >= 18
- Python >= 3.9
- macOS (Apple Silicon M2) 需安装 `Xcode Command Line Tools`：`xcode-select --install`
- 推荐使用 `npm` 或 `pnpm`（示例使用 `npm`）

## 🚀 快速开始

```bash
# 1. 后端 - 创建虚拟环境并安装依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. 启动后端 (端口 5001)
python app.py
# 或使用脚本: ./run.sh

# 3. 新终端，安装前端依赖
cd frontend
npm install

# 4. 启动前端 (端口 5173)
npm run dev

# 访问 http://localhost:5173
```

## 📁 项目结构

```
├── frontend/                # React 前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── lib/             # API & 工具函数
│   │   └── App.tsx          # 主应用
│   └── package.json
│
├── backend/                 # Flask 后端
│   ├── app.py               # 应用入口 & 蓝图注册
│   ├── routes/              # 路由
│   │   ├── types_routes.py
│   │   ├── generate_routes.py
│   │   ├── templates_routes.py
│   │   └── export_routes.py
│   ├── services/            # 业务服务
│   │   ├── data_generator_service.py
│   │   ├── data_type_service.py
│   │   ├── template_service.py
│   │   └── export_service.py
│   ├── models/              # 数据模型
│   ├── data_generator.py    # 旧版生成逻辑（保留）
│   ├── requirements.txt
│   └── run.sh
│
└── README.md
```

## 🔌 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/types` | 获取所有数据类型 |
| GET | `/api/types/:category` | 按分类获取数据类型 |
| GET | `/api/categories` | 获取所有分类 |
| POST | `/api/generate` | 生成测试数据 |
| GET | `/api/templates` | 获取模板列表 |
| GET | `/api/templates/:id` | 获取单个模板 |
| GET | `/api/templates/category/:category` | 按分类获取模板 |
| POST | `/api/templates` | 创建模板 |
| PUT | `/api/templates/:id` | 更新模板 |
| DELETE | `/api/templates/:id` | 删除模板 |
| POST | `/api/export/json` | 导出 JSON |
| POST | `/api/export/csv` | 导出 CSV |
| POST | `/api/export/sql` | 导出 SQL |

### API 示例

- 生成数据

```bash
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "fields": [
      {"name":"id","type":"uuid"},
      {"name":"name","type":"chineseName"},
      {"name":"email","type":"email"},
      {"name":"age","type":"age"}
    ],
    "count": 3
  }'
```

- 导出 CSV

```bash
curl -X POST http://localhost:5001/api/export/csv \
  -H "Content-Type: application/json" \
  -d '{
    "fields": [
      {"name":"id"}, {"name":"name"}, {"name":"email"}, {"name":"age"}
    ],
    "data": [
      {"id":"...","name":"...","email":"...","age":30},
      {"id":"...","name":"...","email":"...","age":28}
    ]
  }' \
  -o generated_data.csv
```

## 📖 使用说明

1. **选择分类** - 左侧边栏选择数据类型分类
2. **配置字段** - 添加字段，设置名称和数据类型
3. **生成数据** - 设置数量，点击"生成数据"
4. **导出使用** - 预览数据，选择格式导出

## ❓ 常见问题

- CORS 报错：确保后端运行在 `http://localhost:5001`，前端在 `http://localhost:5173`
- Mac M2 编译问题：安装 `Xcode Command Line Tools` 并升级 pip：`python3 -m pip install --upgrade pip`
- Node 版本问题：使用 `node -v` 确认版本为 18+；建议通过 `nvm` 管理 Node

## 📝 License

本项目采用专有许可证，源码仅供学习参考。商业使用请联系授权。

详见 [LICENSE](./LICENSE)
