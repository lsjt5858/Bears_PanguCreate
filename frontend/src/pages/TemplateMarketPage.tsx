import { useState } from 'react'
import { Search, Star, Download, Grid, List, Heart } from 'lucide-react'
import { Card, CardContent, Button, Input, Badge, Tabs, TabsList, TabsTrigger } from '@/components/common'
import { cn } from '@/lib/utils'
import type { MarketTemplate } from '@/lib/types'

// 模拟模板市场数据
const mockMarketTemplates: MarketTemplate[] = [
    {
        id: '1',
        name: '用户注册数据',
        description: '包含用户注册所需的完整字段，适用于用户系统测试',
        category: 'user',
        fields: [],
        createdAt: '',
        updatedAt: '',
        author: { id: '1', name: '官方', email: '', role: 'admin', createdAt: '' },
        downloads: 12340,
        rating: 4.8,
        ratingCount: 256,
        isFavorite: true,
        tags: ['用户', '注册', '基础'],
    },
    {
        id: '2',
        name: '电商订单数据',
        description: '电商平台订单测试数据，包含订单、用户、商品关联',
        category: 'order',
        fields: [],
        createdAt: '',
        updatedAt: '',
        author: { id: '2', name: '测试团队', email: '', role: 'lead', createdAt: '' },
        downloads: 8920,
        rating: 4.6,
        ratingCount: 189,
        isFavorite: false,
        tags: ['订单', '电商', '交易'],
    },
    {
        id: '3',
        name: '财务流水记录',
        description: '银行/支付系统的财务流水数据，包含账户、交易信息',
        category: 'finance',
        fields: [],
        createdAt: '',
        updatedAt: '',
        author: { id: '1', name: '官方', email: '', role: 'admin', createdAt: '' },
        downloads: 6780,
        rating: 4.9,
        ratingCount: 312,
        isFavorite: true,
        tags: ['财务', '银行', '流水'],
    },
    {
        id: '4',
        name: '商品信息数据',
        description: '商品基础信息测试数据，适用于商品管理系统',
        category: 'product',
        fields: [],
        createdAt: '',
        updatedAt: '',
        author: { id: '3', name: '社区贡献', email: '', role: 'member', createdAt: '' },
        downloads: 5430,
        rating: 4.4,
        ratingCount: 98,
        isFavorite: false,
        tags: ['商品', 'SKU', '库存'],
    },
    {
        id: '5',
        name: '员工信息数据',
        description: '企业员工信息测试数据，支持HR系统测试',
        category: 'user',
        fields: [],
        createdAt: '',
        updatedAt: '',
        author: { id: '2', name: '测试团队', email: '', role: 'lead', createdAt: '' },
        downloads: 4210,
        rating: 4.3,
        ratingCount: 67,
        isFavorite: false,
        tags: ['员工', 'HR', '企业'],
    },
    {
        id: '6',
        name: '地址信息数据',
        description: '中国省市区地址数据，支持完整的地址体系',
        category: 'address',
        fields: [],
        createdAt: '',
        updatedAt: '',
        author: { id: '1', name: '官方', email: '', role: 'admin', createdAt: '' },
        downloads: 7890,
        rating: 4.7,
        ratingCount: 234,
        isFavorite: false,
        tags: ['地址', '省市区', '物流'],
    },
]

const categories = [
    { id: 'all', name: '全部' },
    { id: 'user', name: '用户相关' },
    { id: 'order', name: '订单交易' },
    { id: 'finance', name: '财务金融' },
    { id: 'product', name: '商品信息' },
    { id: 'address', name: '地址物流' },
]

interface TemplateMarketPageProps {
    onUseTemplate?: (template: MarketTemplate) => void
}

export function TemplateMarketPage({ onUseTemplate }: TemplateMarketPageProps) {
    const [searchQuery, setSearchQuery] = useState('')
    const [activeCategory, setActiveCategory] = useState('all')
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
    const [favorites, setFavorites] = useState<Set<string>>(
        new Set(mockMarketTemplates.filter(t => t.isFavorite).map(t => t.id))
    )

    const filteredTemplates = mockMarketTemplates.filter((template) => {
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
                            {categories.slice(0, 4).map((cat) => (
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
            {viewMode === 'grid' ? (
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

                                <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                                    {template.description}
                                </p>

                                <div className="flex flex-wrap gap-1 mb-3">
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
                                            <p className="text-sm text-muted-foreground mt-0.5">{template.description}</p>
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
