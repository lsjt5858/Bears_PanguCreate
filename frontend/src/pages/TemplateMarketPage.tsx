import { useState, useEffect } from 'react'
import { Search, Star, Download, Grid, List, Heart, Loader2, AlertCircle } from 'lucide-react'
import { Card, CardContent, Button, Input, Badge, Tabs, TabsList, TabsTrigger } from '@/components/common'
import { cn } from '@/lib/utils'
import type { MarketTemplate, Template } from '@/lib/types'
import { fetchTemplates } from '@/lib/api'

// 辅助函数：将基础模板转换为市场模板（填充缺失数据）
const adaptToMarketTemplate = (template: Template): MarketTemplate => {
    // 确定标签
    const tags = [template.category]
    if (template.name.includes('用户')) tags.push('用户')
    if (template.name.includes('订单')) tags.push('交易')
    if (template.name.includes('商品')) tags.push('商品')

    // 生成伪随机数据用于演示（因为后端尚不支持这些字段）
    const seed = template.id.charCodeAt(0) || 0
    const downloads = 100 + (seed * 50) % 5000
    const rating = 4.0 + (seed % 10) / 10
    const ratingCount = 10 + (seed * 2) % 200

    return {
        ...template,
        author: {
            id: 'system',
            name: '系统默认',
            email: 'admin@bears.com',
            role: 'admin',
            createdAt: new Date().toISOString()
        },
        downloads,
        rating: Number(rating.toFixed(1)),
        ratingCount,
        isFavorite: false,
        tags
    }
}

const categories = [
    { id: 'all', name: '全部' },
    { id: 'user', name: '用户相关' },
    { id: 'order', name: '订单交易' },
    { id: 'finance', name: '财务金融' },
    { id: 'product', name: '商品信息' },
    { id: 'address', name: '地址物流' },
    { id: 'other', name: '其他' },
]

interface TemplateMarketPageProps {
    onUseTemplate?: (template: MarketTemplate) => void
}

