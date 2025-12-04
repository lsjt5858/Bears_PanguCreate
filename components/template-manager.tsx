"use client"

import { useState } from "react"
import { FileText, Trash2, Edit2, Copy, Check, FolderOpen, Save, MoreHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Textarea } from "@/components/ui/textarea"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { DataField } from "./data-generator-platform"
import { dataTypes } from "@/lib/data-generator"

export type Template = {
  id: string
  name: string
  description: string
  fields: DataField[]
  createdAt: string
  updatedAt: string
  category: string
}

interface TemplateManagerProps {
  templates: Template[]
  setTemplates: (templates: Template[]) => void
  currentFields: DataField[]
  onApplyTemplate: (fields: DataField[]) => void
}

const templateCategories = [
  { id: "user", name: "用户相关", color: "bg-blue-500/20 text-blue-400" },
  { id: "order", name: "订单相关", color: "bg-green-500/20 text-green-400" },
  { id: "product", name: "商品相关", color: "bg-purple-500/20 text-purple-400" },
  { id: "finance", name: "财务相关", color: "bg-yellow-500/20 text-yellow-400" },
  { id: "other", name: "其他", color: "bg-gray-500/20 text-gray-400" },
]

export function TemplateManager({ templates, setTemplates, currentFields, onApplyTemplate }: TemplateManagerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isSaveDialogOpen, setIsSaveDialogOpen] = useState(false)
  const [editingTemplate, setEditingTemplate] = useState<Template | null>(null)
  const [newTemplate, setNewTemplate] = useState({
    name: "",
    description: "",
    category: "other",
  })
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")

  const handleSaveTemplate = () => {
    if (!newTemplate.name.trim()) return

    const now = new Date().toISOString()

    if (editingTemplate) {
      // 更新现有模板
      const updatedTemplates = templates.map((t) =>
        t.id === editingTemplate.id
          ? {
              ...t,
              name: newTemplate.name,
              description: newTemplate.description,
              category: newTemplate.category,
              fields: currentFields,
              updatedAt: now,
            }
          : t,
      )
      setTemplates(updatedTemplates)
    } else {
      // 创建新模板
      const template: Template = {
        id: Date.now().toString(),
        name: newTemplate.name,
        description: newTemplate.description,
        category: newTemplate.category,
        fields: currentFields.map((f) => ({ ...f, id: Date.now().toString() + Math.random() })),
        createdAt: now,
        updatedAt: now,
      }
      setTemplates([...templates, template])
    }

    setNewTemplate({ name: "", description: "", category: "other" })
    setEditingTemplate(null)
    setIsSaveDialogOpen(false)
  }

  const handleDeleteTemplate = (id: string) => {
    setTemplates(templates.filter((t) => t.id !== id))
  }

  const handleEditTemplate = (template: Template) => {
    setEditingTemplate(template)
    setNewTemplate({
      name: template.name,
      description: template.description,
      category: template.category,
    })
    setIsSaveDialogOpen(true)
  }

  const handleDuplicateTemplate = (template: Template) => {
    const now = new Date().toISOString()
    const duplicated: Template = {
      ...template,
      id: Date.now().toString(),
      name: `${template.name} (副本)`,
      fields: template.fields.map((f) => ({ ...f, id: Date.now().toString() + Math.random() })),
      createdAt: now,
      updatedAt: now,
    }
    setTemplates([...templates, duplicated])
  }

  const handleApplyTemplate = (template: Template) => {
    onApplyTemplate(template.fields.map((f) => ({ ...f, id: Date.now().toString() + Math.random() })))
    setIsOpen(false)
  }

  const getFieldTypeName = (typeId: string) => {
    return dataTypes.find((dt) => dt.id === typeId)?.name || typeId
  }

  const getCategoryInfo = (categoryId: string) => {
    return templateCategories.find((c) => c.id === categoryId) || templateCategories[4]
  }

  const filteredTemplates = templates.filter((t) => {
    const matchesSearch =
      t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === "all" || t.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  return (
    <>
      {/* 模板管理入口按钮 */}
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" className="gap-2 bg-transparent">
            <FolderOpen className="h-4 w-4" />
            模板管理
            {templates.length > 0 && (
              <Badge variant="secondary" className="ml-1">
                {templates.length}
              </Badge>
            )}
          </Button>
        </DialogTrigger>
        <DialogContent className="max-w-4xl max-h-[85vh] p-0">
          <DialogHeader className="px-6 pt-6 pb-4 border-b border-border">
            <DialogTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" />
              模板管理中心
            </DialogTitle>
            <DialogDescription>管理您保存的数据生成模板,快速复用常用配置</DialogDescription>
          </DialogHeader>

          <div className="flex h-[500px]">
            {/* 左侧分类筛选 */}
            <div className="w-48 border-r border-border p-4 flex-shrink-0">
              <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-3">模板分类</div>
              <div className="space-y-1">
                <button
                  onClick={() => setSelectedCategory("all")}
                  className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                    selectedCategory === "all"
                      ? "bg-primary/10 text-primary font-medium"
                      : "text-muted-foreground hover:bg-muted"
                  }`}
                >
                  全部模板 ({templates.length})
                </button>
                {templateCategories.map((cat) => {
                  const count = templates.filter((t) => t.category === cat.id).length
                  return (
                    <button
                      key={cat.id}
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                        selectedCategory === cat.id
                          ? "bg-primary/10 text-primary font-medium"
                          : "text-muted-foreground hover:bg-muted"
                      }`}
                    >
                      {cat.name} ({count})
                    </button>
                  )
                })}
              </div>
            </div>

            {/* 右侧模板列表 */}
            <div className="flex-1 flex flex-col">
              {/* 搜索和操作栏 */}
              <div className="p-4 border-b border-border flex items-center gap-3">
                <Input
                  placeholder="搜索模板..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1 bg-input"
                />
                <Button
                  onClick={() => {
                    setEditingTemplate(null)
                    setNewTemplate({ name: "", description: "", category: "other" })
                    setIsSaveDialogOpen(true)
                  }}
                  disabled={currentFields.length === 0}
                >
                  <Save className="h-4 w-4 mr-2" />
                  保存当前配置
                </Button>
              </div>

              {/* 模板网格 */}
              <ScrollArea className="flex-1 p-4">
                {filteredTemplates.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-center py-12">
                    <FileText className="h-12 w-12 text-muted-foreground/50 mb-4" />
                    <p className="text-muted-foreground">
                      {templates.length === 0 ? "暂无保存的模板" : "没有匹配的模板"}
                    </p>
                    <p className="text-sm text-muted-foreground/70 mt-1">
                      {templates.length === 0 ? "配置字段后点击“保存当前配置”创建模板" : "尝试更改搜索条件"}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-4">
                    {filteredTemplates.map((template) => {
                      const categoryInfo = getCategoryInfo(template.category)
                      return (
                        <Card
                          key={template.id}
                          className="bg-card border-border hover:border-primary/50 transition-colors group"
                        >
                          <CardHeader className="pb-2">
                            <div className="flex items-start justify-between">
                              <div className="flex-1 min-w-0">
                                <CardTitle className="text-base font-medium truncate">{template.name}</CardTitle>
                                <Badge className={`mt-1.5 text-xs ${categoryInfo.color}`}>{categoryInfo.name}</Badge>
                              </div>
                              <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                  <Button
                                    variant="ghost"
                                    size="icon"
                                    className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity"
                                  >
                                    <MoreHorizontal className="h-4 w-4" />
                                  </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end">
                                  <DropdownMenuItem onClick={() => handleApplyTemplate(template)}>
                                    <Check className="h-4 w-4 mr-2" />
                                    应用模板
                                  </DropdownMenuItem>
                                  <DropdownMenuItem onClick={() => handleEditTemplate(template)}>
                                    <Edit2 className="h-4 w-4 mr-2" />
                                    编辑模板
                                  </DropdownMenuItem>
                                  <DropdownMenuItem onClick={() => handleDuplicateTemplate(template)}>
                                    <Copy className="h-4 w-4 mr-2" />
                                    复制模板
                                  </DropdownMenuItem>
                                  <DropdownMenuSeparator />
                                  <DropdownMenuItem
                                    onClick={() => handleDeleteTemplate(template.id)}
                                    className="text-destructive focus:text-destructive"
                                  >
                                    <Trash2 className="h-4 w-4 mr-2" />
                                    删除模板
                                  </DropdownMenuItem>
                                </DropdownMenuContent>
                              </DropdownMenu>
                            </div>
                          </CardHeader>
                          <CardContent>
                            {template.description && (
                              <p className="text-sm text-muted-foreground mb-3 line-clamp-2">{template.description}</p>
                            )}
                            <div className="flex flex-wrap gap-1.5 mb-3">
                              {template.fields.slice(0, 4).map((field) => (
                                <Badge key={field.id} variant="outline" className="text-xs font-normal">
                                  {field.name}: {getFieldTypeName(field.type)}
                                </Badge>
                              ))}
                              {template.fields.length > 4 && (
                                <Badge variant="outline" className="text-xs font-normal">
                                  +{template.fields.length - 4} 更多
                                </Badge>
                              )}
                            </div>
                            <div className="flex items-center justify-between">
                              <span className="text-xs text-muted-foreground">{template.fields.length} 个字段</span>
                              <Button size="sm" onClick={() => handleApplyTemplate(template)}>
                                应用
                              </Button>
                            </div>
                          </CardContent>
                        </Card>
                      )
                    })}
                  </div>
                )}
              </ScrollArea>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* 保存模板对话框 */}
      <Dialog open={isSaveDialogOpen} onOpenChange={setIsSaveDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingTemplate ? "编辑模板" : "保存为模板"}</DialogTitle>
            <DialogDescription>
              {editingTemplate ? "修改模板信息,字段配置将更新为当前配置" : "将当前字段配置保存为可复用的模板"}
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="template-name">模板名称</Label>
              <Input
                id="template-name"
                value={newTemplate.name}
                onChange={(e) => setNewTemplate({ ...newTemplate, name: e.target.value })}
                placeholder="例如: 用户注册数据"
                className="bg-input"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="template-desc">模板描述</Label>
              <Textarea
                id="template-desc"
                value={newTemplate.description}
                onChange={(e) => setNewTemplate({ ...newTemplate, description: e.target.value })}
                placeholder="描述此模板的用途..."
                className="bg-input resize-none"
                rows={3}
              />
            </div>
            <div className="space-y-2">
              <Label>模板分类</Label>
              <div className="flex flex-wrap gap-2">
                {templateCategories.map((cat) => (
                  <Button
                    key={cat.id}
                    type="button"
                    variant={newTemplate.category === cat.id ? "default" : "outline"}
                    size="sm"
                    onClick={() => setNewTemplate({ ...newTemplate, category: cat.id })}
                  >
                    {cat.name}
                  </Button>
                ))}
              </div>
            </div>
            <div className="rounded-lg border border-border bg-muted/30 p-3">
              <p className="text-sm text-muted-foreground mb-2">包含字段:</p>
              <div className="flex flex-wrap gap-1.5">
                {currentFields.map((field) => (
                  <Badge key={field.id} variant="secondary" className="text-xs">
                    {field.name}
                  </Badge>
                ))}
                {currentFields.length === 0 && <span className="text-sm text-muted-foreground">暂无字段配置</span>}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsSaveDialogOpen(false)}>
              取消
            </Button>
            <Button onClick={handleSaveTemplate} disabled={!newTemplate.name.trim() || currentFields.length === 0}>
              {editingTemplate ? "更新模板" : "保存模板"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  )
}
