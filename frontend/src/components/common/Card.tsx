import { cn } from '@/lib/utils'

interface CardProps {
    children: React.ReactNode
    className?: string
    hover?: boolean
    onClick?: () => void
}

export function Card({ children, className, hover = false, onClick }: CardProps) {
    return (
        <div
            className={cn(
                'rounded-xl border border-border bg-card',
                hover && 'cursor-pointer transition-colors hover:border-primary/50 hover:bg-card/80',
                onClick && 'cursor-pointer',
                className
            )}
            onClick={onClick}
        >
            {children}
        </div>
    )
}

interface CardHeaderProps {
    children: React.ReactNode
    className?: string
}

export function CardHeader({ children, className }: CardHeaderProps) {
    return (
        <div className={cn('border-b border-border p-4', className)}>
            {children}
        </div>
    )
}

interface CardTitleProps {
    children: React.ReactNode
    className?: string
}

export function CardTitle({ children, className }: CardTitleProps) {
    return (
        <h3 className={cn('text-lg font-semibold text-foreground', className)}>
            {children}
        </h3>
    )
}

interface CardDescriptionProps {
    children: React.ReactNode
    className?: string
}

export function CardDescription({ children, className }: CardDescriptionProps) {
    return (
        <p className={cn('mt-1 text-sm text-muted-foreground', className)}>
            {children}
        </p>
    )
}

interface CardContentProps {
    children: React.ReactNode
    className?: string
}

export function CardContent({ children, className }: CardContentProps) {
    return <div className={cn('p-4', className)}>{children}</div>
}

interface CardFooterProps {
    children: React.ReactNode
    className?: string
}

export function CardFooter({ children, className }: CardFooterProps) {
    return (
        <div className={cn('border-t border-border p-4', className)}>
            {children}
        </div>
    )
}
