import {
    BarChart3,
    FileJson,
    Users,
    Zap,
    TrendingUp,
    TrendingDown,
    Clock,
    Star,
    Loader2,
    AlertCircle
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common'
import type { DashboardStats, TrendData, ActivityLog } from '@/lib/types'
import { useEffect, useState } from 'react'
import { fetchDashboardStats, fetchTrendData, fetchRecentActivities } from '@/lib/api'

const popularTemplates = [
    { name: '用户注册数据', downloads: 1234, rating: 4.8 },
    { name: '电商订单数据', downloads: 987, rating: 4.6 },
    { name: '财务流水数据', downloads: 756, rating: 4.5 },
    { name: '商品信息数据', downloads: 543, rating: 4.3 },
]

export function DashboardPage() {
    const [stats, setStats] = useState<DashboardStats | null>(null)
    const [trendData, setTrendData] = useState<TrendData[]>([])
    const [activities, setActivities] = useState<ActivityLog[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const loadData = async () => {
            try {
                setLoading(true)
                const [statsData, trend, activitiesData] = await Promise.all([
                    fetchDashboardStats(),
                    fetchTrendData(),
                    fetchRecentActivities()
                ])
                setStats(statsData)
                setTrendData(trend)
                setActivities(activitiesData)
                setError(null)
            } catch (err) {
                console.error(err)
                setError('无法加载仪表盘数据，请稍后重试。')
            } finally {
                setLoading(false)
            }
        }
        loadData()
    }, [])

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center h-full">
                <div className="flex flex-col items-center gap-2 text-muted-foreground">
                    <Loader2 className="h-8 w-8 animate-spin" />
                    <p>正在加载数据...</p>
                </div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="flex-1 flex items-center justify-center h-full p-6">
                <Card className="max-w-md w-full border-destructive/50">
                    <CardContent className="flex flex-col items-center gap-4 p-6 text-center">
                        <AlertCircle className="h-10 w-10 text-destructive" />
                        <div className="space-y-2">
                            <h3 className="font-bold">加载失败</h3>
                            <p className="text-sm text-muted-foreground">{error}</p>
                        </div>
                        <button
                            onClick={() => window.location.reload()}
                            className="text-sm text-primary hover:underline"
                        >
                            重试
                        </button>
                    </CardContent>
                </Card>
            </div>
        )
    }

    if (!stats) return null

    const growthRate = stats.generatedLastMonth > 0
        ? ((stats.generatedThisMonth - stats.generatedLastMonth) / stats.generatedLastMonth * 100).toFixed(1)
        : '100.0'
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
                    value={stats.totalGenerated.toLocaleString()}
                    icon={<BarChart3 className="h-5 w-5" />}
                    trend={isPositiveGrowth ? 'up' : 'down'}
                    trendValue={`${isPositiveGrowth ? '+' : ''}${growthRate}%`}
                    trendLabel="较上月"
                />
                <StatsCard
                    title="模板数量"
                    value={stats.totalTemplates.toString()}
                    icon={<FileJson className="h-5 w-5" />}
                />
                <StatsCard
                    title="团队成员"
                    value={stats.totalMembers.toString()}
                    icon={<Users className="h-5 w-5" />}
                />
                <StatsCard
                    title="API 调用次数"
                    value={stats.apiCalls.toLocaleString()}
                    icon={<Zap className="h-5 w-5" />}
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
                        <div className="h-64 flex items-end gap-2 px-2">
                            {trendData.length > 0 ? (
                                trendData.map((item, index) => {
                                    const maxCount = Math.max(...trendData.map(d => d.count))
                                    const height = maxCount > 0 ? (item.count / maxCount) * 100 : 0
                                    return (
                                        <div key={index} className="flex-1 flex flex-col items-center gap-2 h-full">
                                            <div className="w-full bg-secondary/20 rounded-t-sm relative group h-full flex items-end">
                                                <div
                                                    className="w-full bg-primary rounded-t-sm transition-all hover:bg-primary/80"
                                                    style={{ height: `${height}%` }}
                                                />
                                                <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-card border border-border rounded px-2 py-1 text-xs opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 shadow-sm">
                                                    <p className="font-bold">{item.count.toLocaleString()} 条</p>
                                                    <p className="text-[10px] text-muted-foreground">{item.date}</p>
                                                </div>
                                            </div>
                                        </div>
                                    )
                                })
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-muted-foreground text-sm">
                                    暂无趋势数据
                                </div>
                            )}
                        </div>
                        {trendData.length > 0 && (
                            <div className="flex justify-between mt-4 text-xs text-muted-foreground px-2">
                                <span>{trendData[0].date}</span>
                                <span>{trendData[trendData.length - 1].date}</span>
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* 热门模板 (暂保留Mock数据，因为API尚不支持) */}
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
                        {activities.length > 0 ? (
                            activities.map((activity) => (
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
                            ))
                        ) : (
                            <div className="text-center py-4 text-muted-foreground text-sm">
                                暂无最近活动
                            </div>
                        )}
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
