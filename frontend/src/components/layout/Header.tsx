import {
    Database,
    Settings,
    HelpCircle,
    Bell,
    LayoutDashboard,
    FileJson,
    History,
    Store,
    Server,
    Key,
    Link2
} from 'lucide-react'
import { UserMenu } from './UserMenu'
import { ProjectSwitcher } from './ProjectSwitcher'
import { cn } from '@/lib/utils'

type NavItem = {
    id: string
    label: string
    icon: typeof LayoutDashboard
}

const navItems: NavItem[] = [
    { id: 'dashboard', label: '仪表盘', icon: LayoutDashboard },
    { id: 'generator', label: '数据生成', icon: FileJson },
    { id: 'relation', label: '关联数据', icon: Link2 },
    { id: 'templates', label: '模板市场', icon: Store },
    { id: 'history', label: '历史记录', icon: History },
    { id: 'datasource', label: '数据源', icon: Server },
    { id: 'api', label: 'API', icon: Key },
]

interface HeaderProps {
    activePage: string
    onPageChange: (page: string) => void
}

export function Header({ activePage, onPageChange }: HeaderProps) {
    return (
        <header className="flex h-14 items-center justify-between border-b border-border bg-card px-4 lg:px-6">
            {/* 左侧: Logo + 项目切换 */}
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
                        <Database className="h-4 w-4 text-primary-foreground" />
                    </div>
                    <h1 className="text-lg font-semibold text-foreground hidden sm:block">盘古</h1>
                    <span className="hidden sm:inline-flex ml-1 rounded-full bg-primary/20 px-2 py-0.5 text-xs font-medium text-primary">
                        Enterprise
                    </span>
                </div>

                <div className="hidden md:block">
                    <ProjectSwitcher />
                </div>
            </div>

            {/* 中间: 导航 */}
            <nav className="hidden lg:flex items-center gap-1">
                {navItems.map((item) => {
                    const Icon = item.icon
                    const isActive = activePage === item.id
                    return (
                        <button
                            key={item.id}
                            onClick={() => onPageChange(item.id)}
                            className={cn(
                                'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-colors',
                                isActive
                                    ? 'bg-secondary text-foreground font-medium'
                                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                            )}
                        >
                            <Icon className="h-4 w-4" />
                            {item.label}
                        </button>
                    )
                })}
            </nav>

            {/* 右侧: 操作按钮 + 用户菜单 */}
            <div className="flex items-center gap-2">
                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-secondary rounded-lg transition-colors relative">
                    <Bell className="h-4 w-4" />
                    <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-primary" />
                </button>
                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-secondary rounded-lg transition-colors hidden sm:block">
                    <HelpCircle className="h-4 w-4" />
                </button>
                <button className="p-2 text-muted-foreground hover:text-foreground hover:bg-secondary rounded-lg transition-colors hidden sm:block">
                    <Settings className="h-4 w-4" />
                </button>

                <div className="ml-2">
                    <UserMenu />
                </div>
            </div>
        </header>
    )
}

// 移动端底部导航
interface MobileNavProps {
    activePage: string
    onPageChange: (page: string) => void
}

export function MobileNav({ activePage, onPageChange }: MobileNavProps) {
    const mobileNavItems = navItems.slice(0, 5)

    return (
        <nav className="lg:hidden fixed bottom-0 left-0 right-0 bg-card border-t border-border px-2 py-2 z-50">
            <div className="flex items-center justify-around">
                {mobileNavItems.map((item) => {
                    const Icon = item.icon
                    const isActive = activePage === item.id
                    return (
                        <button
                            key={item.id}
                            onClick={() => onPageChange(item.id)}
                            className={cn(
                                'flex flex-col items-center gap-1 px-3 py-1.5 rounded-lg transition-colors',
                                isActive
                                    ? 'text-primary'
                                    : 'text-muted-foreground'
                            )}
                        >
                            <Icon className="h-5 w-5" />
                            <span className="text-xs">{item.label}</span>
                        </button>
                    )
                })}
            </div>
        </nav>
    )
}
