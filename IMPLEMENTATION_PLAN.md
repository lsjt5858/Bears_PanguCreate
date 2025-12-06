# DataForge 企业级功能扩展实施计划

## 📋 功能概览

基于 v0.app 设计，需要添加以下企业级功能模块：

### 第一阶段：基础企业化
1. ✅ 用户登录与权限管理
2. ✅ 项目空间（多项目隔离）
3. ✅ 历史记录与数据集管理

### 第二阶段：团队协作
4. ✅ 模板市场
5. ✅ 数据源管理（数据库连接）
6. ✅ API 接口管理

### 第三阶段：高级能力
7. ✅ 关联数据生成
8. ✅ 仪表盘（Dashboard）
9. ✅ 定时任务与自动化

### 锦上添花
10. ⬜ 数据脱敏
11. ⬜ 系统设置
12. ⬜ Webhook 通知
13. ⬜ 数据验证规则
14. ⬜ 批量导入
15. ⬜ 审计日志

---

## 🏗️ 实施详情

### 模块 1：用户权限与项目空间

#### 后端
- `models/user.py` - 用户模型
- `models/project.py` - 项目模型
- `services/auth_service.py` - 认证服务
- `services/project_service.py` - 项目服务
- `routes/auth_routes.py` - 认证路由
- `routes/project_routes.py` - 项目路由

#### 前端
- `components/UserMenu.tsx` - 用户菜单（头像、角色、个人设置、API密钥）
- `components/ProjectSwitcher.tsx` - 项目切换器
- `components/modals/UserProfileModal.tsx` - 个人资料弹窗
- `components/modals/ProjectSettingsModal.tsx` - 项目设置弹窗

---

### 模块 2：数据源管理

#### 后端
- `models/datasource.py` - 数据源模型
- `services/datasource_service.py` - 数据源服务
- `routes/datasource_routes.py` - 数据源路由

#### 前端
- `components/DataSourceManager.tsx` - 数据源管理面板
- `components/modals/DataSourceModal.tsx` - 添加/编辑数据源弹窗
- `components/DataSourceBrowser.tsx` - 数据库结构浏览器

---

### 模块 3：历史记录与数据集

#### 后端
- `models/history.py` - 历史记录模型
- `models/dataset.py` - 数据集模型
- `services/history_service.py` - 历史记录服务
- `routes/history_routes.py` - 历史记录路由

#### 前端
- `components/HistoryPanel.tsx` - 历史记录面板
- `components/DatasetList.tsx` - 数据集列表
- `pages/HistoryPage.tsx` - 历史记录页面

---

### 模块 4：模板市场

#### 后端
- `models/template_market.py` - 市场模板模型（评分、下载量、收藏）
- `services/template_market_service.py` - 模板市场服务
- `routes/template_market_routes.py` - 模板市场路由

#### 前端
- `pages/TemplateMarketPage.tsx` - 模板市场页面
- `components/TemplateCard.tsx` - 模板卡片组件
- `components/TemplateFilters.tsx` - 筛选组件

---

### 模块 5：API 与自动化

#### 后端
- `models/api_key.py` - API 密钥模型
- `models/scheduled_task.py` - 定时任务模型
- `services/api_key_service.py` - API 密钥服务
- `services/scheduler_service.py` - 调度服务
- `routes/api_key_routes.py` - API 密钥路由
- `routes/scheduler_routes.py` - 定时任务路由

#### 前端
- `pages/ApiPage.tsx` - API 管理页面
- `components/ApiKeyManager.tsx` - API 密钥管理
- `components/ScheduledTasks.tsx` - 定时任务管理
- `components/ApiDocumentation.tsx` - API 文档

---

### 模块 6：关联数据生成

#### 后端
- `models/relation.py` - 表关系模型
- `services/relation_generator_service.py` - 关联数据生成服务
- `routes/relation_routes.py` - 关联数据路由

#### 前端
- `components/RelationEditor.tsx` - 关系配置编辑器
- `components/RelationVisualizer.tsx` - 关系可视化
- `pages/RelationPage.tsx` - 关联数据页面

---

### 模块 7：仪表盘

#### 后端
- `services/stats_service.py` - 统计服务
- `routes/stats_routes.py` - 统计路由

#### 前端
- `pages/DashboardPage.tsx` - 仪表盘页面
- `components/StatsCard.tsx` - 统计卡片
- `components/TrendChart.tsx` - 趋势图表
- `components/ActivityLog.tsx` - 活动日志

