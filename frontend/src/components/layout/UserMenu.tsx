import { useState, useRef, useEffect } from 'react'
import { ChevronDown, User, Settings, Key, LogOut, Shield } from 'lucide-react'
import { cn } from '@/lib/utils'
import { useAuth } from '@/context/AuthContext'

const roleLabels: Record<string, string> = {
    admin: '管理员',
    lead: '负责人',
    member: '成员',
    user: '用户'
}

const roleBadgeColors: Record<string, string> = {
    admin: 'bg-red-500/20 text-red-400',
    lead: 'bg-yellow-500/20 text-yellow-400',
    member: 'bg-blue-500/20 text-blue-400',
    user: 'bg-gray-500/20 text-gray-400'
}

interface UserMenuProps {
    onProfileClick?: () => void
    onApiKeysClick?: () => void
    onSettingsClick?: () => void
}

export function UserMenu({ onProfileClick, onApiKeysClick, onSettingsClick }: UserMenuProps) {
    const { user, logout } = useAuth()
    const [isOpen, setIsOpen] = useState(false)
    const ref = useRef<HTMLDivElement>(null)

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    if (!user) return null

    // 如果用户没有角色，默认为 member/user
    const userRole = (user.role || 'user') as string
    const displayName = user.nickname || user.username || '用户'
    const displayEmail = user.email

    const menuItems = [
        { icon: User, label: '个人资料', onClick: onProfileClick },
        { icon: Key, label: 'API 密钥', onClick: onApiKeysClick },
        { icon: Settings, label: '设置', onClick: onSettingsClick },
        { divider: true },
        { icon: LogOut, label: '退出登录', onClick: logout, danger: true },
    ]

    return (
        <div className="relative" ref={ref}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 rounded-lg px-2 py-1.5 hover:bg-secondary transition-colors"
            >
                {/* 头像 */}
                <div className="h-8 w-8 rounded-full bg-gradient-to-br from-primary to-green-600 flex items-center justify-center text-xs font-semibold text-primary-foreground overflow-hidden">
                    {user.avatar ? (
                        <img src={user.avatar} alt={displayName} className="h-full w-full object-cover" />
                    ) : (
                        displayName.charAt(0).toUpperCase()
                    )}
                </div>

                {/* 用户信息 - 仅在大屏显示 */}
                <div className="hidden md:flex flex-col items-start text-left">
                    <span className="text-sm font-medium text-foreground max-w-[100px] truncate">{displayName}</span>
                    <span className={cn('text-xs px-1.5 py-0.5 rounded-full flex items-center', roleBadgeColors[userRole] || roleBadgeColors.user)}>
                        <Shield className="h-3 w-3 mr-0.5" />
                        {roleLabels[userRole] || userRole}
                    </span>
                </div>

                <ChevronDown className={cn('h-4 w-4 text-muted-foreground transition-transform', isOpen && 'rotate-180')} />
            </button>

            {/* 下拉菜单 */}
            {isOpen && (
                <div className="absolute right-0 top-full mt-2 w-56 rounded-xl border border-border bg-card shadow-lg py-1 z-50 animate-in fade-in slide-in-from-top-2">
                    {/* 用户信息头部 */}
                    <div className="px-3 py-2 border-b border-border">
                        <p className="text-sm font-medium text-foreground truncate">{displayName}</p>
                        <p className="text-xs text-muted-foreground truncate">{displayEmail}</p>
                    </div>

                    {/* 菜单项 */}
                    <div className="py-1">
                        {menuItems.map((item, index) => {
                            if ('divider' in item && item.divider) {
                                return <div key={index} className="my-1 border-t border-border" />
                            }
                            // @ts-ignore
                            const Icon = item.icon
                            return (
                                <button
                                    key={index}
                                    onClick={() => {
                                        // @ts-ignore
                                        item.onClick?.()
                                        setIsOpen(false)
                                    }}
                                    className={cn(
                                        'flex w-full items-center gap-2 px-3 py-2 text-sm transition-colors',
                                        // @ts-ignore
                                        item.danger
                                            ? 'text-destructive hover:bg-destructive/10'
                                            : 'text-foreground hover:bg-secondary'
                                    )}
                                >
                                    <Icon className="h-4 w-4" />
                                    {/* @ts-ignore */}
                                    {item.label}
                                </button>
                            )
                        })}
                    </div>
                </div>
            )}
        </div>
    )
}
