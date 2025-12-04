"use client"

import { useState } from "react"
import { Plus, Trash2, Play, GripVertical, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import type { DataField, GeneratedData } from "./data-generator-platform"
import { generateMockData, dataTypes, getDataTypesByCategory } from "@/lib/data-generator"
import { TemplateManager, type Template } from "./template-manager"

interface GeneratorPanelProps {
  fields: DataField[]
  setFields: (fields: DataField[]) => void
  recordCount: number
  setRecordCount: (count: number) => void
  setGeneratedData: (data: GeneratedData) => void
  activeCategory: string
  templates: Template[]
  setTemplates: (templates: Template[]) => void
}

export function GeneratorPanel({
  fields,
  setFields,
  recordCount,
  setRecordCount,
  setGeneratedData,
  activeCategory,
  templates,
  setTemplates,
}: GeneratorPanelProps) {
  const [isGenerating, setIsGenerating] = useState(false)

  const addField = () => {
    const newField: DataField = {
      id: Date.now().toString(),
      name: `field_${fields.length + 1}`,
      type: "string",
    }
    setFields([...fields, newField])
  }

  const removeField = (id: string) => {
    setFields(fields.filter((f) => f.id !== id))
  }

  const updateField = (id: string, updates: Partial<DataField>) => {
    setFields(fields.map((f) => (f.id === id ? { ...f, ...updates } : f)))
  }

  const handleGenerate = async () => {
    setIsGenerating(true)
    await new Promise((resolve) => setTimeout(resolve, 500))
    const data = generateMockData(fields, recordCount)
    setGeneratedData(data)
    setIsGenerating(false)
  }

  const filteredDataTypes = activeCategory === "all" ? dataTypes : getDataTypesByCategory(activeCategory)

  return (
    <div className="flex w-full flex-col overflow-hidden border-r border-border lg:w-1/2">
      <div className="border-b border-border bg-card p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">字段配置</h2>
            <p className="text-sm text-muted-foreground">定义数据结构和生成规则</p>
          </div>
          <div className="flex items-center gap-3">
            <TemplateManager
              templates={templates}
              setTemplates={setTemplates}
              currentFields={fields}
              onApplyTemplate={setFields}
            />
            <div className="flex items-center gap-2">
              <Label htmlFor="count" className="text-sm text-muted-foreground whitespace-nowrap">
                生成数量
              </Label>
              <Input
                id="count"
                type="number"
                value={recordCount}
                onChange={(e) => setRecordCount(Number(e.target.value))}
                className="w-20 bg-input"
                min={1}
                max={10000}
              />
            </div>
            <Button onClick={handleGenerate} disabled={isGenerating || fields.length === 0}>
              {isGenerating ? (
                <>
                  <Sparkles className="mr-2 h-4 w-4 animate-spin" />
                  生成中...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  生成数据
                </>
              )}
            </Button>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-4">
        <div className="space-y-3">
          {fields.map((field, index) => (
            <Card key={field.id} className="bg-card border-border">
              <CardContent className="p-4">
                <div className="flex items-start gap-3">
                  <button className="mt-2.5 cursor-grab text-muted-foreground hover:text-foreground">
                    <GripVertical className="h-4 w-4" />
                  </button>
                  <div className="flex-1 grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <div>
                      <Label className="text-xs text-muted-foreground mb-1.5 block">字段名称</Label>
                      <Input
                        value={field.name}
                        onChange={(e) => updateField(field.id, { name: e.target.value })}
                        placeholder="字段名"
                        className="bg-input"
                      />
                    </div>
                    <div>
                      <Label className="text-xs text-muted-foreground mb-1.5 block">数据类型</Label>
                      <Select value={field.type} onValueChange={(value) => updateField(field.id, { type: value })}>
                        <SelectTrigger className="bg-input">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {filteredDataTypes.map((dt) => (
                            <SelectItem key={dt.id} value={dt.id}>
                              <div className="flex items-center gap-2">
                                <span className="text-xs text-muted-foreground">{dt.icon}</span>
                                {dt.name}
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="flex items-end gap-2">
                      <div className="flex-1">
                        <Label className="text-xs text-muted-foreground mb-1.5 block">预览</Label>
                        <div className="h-9 rounded-md border border-border bg-muted/50 px-3 py-2 text-sm text-muted-foreground truncate">
                          {getPreview(field.type)}
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeField(field.id)}
                        className="text-muted-foreground hover:text-destructive shrink-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Button
          variant="outline"
          onClick={addField}
          className="mt-4 w-full border-dashed border-border hover:border-primary hover:bg-primary/5 bg-transparent"
        >
          <Plus className="mr-2 h-4 w-4" />
          添加字段
        </Button>

        <div className="mt-6">
          <Card className="bg-card border-border">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-foreground flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-primary" />
                快速模板
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-0">
              <div className="grid grid-cols-2 gap-2">
                {quickTemplates.map((template) => (
                  <Button
                    key={template.name}
                    variant="secondary"
                    size="sm"
                    onClick={() => setFields(template.fields)}
                    className="justify-start text-xs"
                  >
                    {template.icon} {template.name}
                  </Button>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

function getPreview(type: string): string {
  const previews: Record<string, string> = {
    uuid: "550e8400-e29b-41d4...",
    chineseName: "张三",
    englishName: "John Smith",
    email: "test@example.com",
    chinesePhone: "138****8888",
    phone: "+1 555-123-4567",
    chineseIdCard: "110101199003...",
    age: "28",
    gender: "男",
    string: "随机文本...",
    number: "12345",
    boolean: "true / false",
    date: "2024-01-15",
    datetime: "2024-01-15 14:30:00",
    timestamp: "1705312200000",
    chineseAddress: "北京市朝阳区...",
    city: "上海",
    province: "广东省",
    zipcode: "100000",
    url: "https://example.com",
    ip: "192.168.1.1",
    ipv6: "2001:0db8:85a3...",
    mac: "00:1A:2B:3C:4D:5E",
    domain: "example.com",
    bankCard: "6222****8888",
    amount: "¥1,234.56",
    company: "科技有限公司",
    jobTitle: "高级工程师",
    paragraph: "这是一段文本...",
    sentence: "这是一句话。",
    word: "测试",
  }
  return previews[type] || "示例数据"
}

const quickTemplates = [
  {
    name: "用户信息",
    icon: "👤",
    fields: [
      { id: "1", name: "id", type: "uuid" },
      { id: "2", name: "name", type: "chineseName" },
      { id: "3", name: "email", type: "email" },
      { id: "4", name: "phone", type: "chinesePhone" },
      { id: "5", name: "age", type: "age" },
      { id: "6", name: "gender", type: "gender" },
    ],
  },
  {
    name: "订单数据",
    icon: "🛒",
    fields: [
      { id: "1", name: "order_id", type: "uuid" },
      { id: "2", name: "user_name", type: "chineseName" },
      { id: "3", name: "amount", type: "amount" },
      { id: "4", name: "created_at", type: "datetime" },
      { id: "5", name: "address", type: "chineseAddress" },
    ],
  },
  {
    name: "地址信息",
    icon: "📍",
    fields: [
      { id: "1", name: "id", type: "uuid" },
      { id: "2", name: "province", type: "province" },
      { id: "3", name: "city", type: "city" },
      { id: "4", name: "address", type: "chineseAddress" },
      { id: "5", name: "zipcode", type: "zipcode" },
    ],
  },
  {
    name: "企业信息",
    icon: "🏢",
    fields: [
      { id: "1", name: "id", type: "uuid" },
      { id: "2", name: "company", type: "company" },
      { id: "3", name: "contact", type: "chineseName" },
      { id: "4", name: "phone", type: "chinesePhone" },
      { id: "5", name: "email", type: "email" },
    ],
  },
]
