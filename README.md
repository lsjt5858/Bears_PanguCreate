# DataForge

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
| 框架 | Next.js 16 (App Router) |
| UI | React 19 + Tailwind CSS 4 |
| 组件 | Radix UI + shadcn/ui |
| 图标 | Lucide React |

## 🚀 快速开始

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev

# 访问 http://localhost:3000
```

## 📁 项目结构

```
├── app/                    # Next.js 路由入口
├── components/
│   ├── data-generator-platform.tsx   # 主容器
│   ├── generator-panel.tsx           # 字段配置面板
│   ├── preview-panel.tsx             # 数据预览与导出
│   ├── template-manager.tsx          # 模板管理
│   ├── sidebar.tsx                   # 分类侧边栏
│   └── ui/                           # 基础 UI 组件
├── lib/
│   ├── data-generator.ts             # 数据生成核心逻辑
│   └── utils.ts                      # 工具函数
└── hooks/                            # React Hooks
```

## 📖 使用说明

1. **选择分类** - 左侧边栏选择数据类型分类
2. **配置字段** - 添加字段，设置名称和数据类型
3. **生成数据** - 设置数量，点击"生成数据"
4. **导出使用** - 预览数据，选择格式导出

## 🔧 常用命令

```bash
pnpm dev      # 开发模式
pnpm build    # 生产构建
pnpm start    # 启动生产服务
pnpm lint     # 代码检查
```

## 📝 License

本项目采用专有许可证，源码仅供学习参考。商业使用请联系授权。

详见 [LICENSE](./LICENSE)