export function TemplateMarketPage({ onUseTemplate }: TemplateMarketPageProps) {
    const [templates, setTemplates] = useState<MarketTemplate[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    const [searchQuery, setSearchQuery] = useState('')
    const [activeCategory, setActiveCategory] = useState('all')
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
    const [favorites, setFavorites] = useState<Set<string>>(new Set())

    useEffect(() => {
        const loadTemplates = async () => {
            try {
                setLoading(true)
                const data = await fetchTemplates()
                // 转换后端基础模板为市场模板格式
                const marketTemplates = data.map(adaptToMarketTemplate)
                setTemplates(marketTemplates)
                setError(null)
            } catch (err) {
                console.error('Failed to fetch templates:', err)
                setError('获取模板列表失败，请稍后重试。')
            } finally {
                setLoading(false)
            }
        }
        loadTemplates()
    }, [])

    const filteredTemplates = templates.filter((template) => {
        const matchesSearch = template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            template.description.toLowerCase().includes(searchQuery.toLowerCase())
        const matchesCategory = activeCategory === 'all' || template.category === activeCategory
        return matchesSearch && matchesCategory
    })

    const toggleFavorite = (templateId: string) => {
        setFavorites(prev => {
            const next = new Set(prev)
            if (next.has(templateId)) {
                next.delete(templateId)
            } else {
                next.add(templateId)
            }
            return next
        })
    }

    const formatDownloads = (count: number) => {
        if (count >= 10000) return `${(count / 10000).toFixed(1)}万`
        if (count >= 1000) return `${(count / 1000).toFixed(1)}k`
        return count.toString()
    }

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center h-full">
                <div className="flex flex-col items-center gap-2 text-muted-foreground">
                    <Loader2 className="h-8 w-8 animate-spin" />
                    <p>正在加载模板市场...</p>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="flex-1 flex items-center justify-center h-full p-6">
                <Card className="max-w-md w-full border-destructive/50">
                    <CardContent className="flex flex-col items-center gap-4 p-6 text-center">
                        <AlertCircle className="h-10 w-10 text-destructive" />
                        <div className="space-y-2">
                            <h3 className="font-bold">加载失败</h3>
                            <p className="text-sm text-muted-foreground">{error}</p>
                        </div>
                        <Button
                            variant="primary"
                            onClick={() => window.location.reload()}
                        >
                            重试
                        </Button>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-foreground">模板市场</h1>
                <p className="text-muted-foreground">发现和使用团队共享的数据模板</p>
            </div>

            {/* 搜索和筛选 */}
            <div className="flex flex-col lg:flex-row gap-4 mb-6">
                <div className="flex-1">
                    <Input
                        placeholder="搜索模板..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        leftIcon={<Search className="h-4 w-4" />}
                    />
                </div>
                <div className="flex items-center gap-2">
                    <Tabs value={activeCategory} onChange={setActiveCategory}>
                        <TabsList>
                            {categories.map((cat) => (
                                <TabsTrigger key={cat.id} value={cat.id}>
                                    {cat.name}
                                </TabsTrigger>
                            ))}
                        </TabsList>
                    </Tabs>
                    <div className="flex items-center border border-border rounded-lg p-1">
                        <button
                            onClick={() => setViewMode('grid')}
                            className={cn(
                                'p-1.5 rounded',
                                viewMode === 'grid' ? 'bg-secondary text-foreground' : 'text-muted-foreground'
                            )}
                        >
                            <Grid className="h-4 w-4" />
                        </button>
                        <button
                            onClick={() => setViewMode('list')}
                            className={cn(
                                'p-1.5 rounded',
                                viewMode === 'list' ? 'bg-secondary text-foreground' : 'text-muted-foreground'
                            )}
                        >
                            <List className="h-4 w-4" />
                        </button>
                    </div>
                </div>
            </div>

            {/* 模板列表 */}
            {filteredTemplates.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-64 text-muted-foreground">
                    <p>没有找到匹配的模板</p>
                </div>
            ) : viewMode === 'grid' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filteredTemplates.map((template) => (
                        <Card key={template.id} hover className="group">
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <h3 className="text-base font-semibold text-foreground">{template.name}</h3>
                                        <p className="text-xs text-muted-foreground mt-0.5">by {template.author.name}</p>
                                    </div>
                                    <button
                                        onClick={() => toggleFavorite(template.id)}
                                        className="p-1 rounded hover:bg-secondary transition-colors"
                                    >
                                        <Heart
                                            className={cn(
                                                'h-5 w-5',
                                                favorites.has(template.id) ? 'fill-red-500 text-red-500' : 'text-muted-foreground'
                                            )}
                                        />
                                    </button>
                                </div>

                                <p className="text-sm text-muted-foreground line-clamp-2 mb-3 h-10">
                                    {template.description || '暂无描述'}
                                </p>

                                <div className="flex flex-wrap gap-1 mb-3 h-6 overflow-hidden">
                                    {template.tags.map((tag) => (
                                        <Badge key={tag} variant="outline" className="text-xs">
                                            {tag}
                                        </Badge>
                                    ))}
                                </div>

                                <div className="flex items-center justify-between pt-3 border-t border-border">
                                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                        <span className="flex items-center gap-1">
                                            <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                                            {template.rating}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Download className="h-4 w-4" />
                                            {formatDownloads(template.downloads)}
                                        </span>
                                    </div>
                                    <Button
                                        size="sm"
                                        variant="primary"
                                        onClick={() => onUseTemplate?.(template)}
                                    >
                                        使用
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className="space-y-3">
                    {filteredTemplates.map((template) => (
                        <Card key={template.id} hover>
                            <CardContent className="p-4">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-4 flex-1">
                                        <button
                                            onClick={() => toggleFavorite(template.id)}
                                            className="p-1 rounded hover:bg-secondary transition-colors"
                                        >
                                            <Heart
                                                className={cn(
                                                    'h-5 w-5',
                                                    favorites.has(template.id) ? 'fill-red-500 text-red-500' : 'text-muted-foreground'
                                                )}
                                            />
                                        </button>
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2">
                                                <h3 className="text-base font-semibold text-foreground">{template.name}</h3>
                                                <span className="text-xs text-muted-foreground">by {template.author.name}</span>
                                            </div>
                                            <p className="text-sm text-muted-foreground mt-0.5">{template.description || '暂无描述'}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-6">
                                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                            <span className="flex items-center gap-1">
                                                <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                                                {template.rating}
                                            </span>
                                            <span className="flex items-center gap-1">
                                                <Download className="h-4 w-4" />
                                                {formatDownloads(template.downloads)}
                                            </span>
                                        </div>
                                        <Button
                                            size="sm"
                                            variant="primary"
                                            onClick={() => onUseTemplate?.(template)}
                                        >
                                            使用模板
                                        </Button>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    )
}
