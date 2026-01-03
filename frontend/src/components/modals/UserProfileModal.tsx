import { useState, useEffect } from 'react'
import { User, Mail, Shield, Camera } from 'lucide-react'
import { Modal, ModalFooter, Button, Input } from '@/components/common'
import { useAuth } from '@/context/AuthContext'

interface UserProfileModalProps {
    isOpen: boolean
    onClose: () => void
}

export function UserProfileModal({ isOpen, onClose }: UserProfileModalProps) {
    const { user } = useAuth()
    const [isLoading, setIsLoading] = useState(false)
    const [formData, setFormData] = useState({
        nickname: '',
        email: '',
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
    })

    useEffect(() => {
        if (user && isOpen) {
            setFormData(prev => ({
                ...prev,
                nickname: user.nickname || user.username || '',
                email: user.email || '',
                currentPassword: '',
                newPassword: '',
                confirmPassword: ''
            }))
        }
    }, [user, isOpen])

    const handleSave = async () => {
        setIsLoading(true)
        // Simulate API call
        setTimeout(() => {
            setIsLoading(false)
            alert('个人资料更新成功（模拟）')
            onClose()
        }, 1000)
    }

    if (!user) return null

    return (
        <Modal
            isOpen={isOpen}
            onClose={onClose}
            title="个人资料"
            description="管理您的个人账户信息"
            size="md"
        >
            <div className="space-y-6">
                {/* Avatar Section */}
                <div className="flex flex-col items-center justify-center gap-3">
                    <div className="relative group cursor-pointer">
                        <div className="h-24 w-24 rounded-full bg-gradient-to-br from-primary to-green-600 flex items-center justify-center text-2xl font-bold text-primary-foreground overflow-hidden">
                            {user.avatar ? (
                                <img src={user.avatar} alt="Avatar" className="h-full w-full object-cover" />
                            ) : (
                                (user.nickname?.[0] || user.username?.[0] || 'U').toUpperCase()
                            )}
                        </div>
                        <div className="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                            <Camera className="h-8 w-8 text-white" />
                        </div>
                    </div>
                    <div className="text-center">
                        <div className="font-medium">{user.username}</div>
                        <div className="text-xs text-muted-foreground bg-secondary px-2 py-0.5 rounded-full inline-flex items-center gap-1 mt-1">
                            <Shield className="h-3 w-3" />
                            {user.role === 'admin' ? '系统管理员' : '普通用户'}
                        </div>
                    </div>
                </div>

                {/* Form Fields */}
                <div className="space-y-4">
                    <Input
                        label="昵称"
                        value={formData.nickname}
                        onChange={(e) => setFormData({ ...formData, nickname: e.target.value })}
                        placeholder="请输入昵称"
                        leftIcon={<User className="h-4 w-4 text-muted-foreground" />}
                    />

                    <Input
                        label="电子邮箱"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        placeholder="example@email.com"
                        type="email"
                        disabled // Assuming email change needs verified process
                        leftIcon={<Mail className="h-4 w-4 text-muted-foreground" />}
                    />

                    <div className="border-t border-border pt-4 mt-4">
                        <h4 className="text-sm font-medium mb-3">修改密码</h4>
                        <div className="space-y-3">
                            <Input
                                placeholder="当前密码" // Only needed if verifying
                                type="password"
                                value={formData.currentPassword}
                                onChange={(e) => setFormData({ ...formData, currentPassword: e.target.value })}
                            />
                            <div className="grid grid-cols-2 gap-3">
                                <Input
                                    placeholder="新密码"
                                    type="password"
                                    value={formData.newPassword}
                                    onChange={(e) => setFormData({ ...formData, newPassword: e.target.value })}
                                />
                                <Input
                                    placeholder="确认新密码"
                                    type="password"
                                    value={formData.confirmPassword}
                                    onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <ModalFooter>
                <Button variant="ghost" onClick={onClose} disabled={isLoading}>取消</Button>
                <Button variant="primary" onClick={handleSave} disabled={isLoading}>
                    {isLoading ? '保存中...' : '保存更改'}
                </Button>
            </ModalFooter>
        </Modal>
    )
}
