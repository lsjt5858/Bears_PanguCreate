import { cn } from '@/lib/utils'

interface TabsProps {
    value: string
    onChange: (value: string) => void
    children: React.ReactNode
    className?: string
}

export function Tabs({ value, onChange, children, className }: TabsProps) {
    return (
        <div className={cn('', className)}>
            <TabsContext.Provider value={{ value, onChange }}>
                {children}
            </TabsContext.Provider>
        </div>
    )
}

interface TabsListProps {
    children: React.ReactNode
    className?: string
}

export function TabsList({ children, className }: TabsListProps) {
    return (
        <div
            className={cn(
                'inline-flex items-center gap-1 rounded-lg border border-border bg-muted/50 p-1',
                className
            )}
        >
            {children}
        </div>
    )
}

interface TabsTriggerProps {
    value: string
    children: React.ReactNode
    className?: string
    icon?: React.ReactNode
}

export function TabsTrigger({ value, children, className, icon }: TabsTriggerProps) {
    const context = useTabsContext()
    const isActive = context.value === value

    return (
        <button
            type="button"
            onClick={() => context.onChange(value)}
            className={cn(
                'inline-flex items-center gap-2 rounded-md px-3 py-1.5 text-sm font-medium transition-colors',
                isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary',
                className
            )}
        >
            {icon}
            {children}
        </button>
    )
}

interface TabsContentProps {
    value: string
    children: React.ReactNode
    className?: string
}

export function TabsContent({ value, children, className }: TabsContentProps) {
    const context = useTabsContext()

    if (context.value !== value) return null

    return <div className={cn('mt-4', className)}>{children}</div>
}

// Context
import { createContext, useContext } from 'react'

interface TabsContextValue {
    value: string
    onChange: (value: string) => void
}

const TabsContext = createContext<TabsContextValue | null>(null)

function useTabsContext() {
    const context = useContext(TabsContext)
    if (!context) {
        throw new Error('Tabs components must be used within a Tabs provider')
    }
    return context
}
