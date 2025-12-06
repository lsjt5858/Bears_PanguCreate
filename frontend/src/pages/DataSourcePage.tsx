import { useState } from 'react'
import {
    Database,
    Plus,
    Settings,
    Trash2,
    RefreshCw,
    CheckCircle,
    XCircle,
    AlertCircle,
    Server,
    Globe
} from 'lucide-react'
import { Card, CardContent, Button, Input, Modal, ModalFooter, Select, Badge } from '@/components/common'
import type { DataSource, DataSourceType } from '@/lib/types'

// 模拟数据源
const mockDataSources: DataSource[] = [
    {
        id: '1',
        name: '测试MySQL数据库',
        type: 'mysql',
        host: '192.168.1.100',
        port: 3306,
        database: 'test_db',
        username: 'test_user',
        status: 'connected',
        lastConnected: '2024-07-15T10:30:00.000Z',
        createdAt: '2024-01-01T00:00:00.000Z',
    },
    {
        id: '2',
        name: '生产PostgreSQL',
        type: 'postgresql',
        host: '10.0.0.50',
        port: 5432,
        database: 'prod_db',
        username: 'admin',
        status: 'disconnected',
        createdAt: '2024-02-01T00:00:00.000Z',
    },
    {
        id: '3',
        name: 'MongoDB集群',
        type: 'mongodb',
        host: 'mongo.example.com',
        port: 27017,
        database: 'analytics',
        status: 'connected',
        lastConnected: '2024-07-15T09:00:00.000Z',
        createdAt: '2024-03-01T00:00:00.000Z',
    },
    {
        id: '4',
        name: '外部API服务',
        type: 'restapi',
        host: 'api.example.com',
        port: 443,
        status: 'error',
        createdAt: '2024-04-01T00:00:00.000Z',
    },
]

const dataSourceTypes: { value: DataSourceType; label: string; icon: React.ReactNode }[] = [
    { value: 'mysql', label: 'MySQL', icon: <Database className="h-4 w-4" /> },
    { value: 'postgresql', label: 'PostgreSQL', icon: <Database className="h-4 w-4" /> },
    { value: 'mongodb', label: 'MongoDB', icon: <Server className="h-4 w-4" /> },
    { value: 'restapi', label: 'REST API', icon: <Globe className="h-4 w-4" /> },
]

const statusConfig = {
    connected: { label: '已连接', icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/20' },
    disconnected: { label: '未连接', icon: XCircle, color: 'text-gray-400', bg: 'bg-gray-500/20' },
    error: { label: '连接错误', icon: AlertCircle, color: 'text-red-400', bg: 'bg-red-500/20' },
}

export function DataSourcePage() {
    const [dataSources, _setDataSources] = useState<DataSource[]>(mockDataSources)
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [editingSource, setEditingSource] = useState<DataSource | null>(null)
    const [formData, setFormData] = useState({
        name: '',
        type: 'mysql' as DataSourceType,
        host: '',
        port: '',
        database: '',
        username: '',
        password: '',
    })

    const handleOpenModal = (source?: DataSource) => {
        if (source) {
            setEditingSource(source)
            setFormData({
                name: source.name,
                type: source.type,
                host: source.host,
                port: source.port.toString(),
                database: source.database || '',
                username: source.username || '',
                password: '',
            })
        } else {
            setEditingSource(null)
            setFormData({
                name: '',
                type: 'mysql',
                host: '',
                port: '3306',
                database: '',
                username: '',
                password: '',
            })
        }
        setIsModalOpen(true)
    }

    const handleSave = () => {
        // 保存逻辑
        setIsModalOpen(false)
    }

    const handleTestConnection = () => {
        // 测试连接逻辑
        alert('测试连接...')
    }

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-foreground">数据源管理</h1>
                    <p className="text-muted-foreground">管理数据库和API连接</p>
                </div>
                <Button variant="primary" onClick={() => handleOpenModal()}>
                    <Plus className="h-4 w-4" />
                    添加数据源
                </Button>
            </div>

            {/* 数据源列表 */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {dataSources.map((source) => {
                    const status = statusConfig[source.status]
                    const StatusIcon = status.icon
                    const typeInfo = dataSourceTypes.find(t => t.value === source.type)

                    return (
                        <Card key={source.id} hover>
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-start gap-3">
                                        <div className="h-10 w-10 rounded-lg bg-primary/20 flex items-center justify-center">
                                            {typeInfo?.icon || <Database className="h-5 w-5 text-primary" />}
                                        </div>
                                        <div>
                                            <h3 className="text-base font-semibold text-foreground">{source.name}</h3>
                                            <p className="text-sm text-muted-foreground mt-0.5">
                                                {source.host}:{source.port}
                                                {source.database && ` / ${source.database}`}
                                            </p>
                                            <div className="flex items-center gap-2 mt-2">
                                                <Badge variant="outline">{typeInfo?.label}</Badge>
                                                <span className={`flex items-center gap-1 text-xs ${status.color}`}>
                                                    <StatusIcon className="h-3.5 w-3.5" />
                                                    {status.label}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-1">
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            title="刷新连接"
                                        >
                                            <RefreshCw className="h-4 w-4" />
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={() => handleOpenModal(source)}
                                            title="设置"
                                        >
                                            <Settings className="h-4 w-4" />
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="text-muted-foreground hover:text-destructive"
                                            title="删除"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                                {source.lastConnected && (
                                    <p className="text-xs text-muted-foreground mt-3 pt-3 border-t border-border">
                                        上次连接: {new Date(source.lastConnected).toLocaleString('zh-CN')}
                                    </p>
                                )}
                            </CardContent>
                        </Card>
                    )
                })}
            </div>

            {/* 添加/编辑数据源弹窗 */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={editingSource ? '编辑数据源' : '添加数据源'}
                size="lg"
            >
                <div className="space-y-4">
                    <Input
                        label="名称"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="给数据源起个名字"
                    />

                    <Select
                        label="类型"
                        value={formData.type}
                        onChange={(value) => setFormData({ ...formData, type: value as DataSourceType })}
                        options={dataSourceTypes.map(t => ({ value: t.value, label: t.label, icon: t.icon }))}
                    />

                    <div className="grid grid-cols-2 gap-4">
                        <Input
                            label="主机地址"
                            value={formData.host}
                            onChange={(e) => setFormData({ ...formData, host: e.target.value })}
                            placeholder="localhost 或 IP地址"
                        />
                        <Input
                            label="端口"
                            value={formData.port}
                            onChange={(e) => setFormData({ ...formData, port: e.target.value })}
                            placeholder="3306"
                        />
                    </div>

                    {formData.type !== 'restapi' && (
                        <>
                            <Input
                                label="数据库名"
                                value={formData.database}
                                onChange={(e) => setFormData({ ...formData, database: e.target.value })}
                                placeholder="test_db"
                            />
                            <div className="grid grid-cols-2 gap-4">
                                <Input
                                    label="用户名"
                                    value={formData.username}
                                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                                    placeholder="root"
                                />
                                <Input
                                    label="密码"
                                    type="password"
                                    value={formData.password}
                                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                    placeholder="••••••••"
                                />
                            </div>
                        </>
                    )}
                </div>

                <ModalFooter>
                    <Button variant="outline" onClick={handleTestConnection}>
                        测试连接
                    </Button>
                    <Button variant="ghost" onClick={() => setIsModalOpen(false)}>
                        取消
                    </Button>
                    <Button variant="primary" onClick={handleSave}>
                        保存
                    </Button>
                </ModalFooter>
            </Modal>
        </div>
    )
}
