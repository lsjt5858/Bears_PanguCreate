import {
    BarChart3,
    FileJson,
    Users,
    Zap,
    TrendingUp,
    TrendingDown,
    Clock,
    Star
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common'
import type { DashboardStats, TrendData, ActivityLog } from '@/lib/types'

// 模拟数据
const mockStats: DashboardStats = {
    totalGenerated: 128470,
    totalTemplates: 24,
    totalMembers: 8,
    apiCalls: 3420,
    generatedThisMonth: 45230,
    generatedLastMonth: 38900,
}

const mockTrendData: TrendData[] = [
    { date: '2024-01', count: 12000 },
    { date: '2024-02', count: 18500 },
    { date: '2024-03', count: 15200 },
    { date: '2024-04', count: 22800 },
    { date: '2024-05', count: 28400 },
    { date: '2024-06', count: 35600 },
    { date: '2024-07', count: 45230 },
]

const mockActivities: ActivityLog[] = [
    {
        id: '1',
        userId: '1',
        user: { id: '1', name: '张三', email: '', role: 'admin', createdAt: '' },
        action: '生成数据',
        target: '用户注册数据模板 (1000条)',
        createdAt: '2024-07-15T10:30:00.000Z',
    },
    {
        id: '2',
        userId: '2',
        user: { id: '2', name: '李四', email: '', role: 'member', createdAt: '' },
        action: '创建模板',
        target: '订单测试数据',
        createdAt: '2024-07-15T09:45:00.000Z',
    },
    {
        id: '3',
        userId: '1',
        user: { id: '1', name: '张三', email: '', role: 'admin', createdAt: '' },
        action: '导出数据',
        target: 'CSV格式 (5000条)',
        createdAt: '2024-07-15T09:20:00.000Z',
    },
    {
        id: '4',
        userId: '3',
        user: { id: '3', name: '王五', email: '', role: 'lead', createdAt: '' },
        action: 'API调用',
        target: '/api/generate',
        createdAt: '2024-07-15T08:55:00.000Z',
    },
]

const popularTemplates = [
    { name: '用户注册数据', downloads: 1234, rating: 4.8 },
    { name: '电商订单数据', downloads: 987, rating: 4.6 },
    { name: '财务流水数据', downloads: 756, rating: 4.5 },
    { name: '商品信息数据', downloads: 543, rating: 4.3 },
]

export function DashboardPage() {
    const growthRate = ((mockStats.generatedThisMonth - mockStats.generatedLastMonth) / mockStats.generatedLastMonth * 100).toFixed(1)
    const isPositiveGrowth = parseFloat(growthRate) > 0

    return (
        <div className="flex-1 overflow-auto p-6">
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-foreground">仪表盘</h1>
                <p className="text-muted-foreground">数据生成平台概览</p>
            </div>

            {/* 统计卡片 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                <StatsCard
                    title="数据生成总量"
                    value={mockStats.totalGenerated.toLocaleString()}
                    icon={<BarChart3 className="h-5 w-5" />}
                    trend={isPositiveGrowth ? 'up' : 'down'}
                    trendValue={`${isPositiveGrowth ? '+' : ''}${growthRate}%`}
                    trendLabel="较上月"
                />
                <StatsCard
                    title="模板数量"
                    value={mockStats.totalTemplates.toString()}
                    icon={<FileJson className="h-5 w-5" />}
                />
                <StatsCard
                    title="团队成员"
                    value={mockStats.totalMembers.toString()}
                    icon={<Users className="h-5 w-5" />}
                />
                <StatsCard
                    title="API 调用次数"
                    value={mockStats.apiCalls.toLocaleString()}
                    icon={<Zap className="h-5 w-5" />}
                    trend="up"
                    trendValue="+12.5%"
                    trendLabel="本周"
                />
            </div>

            {/* 图表和活动区域 */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* 生成趋势图 */}
                <Card className="lg:col-span-2">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <BarChart3 className="h-5 w-5 text-primary" />
                            生成趋势
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="h-64 flex items-end gap-2">
                            {mockTrendData.map((item, index) => {
                                const maxCount = Math.max(...mockTrendData.map(d => d.count))
                                const height = (item.count / maxCount) * 100
                                return (
                                    <div key={index} className="flex-1 flex flex-col items-center gap-2">
                                        <div className="w-full bg-secondary rounded-t-sm relative group">
                                            <div
                                                className="bg-primary rounded-t-sm transition-all hover:bg-primary/80"
                                                style={{ height: `${height * 2}px` }}
                                            />
                                            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-card border border-border rounded px-2 py-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                                                {item.count.toLocaleString()} 条
                                            </div>
                                        </div>
                                        <span className="text-xs text-muted-foreground">
                                            {item.date.split('-')[1]}月
                                        </span>
                                    </div>
                                )
                            })}
                        </div>
                    </CardContent>
                </Card>

                {/* 热门模板 */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Star className="h-5 w-5 text-yellow-400" />
                            热门模板
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                        {popularTemplates.map((template, index) => (
                            <div key={index} className="flex items-center justify-between p-2 rounded-lg hover:bg-secondary transition-colors">
                                <div className="flex items-center gap-3">
                                    <span className="flex h-6 w-6 items-center justify-center rounded-full bg-primary/20 text-xs font-medium text-primary">
                                        {index + 1}
                                    </span>
                                    <span className="text-sm text-foreground">{template.name}</span>
                                </div>
                                <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                    <Star className="h-3 w-3 text-yellow-400 fill-yellow-400" />
                                    {template.rating}
                                </div>
                            </div>
                        ))}
                    </CardContent>
                </Card>
            </div>

            {/* 最近活动 */}
            <Card className="mt-6">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Clock className="h-5 w-5 text-primary" />
                        最近活动
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {mockActivities.map((activity) => (
                            <div key={activity.id} className="flex items-start gap-4">
                                <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary to-green-600 flex items-center justify-center text-xs font-semibold text-primary-foreground flex-shrink-0">
                                    {activity.user.name.charAt(0)}
                                </div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm text-foreground">
                                        <span className="font-medium">{activity.user.name}</span>
                                        <span className="text-muted-foreground"> {activity.action}：</span>
                                        <span className="text-primary">{activity.target}</span>
                                    </p>
                                    <p className="text-xs text-muted-foreground mt-0.5">
                                        {new Date(activity.createdAt).toLocaleString('zh-CN')}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

// 统计卡片组件
interface StatsCardProps {
    title: string
    value: string
    icon: React.ReactNode
    trend?: 'up' | 'down'
    trendValue?: string
    trendLabel?: string
}

function StatsCard({ title, value, icon, trend, trendValue, trendLabel }: StatsCardProps) {
    return (
        <Card>
            <CardContent className="p-4">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-muted-foreground">{title}</span>
                    <div className="h-8 w-8 rounded-lg bg-primary/20 flex items-center justify-center text-primary">
                        {icon}
                    </div>
                </div>
                <div className="flex items-end justify-between">
                    <span className="text-2xl font-bold text-foreground">{value}</span>
                    {trend && trendValue && (
                        <div className={`flex items-center gap-1 text-xs ${trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                            {trend === 'up' ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
                            <span>{trendValue}</span>
                            {trendLabel && <span className="text-muted-foreground">{trendLabel}</span>}
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}
