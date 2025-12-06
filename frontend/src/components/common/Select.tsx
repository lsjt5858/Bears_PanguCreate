import { useState, useRef, useEffect } from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'

interface SelectOption {
    value: string
    label: string
    icon?: React.ReactNode
}

interface SelectProps {
    value: string
    onChange: (value: string) => void
    options: SelectOption[]
    placeholder?: string
    label?: string
    className?: string
    disabled?: boolean
}

export function Select({
    value,
    onChange,
    options,
    placeholder = '请选择',
    label,
    className,
    disabled,
}: SelectProps) {
    const [isOpen, setIsOpen] = useState(false)
    const ref = useRef<HTMLDivElement>(null)

    const selectedOption = options.find((opt) => opt.value === value)

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    return (
        <div className={cn('w-full', className)} ref={ref}>
            {label && (
                <label className="mb-1.5 block text-xs font-medium text-muted-foreground">
                    {label}
                </label>
            )}
            <div className="relative">
                <button
                    type="button"
                    onClick={() => !disabled && setIsOpen(!isOpen)}
                    disabled={disabled}
                    className={cn(
                        'flex w-full items-center justify-between rounded-lg border border-border bg-input px-3 py-2 text-sm',
                        'focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary/50',
                        'disabled:cursor-not-allowed disabled:opacity-50',
                        isOpen && 'border-primary ring-1 ring-primary/50'
                    )}
                >
                    <span className={cn(!selectedOption && 'text-muted-foreground')}>
                        {selectedOption ? (
                            <span className="flex items-center gap-2">
                                {selectedOption.icon}
                                {selectedOption.label}
                            </span>
                        ) : (
                            placeholder
                        )}
                    </span>
                    <ChevronDown
                        className={cn(
                            'h-4 w-4 text-muted-foreground transition-transform',
                            isOpen && 'rotate-180'
                        )}
                    />
                </button>

                {isOpen && (
                    <div className="absolute z-50 mt-1 w-full rounded-lg border border-border bg-card py-1 shadow-lg animate-in fade-in slide-in-from-top-2">
                        {options.map((option) => (
                            <button
                                key={option.value}
                                type="button"
                                onClick={() => {
                                    onChange(option.value)
                                    setIsOpen(false)
                                }}
                                className={cn(
                                    'flex w-full items-center gap-2 px-3 py-2 text-sm text-foreground hover:bg-secondary',
                                    option.value === value && 'bg-secondary font-medium'
                                )}
                            >
                                {option.icon}
                                {option.label}
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
