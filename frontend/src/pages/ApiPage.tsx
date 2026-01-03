import { useState, useEffect } from 'react'
import {
    Key,
    Plus,
    Copy,
    EyeOff,
    Trash2,
    Clock,
    Calendar,
    Play,
    Pause,
    Settings,
    FileCode,
    Loader2,
    CheckCircle2
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, Button, Input, Modal, ModalFooter, Badge, Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/common'
import type { ApiKey, ScheduledTask, ApiKeyPermission, TaskStatus } from '@/lib/types'
import { fetchApiKeys, createApiKey, deleteApiKey } from '@/lib/api'

// 模拟定时任务数据 (后端尚未就绪)
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
    const [apiKeys, setApiKeys] = useState<ApiKey[]>([])
    const [loading, setLoading] = useState(false)

    // 创建密钥状态
    const [isCreateKeyModalOpen, setIsCreateKeyModalOpen] = useState(false)
    const [newKeyName, setNewKeyName] = useState('')
    const [newKeyPermissions, setNewKeyPermissions] = useState<ApiKeyPermission[]>(['read'])
    const [newKeyExpiresAt, setNewKeyExpiresAt] = useState('')
    const [isCreating, setIsCreating] = useState(false)

    // 成功弹窗状态
    const [createdKey, setCreatedKey] = useState<{ name: string, key: string } | null>(null)

    // 加载密钥列表
    const loadKeys = async () => {
        try {
            setLoading(true)
            const keys = await fetchApiKeys()
            setApiKeys(keys)
        } catch (err) {
            console.error('Failed to fetch api keys:', err)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadKeys()
    }, [])

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text)
        // TODO: 显示 toast
    }

    const handleCreateKey = async () => {
        if (!newKeyName || isCreating) return

        try {
            setIsCreating(true)
            // 处理日期格式
            let expiresAt = undefined
            if (newKeyExpiresAt) {
                expiresAt = new Date(newKeyExpiresAt).toISOString()
            }

            const { apiKey, fullKey } = await createApiKey(newKeyName, newKeyPermissions, expiresAt)

            // 更新列表
            setApiKeys(prev => [apiKey, ...prev])

            // 显示成功弹窗
            setCreatedKey({ name: apiKey.name, key: fullKey })
            setIsCreateKeyModalOpen(false)

            // 重置表单
            setNewKeyName('')
            setNewKeyPermissions(['read'])
            setNewKeyExpiresAt('')
        } catch (err: any) {
            alert(err.message || '创建失败')
        } finally {
            setIsCreating(false)
        }
    }

    const handleDeleteKey = async (id: string, name: string) => {
        if (!confirm(`确定要删除密钥 "${name}" 吗？此操作不可恢复。`)) return

        try {
            await deleteApiKey(id)
            setApiKeys(prev => prev.filter(k => k.id !== id))
        } catch (err: any) {
            alert(err.message || '删除失败')
        }
    }

    const togglePermission = (perm: ApiKeyPermission) => {
        setNewKeyPermissions(prev => {
            if (prev.includes(perm)) {
                return prev.filter(p => p !== perm)
            } else {
                return [...prev, perm]
            }
        })
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

                    {loading && apiKeys.length === 0 ? (
                        <div className="flex justify-center p-8">
                            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                        </div>
                    ) : apiKeys.length === 0 ? (
                        <Card>
                            <CardContent className="flex flex-col items-center justify-center p-8 text-muted-foreground">
                                <Key className="h-12 w-12 mb-4 opacity-20" />
                                <p>暂无 API 密钥</p>
                            </CardContent>
                        </Card>
                    ) : (
                        <div className="space-y-4">
                            {apiKeys.map((apiKey) => (
                                <Card key={apiKey.id}>
                                    <CardContent className="p-4">
                                        <div className="flex items-start justify-between">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-2">
                                                    <h3 className="text-base font-semibold text-foreground">{apiKey.name}</h3>
                                                    {apiKey.permissions.map((perm) => (
                                                        <span
                                                            key={perm}
                                                            className={`text-xs px-2 py-0.5 rounded-full ${permissionLabels[perm as ApiKeyPermission]?.color || 'bg-gray-500/20'}`}
                                                        >
                                                            {permissionLabels[perm as ApiKeyPermission]?.label || perm}
                                                        </span>
                                                    ))}
                                                </div>

                                                <div className="flex items-center gap-2 bg-muted/50 rounded-lg px-3 py-2 font-mono text-sm max-w-md">
                                                    <Key className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                                                    <span className="text-foreground truncate flex-1">
                                                        {apiKey.key}
                                                    </span>
                                                    <button // 既然无法查看完整key，这里只保留复制掩码后的（或提示无法复制完整）
                                                        onClick={() => {
                                                            alert('出于安全考虑，无法查看完整密钥。如需使用请创建一个新的。')
                                                        }}
                                                        className="p-1 hover:bg-secondary rounded"
                                                        title="无法查看完整密钥"
                                                    >
                                                        <EyeOff className="h-4 w-4 text-muted-foreground" />
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

                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="text-muted-foreground hover:text-destructive"
                                                onClick={() => handleDeleteKey(apiKey.id, apiKey.name)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}
                </TabsContent>

                {/* 定时任务 (Mock) */}
                <TabsContent value="tasks">
                    <div className="flex justify-end mb-4">
                        <Button variant="primary" disabled title="功能开发中">
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
                                            </div>

                                            <div className="flex items-center gap-1">
                                                <Button variant="ghost" size="icon" disabled>
                                                    <Play className="h-4 w-4" />
                                                </Button>
                                                <Button variant="ghost" size="icon" disabled>
                                                    <Settings className="h-4 w-4" />
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
                    <Input
                        label="密钥名称"
                        placeholder="例如: 生产环境"
                        value={newKeyName}
                        onChange={(e) => setNewKeyName(e.target.value)}
                    />
                    <div>
                        <label className="text-xs font-medium text-muted-foreground mb-2 block">权限</label>
                        <div className="flex gap-2">
                            {(['read', 'write', 'admin'] as const).map((perm) => (
                                <button
                                    key={perm}
                                    onClick={() => togglePermission(perm)}
                                    className={`px-3 py-1.5 text-sm rounded-lg border transition-colors ${newKeyPermissions.includes(perm)
                                            ? 'bg-primary text-primary-foreground border-primary'
                                            : 'border-border hover:bg-secondary'
                                        }`}
                                >
                                    {permissionLabels[perm].label}
                                </button>
                            ))}
                        </div>
                    </div>
                    <Input
                        label="过期时间 (可选)"
                        type="date"
                        value={newKeyExpiresAt}
                        onChange={(e) => setNewKeyExpiresAt(e.target.value)}
                    />
                </div>
                <ModalFooter>
                    <Button variant="ghost" onClick={() => setIsCreateKeyModalOpen(false)}>取消</Button>
                    <Button variant="primary" onClick={handleCreateKey} disabled={isCreating || !newKeyName}>
                        {isCreating ? '创建中...' : '创建'}
                    </Button>
                </ModalFooter>
            </Modal>

            {/* 密钥创建成功弹窗 */}
            <Modal
                isOpen={!!createdKey}
                onClose={() => setCreatedKey(null)}
                title="密钥创建成功"
            >
                <div className="space-y-4">
                    <div className="flex items-center gap-2 text-green-500 mb-2">
                        <CheckCircle2 className="h-5 w-5" />
                        <span className="font-medium">密钥已生成</span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                        请立即复制并保存您的密钥。出于安全考虑，<strong className="text-foreground">您将无法再次查看此密钥</strong>。
                    </p>

                    <div className="bg-muted p-3 rounded-lg flex items-center gap-2">
                        <code className="text-sm flex-1 break-all font-mono">{createdKey?.key}</code>
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => copyToClipboard(createdKey?.key || '')}
                        >
                            <Copy className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
                <ModalFooter>
                    <Button variant="primary" onClick={() => setCreatedKey(null)}>我知道了</Button>
                </ModalFooter>
            </Modal>
        </div>
    )
}