---

## 📂 目标项目结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/           # 通用组件
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Card.tsx
│   │   │   └── ...
│   │   ├── layout/           # 布局组件
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── UserMenu.tsx
│   │   │   └── ProjectSwitcher.tsx
│   │   ├── generator/        # 数据生成相关
│   │   │   ├── GeneratorPanel.tsx
│   │   │   ├── PreviewPanel.tsx
│   │   │   └── FieldEditor.tsx
│   │   ├── datasource/       # 数据源管理
│   │   │   ├── DataSourceManager.tsx
│   │   │   └── DataSourceBrowser.tsx
│   │   ├── templates/        # 模板相关
│   │   │   ├── TemplateCard.tsx
│   │   │   └── TemplateFilters.tsx
│   │   ├── history/          # 历史记录
│   │   │   ├── HistoryPanel.tsx
│   │   │   └── DatasetList.tsx
│   │   ├── api/              # API 管理
│   │   │   ├── ApiKeyManager.tsx
│   │   │   └── ScheduledTasks.tsx
│   │   ├── dashboard/        # 仪表盘
│   │   │   ├── StatsCard.tsx
│   │   │   └── TrendChart.tsx
│   │   └── modals/           # 弹窗组件
│   │       ├── UserProfileModal.tsx
│   │       ├── ProjectSettingsModal.tsx
│   │       └── DataSourceModal.tsx
│   ├── pages/                # 页面组件
│   │   ├── GeneratorPage.tsx
│   │   ├── TemplateMarketPage.tsx
│   │   ├── HistoryPage.tsx
│   │   ├── DataSourcePage.tsx
│   │   ├── ApiPage.tsx
│   │   ├── DashboardPage.tsx
│   │   └── RelationPage.tsx
│   ├── lib/
│   │   ├── api.ts            # API 调用
│   │   ├── utils.ts          # 工具函数
│   │   └── types.ts          # 类型定义
│   ├── hooks/                # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   └── useProject.ts
│   ├── context/              # React Context
│   │   ├── AuthContext.tsx
│   │   └── ProjectContext.tsx
│   ├── App.tsx
│   └── main.tsx

backend/
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── project.py
│   ├── datasource.py
│   ├── history.py
│   ├── dataset.py
│   ├── template_market.py
│   ├── api_key.py
│   ├── scheduled_task.py
│   └── relation.py
├── services/
│   ├── __init__.py
│   ├── data_generator_service.py
│   ├── data_type_service.py
│   ├── template_service.py
│   ├── export_service.py
│   ├── auth_service.py
│   ├── project_service.py
│   ├── datasource_service.py
│   ├── history_service.py
│   ├── template_market_service.py
│   ├── api_key_service.py
│   ├── scheduler_service.py
│   ├── relation_generator_service.py
│   └── stats_service.py
├── routes/
│   ├── __init__.py
│   ├── types_routes.py
│   ├── generate_routes.py
│   ├── templates_routes.py
│   ├── export_routes.py
│   ├── auth_routes.py
│   ├── project_routes.py
│   ├── datasource_routes.py
│   ├── history_routes.py
│   ├── template_market_routes.py
│   ├── api_key_routes.py
│   ├── scheduler_routes.py
│   ├── relation_routes.py
│   └── stats_routes.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── app.py
└── requirements.txt
```

---

## 🚀 执行顺序

### Phase 1: 基础设施
1. 创建目录结构
2. 添加路由系统（react-router-dom）
3. 创建通用 UI 组件库

### Phase 2: 核心功能页面
4. UserMenu + ProjectSwitcher
5. Dashboard 仪表盘
6. History 历史记录页面
7. Template Market 模板市场

### Phase 3: 高级功能
8. DataSource 数据源管理
9. API 管理 + 定时任务
10. Relation 关联数据生成

### Phase 4: 完善
11. 集成测试
12. 优化 UI/UX
13. 文档更新

---

## ⏱️ 预计工作量

| 阶段 | 预计时间 |
|------|----------|
| Phase 1 | 1-2 小时 |
| Phase 2 | 3-4 小时 |
| Phase 3 | 3-4 小时 |
| Phase 4 | 1-2 小时 |
| **总计** | **8-12 小时** |

---

## ✅ 开始执行

现在开始按计划执行，首先从 Phase 1 基础设施开始。
