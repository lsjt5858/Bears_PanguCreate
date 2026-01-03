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

// 辅助函数：获取认证头
function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem('access_token')
  return token ? {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  } : {
    'Content-Type': 'application/json'
  }
}

// 获取数据类型
export async function fetchDataTypes(): Promise<DataType[]> {
  const res = await fetch(`${API_BASE}/types`, {
    headers: getAuthHeaders()
  })
  const data = await res.json()
  return data.types
}

// 生成数据
export async function generateData(fields: DataField[], count: number): Promise<Record<string, unknown>[]> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ fields, count }),
  })
  const data = await res.json()
  return data.data
}

// 获取模板列表
export async function fetchTemplates(): Promise<Template[]> {
  const res = await fetch(`${API_BASE}/templates`, {
    headers: getAuthHeaders()
  })
  const data = await res.json()
  return data.templates
}

// 创建模板
export async function createTemplate(template: Omit<Template, 'id' | 'createdAt' | 'updatedAt'>): Promise<Template> {
  const res = await fetch(`${API_BASE}/templates`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(template),
  })
  const data = await res.json()
  return data.template
}

// 删除模板
export async function deleteTemplate(id: string): Promise<void> {
  await fetch(`${API_BASE}/templates/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  })
}

// 导出为JSON（后端导出）
export async function exportToJson(data: Record<string, unknown>[], fields: DataField[]): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export/json`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ data, fields }),
  })
  return res.blob()
}

// 导出为CSV（后端导出）
export async function exportToCsv(data: Record<string, unknown>[], fields: DataField[]): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export/csv`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ data, fields }),
  })
  return res.blob()
}

// 导出为SQL（后端导出）
export async function exportToSql(data: Record<string, unknown>[], fields: DataField[], tableName: string = 'test_data'): Promise<Blob> {
  const res = await fetch(`${API_BASE}/export/sql`, {
    method: 'POST',
    headers: getAuthHeaders(),
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
// 历史记录 API
// ==========================================

export interface HistoryParams {
  page?: number
  page_size?: number
  project_id?: number
  search?: string
  format?: string
  start_date?: string
  end_date?: string
}

export interface HistoryListResponse {
  data: any[] // 使用 any 或定义详细的 BackendHistoryRecord 类型
  pagination: {
    page: number
    page_size: number
    total: number
    total_pages: number
  }
}

export async function fetchHistory(params: HistoryParams = {}): Promise<HistoryListResponse> {
  const searchParams = new URLSearchParams()
  if (params.page) searchParams.append('page', params.page.toString())
  if (params.page_size) searchParams.append('page_size', params.page_size.toString())
  if (params.project_id) searchParams.append('project_id', params.project_id.toString())
  if (params.search) searchParams.append('search', params.search)
  if (params.format && params.format !== 'all') searchParams.append('format', params.format)

  const res = await fetch(`${API_BASE}/history?${searchParams.toString()}`, {
    headers: getAuthHeaders()
  })

  if (!res.ok) {
    throw new Error('获取历史记录失败')
  }

  return await res.json()
}

export async function deleteHistory(id: string | number): Promise<void> {
  const res = await fetch(`${API_BASE}/history/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.error || '删除失败')
  }
}

