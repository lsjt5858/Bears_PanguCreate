import { useState, useEffect } from 'react'
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
import { fetchDataSources, createDataSource, updateDataSource, deleteDataSource, testDataSourceConnection, testConnectionParams } from '@/lib/api'

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
    const [dataSources, setDataSources] = useState<DataSource[]>([])
    const [loading, setLoading] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false)
    const [editingSource, setEditingSource] = useState<DataSource | null>(null)
    const [isSaving, setIsSaving] = useState(false)
    const [isTesting, setIsTesting] = useState(false)

    // 表单状态
    const [formData, setFormData] = useState({
        name: '',
        type: 'mysql' as DataSourceType,
        host: '',
        port: '3306',
        database: '',
        username: '',
        password: '',
        description: '',
    })

    // 加载数据源
    const loadDataSources = async () => {
        try {
            setLoading(true)
            const list = await fetchDataSources()
            setDataSources(list)
        } catch (err) {
            console.error('Failed to load data sources:', err)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadDataSources()
    }, [])

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
                password: '', // 编辑时不回显密码
                description: source.description || '',
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
                description: '',
            })
        }
        setIsModalOpen(true)
    }

    const handleSave = async () => {
        if (!formData.name || !formData.host || !formData.port) {
            alert('请填写必要信息')
            return
        }

        try {
            setIsSaving(true)
            const payload = {
                ...formData,
                port: parseInt(formData.port),
            }

            if (editingSource) {
                await updateDataSource(editingSource.id, payload)
            } else {
                await createDataSource(payload)
            }

            setIsModalOpen(false)
            loadDataSources()
        } catch (err: any) {
            alert(err.message || '保存失败')
        } finally {
            setIsSaving(false)
        }
    }

    // Modal 内测试连接
    const handleTestParams = async () => {
        if (!formData.host || !formData.port) {
            alert('需填写主机和端口')
            return
        }
        try {
            setIsTesting(true)
            const res = await testConnectionParams({
                ...formData,
                port: parseInt(formData.port)
            })
            alert(res.success ? '连接成功！' : `连接失败: ${res.message}`)
        } catch (err: any) {
            alert(err.message || '测试连接出错')
        } finally {
            setIsTesting(false)
        }
    }

    // 列表卡片上的刷新连接
    const handleRefreshConnection = async (id: string) => {
        try {
            const res = await testDataSourceConnection(id)
            if (res.success) {
                // 如果成功，重新加载列表以更新状态
                loadDataSources()
                // alert('连接正常')
            } else {
                alert(`连接失败: ${res.message}`)
            }
        } catch (err: any) {
            alert(err.message || '连接测试出错')
        }
    }

    const handleDelete = async (id: string, name: string) => {
        if (!confirm(`确定要删除数据源 "${name}" 吗？`)) return
        try {
            await deleteDataSource(id)
            setDataSources(prev => prev.filter(ds => ds.id !== id))
        } catch (err: any) {
            alert(err.message || '删除失败')
        }
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
                    // 默认状态处理
                    const status = statusConfig[source.status] || statusConfig.disconnected
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
                                            onClick={() => handleRefreshConnection(source.id)}
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
                                            onClick={() => handleDelete(source.id, source.name)}
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
                {!loading && dataSources.length === 0 && (
                    <div className="col-span-full flex flex-col items-center justify-center py-12 text-muted-foreground">
                        <Database className="h-12 w-12 mb-4 opacity-50" />
                        <p>暂无数据源，请点击右上角添加。</p>
                    </div>
                )}
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
                                    placeholder={editingSource ? "若不修改请留空" : "••••••••"}
                                />
                            </div>
                        </>
                    )}

                    <Input
                        label="描述 (可选)"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="备注信息"
                    />
                </div>

                <ModalFooter>
                    <Button variant="outline" onClick={handleTestParams} disabled={isTesting}>
                        {isTesting ? '测试中...' : '测试连接'}
                    </Button>
                    <Button variant="ghost" onClick={() => setIsModalOpen(false)}>
                        取消
                    </Button>
                    <Button variant="primary" onClick={handleSave} disabled={isSaving}>
                        {isSaving ? '保存中...' : '保存'}
                    </Button>
                </ModalFooter>
            </Modal>
        </div>
    )
}
