import { useState, useEffect } from 'react'
import { Search, Filter, Clock, FileJson, FileSpreadsheet, FileCode, RotateCcw, Trash2, ChevronDown, Loader2 } from 'lucide-react'
import { Card, CardContent, Button, Input, Badge } from '@/components/common'
import type { HistoryRecord, ExportFormat } from '@/lib/types'
import { fetchHistory, deleteHistory } from '@/lib/api'
import { useAuth } from '@/context/AuthContext'

const formatIcons: Record<string, React.ReactNode> = {
    json: <FileJson className="h-4 w-4" />,
    csv: <FileSpreadsheet className="h-4 w-4" />,
    sql: <FileCode className="h-4 w-4" />,
}

const formatColors: Record<string, string> = {
    json: 'text-yellow-400',
    csv: 'text-green-400',
    sql: 'text-blue-400',
}

interface HistoryPageProps {
    onReuse?: (record: HistoryRecord) => void
}

export function HistoryPage({ onReuse }: HistoryPageProps) {
    const { isAuthenticated } = useAuth()
    const [history, setHistory] = useState<HistoryRecord[]>([])
    const [loading, setLoading] = useState(false)
    const [searchQuery, setSearchQuery] = useState('')
    const [filterFormat, setFilterFormat] = useState<ExportFormat | 'all'>('all')
    const [isFilterOpen, setIsFilterOpen] = useState(false)
    const [page, setPage] = useState(1)
    const [total, setTotal] = useState(0)

    const loadHistory = async () => {
        if (!isAuthenticated) return

        setLoading(true)
        try {
            const res = await fetchHistory({
                page,
                page_size: 20,
                search: searchQuery,
                format: filterFormat === 'all' ? undefined : filterFormat
            })

            // Map backend data to HistoryRecord
            const mappedHistory: HistoryRecord[] = res.data.map((item: any) => ({
                id: item.id.toString(),
                name: item.name,
                fields: item.fields,
                count: item.row_count, // map row_count to count
                format: item.export_format as ExportFormat, // map export_format to format
                createdAt: item.created_at || new Date().toISOString(),
                projectId: item.project_id?.toString() || ''
            }))

            setHistory(mappedHistory)
            setTotal(res.pagination.total)
        } catch (error) {
            console.error('Failed to load history:', error)
        } finally {
            setLoading(false)
        }
    }

    // Load history on mount and when params change
    useEffect(() => {
        loadHistory()
    }, [isAuthenticated, page, filterFormat])

    // Handle search with debounce could be better, but simple effect is okay for small scale
    useEffect(() => {
        const timer = setTimeout(() => {
            setPage(1) // reset to page 1 on search
            loadHistory()
        }, 500)
        return () => clearTimeout(timer)
    }, [searchQuery])

    const handleDelete = async (id: string) => {
        if (!confirm('确定要删除这条记录吗？')) return
        try {
            await deleteHistory(id)
            // Remove from local state
            setHistory(prev => prev.filter(item => item.id !== id))
            setTotal(prev => prev - 1)
        } catch (error) {
            console.error('Failed to delete history:', error)
            alert('删除失败')
        }
    }

    const formatDate = (dateString: string) => {
        // 后端返回的是 UTC 时间（ISO 格式），需要正确解析
        // 如果没有时区信息，添加 Z 表示 UTC
        let isoString = dateString
        if (!dateString.endsWith('Z') && !dateString.includes('+')) {
            isoString = dateString + 'Z'
        }
        
        const date = new Date(isoString)
        const now = new Date()
        const diffMs = now.getTime() - date.getTime()
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

        if (diffDays === 0) {
            return `今天 ${date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
        } else if (diffDays === 1) {
            return `昨天 ${date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
        } else if (diffDays < 7) {
            return `${diffDays}天前`
        } else {
            return date.toLocaleDateString('zh-CN')
        }
    }

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-foreground">历史记录</h1>
                <p className="text-muted-foreground">查看和管理数据生成历史</p>
            </div>

            {/* 搜索和筛选 */}
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
                <div className="flex-1">
                    <Input
                        placeholder="搜索历史记录..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        leftIcon={<Search className="h-4 w-4" />}
                    />
                </div>
                <div className="relative">
                    <Button
                        variant="outline"
                        onClick={() => setIsFilterOpen(!isFilterOpen)}
                        className="w-full sm:w-auto"
                    >
                        <Filter className="h-4 w-4" />
                        筛选
                        <ChevronDown className={`h-4 w-4 transition-transform ${isFilterOpen ? 'rotate-180' : ''}`} />
                    </Button>
                    {isFilterOpen && (
                        <div className="absolute right-0 top-full mt-2 w-48 rounded-lg border border-border bg-card shadow-lg p-2 z-10">
                            <p className="text-xs text-muted-foreground px-2 py-1">导出格式</p>
                            {(['all', 'json', 'csv', 'sql'] as const).map((format) => (
                                <button
                                    key={format}
                                    onClick={() => {
                                        setFilterFormat(format)
                                        setPage(1)
                                        setIsFilterOpen(false)
                                    }}
                                    className={`flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-sm ${filterFormat === format ? 'bg-secondary text-foreground' : 'text-muted-foreground hover:bg-secondary/50'
                                        }`}
                                >
                                    {format === 'all' ? '全部' : format.toUpperCase()}
                                </button>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* 历史记录列表 */}
            <div className="space-y-4">
                {loading && history.length === 0 ? (
                    <div className="py-12 text-center">
                        <Loader2 className="h-8 w-8 animate-spin mx-auto text-primary" />
                        <p className="text-muted-foreground mt-2">加载中...</p>
                    </div>
                ) : history.length === 0 ? (
                    <Card>
                        <CardContent className="py-12 text-center">
                            <Clock className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-foreground">暂无历史记录</h3>
                            <p className="text-muted-foreground mt-1">生成数据后会自动记录在这里</p>
                        </CardContent>
                    </Card>
                ) : (
                    history.map((record) => (
                        <Card key={record.id} hover>
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <h3 className="text-base font-medium text-foreground">{record.name}</h3>
                                            <Badge variant="outline" className={formatColors[record.format] || 'text-gray-400'}>
                                                {formatIcons[record.format]}
                                                <span className="ml-1">{record.format ? record.format.toUpperCase() : 'UNKNOWN'}</span>
                                            </Badge>
                                        </div>
                                        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                                            <span className="flex items-center gap-1">
                                                <Clock className="h-3.5 w-3.5" />
                                                {formatDate(record.createdAt)}
                                            </span>
                                            <span>生成 {record.count.toLocaleString()} 条数据</span>
                                            <span>{record.fields ? record.fields.length : 0} 个字段</span>
                                        </div>
                                        <div className="flex flex-wrap gap-1 mt-2">
                                            {record.fields && record.fields.slice(0, 5).map((field) => (
                                                <span key={field.id} className="text-xs bg-secondary px-2 py-0.5 rounded-full text-muted-foreground">
                                                    {field.name}
                                                </span>
                                            ))}
                                            {record.fields && record.fields.length > 5 && (
                                                <span className="text-xs bg-secondary px-2 py-0.5 rounded-full text-muted-foreground">
                                                    +{record.fields.length - 5}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2 ml-4">
                                        <Button
                                            variant="ghost"
                                            size="sm"
                                            onClick={() => onReuse?.(record)}
                                            title="复用配置"
                                        >
                                            <RotateCcw className="h-4 w-4" />
                                            复用
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            className="text-muted-foreground hover:text-destructive"
                                            title="删除"
                                            onClick={() => handleDelete(record.id)}
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>

            {/* 简单的分页加载更多 (可选) */}
            {total > history.length && !loading && (
                <div className="mt-4 text-center">
                    <Button variant="outline" onClick={() => setPage(p => p + 1)}>
                        加载更多
                    </Button>
                </div>
            )}
        </div>
    )
}
