import { useState } from 'react'
import { Search, Filter, Clock, FileJson, FileSpreadsheet, FileCode, RotateCcw, Trash2, ChevronDown } from 'lucide-react'
import { Card, CardContent, Button, Input, Badge } from '@/components/common'
import type { HistoryRecord, ExportFormat } from '@/lib/types'

// 模拟历史记录数据
const mockHistory: HistoryRecord[] = [
    {
        id: '1',
        name: '用户注册测试数据',
        fields: [
            { id: '1', name: 'id', type: 'uuid' },
            { id: '2', name: 'name', type: 'chineseName' },
            { id: '3', name: 'email', type: 'email' },
        ],
        count: 1000,
        format: 'json',
        createdAt: '2024-07-15T10:30:00.000Z',
        projectId: '1',
    },
    {
        id: '2',
        name: '订单数据生成',
        fields: [
            { id: '1', name: 'order_id', type: 'uuid' },
            { id: '2', name: 'amount', type: 'amount' },
        ],
        count: 5000,
        format: 'csv',
        createdAt: '2024-07-14T15:20:00.000Z',
        projectId: '1',
    },
    {
        id: '3',
        name: '财务流水导入',
        fields: [
            { id: '1', name: 'transaction_id', type: 'uuid' },
            { id: '2', name: 'bank_card', type: 'bankCard' },
            { id: '3', name: 'amount', type: 'amount' },
        ],
        count: 10000,
        format: 'sql',
        createdAt: '2024-07-13T09:45:00.000Z',
        projectId: '1',
    },
    {
        id: '4',
        name: '商品信息批量生成',
        fields: [
            { id: '1', name: 'product_id', type: 'uuid' },
            { id: '2', name: 'name', type: 'word' },
            { id: '3', name: 'price', type: 'amount' },
        ],
        count: 2000,
        format: 'json',
        createdAt: '2024-07-12T14:10:00.000Z',
        projectId: '1',
    },
]

const formatIcons: Record<ExportFormat, React.ReactNode> = {
    json: <FileJson className="h-4 w-4" />,
    csv: <FileSpreadsheet className="h-4 w-4" />,
    sql: <FileCode className="h-4 w-4" />,
}

const formatColors: Record<ExportFormat, string> = {
    json: 'text-yellow-400',
    csv: 'text-green-400',
    sql: 'text-blue-400',
}

interface HistoryPageProps {
    onReuse?: (record: HistoryRecord) => void
}

export function HistoryPage({ onReuse }: HistoryPageProps) {
    const [searchQuery, setSearchQuery] = useState('')
    const [filterFormat, setFilterFormat] = useState<ExportFormat | 'all'>('all')
    const [isFilterOpen, setIsFilterOpen] = useState(false)

    const filteredHistory = mockHistory.filter((record) => {
        const matchesSearch = record.name.toLowerCase().includes(searchQuery.toLowerCase())
        const matchesFormat = filterFormat === 'all' || record.format === filterFormat
        return matchesSearch && matchesFormat
    })

    const formatDate = (dateString: string) => {
        const date = new Date(dateString)
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
                {filteredHistory.length === 0 ? (
                    <Card>
                        <CardContent className="py-12 text-center">
                            <Clock className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                            <h3 className="text-lg font-medium text-foreground">暂无历史记录</h3>
                            <p className="text-muted-foreground mt-1">生成数据后会自动记录在这里</p>
                        </CardContent>
                    </Card>
                ) : (
                    filteredHistory.map((record) => (
                        <Card key={record.id} hover>
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <h3 className="text-base font-medium text-foreground">{record.name}</h3>
                                            <Badge variant="outline" className={formatColors[record.format]}>
                                                {formatIcons[record.format]}
                                                <span className="ml-1">{record.format.toUpperCase()}</span>
                                            </Badge>
                                        </div>
                                        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                                            <span className="flex items-center gap-1">
                                                <Clock className="h-3.5 w-3.5" />
                                                {formatDate(record.createdAt)}
                                            </span>
                                            <span>生成 {record.count.toLocaleString()} 条数据</span>
                                            <span>{record.fields.length} 个字段</span>
                                        </div>
                                        <div className="flex flex-wrap gap-1 mt-2">
                                            {record.fields.slice(0, 5).map((field) => (
                                                <span key={field.id} className="text-xs bg-secondary px-2 py-0.5 rounded-full text-muted-foreground">
                                                    {field.name}
                                                </span>
                                            ))}
                                            {record.fields.length > 5 && (
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
        </div>
    )
}
