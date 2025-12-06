/**
 * Bears_PanguCreate 类型定义
 */

// ==================== 基础类型 ====================

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

// ==================== 用户与权限 ====================

export type UserRole = 'admin' | 'lead' | 'member'

export interface User {
    id: string
    name: string
    email: string
    avatar?: string
    role: UserRole
    createdAt: string
}

export interface Project {
    id: string
    name: string
    description: string
    members: ProjectMember[]
    createdAt: string
    updatedAt: string
}

export interface ProjectMember {
    userId: string
    user: User
    role: UserRole
    joinedAt: string
}

// ==================== 模板 ====================

export interface Template {
    id: string
    name: string
    description: string
    category: string
    fields: DataField[]
    createdAt: string
    updatedAt: string
}

export interface MarketTemplate extends Template {
    author: User
    downloads: number
    rating: number
    ratingCount: number
    isFavorite: boolean
    tags: string[]
}

// ==================== 数据源 ====================

export type DataSourceType = 'mysql' | 'postgresql' | 'mongodb' | 'restapi'

export interface DataSource {
    id: string
    name: string
    type: DataSourceType
    host: string
    port: number
    database?: string
    username?: string
    status: 'connected' | 'disconnected' | 'error'
    lastConnected?: string
    createdAt: string
}

export interface DatabaseTable {
    name: string
    columns: DatabaseColumn[]
}

export interface DatabaseColumn {
    name: string
    type: string
    nullable: boolean
    primaryKey: boolean
}

// ==================== 历史记录 ====================

export type ExportFormat = 'json' | 'csv' | 'sql'

export interface HistoryRecord {
    id: string
    name: string
    fields: DataField[]
    count: number
    format: ExportFormat
    createdAt: string
    projectId: string
}

export interface Dataset {
    id: string
    name: string
    description: string
    recordCount: number
    fields: DataField[]
    createdAt: string
    updatedAt: string
}

// ==================== API 管理 ====================

export type ApiKeyPermission = 'read' | 'write' | 'admin'

export interface ApiKey {
    id: string
    name: string
    key: string
    permissions: ApiKeyPermission[]
    callCount: number
    lastUsed?: string
    expiresAt?: string
    createdAt: string
}

// ==================== 定时任务 ====================

export type TaskStatus = 'active' | 'paused' | 'error'

export interface ScheduledTask {
    id: string
    name: string
    templateId: string
    template?: Template
    cronExpression: string
    targetDataSourceId?: string
    targetDataSource?: DataSource
    count: number
    status: TaskStatus
    lastRun?: string
    nextRun?: string
    createdAt: string
}

// ==================== 关联数据 ====================

export type RelationType = 'one-to-one' | 'one-to-many' | 'many-to-many'

export interface TableRelation {
    id: string
    sourceTable: string
    sourceColumn: string
    targetTable: string
    targetColumn: string
    relationType: RelationType
}

export interface RelationConfig {
    id: string
    name: string
    tables: RelationTable[]
    relations: TableRelation[]
    createdAt: string
}

export interface RelationTable {
    id: string
    name: string
    fields: DataField[]
    count: number
}

// ==================== 仪表盘 ====================

export interface DashboardStats {
    totalGenerated: number
    totalTemplates: number
    totalMembers: number
    apiCalls: number
    generatedThisMonth: number
    generatedLastMonth: number
}

export interface TrendData {
    date: string
    count: number
}

export interface ActivityLog {
    id: string
    userId: string
    user: User
    action: string
    target: string
    createdAt: string
}

// ==================== API 响应 ====================

export interface ApiResponse<T> {
    success: boolean
    data?: T
    error?: string
}

export interface PaginatedResponse<T> {
    success: boolean
    data: T[]
    total: number
    page: number
    pageSize: number
}
