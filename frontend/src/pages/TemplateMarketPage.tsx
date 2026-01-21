import { useState, useEffect } from 'react'
import { Search, Star, Download, Grid, List, Heart, Loader2, AlertCircle, Plus, X } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, Button, Input, Badge, Tabs, TabsList, TabsTrigger } from '@/components/common'
import { cn } from '@/lib/utils'
import type { MarketTemplate, DataField } from '@/lib/types'
import { fetchMarketTemplates, createMarketTemplate, toggleTemplateFavorite } from '@/lib/api'

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
    const [showCreateModal, setShowCreateModal] = useState(false)

    const loadTemplates = async () => {
        try {
            setLoading(true)
            const data = await fetchMarketTemplates({
                category: activeCategory !== 'all' ? activeCategory : undefined,
                search: searchQuery || undefined
            })
            setTemplates(data)
            setError(null)
        } catch (err) {
            console.error('Failed to fetch templates:', err)
            setError('获取模板列表失败，请稍后重试。')
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadTemplates()
    }, [activeCategory])

    // 搜索防抖
    useEffect(() => {
        const timer = setTimeout(() => {
            if (!loading) loadTemplates()
        }, 300)
        return () => clearTimeout(timer)
    }, [searchQuery])

    const filteredTemplates = templates.filter((template) => {
        const matchesSearch = !searchQuery || 
            template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            template.description.toLowerCase().includes(searchQuery.toLowerCase())
        return matchesSearch
    })

    const toggleFavorite = async (templateId: string) => {
        try {
            const result = await toggleTemplateFavorite(templateId)
            setTemplates(prev => prev.map(t => 
                t.id === templateId ? { ...t, isFavorite: result.is_favorite } : t
            ))
        } catch (err) {
            console.error('Failed to toggle favorite:', err)
        }
    }

    const formatDownloads = (count: number) => {
        if (count >= 10000) return `${(count / 10000).toFixed(1)}万`
        if (count >= 1000) return `${(count / 1000).toFixed(1)}k`
        return count.toString()
    }

    const handleCreateTemplate = async (data: { name: string; description: string; category: string; fields: DataField[]; tags: string[] }) => {
        try {
            await createMarketTemplate(data)
            setShowCreateModal(false)
            loadTemplates()
        } catch (err) {
            console.error('Failed to create template:', err)
            throw err
        }
    }

    if (loading && templates.length === 0) {
        return (
            <div className="flex-1 flex items-center justify-center h-full">
                <div className="flex flex-col items-center gap-2 text-muted-foreground">
                    <Loader2 className="h-8 w-8 animate-spin" />
                    <p>正在加载模板市场...</p>
                </div>
            </div>
        )
    }

    if (error && templates.length === 0) {
        return (
            <div className="flex-1 flex items-center justify-center h-full p-6">
                <Card className="max-w-md w-full border-destructive/50">
                    <CardContent className="flex flex-col items-center gap-4 p-6 text-center">
                        <AlertCircle className="h-10 w-10 text-destructive" />
                        <div className="space-y-2">
                            <h3 className="font-bold">加载失败</h3>
                            <p className="text-sm text-muted-foreground">{error}</p>
                        </div>
                        <Button variant="primary" onClick={() => loadTemplates()}>
                            重试
                        </Button>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-foreground">模板市场</h1>
                    <p className="text-muted-foreground">发现和使用团队共享的数据模板</p>
                </div>
                <Button variant="primary" onClick={() => setShowCreateModal(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    创建模板
                </Button>
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
                    <Button variant="ghost" className="mt-2" onClick={() => setShowCreateModal(true)}>
                        创建第一个模板
                    </Button>
                </div>
            ) : viewMode === 'grid' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {filteredTemplates.map((template) => (
                        <Card key={template.id} hover className="group">
                            <CardContent className="p-4">
                                <div className="flex items-start justify-between mb-3">
                                    <div>
                                        <h3 className="text-base font-semibold text-foreground">{template.name}</h3>
                                        <p className="text-xs text-muted-foreground mt-0.5">by {template.author?.name || '系统'}</p>
                                    </div>
                                    <button
                                        onClick={() => toggleFavorite(template.id)}
                                        className="p-1 rounded hover:bg-secondary transition-colors"
                                    >
                                        <Heart
                                            className={cn(
                                                'h-5 w-5',
                                                template.isFavorite ? 'fill-red-500 text-red-500' : 'text-muted-foreground'
                                            )}
                                        />
                                    </button>
                                </div>

                                <p className="text-sm text-muted-foreground line-clamp-2 mb-3 h-10">
                                    {template.description || '暂无描述'}
                                </p>

                                <div className="flex flex-wrap gap-1 mb-3 h-6 overflow-hidden">
                                    {template.tags?.map((tag) => (
                                        <Badge key={tag} variant="outline" className="text-xs">
                                            {tag}
                                        </Badge>
                                    ))}
                                </div>

                                <div className="flex items-center justify-between pt-3 border-t border-border">
                                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                        <span className="flex items-center gap-1">
                                            <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                                            {template.rating?.toFixed(1) || '0.0'}
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Download className="h-4 w-4" />
                                            {formatDownloads(template.downloads || 0)}
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
                                                    template.isFavorite ? 'fill-red-500 text-red-500' : 'text-muted-foreground'
                                                )}
                                            />
                                        </button>
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2">
                                                <h3 className="text-base font-semibold text-foreground">{template.name}</h3>
                                                <span className="text-xs text-muted-foreground">by {template.author?.name || '系统'}</span>
                                            </div>
                                            <p className="text-sm text-muted-foreground mt-0.5">{template.description || '暂无描述'}</p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-6">
                                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                                            <span className="flex items-center gap-1">
                                                <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                                                {template.rating?.toFixed(1) || '0.0'}
                                            </span>
                                            <span className="flex items-center gap-1">
                                                <Download className="h-4 w-4" />
                                                {formatDownloads(template.downloads || 0)}
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

            {/* 创建模板弹窗 */}
            {showCreateModal && (
                <CreateTemplateModal
                    onClose={() => setShowCreateModal(false)}
                    onSubmit={handleCreateTemplate}
                />
            )}
        </div>
    )
}

// 创建模板弹窗组件
interface CreateTemplateModalProps {
    onClose: () => void
    onSubmit: (data: { name: string; description: string; category: string; fields: DataField[]; tags: string[] }) => Promise<void>
}

function CreateTemplateModal({ onClose, onSubmit }: CreateTemplateModalProps) {
    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [category, setCategory] = useState('other')
    const [tagsInput, setTagsInput] = useState('')
    const [fields, setFields] = useState<DataField[]>([
        { id: '1', name: '', type: 'string' }
    ])
    const [submitting, setSubmitting] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const dataTypes = [
        { id: 'string', name: '字符串' },
        { id: 'integer', name: '整数' },
        { id: 'float', name: '浮点数' },
        { id: 'boolean', name: '布尔值' },
        { id: 'uuid', name: 'UUID' },
        { id: 'email', name: '邮箱' },
        { id: 'chineseName', name: '中文姓名' },
        { id: 'chinesePhone', name: '手机号' },
        { id: 'chineseAddress', name: '中文地址' },
        { id: 'date', name: '日期' },
        { id: 'datetime', name: '日期时间' },
        { id: 'amount', name: '金额' },
        { id: 'bankCard', name: '银行卡号' },
    ]

    const addField = () => {
        setFields([...fields, { id: String(Date.now()), name: '', type: 'string' }])
    }

    const removeField = (id: string) => {
        if (fields.length > 1) {
            setFields(fields.filter(f => f.id !== id))
        }
    }

    const updateField = (id: string, key: keyof DataField, value: string) => {
        setFields(fields.map(f => f.id === id ? { ...f, [key]: value } : f))
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        
        if (!name.trim()) {
            setError('请输入模板名称')
            return
        }
        
        const validFields = fields.filter(f => f.name.trim())
        if (validFields.length === 0) {
            setError('请至少添加一个字段')
            return
        }

        const tags = tagsInput.split(/[,，\s]+/).filter(t => t.trim())

        try {
            setSubmitting(true)
            setError(null)
            await onSubmit({
                name: name.trim(),
                description: description.trim(),
                category,
                fields: validFields,
                tags
            })
        } catch (err: any) {
            setError(err.message || '创建失败')
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-2xl max-h-[90vh] overflow-auto">
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle>创建模板</CardTitle>
                    <button onClick={onClose} className="p-1 rounded hover:bg-secondary">
                        <X className="h-5 w-5" />
                    </button>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {error && (
                            <div className="p-3 bg-destructive/10 border border-destructive/30 rounded-lg text-sm text-destructive">
                                {error}
                            </div>
                        )}

                        <div>
                            <label className="block text-sm font-medium mb-1">模板名称 *</label>
                            <Input
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="例如：用户注册数据"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium mb-1">描述</label>
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                placeholder="模板用途说明..."
                                className="w-full px-3 py-2 border border-border rounded-lg bg-background text-foreground resize-none h-20"
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium mb-1">分类</label>
                                <select
                                    value={category}
                                    onChange={(e) => setCategory(e.target.value)}
                                    className="w-full px-3 py-2 border border-border rounded-lg bg-background text-foreground"
                                >
                                    {categories.filter(c => c.id !== 'all').map(cat => (
                                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium mb-1">标签</label>
                                <Input
                                    value={tagsInput}
                                    onChange={(e) => setTagsInput(e.target.value)}
                                    placeholder="用逗号分隔，如：用户,注册"
                                />
                            </div>
                        </div>

                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <label className="block text-sm font-medium">字段配置 *</label>
                                <Button type="button" size="sm" variant="ghost" onClick={addField}>
                                    <Plus className="h-4 w-4 mr-1" />
                                    添加字段
                                </Button>
                            </div>
                            <div className="space-y-2 max-h-60 overflow-auto">
                                {fields.map((field, index) => (
                                    <div key={field.id} className="flex items-center gap-2">
                                        <span className="text-xs text-muted-foreground w-6">{index + 1}</span>
                                        <Input
                                            value={field.name}
                                            onChange={(e) => updateField(field.id, 'name', e.target.value)}
                                            placeholder="字段名"
                                            className="flex-1"
                                        />
                                        <select
                                            value={field.type}
                                            onChange={(e) => updateField(field.id, 'type', e.target.value)}
                                            className="px-3 py-2 border border-border rounded-lg bg-background text-foreground w-32"
                                        >
                                            {dataTypes.map(dt => (
                                                <option key={dt.id} value={dt.id}>{dt.name}</option>
                                            ))}
                                        </select>
                                        <button
                                            type="button"
                                            onClick={() => removeField(field.id)}
                                            className="p-2 text-muted-foreground hover:text-destructive"
                                            disabled={fields.length === 1}
                                        >
                                            <X className="h-4 w-4" />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="flex justify-end gap-2 pt-4 border-t">
                            <Button type="button" variant="ghost" onClick={onClose}>
                                取消
                            </Button>
                            <Button type="submit" variant="primary" disabled={submitting}>
                                {submitting ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                                创建模板
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