export async function batchDeleteHistory(ids: (string | number)[]): Promise<void> {
  const res = await fetch(`${API_BASE}/history/batch`, {
    method: 'DELETE',
    headers: getAuthHeaders(),
    body: JSON.stringify({ ids })
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.error || '批量删除失败')
  }
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

// ==========================================
// 统计 API
// ==========================================

import type { DashboardStats, TrendData, ActivityLog } from './types'

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE}/stats/dashboard`, {
    headers: getAuthHeaders()
  })

  if (!res.ok) {
    throw new Error('获取仪表盘数据失败')
  }

  const result = await res.json()
  const data = result.data

  return {
    totalGenerated: data.total_generated,
    totalTemplates: data.total_templates,
    totalMembers: data.total_members,
    apiCalls: data.api_calls,
    generatedThisMonth: data.generated_this_month,
    generatedLastMonth: data.generated_last_month
  }
}

export async function fetchTrendData(days: number = 30): Promise<TrendData[]> {
  const res = await fetch(`${API_BASE}/stats/trend?days=${days}`, {
    headers: getAuthHeaders()
  })

  if (!res.ok) {
    throw new Error('获取趋势数据失败')
  }

  const result = await res.json()

  return result.data.map((item: any) => ({
    date: item.date,
    count: item.rows // 使用 rows 作为生成量
  }))
}

export async function fetchRecentActivities(limit: number = 10): Promise<ActivityLog[]> {
  const res = await fetch(`${API_BASE}/stats/activities?limit=${limit}`, {
    headers: getAuthHeaders()
  })

  if (!res.ok) {
    throw new Error('获取最近活动失败')
  }

  const result = await res.json()

  return result.data.map((item: any) => ({
    id: item.id,
    userId: item.user_id,
    user: {
      id: item.user.id,
      name: item.user.name,
      email: item.user.email,
      avatar: item.user.avatar,
      role: 'member', // 后端未返回角色，默认为 member
      createdAt: ''   // 后端未返回创建时间，留空
    },
    action: item.action,
    target: item.target,
    createdAt: item.created_at
  }))
}

// ==========================================
// API 密钥管理
// ==========================================

import type { ApiKey, ApiKeyPermission } from './types'

export async function fetchApiKeys(): Promise<ApiKey[]> {
  const res = await fetch(`${API_BASE}/api-keys`, {
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('获取密钥列表失败')
  const result = await res.json()
  // 转换后端数据格式
  return result.data.map((key: any) => ({
    id: key.id,
    name: key.name,
    key: key.prefix + '****************' + key.suffix, // 掩码显示
    permissions: key.permissions || [],
    callCount: key.call_count || 0,
    lastUsed: key.last_used_at,
    expiresAt: key.expires_at,
    createdAt: key.created_at
  }))
}

export async function createApiKey(name: string, permissions: ApiKeyPermission[] = ['read'], expiresAt?: string): Promise<{ apiKey: ApiKey, fullKey: string }> {
  const res = await fetch(`${API_BASE}/api-keys`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ name, permissions, expires_at: expiresAt })
  })

  const result = await res.json()

  if (!res.ok) throw new Error(result.error || '创建密钥失败')

  // 后端返回的 data 包含完整的 key
  const data = result.data
  return {
    apiKey: {
      id: data.id,
      name: data.name,
      key: data.key, // 包含完整密钥
      permissions: data.permissions || [],
      callCount: 0,
      createdAt: data.created_at,
      expiresAt: data.expires_at
    },
    fullKey: data.key
  }
}

export async function deleteApiKey(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api-keys/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('删除密钥失败')
}

export async function revokeApiKey(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api-keys/${id}/revoke`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('撤销密钥失败')
}

// ==========================================
// 定时任务管理
// ==========================================

import type { ScheduledTask, CronPreset, TaskExecutionLog } from './types'

function mapScheduledTask(data: any): ScheduledTask {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    templateId: data.template_id,
    cronExpression: data.cron_expression,
    timezone: data.timezone,
    fields: data.fields,
    rowCount: data.row_count,
    exportFormat: data.export_format,
    tableName: data.table_name,
    outputType: data.output_type,
    outputConfig: data.output_config,
    status: data.status,
    isEnabled: data.is_enabled,
    isActive: data.is_active,
    runCount: data.run_count,
    successCount: data.success_count,
    failCount: data.fail_count,
    lastRunAt: data.last_run_at,
    lastRunStatus: data.last_run_status,
    lastError: data.last_error,
    nextRunAt: data.next_run_at,
    maxRuns: data.max_runs,
    expiresAt: data.expires_at,
    createdAt: data.created_at,
    updatedAt: data.updated_at
  }
}

export async function fetchScheduledTasks(): Promise<ScheduledTask[]> {
  const res = await fetch(`${API_BASE}/scheduled-tasks`, {
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('获取任务列表失败')
  const result = await res.json()
  return result.data.map(mapScheduledTask)
}

export async function createScheduledTask(data: Partial<ScheduledTask>): Promise<ScheduledTask> {
  // 转换为后端字段
  const backendData = {
    name: data.name,
    description: data.description,
    template_id: data.templateId,
    cron_expression: data.cronExpression,
    fields: data.fields,
    row_count: data.rowCount,
    export_format: data.exportFormat,
    output_type: data.outputType || 'none',
    timezone: data.timezone
  }

  const res = await fetch(`${API_BASE}/scheduled-tasks`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(backendData)
  })

  if (!res.ok) {
    const error = await res.json()
    throw new Error(error.error || '创建任务失败')
  }

  const result = await res.json()
  return mapScheduledTask(result.data)
}

export async function deleteScheduledTask(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/scheduled-tasks/${id}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('删除任务失败')
}

export async function pauseScheduledTask(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/scheduled-tasks/${id}/pause`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('暂停任务失败')
}

export async function resumeScheduledTask(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/scheduled-tasks/${id}/resume`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('恢复任务失败')
}

export async function runScheduledTask(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/scheduled-tasks/${id}/run`, {
    method: 'POST',
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('触发任务失败')
}

export async function fetchCronPresets(): Promise<CronPreset[]> {
  const res = await fetch(`${API_BASE}/scheduled-tasks/cron/presets`, {
    headers: getAuthHeaders()
  })
  if (!res.ok) return [] // 不报错，返回空
  const result = await res.json()
  return result.data
}

export async function fetchTaskLogs(taskId: string, page = 1, pageSize = 20): Promise<{ data: TaskExecutionLog[], total: number }> {
  const res = await fetch(`${API_BASE}/scheduled-tasks/${taskId}/logs?page=${page}&page_size=${pageSize}`, {
    headers: getAuthHeaders()
  })
  if (!res.ok) throw new Error('获取执行日志失败')
  const result = await res.json()
  return {
    data: result.data,
    total: result.pagination.total
  }
}
