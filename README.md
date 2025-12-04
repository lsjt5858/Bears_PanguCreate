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

## 🚀 快速开始

```bash
# 1. 后端 - 创建虚拟环境并安装依赖
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. 启动后端 (端口 5000)
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
│   │   ├── components/      # React 组件
│   │   ├── lib/             # API 调用 & 工具函数
│   │   └── App.tsx          # 主应用
│   └── package.json
│
├── backend/                 # Flask 后端
│   ├── app.py               # API 入口
│   ├── data_generator.py    # 数据生成核心逻辑
│   └── requirements.txt
│
└── README.md
```

## 🔌 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/types` | 获取支持的数据类型 |
| POST | `/api/generate` | 生成测试数据 |
| GET | `/api/templates` | 获取模板列表 |
| POST | `/api/templates` | 创建模板 |
| PUT | `/api/templates/:id` | 更新模板 |
| DELETE | `/api/templates/:id` | 删除模板 |

## 📖 使用说明

1. **选择分类** - 左侧边栏选择数据类型分类
2. **配置字段** - 添加字段，设置名称和数据类型
3. **生成数据** - 设置数量，点击"生成数据"
4. **导出使用** - 预览数据，选择格式导出

## 📝 License

本项目采用专有许可证，源码仅供学习参考。商业使用请联系授权。

详见 [LICENSE](./LICENSE)
