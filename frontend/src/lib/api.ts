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

export interface GenerateResponse {
  success: boolean
  data: Record<string, unknown>[]
  count: number
  fields: DataField[]
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

// 导出为JSON（后端导出）
export async function exportToJson(data: Record<string, unknown>[], fields: DataField[]): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export/json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data, fields }),
  })
  return res.blob()
}

// 导出为CSV（后端导出）
export async function exportToCsv(data: Record<string, unknown>[], fields: DataField[]): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export/csv`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data, fields }),
  })
  return res.blob()
}

// 导出为SQL（后端导出）
export async function exportToSql(data: Record<string, unknown>[], fields: DataField[], tableName: string = 'test_data'): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export/sql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data, fields, tableName }),
  })
  return res.blob()
}

// 下载Blob文件
export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// ==========================================
// 认证相关 API
// ==========================================

export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  nickname?: string
  role?: string
  created_at?: string
  [key: string]: unknown
}

export interface LoginResponse {
  message: string
  data: {
    access_token: string
    refresh_token: string
    user: User
  }
}

export interface RegisterResponse {
  message: string
  data: {
    access_token: string
    refresh_token: string
    user: User
  }
}

// 登录
export async function login(data: { username?: string, email?: string, password: string }): Promise<LoginResponse> {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  
  const result = await res.json()
  
  if (!res.ok) {
    throw new Error(result.error || '登录失败')
  }
  
  return result
}

// 注册
export async function register(data: { username: string, email: string, password: string }): Promise<RegisterResponse> {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  
  const result = await res.json()
  
  if (!res.ok) {
    throw new Error(result.error || '注册失败')
  }
  
  return result
}

// 获取当前用户信息
export async function getCurrentUser(token: string): Promise<User> {
  const res = await fetch(`${API_BASE}/auth/me`, {
    method: 'GET',
    headers: { 
      'Authorization': `Bearer ${token}` 
    },
  })
  
  const result = await res.json()
  
  if (!res.ok) {
    throw new Error(result.error || '获取用户信息失败')
  }
  
  return result.user
}
