import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string
    error?: string
    leftIcon?: React.ReactNode
    rightIcon?: React.ReactNode
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
    ({ className, label, error, leftIcon, rightIcon, ...props }, ref) => {
        return (
            <div className="w-full">
                {label && (
                    <label className="mb-1.5 block text-xs font-medium text-muted-foreground">
                        {label}
                    </label>
                )}
                <div className="relative">
                    {leftIcon && (
                        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                            {leftIcon}
                        </div>
                    )}
                    <input
                        ref={ref}
                        className={cn(
                            'w-full rounded-lg border border-border bg-input px-3 py-2 text-sm text-foreground',
                            'placeholder:text-muted-foreground',
                            'focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary/50',
                            'disabled:cursor-not-allowed disabled:opacity-50',
                            leftIcon && 'pl-10',
                            rightIcon && 'pr-10',
                            error && 'border-destructive focus:border-destructive focus:ring-destructive/50',
                            className
                        )}
                        {...props}
                    />
                    {rightIcon && (
                        <div className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground">
                            {rightIcon}
                        </div>
                    )}
                </div>
                {error && (
                    <p className="mt-1 text-xs text-destructive">{error}</p>
                )}
            </div>
        )
    }
)

Input.displayName = 'Input'
