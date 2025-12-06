import { Fragment, useEffect } from 'react'
import { X } from 'lucide-react'
import { cn } from '@/lib/utils'

interface ModalProps {
    isOpen: boolean
    onClose: () => void
    title?: string
    description?: string
    children: React.ReactNode
    size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
    showClose?: boolean
}

export function Modal({
    isOpen,
    onClose,
    title,
    description,
    children,
    size = 'md',
    showClose = true,
}: ModalProps) {
    // 阻止背景滚动
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden'
        } else {
            document.body.style.overflow = 'unset'
        }
        return () => {
            document.body.style.overflow = 'unset'
        }
    }, [isOpen])

    // ESC 关闭
    useEffect(() => {
        const handleEsc = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose()
        }
        if (isOpen) {
            window.addEventListener('keydown', handleEsc)
        }
        return () => window.removeEventListener('keydown', handleEsc)
    }, [isOpen, onClose])

    if (!isOpen) return null

    const sizes = {
        sm: 'max-w-sm',
        md: 'max-w-md',
        lg: 'max-w-lg',
        xl: 'max-w-xl',
        full: 'max-w-4xl',
    }

    return (
        <Fragment>
            {/* Backdrop */}
            <div
                className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm animate-in fade-in"
                onClick={onClose}
            />

            {/* Modal */}
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                <div
                    className={cn(
                        'w-full rounded-xl border border-border bg-card shadow-2xl animate-in zoom-in-95 fade-in',
                        sizes[size]
                    )}
                    onClick={(e) => e.stopPropagation()}
                >
                    {/* Header */}
                    {(title || showClose) && (
                        <div className="flex items-start justify-between border-b border-border p-4">
                            <div>
                                {title && (
                                    <h2 className="text-lg font-semibold text-foreground">{title}</h2>
                                )}
                                {description && (
                                    <p className="mt-1 text-sm text-muted-foreground">{description}</p>
                                )}
                            </div>
                            {showClose && (
                                <button
                                    onClick={onClose}
                                    className="rounded-lg p-1 text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
                                >
                                    <X className="h-5 w-5" />
                                </button>
                            )}
                        </div>
                    )}

                    {/* Content */}
                    <div className="p-4">{children}</div>
                </div>
            </div>
        </Fragment>
    )
}

// Modal Footer 组件
interface ModalFooterProps {
    children: React.ReactNode
    className?: string
}

export function ModalFooter({ children, className }: ModalFooterProps) {
    return (
        <div className={cn('flex items-center justify-end gap-2 border-t border-border pt-4 mt-4', className)}>
            {children}
        </div>
    )
}
