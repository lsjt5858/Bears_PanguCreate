import { cn } from '@/lib/utils'

type BadgeVariant = 'default' | 'primary' | 'success' | 'warning' | 'error' | 'outline'

interface BadgeProps {
    children: React.ReactNode
    variant?: BadgeVariant
    className?: string
}

export function Badge({ children, variant = 'default', className }: BadgeProps) {
    const variants: Record<BadgeVariant, string> = {
        default: 'bg-secondary text-secondary-foreground',
        primary: 'bg-primary/20 text-primary',
        success: 'bg-green-500/20 text-green-400',
        warning: 'bg-yellow-500/20 text-yellow-400',
        error: 'bg-red-500/20 text-red-400',
        outline: 'border border-border text-muted-foreground',
    }

    return (
        <span
            className={cn(
                'inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium',
                variants[variant],
                className
            )}
        >
            {children}
        </span>
    )
}
