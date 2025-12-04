import { Database, Settings, HelpCircle, Bell } from 'lucide-react'

export function Header() {
  return (
    <header className="flex h-14 items-center justify-between border-b border-border bg-card px-6">
      <div className="flex items-center gap-3">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
          <Database className="h-4 w-4 text-primary-foreground" />
        </div>
        <h1 className="text-lg font-semibold text-foreground">DataForge</h1>
        <span className="ml-2 rounded-full bg-primary/20 px-2 py-0.5 text-xs font-medium text-primary">Enterprise</span>
      </div>

      <nav className="hidden items-center gap-6 md:flex">
        <a href="#" className="text-sm font-medium text-foreground border-b-2 border-primary pb-1">数据生成</a>
        <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors">模板管理</a>
        <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors">历史记录</a>
        <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors">API 文档</a>
      </nav>

      <div className="flex items-center gap-2">
        <button className="p-2 text-muted-foreground hover:text-foreground"><Bell className="h-4 w-4" /></button>
        <button className="p-2 text-muted-foreground hover:text-foreground"><HelpCircle className="h-4 w-4" /></button>
        <button className="p-2 text-muted-foreground hover:text-foreground"><Settings className="h-4 w-4" /></button>
        <div className="ml-2 h-8 w-8 rounded-full bg-gradient-to-br from-primary to-green-600 flex items-center justify-center text-xs font-semibold text-primary-foreground">测</div>
      </div>
    </header>
  )
}
