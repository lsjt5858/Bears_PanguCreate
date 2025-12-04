const API_BASE = '/api'

export interface DataField {
  id: string
  name: string
  type: string
  options?: Record<string, unknown>
}

export interface DataType {
  id: string
  name: string
  icon: string
  category: string
}

export interface Template {
  id: string
  name: string
  description: string
  category: string
  fields: DataField[]
  createdAt: string
  updatedAt: string
}

// 获取数据类型
export async function fetchDataTypes(): Promise<DataType[]> {
  const res = await fetch(`${API_BASE}/types`)
  const data = await res.json()
  return data.types
}

// 生成数据
export async function generateData(fields: DataField[], count: number): Promise<Record<string, unknown>[]> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fields, count }),
  })
  const data = await res.json()
  return data.data
}

// 获取模板列表
export async function fetchTemplates(): Promise<Template[]> {
  const res = await fetch(`${API_BASE}/templates`)
  const data = await res.json()
  return data.templates
}

// 创建模板
export async function createTemplate(template: Omit<Template, 'id' | 'createdAt' | 'updatedAt'>): Promise<Template> {
  const res = await fetch(`${API_BASE}/templates`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(template),
  })
  const data = await res.json()
  return data.template
}

// 删除模板
export async function deleteTemplate(id: string): Promise<void> {
  await fetch(`${API_BASE}/templates/${id}`, { method: 'DELETE' })
}
