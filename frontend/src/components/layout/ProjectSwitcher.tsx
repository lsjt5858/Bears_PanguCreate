import { useState, useRef, useEffect } from 'react'
import { ChevronDown, Plus, Settings, Users, FolderKanban } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { Project } from '@/lib/types'

// 模拟项目数据
const mockProjects: Project[] = [
    {
        id: '1',
        name: '电商平台测试',
        description: '电商平台相关测试数据',
        members: [],
        createdAt: '2024-01-01T00:00:00.000Z',
        updatedAt: '2024-01-01T00:00:00.000Z',
    },
    {
        id: '2',
        name: '金融系统测试',
        description: '银行核心系统测试数据',
        members: [],
        createdAt: '2024-02-01T00:00:00.000Z',
        updatedAt: '2024-02-01T00:00:00.000Z',
    },
    {
        id: '3',
        name: '用户中心',
        description: '用户中心模块测试数据',
        members: [],
        createdAt: '2024-03-01T00:00:00.000Z',
        updatedAt: '2024-03-01T00:00:00.000Z',
    },
]

interface ProjectSwitcherProps {
    onProjectChange?: (project: Project) => void
    onCreateProject?: () => void
    onProjectSettings?: (project: Project) => void
}

export function ProjectSwitcher({
    onProjectChange,
    onCreateProject,
    onProjectSettings
}: ProjectSwitcherProps) {
    const [isOpen, setIsOpen] = useState(false)
    const [currentProject, setCurrentProject] = useState<Project>(mockProjects[0])
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

    const handleProjectSelect = (project: Project) => {
        setCurrentProject(project)
        onProjectChange?.(project)
        setIsOpen(false)
    }

    return (
        <div className="relative" ref={ref}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 rounded-lg border border-border bg-card px-3 py-2 hover:bg-secondary transition-colors"
            >
                <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary/20">
                    <FolderKanban className="h-4 w-4 text-primary" />
                </div>
                <div className="flex flex-col items-start">
                    <span className="text-sm font-medium text-foreground">{currentProject.name}</span>
                </div>
                <ChevronDown
                    className={cn(
                        'ml-2 h-4 w-4 text-muted-foreground transition-transform',
                        isOpen && 'rotate-180'
                    )}
                />
            </button>

            {/* 下拉菜单 */}
            {isOpen && (
                <div className="absolute left-0 top-full mt-2 w-72 rounded-xl border border-border bg-card shadow-lg z-50 animate-in fade-in slide-in-from-top-2">
                    {/* 项目列表 */}
                    <div className="p-2">
                        <p className="px-2 py-1 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                            项目空间
                        </p>
                        {mockProjects.map((project) => (
                            <div
                                key={project.id}
                                className={cn(
                                    'flex items-center justify-between rounded-lg px-2 py-2 hover:bg-secondary transition-colors group',
                                    currentProject.id === project.id && 'bg-secondary'
                                )}
                            >
                                <button
                                    onClick={() => handleProjectSelect(project)}
                                    className="flex items-center gap-2 flex-1"
                                >
                                    <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary/20">
                                        <FolderKanban className="h-4 w-4 text-primary" />
                                    </div>
                                    <div className="flex flex-col items-start">
                                        <span className="text-sm font-medium text-foreground">{project.name}</span>
                                        <span className="text-xs text-muted-foreground">{project.description}</span>
                                    </div>
                                </button>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation()
                                        onProjectSettings?.(project)
                                    }}
                                    className="p-1 rounded opacity-0 group-hover:opacity-100 hover:bg-muted transition-all"
                                >
                                    <Settings className="h-4 w-4 text-muted-foreground" />
                                </button>
                            </div>
                        ))}
                    </div>

                    {/* 分隔线 */}
                    <div className="border-t border-border" />

                    {/* 操作按钮 */}
                    <div className="p-2">
                        <button
                            onClick={() => {
                                onCreateProject?.()
                                setIsOpen(false)
                            }}
                            className="flex w-full items-center gap-2 rounded-lg px-2 py-2 text-sm text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
                        >
                            <Plus className="h-4 w-4" />
                            创建新项目
                        </button>
                        <button
                            className="flex w-full items-center gap-2 rounded-lg px-2 py-2 text-sm text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
                        >
                            <Users className="h-4 w-4" />
                            成员管理
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}
