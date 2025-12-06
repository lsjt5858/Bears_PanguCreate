import { Plus, Trash2, Play, GripVertical, Sparkles, FolderOpen } from 'lucide-react'
import type { DataField, DataType, Template } from '@/lib/api'

interface GeneratorPanelProps {
  fields: DataField[]
  setFields: (fields: DataField[]) => void
  recordCount: number
  setRecordCount: (count: number) => void
  onGenerate: () => void
  isGenerating: boolean
  dataTypes: DataType[]
  templates: Template[]
  setTemplates: (templates: Template[]) => void
}

const quickTemplates = [
  {
    name: '用户信息',
    icon: '👤',
    fields: [
      { id: '1', name: 'id', type: 'uuid' },
      { id: '2', name: 'name', type: 'chineseName' },
      { id: '3', name: 'email', type: 'email' },
      { id: '4', name: 'phone', type: 'chinesePhone' },
      { id: '5', name: 'age', type: 'age' },
      { id: '6', name: 'gender', type: 'gender' },
    ],
  },
  {
    name: '订单数据',
    icon: '🛒',
    fields: [
      { id: '1', name: 'order_id', type: 'uuid' },
      { id: '2', name: 'user_name', type: 'chineseName' },
      { id: '3', name: 'amount', type: 'amount' },
      { id: '4', name: 'created_at', type: 'datetime' },
      { id: '5', name: 'address', type: 'chineseAddress' },
    ],
  },
  {
    name: '地址信息',
    icon: '📍',
    fields: [
      { id: '1', name: 'id', type: 'uuid' },
      { id: '2', name: 'province', type: 'province' },
      { id: '3', name: 'city', type: 'city' },
      { id: '4', name: 'address', type: 'chineseAddress' },
      { id: '5', name: 'zipcode', type: 'zipcode' },
    ],
  },
  {
    name: '企业信息',
    icon: '🏢',
    fields: [
      { id: '1', name: 'id', type: 'uuid' },
      { id: '2', name: 'company', type: 'company' },
      { id: '3', name: 'contact', type: 'chineseName' },
      { id: '4', name: 'phone', type: 'chinesePhone' },
      { id: '5', name: 'email', type: 'email' },
    ],
  },
]

const previews: Record<string, string> = {
  uuid: '550e8400-e29b-41d4...',
  chineseName: '张三',
  englishName: 'John Smith',
  email: 'test@example.com',
  chinesePhone: '138****8888',
  phone: '+1 555-123-4567',
  chineseIdCard: '110101199003...',
  age: '28',
  gender: '男',
  string: '随机文本...',
  number: '12345',
  boolean: 'true / false',
  date: '2024-01-15',
  datetime: '2024-01-15 14:30:00',
  timestamp: '1705312200000',
  chineseAddress: '北京市朝阳区...',
  city: '上海',
  province: '广东省',
  zipcode: '100000',
  url: 'https://example.com',
  ip: '192.168.1.1',
  ipv6: '2001:0db8:85a3...',
  mac: '00:1A:2B:3C:4D:5E',
  domain: 'example.com',
  bankCard: '6222****8888',
  amount: '¥1,234.56',
  company: '科技有限公司',
  jobTitle: '高级工程师',
  paragraph: '这是一段文本...',
  sentence: '这是一句话。',
  word: '测试',
}

export function GeneratorPanel({
  fields,
  setFields,
  recordCount,
  setRecordCount,
  onGenerate,
  isGenerating,
  dataTypes,
}: GeneratorPanelProps) {
  const addField = () => {
    const newField: DataField = {
      id: Date.now().toString(),
      name: `field_${fields.length + 1}`,
      type: 'string',
    }
    setFields([...fields, newField])
  }

  const removeField = (id: string) => {
    setFields(fields.filter((f) => f.id !== id))
  }

  const updateField = (id: string, updates: Partial<DataField>) => {
    setFields(fields.map((f) => (f.id === id ? { ...f, ...updates } : f)))
  }

  return (
    <div className="flex w-full flex-col overflow-hidden border-r border-border lg:w-1/2">
      <div className="border-b border-border bg-card p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">字段配置</h2>
            <p className="text-sm text-muted-foreground">定义数据结构和生成规则</p>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-2 px-3 py-2 text-sm border border-border rounded-lg hover:bg-secondary">
              <FolderOpen className="h-4 w-4" />
              模板管理
            </button>
            <div className="flex items-center gap-2">
              <label className="text-sm text-muted-foreground whitespace-nowrap">生成数量</label>
              <input
                type="number"
                value={recordCount}
                onChange={(e) => setRecordCount(Number(e.target.value))}
                className="w-20 px-2 py-1 text-sm bg-input border border-border rounded-lg"
                min={1}
                max={10000}
              />
            </div>
            <button
              onClick={onGenerate}
              disabled={isGenerating || fields.length === 0}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 disabled:opacity-50"
            >
              {isGenerating ? (
                <>
                  <Sparkles className="h-4 w-4 animate-spin" />
                  生成中...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4" />
                  生成数据
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        <div className="space-y-3">
          {fields.map((field) => (
            <div key={field.id} className="bg-card border border-border rounded-lg p-4">
              <div className="flex items-start gap-3">
                <button className="mt-2.5 cursor-grab text-muted-foreground hover:text-foreground">
                  <GripVertical className="h-4 w-4" />
                </button>
                <div className="flex-1 grid grid-cols-1 gap-3 sm:grid-cols-3">
                  <div>
                    <label className="text-xs text-muted-foreground mb-1.5 block">字段名称</label>
                    <input
                      value={field.name}
                      onChange={(e) => updateField(field.id, { name: e.target.value })}
                      placeholder="字段名"
                      className="w-full px-3 py-2 text-sm bg-input border border-border rounded-lg"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-muted-foreground mb-1.5 block">数据类型</label>
                    <select
                      value={field.type}
                      onChange={(e) => updateField(field.id, { type: e.target.value })}
                      className="w-full px-3 py-2 text-sm bg-input border border-border rounded-lg"
                    >
                      {dataTypes.map((dt) => (
                        <option key={dt.id} value={dt.id}>
                          {dt.icon} {dt.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="flex items-end gap-2">
                    <div className="flex-1">
                      <label className="text-xs text-muted-foreground mb-1.5 block">预览</label>
                      <div className="h-9 rounded-lg border border-border bg-muted/50 px-3 py-2 text-sm text-muted-foreground truncate">
                        {previews[field.type] || '示例数据'}
                      </div>
                    </div>
                    <button
                      onClick={() => removeField(field.id)}
                      className="p-2 text-muted-foreground hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={addField}
          className="mt-4 w-full py-2 border border-dashed border-border rounded-lg text-sm text-muted-foreground hover:border-primary hover:text-primary flex items-center justify-center gap-2"
        >
          <Plus className="h-4 w-4" />
          添加字段
        </button>

        <div className="mt-6 bg-card border border-border rounded-lg p-4">
          <h3 className="text-sm font-medium text-foreground flex items-center gap-2 mb-3">
            <Sparkles className="h-4 w-4 text-primary" />
            快速模板
          </h3>
          <div className="grid grid-cols-2 gap-2">
            {quickTemplates.map((template) => (
              <button
                key={template.name}
                onClick={() => setFields(template.fields)}
                className="px-3 py-2 text-xs text-left bg-secondary hover:bg-secondary/80 rounded-lg"
              >
                {template.icon} {template.name}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
