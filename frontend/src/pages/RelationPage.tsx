import { useState } from 'react'
import {
    Plus,
    Trash2,
    ArrowRight,
    Play,
    Table,
    Key,
    Link2
} from 'lucide-react'
import { Card, CardContent, CardHeader, Button, Input, Select, Badge, Modal, ModalFooter, Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/common'
import type { RelationTable, TableRelation, RelationType, DataField } from '@/lib/types'
import { generateRelationData } from '@/lib/api'

// 模拟数据类型
const dataTypeOptions = [
    { value: 'uuid', label: 'UUID' },
    { value: 'chineseName', label: '中文姓名' },
    { value: 'email', label: '邮箱' },
    { value: 'chinesePhone', label: '手机号' },
    { value: 'amount', label: '金额' },
    { value: 'datetime', label: '日期时间' },
    { value: 'number', label: '数字' },
    { value: 'string', label: '字符串' },
]

const relationTypeOptions: { value: RelationType; label: string }[] = [
    { value: 'one-to-one', label: '一对一' },
    { value: 'one-to-many', label: '一对多' },
    { value: 'many-to-many', label: '多对多' },
]

// 初始表结构
const initialTables: RelationTable[] = [
    {
        id: 't1',
        name: 'users',
        fields: [
            { id: 'f1-1', name: 'id', type: 'uuid' },
            { id: 'f1-2', name: 'name', type: 'chineseName' },
            { id: 'f1-3', name: 'email', type: 'email' },
        ],
        count: 100,
    },
    {
        id: 't2',
        name: 'orders',
        fields: [
            { id: 'f2-1', name: 'id', type: 'uuid' },
            { id: 'f2-2', name: 'user_id', type: 'uuid' },
            { id: 'f2-3', name: 'amount', type: 'amount' },
            { id: 'f2-4', name: 'created_at', type: 'datetime' },
        ],
        count: 500,
    },
]

const initialRelations: TableRelation[] = [
    {
        id: 'r1',
        sourceTable: 'users',
        sourceColumn: 'id',
        targetTable: 'orders',
        targetColumn: 'user_id',
        relationType: 'one-to-many',
    },
]

export function RelationPage() {
    const [tables, setTables] = useState<RelationTable[]>(initialTables)
    const [relations, setRelations] = useState<TableRelation[]>(initialRelations)
    const [isGenerating, setIsGenerating] = useState(false)
    const [generatedData, setGeneratedData] = useState<Record<string, any[]> | null>(null)
    const [isResultModalOpen, setIsResultModalOpen] = useState(false)
    const [activeResultTab, setActiveResultTab] = useState<string>('')

    const addTable = () => {
        const newTable: RelationTable = {
            id: `t${Date.now()}`,
            name: `table_${tables.length + 1}`,
            fields: [
                { id: `f${Date.now()}-1`, name: 'id', type: 'uuid' },
            ],
            count: 100,
        }
        setTables([...tables, newTable])
    }

    const removeTable = (tableId: string) => {
        setTables(tables.filter(t => t.id !== tableId))
        // 移除相关的关系
        const tableName = tables.find(t => t.id === tableId)?.name
        if (tableName) {
            setRelations(relations.filter(r => r.sourceTable !== tableName && r.targetTable !== tableName))
        }
    }

    const addField = (tableId: string) => {
        setTables(tables.map(t => {
            if (t.id === tableId) {
                return {
                    ...t,
                    fields: [...t.fields, { id: `f${Date.now()}`, name: `field_${t.fields.length + 1}`, type: 'string' }],
                }
            }
            return t
        }))
    }

    const removeField = (tableId: string, fieldId: string) => {
        setTables(tables.map(t => {
            if (t.id === tableId) {
                return {
                    ...t,
                    fields: t.fields.filter(f => f.id !== fieldId),
                }
            }
            return t
        }))
    }

    const updateField = (tableId: string, fieldId: string, updates: Partial<DataField>) => {
        setTables(tables.map(t => {
            if (t.id === tableId) {
                return {
                    ...t,
                    fields: t.fields.map(f => f.id === fieldId ? { ...f, ...updates } : f),
                }
            }
            return t
        }))
    }

    const updateTableName = (tableId: string, name: string) => {
        const oldName = tables.find(t => t.id === tableId)?.name
        setTables(tables.map(t => t.id === tableId ? { ...t, name } : t))
        // 更新关系中的表名
        if (oldName) {
            setRelations(relations.map(r => ({
                ...r,
                sourceTable: r.sourceTable === oldName ? name : r.sourceTable,
                targetTable: r.targetTable === oldName ? name : r.targetTable,
            })))
        }
    }

    const updateTableCount = (tableId: string, count: number) => {
        setTables(tables.map(t => t.id === tableId ? { ...t, count } : t))
    }

    const addRelation = () => {
        if (tables.length < 2) return
        const newRelation: TableRelation = {
            id: `r${Date.now()}`,
            sourceTable: tables[0].name,
            sourceColumn: tables[0].fields[0]?.name || 'id',
            targetTable: tables[1].name,
            targetColumn: tables[1].fields[0]?.name || 'id',
            relationType: 'one-to-many',
        }
        setRelations([...relations, newRelation])
    }

    const removeRelation = (relationId: string) => {
        setRelations(relations.filter(r => r.id !== relationId))
    }

    const updateRelation = (relationId: string, updates: Partial<TableRelation>) => {
        setRelations(relations.map(r => r.id === relationId ? { ...r, ...updates } : r))
    }

    const handleGenerate = async () => {
        if (tables.length === 0) return

        setIsGenerating(true)
        try {
            const data = await generateRelationData(tables, relations)
            setGeneratedData(data)
            if (Object.keys(data).length > 0) {
                setActiveResultTab(Object.keys(data)[0])
            }
            setIsResultModalOpen(true)
        } catch (error: any) {
            alert(error.message || '生成关联数据失败')
        } finally {
            setIsGenerating(false)
        }
    }

    const downloadJson = (tableName: string) => {
        if (!generatedData || !generatedData[tableName]) return
        const blob = new Blob([JSON.stringify(generatedData[tableName], null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${tableName}.json`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
    }

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h1 className="text-2xl font-bold text-foreground">关联数据生成</h1>
                    <p className="text-muted-foreground">配置表结构和关系，生成符合外键约束的多表数据</p>
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="outline" onClick={addTable}>
                        <Plus className="h-4 w-4" />
                        添加表
                    </Button>
                    <Button
                        variant="primary"
                        onClick={handleGenerate}
                        disabled={isGenerating || tables.length === 0}
                    >
                        <Play className="h-4 w-4" />
                        {isGenerating ? '生成中...' : '生成数据'}
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* 表结构配置 */}
                <div className="space-y-4">
                    <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
                        <Table className="h-5 w-5 text-primary" />
                        表结构
                    </h2>

                    {tables.map((table) => (
                        <Card key={table.id}>
                            <CardHeader className="pb-2">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <Input
                                            value={table.name}
                                            onChange={(e) => updateTableName(table.id, e.target.value)}
                                            className="w-40 font-mono"
                                        />
                                        <Badge variant="outline">
                                            {table.count} 条
                                        </Badge>
                                    </div>
                                    <div className="flex items-center gap-1">
                                        <Input
                                            type="number"
                                            value={table.count}
                                            onChange={(e) => updateTableCount(table.id, parseInt(e.target.value) || 1)}
                                            className="w-20 text-center"
                                            min={1}
                                            max={10000}
                                        />
                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={() => removeTable(table.id)}
                                            className="text-muted-foreground hover:text-destructive"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            </CardHeader>
                            <CardContent className="pt-2">
                                <div className="space-y-2">
                                    {table.fields.map((field, index) => (
                                        <div key={field.id} className="flex items-center gap-2">
                                            {index === 0 && <Key className="h-4 w-4 text-yellow-400" />}
                                            {index !== 0 && <div className="w-4" />}
                                            <Input
                                                value={field.name}
                                                onChange={(e) => updateField(table.id, field.id, { name: e.target.value })}
                                                className="flex-1 font-mono text-sm"
                                                placeholder="字段名"
                                            />
                                            <Select
                                                value={field.type}
                                                onChange={(value) => updateField(table.id, field.id, { type: value })}
                                                options={dataTypeOptions}
                                                className="w-32"
                                            />
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => removeField(table.id, field.id)}
                                                disabled={table.fields.length === 1}
                                                className="text-muted-foreground hover:text-destructive"
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    ))}
                                </div>
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => addField(table.id)}
                                    className="mt-2 w-full"
                                >
                                    <Plus className="h-4 w-4" />
                                    添加字段
                                </Button>
                            </CardContent>
                        </Card>
                    ))}

                    {tables.length === 0 && (
                        <Card>
                            <CardContent className="py-12 text-center">
                                <Table className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                                <h3 className="text-lg font-medium text-foreground">暂无表结构</h3>
                                <p className="text-muted-foreground mt-1">点击"添加表"开始配置</p>
                            </CardContent>
                        </Card>
                    )}
                </div>

                {/* 表关系配置 */}
                <div className="space-y-4">
                    <div className="flex items-center justify-between">
                        <h2 className="text-lg font-semibold text-foreground flex items-center gap-2">
                            <Link2 className="h-5 w-5 text-primary" />
                            表关系
                        </h2>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={addRelation}
                            disabled={tables.length < 2}
                        >
                            <Plus className="h-4 w-4" />
                            添加关系
                        </Button>
                    </div>

                    {relations.map((relation) => {
                        const sourceTable = tables.find(t => t.name === relation.sourceTable)
                        const targetTable = tables.find(t => t.name === relation.targetTable)

                        return (
                            <Card key={relation.id}>
                                <CardContent className="p-4">
                                    <div className="flex items-center gap-4">
                                        {/* 源表 */}
                                        <div className="flex-1 space-y-2">
                                            <Select
                                                value={relation.sourceTable}
                                                onChange={(value) => updateRelation(relation.id, { sourceTable: value })}
                                                options={tables.map(t => ({ value: t.name, label: t.name }))}
                                                label="源表"
                                            />
                                            <Select
                                                value={relation.sourceColumn}
                                                onChange={(value) => updateRelation(relation.id, { sourceColumn: value })}
                                                options={sourceTable?.fields.map(f => ({ value: f.name, label: f.name })) || []}
                                                label="源字段"
                                            />
                                        </div>

                                        {/* 关系类型 */}
                                        <div className="flex flex-col items-center gap-2">
                                            <ArrowRight className="h-5 w-5 text-primary" />
                                            <Select
                                                value={relation.relationType}
                                                onChange={(value) => updateRelation(relation.id, { relationType: value as RelationType })}
                                                options={relationTypeOptions}
                                                className="w-28"
                                            />
                                        </div>

                                        {/* 目标表 */}
                                        <div className="flex-1 space-y-2">
                                            <Select
                                                value={relation.targetTable}
                                                onChange={(value) => updateRelation(relation.id, { targetTable: value })}
                                                options={tables.map(t => ({ value: t.name, label: t.name }))}
                                                label="目标表"
                                            />
                                            <Select
                                                value={relation.targetColumn}
                                                onChange={(value) => updateRelation(relation.id, { targetColumn: value })}
                                                options={targetTable?.fields.map(f => ({ value: f.name, label: f.name })) || []}
                                                label="目标字段 (外键)"
                                            />
                                        </div>

                                        <Button
                                            variant="ghost"
                                            size="icon"
                                            onClick={() => removeRelation(relation.id)}
                                            className="text-muted-foreground hover:text-destructive"
                                        >
                                            <Trash2 className="h-4 w-4" />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        )
                    })}

                    {relations.length === 0 && (
                        <Card>
                            <CardContent className="py-8 text-center">
                                <Link2 className="h-10 w-10 text-muted-foreground mx-auto mb-3" />
                                <h3 className="text-base font-medium text-foreground">暂无表关系</h3>
                                <p className="text-sm text-muted-foreground mt-1">
                                    {tables.length < 2 ? '至少需要2个表才能创建关系' : '点击"添加关系"来配置外键约束'}
                                </p>
                            </CardContent>
                        </Card>
                    )}

                    {/* 关系说明 */}
                    <Card>
                        <CardContent className="p-4">
                            <h3 className="text-sm font-medium text-foreground mb-2">关系类型说明</h3>
                            <dl className="space-y-1 text-sm text-muted-foreground">
                                <div className="flex">
                                    <dt className="w-20 font-mono">1:1</dt>
                                    <dd>一对一：每条源记录对应一条目标记录</dd>
                                </div>
                                <div className="flex">
                                    <dt className="w-20 font-mono">1:N</dt>
                                    <dd>一对多：每条源记录对应多条目标记录</dd>
                                </div>
                                <div className="flex">
                                    <dt className="w-20 font-mono">N:M</dt>
                                    <dd>多对多：需要中间表进行关联</dd>
                                </div>
                            </dl>
                        </CardContent>
                    </Card>
                </div>
            </div>

            {/* 结果展示弹窗 */}
            <Modal
                isOpen={isResultModalOpen}
                onClose={() => setIsResultModalOpen(false)}
                title="关联数据生成结果"
                size="xl"
            >
                {generatedData && (
                    <div className="h-[60vh] flex flex-col">
                        <Tabs value={activeResultTab} onChange={setActiveResultTab} className="h-full flex flex-col">
                            <div className="flex items-center justify-between border-b pb-2 mb-2">
                                <TabsList>
                                    {Object.keys(generatedData).map(tableName => (
                                        <TabsTrigger key={tableName} value={tableName}>
                                            {tableName} ({generatedData[tableName].length})
                                        </TabsTrigger>
                                    ))}
                                </TabsList>
                                <Button size="sm" variant="outline" onClick={() => downloadJson(activeResultTab)}>
                                    下载 JSON
                                </Button>
                            </div>

                            {Object.keys(generatedData).map(tableName => (
                                <TabsContent key={tableName} value={tableName} className="flex-1 overflow-auto mt-0">
                                    <div className="bg-muted p-4 rounded-md overflow-auto font-mono text-xs h-full">
                                        <pre>{JSON.stringify(generatedData[tableName].slice(0, 50), null, 2)}</pre>
                                        {generatedData[tableName].length > 50 && (
                                            <div className="text-muted-foreground mt-2 italic text-center">
                                                ... 仅展示前 50 条，请下载查看完整数据 ...
                                            </div>
                                        )}
                                    </div>
                                </TabsContent>
                            ))}
                        </Tabs>
                    </div>
                )}
                <ModalFooter>
                    <Button variant="primary" onClick={() => setIsResultModalOpen(false)}>
                        关闭
                    </Button>
                </ModalFooter>
            </Modal>
        </div>
    )
}
