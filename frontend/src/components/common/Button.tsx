import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'default' | 'primary' | 'secondary' | 'ghost' | 'destructive' | 'outline'
    size?: 'sm' | 'md' | 'lg' | 'icon'
    loading?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'default', size = 'md', loading, disabled, children, ...props }, ref) => {
        const baseStyles = 'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50 disabled:cursor-not-allowed'

        const variants = {
            default: 'bg-card border border-border text-foreground hover:bg-secondary',
            primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
            secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
            ghost: 'text-muted-foreground hover:text-foreground hover:bg-secondary',
            destructive: 'bg-destructive text-white hover:bg-destructive/90',
            outline: 'border border-border text-foreground hover:bg-secondary',
        }

        const sizes = {
            sm: 'h-8 px-3 text-xs',
            md: 'h-9 px-4 text-sm',
            lg: 'h-10 px-6 text-sm',
            icon: 'h-9 w-9',
        }

        return (
            <button
                ref={ref}
                className={cn(baseStyles, variants[variant], sizes[size], className)}
                disabled={disabled || loading}
                {...props}
            >
                {loading && (
                    <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                )}
                {children}
            </button>
        )
    }
)

Button.displayName = 'Button'
