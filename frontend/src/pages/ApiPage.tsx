import { useState } from 'react'
import {
    Key,
    Plus,
    Copy,
    Eye,
    EyeOff,
    Trash2,
    Clock,
    Calendar,
    Play,
    Pause,
    Settings,
    FileCode
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, Button, Input, Modal, ModalFooter, Badge, Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/common'
import type { ApiKey, ScheduledTask, ApiKeyPermission, TaskStatus } from '@/lib/types'

// 模拟API密钥数据
const mockApiKeys: ApiKey[] = [
    {
        id: '1',
        name: '生产环境密钥',
        key: 'df_prod_a1b2c3d4e5f6g7h8i9j0',
        permissions: ['read', 'write'],
        callCount: 12450,
        lastUsed: '2024-07-15T10:30:00.000Z',
        expiresAt: '2025-01-01T00:00:00.000Z',
        createdAt: '2024-01-01T00:00:00.000Z',
    },
    {
        id: '2',
        name: '测试环境密钥',
        key: 'df_test_k1l2m3n4o5p6q7r8s9t0',
        permissions: ['read'],
        callCount: 3280,
        lastUsed: '2024-07-14T15:20:00.000Z',
        createdAt: '2024-02-01T00:00:00.000Z',
    },
    {
        id: '3',
        name: 'CI/CD自动化',
        key: 'df_ci_u1v2w3x4y5z6a7b8c9d0',
        permissions: ['admin'],
        callCount: 890,
        lastUsed: '2024-07-15T08:00:00.000Z',
        expiresAt: '2024-12-31T00:00:00.000Z',
        createdAt: '2024-03-01T00:00:00.000Z',
    },
]

// 模拟定时任务数据
const mockScheduledTasks: ScheduledTask[] = [
    {
        id: '1',
        name: '每日用户数据同步',
        templateId: '1',
        cronExpression: '0 0 * * *',
        count: 1000,
        status: 'active',
        lastRun: '2024-07-15T00:00:00.000Z',
        nextRun: '2024-07-16T00:00:00.000Z',
        createdAt: '2024-01-01T00:00:00.000Z',
    },
    {
        id: '2',
        name: '订单数据周报',
        templateId: '2',
        cronExpression: '0 8 * * 1',
        count: 5000,
        status: 'active',
        lastRun: '2024-07-08T08:00:00.000Z',
        nextRun: '2024-07-15T08:00:00.000Z',
        createdAt: '2024-02-01T00:00:00.000Z',
    },
    {
        id: '3',
        name: '测试数据清理',
        templateId: '3',
        cronExpression: '0 2 1 * *',
        count: 10000,
        status: 'paused',
        lastRun: '2024-07-01T02:00:00.000Z',
        createdAt: '2024-03-01T00:00:00.000Z',
    },
]

const permissionLabels: Record<ApiKeyPermission, { label: string; color: string }> = {
    read: { label: '只读', color: 'bg-blue-500/20 text-blue-400' },
    write: { label: '读写', color: 'bg-green-500/20 text-green-400' },
    admin: { label: '管理', color: 'bg-red-500/20 text-red-400' },
}

const taskStatusConfig: Record<TaskStatus, { label: string; color: string; icon: typeof Play }> = {
    active: { label: '运行中', color: 'text-green-400', icon: Play },
    paused: { label: '已暂停', color: 'text-yellow-400', icon: Pause },
    error: { label: '错误', color: 'text-red-400', icon: Clock },
}

export function ApiPage() {
    const [activeTab, setActiveTab] = useState('keys')
    const [visibleKeys, setVisibleKeys] = useState<Set<string>>(new Set())
    const [isCreateKeyModalOpen, setIsCreateKeyModalOpen] = useState(false)

    const toggleKeyVisibility = (keyId: string) => {
        setVisibleKeys(prev => {
            const next = new Set(prev)
            if (next.has(keyId)) {
                next.delete(keyId)
            } else {
                next.add(keyId)
            }
            return next
        })
    }

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text)
        // TODO: 显示复制成功提示
    }

    const maskKey = (key: string) => {
        const prefix = key.substring(0, 8)
        const suffix = key.substring(key.length - 4)
        return `${prefix}${'*'.repeat(12)}${suffix}`
    }

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-foreground">API 与自动化</h1>
                <p className="text-muted-foreground">管理API密钥和定时任务</p>
            </div>

            <Tabs value={activeTab} onChange={setActiveTab}>
                <TabsList className="mb-6">
                    <TabsTrigger value="keys" icon={<Key className="h-4 w-4" />}>
                        API 密钥
                    </TabsTrigger>
                    <TabsTrigger value="tasks" icon={<Clock className="h-4 w-4" />}>
                        定时任务
                    </TabsTrigger>
                    <TabsTrigger value="docs" icon={<FileCode className="h-4 w-4" />}>
                        API 文档
                    </TabsTrigger>
                </TabsList>

                {/* API 密钥管理 */}
                <TabsContent value="keys">
                    <div className="flex justify-end mb-4">
                        <Button variant="primary" onClick={() => setIsCreateKeyModalOpen(true)}>
                            <Plus className="h-4 w-4" />
                            创建密钥
                        </Button>
                    </div>

                    <div className="space-y-4">
                        {mockApiKeys.map((apiKey) => (
                            <Card key={apiKey.id}>
                                <CardContent className="p-4">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-2">
                                                <h3 className="text-base font-semibold text-foreground">{apiKey.name}</h3>
                                                {apiKey.permissions.map((perm) => (
                                                    <span
                                                        key={perm}
                                                        className={`text-xs px-2 py-0.5 rounded-full ${permissionLabels[perm].color}`}
                                                    >
                                                        {permissionLabels[perm].label}
                                                    </span>
                                                ))}
                                            </div>

                                            <div className="flex items-center gap-2 bg-muted/50 rounded-lg px-3 py-2 font-mono text-sm">
                                                <Key className="h-4 w-4 text-muted-foreground" />
                                                <span className="text-foreground">
                                                    {visibleKeys.has(apiKey.id) ? apiKey.key : maskKey(apiKey.key)}
                                                </span>
                                                <button
                                                    onClick={() => toggleKeyVisibility(apiKey.id)}
                                                    className="p-1 hover:bg-secondary rounded"
                                                >
                                                    {visibleKeys.has(apiKey.id) ? (
                                                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                                                    ) : (
                                                        <Eye className="h-4 w-4 text-muted-foreground" />
                                                    )}
                                                </button>
                                                <button
                                                    onClick={() => copyToClipboard(apiKey.key)}
                                                    className="p-1 hover:bg-secondary rounded"
                                                >
                                                    <Copy className="h-4 w-4 text-muted-foreground" />
                                                </button>
                                            </div>

                                            <div className="flex flex-wrap gap-4 mt-3 text-xs text-muted-foreground">
                                                <span className="flex items-center gap-1">
                                                    <Clock className="h-3.5 w-3.5" />
                                                    调用次数: {apiKey.callCount.toLocaleString()}
                                                </span>
                                                {apiKey.lastUsed && (
                                                    <span>
                                                        最后使用: {new Date(apiKey.lastUsed).toLocaleString('zh-CN')}
                                                    </span>
                                                )}
                                                {apiKey.expiresAt && (
                                                    <span className="flex items-center gap-1">
                                                        <Calendar className="h-3.5 w-3.5" />
                                                        过期时间: {new Date(apiKey.expiresAt).toLocaleDateString('zh-CN')}
                                                    </span>
                                                )}
                                            </div>
                                        </div>

                                        <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-destructive">
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>

                {/* 定时任务 */}
                <TabsContent value="tasks">
                    <div className="flex justify-end mb-4">
                        <Button variant="primary">
                            <Plus className="h-4 w-4" />
                            创建任务
                        </Button>
                    </div>

                    <div className="space-y-4">
                        {mockScheduledTasks.map((task) => {
                            const status = taskStatusConfig[task.status]
                            const StatusIcon = status.icon

                            return (
                                <Card key={task.id}>
                                    <CardContent className="p-4">
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-2">
                                                    <h3 className="text-base font-semibold text-foreground">{task.name}</h3>
                                                    <span className={`flex items-center gap-1 text-xs ${status.color}`}>
                                                        <StatusIcon className="h-3.5 w-3.5" />
                                                        {status.label}
                                                    </span>
                                                </div>

                                                <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                                                    <span className="font-mono bg-muted/50 px-2 py-0.5 rounded">
                                                        {task.cronExpression}
                                                    </span>
                                                    <span>生成 {task.count.toLocaleString()} 条</span>
                                                </div>

                                                <div className="flex flex-wrap gap-4 mt-2 text-xs text-muted-foreground">
                                                    {task.lastRun && (
                                                        <span>上次运行: {new Date(task.lastRun).toLocaleString('zh-CN')}</span>
                                                    )}
                                                    {task.nextRun && (
                                                        <span>下次运行: {new Date(task.nextRun).toLocaleString('zh-CN')}</span>
                                                    )}
                                                </div>
                                            </div>

                                            <div className="flex items-center gap-1">
                                                <Button variant="ghost" size="icon">
                                                    {task.status === 'active' ? (
                                                        <Pause className="h-4 w-4" />
                                                    ) : (
                                                        <Play className="h-4 w-4" />
                                                    )}
                                                </Button>
                                                <Button variant="ghost" size="icon">
                                                    <Settings className="h-4 w-4" />
                                                </Button>
                                                <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-destructive">
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            )
                        })}
                    </div>
                </TabsContent>

                {/* API 文档 */}
                <TabsContent value="docs">
                    <Card>
                        <CardHeader>
                            <CardTitle>API 接口文档</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-6">
                                <div>
                                    <h4 className="text-sm font-semibold text-foreground mb-2">生成数据</h4>
                                    <div className="bg-muted/50 rounded-lg p-4 font-mono text-sm">
                                        <div className="flex items-center gap-2 text-primary mb-2">
                                            <Badge variant="primary">POST</Badge>
                                            <span>/api/generate</span>
                                        </div>
                                        <pre className="text-muted-foreground overflow-x-auto">
                                            {`curl -X POST http://localhost:5001/api/generate \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -d '{
    "fields": [
      {"name": "id", "type": "uuid"},
      {"name": "name", "type": "chineseName"},
      {"name": "email", "type": "email"}
    ],
    "count": 100
  }'`}
                                        </pre>
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-sm font-semibold text-foreground mb-2">获取模板列表</h4>
                                    <div className="bg-muted/50 rounded-lg p-4 font-mono text-sm">
                                        <div className="flex items-center gap-2 text-green-400 mb-2">
                                            <Badge variant="success">GET</Badge>
                                            <span>/api/templates</span>
                                        </div>
                                        <pre className="text-muted-foreground overflow-x-auto">
                                            {`curl http://localhost:5001/api/templates \\
  -H "Authorization: Bearer YOUR_API_KEY"`}
                                        </pre>
                                    </div>
                                </div>

                                <div>
                                    <h4 className="text-sm font-semibold text-foreground mb-2">导出数据</h4>
                                    <div className="bg-muted/50 rounded-lg p-4 font-mono text-sm">
                                        <div className="flex items-center gap-2 text-primary mb-2">
                                            <Badge variant="primary">POST</Badge>
                                            <span>/api/export/:format</span>
                                        </div>
                                        <p className="text-muted-foreground mb-2">支持格式: json, csv, sql</p>
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>

            {/* 创建API密钥弹窗 */}
            <Modal
                isOpen={isCreateKeyModalOpen}
                onClose={() => setIsCreateKeyModalOpen(false)}
                title="创建 API 密钥"
            >
                <div className="space-y-4">
                    <Input label="密钥名称" placeholder="例如: 生产环境" />
                    <div>
                        <label className="text-xs font-medium text-muted-foreground mb-2 block">权限</label>
                        <div className="flex gap-2">
                            {(['read', 'write', 'admin'] as const).map((perm) => (
                                <button
                                    key={perm}
                                    className={`px-3 py-1.5 text-sm rounded-lg border border-border hover:bg-secondary`}
                                >
                                    {permissionLabels[perm].label}
                                </button>
                            ))}
                        </div>
                    </div>
                    <Input label="过期时间 (可选)" type="date" />
                </div>
                <ModalFooter>
                    <Button variant="ghost" onClick={() => setIsCreateKeyModalOpen(false)}>取消</Button>
                    <Button variant="primary">创建</Button>
                </ModalFooter>
            </Modal>
        </div>
    )
}
