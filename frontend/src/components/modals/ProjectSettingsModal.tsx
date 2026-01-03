import { useState, useEffect } from 'react'
import { FolderKanban, Users, Trash2, ShieldAlert, Plus } from 'lucide-react'
import { Modal, ModalFooter, Button, Input, Tabs, TabsList, TabsTrigger, TabsContent, Badge } from '@/components/common'
import type { Project } from '@/lib/types'

interface ProjectSettingsModalProps {
    project: Project | null
    isOpen: boolean
    onClose: () => void
    onUpdate?: (project: Project) => void
}

export function ProjectSettingsModal({ project, isOpen, onClose }: ProjectSettingsModalProps) {
    const [activeTab, setActiveTab] = useState('general')
    const [isLoading, setIsLoading] = useState(false)
    const [formData, setFormData] = useState({
        name: '',
        description: ''
    })

    useEffect(() => {
        if (project && isOpen) {
            setFormData({
                name: project.name,
                description: project.description
            })
        }
    }, [project, isOpen])

    const handleSave = async () => {
        setIsLoading(true)
        // Simulate API call
        setTimeout(() => {
            setIsLoading(false)
            alert('项目设置已更新（模拟）')
            onClose()
        }, 1000)
    }

    if (!project) return null

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title="项目设置"
            size="lg"
        >
            <Tabs value={activeTab} onChange={setActiveTab} className="h-full">
                <div className="mb-4">
                    <TabsList>
                        <TabsTrigger value="general" icon={<FolderKanban className="h-4 w-4" />}>
                            常规设置
                        </TabsTrigger>
                        <TabsTrigger value="members" icon={<Users className="h-4 w-4" />}>
                            成员管理
                        </TabsTrigger>
                        <TabsTrigger value="advanced" className="text-destructive hover:bg-destructive/10 hover:text-destructive" icon={<ShieldAlert className="h-4 w-4" />}>
                            高级选项
                        </TabsTrigger>
                    </TabsList>
                </div>

                <div className="min-h-[300px]">
                    <TabsContent value="general">
                        <div className="space-y-4">
                            <Input
                                label="项目名称"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                placeholder="请输入项目名称"
                            />
                            <div className="space-y-1">
                                <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                                    项目描述
                                </label>
                                <textarea
                                    className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    placeholder="描述项目的用途..."
                                />
                            </div>
                        </div>
                    </TabsContent>

                    <TabsContent value="members">
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h3 className="text-sm font-medium">项目成员 ({project.members?.length || 0})</h3>
                                <Button size="sm" variant="outline">
                                    <Plus className="h-4 w-4 mr-1" />
                                    邀请成员
                                </Button>
                            </div>

                            <div className="rounded-lg border border-border divide-y divide-border">
                                {project.members && project.members.length > 0 ? (
                                    project.members.map((member) => (
                                        <div key={member.userId} className="flex items-center justify-between p-3">
                                            <div className="flex items-center gap-3">
                                                <div className="h-8 w-8 rounded-full bg-primary/20 flex items-center justify-center text-xs font-medium text-primary">
                                                    {member.user?.name?.[0] || 'U'}
                                                </div>
                                                <div>
                                                    <div className="text-sm font-medium">{member.user?.name || 'Unknown'}</div>
                                                    <div className="text-xs text-muted-foreground">{member.user?.email || 'No email'}</div>
                                                </div>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <Badge variant="outline">{member.role}</Badge>
                                                {member.role !== 'admin' && (
                                                    <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive">
                                                        <Trash2 className="h-4 w-4" />
                                                    </Button>
                                                )}
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="p-8 text-center text-muted-foreground">
                                        暂无成员
                                    </div>
                                )}
                            </div>
                        </div>
                    </TabsContent>

                    <TabsContent value="advanced">
                        <div className="rounded-lg border border-destructive/50 bg-destructive/5 p-4">
                            <h3 className="text-sm font-medium text-destructive flex items-center gap-2 mb-2">
                                <ShieldAlert className="h-4 w-4" />
                                危险区域
                            </h3>
                            <p className="text-sm text-destructive/80 mb-4">
                                删除项目是不可逆的操作。所有相关的数据、模板和历史记录都将被永久删除。
                            </p>
                            <Button variant="destructive" className="w-full sm:w-auto">
                                删除项目
                            </Button>
                        </div>
                    </TabsContent>
                </div>
            </Tabs>

            <ModalFooter>
                <Button variant="ghost" onClick={onClose} disabled={isLoading}>取消</Button>
                {activeTab === 'general' && (
                    <Button variant="primary" onClick={handleSave} disabled={isLoading}>
                        {isLoading ? '保存中...' : '保存更改'}
                    </Button>
                )}
            </ModalFooter>
        </Modal>
    )
}
