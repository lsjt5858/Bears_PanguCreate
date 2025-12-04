"use client"

import {
  User,
  MapPin,
  CreditCard,
  ShoppingCart,
  Calendar,
  Hash,
  Globe,
  Building2,
  FileText,
  Layers,
} from "lucide-react"
import { cn } from "@/lib/utils"

const categories = [
  { id: "all", name: "全部类型", icon: Layers },
  { id: "personal", name: "个人信息", icon: User },
  { id: "address", name: "地址位置", icon: MapPin },
  { id: "finance", name: "金融数据", icon: CreditCard },
  { id: "commerce", name: "电商数据", icon: ShoppingCart },
  { id: "datetime", name: "日期时间", icon: Calendar },
  { id: "identifier", name: "标识符", icon: Hash },
  { id: "internet", name: "互联网", icon: Globe },
  { id: "company", name: "企业信息", icon: Building2 },
  { id: "text", name: "文本内容", icon: FileText },
]

interface SidebarProps {
  activeCategory: string
  setActiveCategory: (category: string) => void
}

export function Sidebar({ activeCategory, setActiveCategory }: SidebarProps) {
  return (
    <aside className="hidden w-56 flex-shrink-0 border-r border-border bg-sidebar lg:block">
      <div className="p-4">
        <div className="relative">
          <input
            type="text"
            placeholder="搜索数据类型..."
            className="w-full rounded-lg border border-border bg-input px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <kbd className="absolute right-2 top-1/2 -translate-y-1/2 rounded border border-border bg-muted px-1.5 text-xs text-muted-foreground">
            ⌘K
          </kbd>
        </div>
      </div>

      <nav className="px-2 pb-4">
        <div className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">数据分类</div>
        {categories.map((category) => {
          const Icon = category.icon
          const isActive = activeCategory === category.id
          return (
            <button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              className={cn(
                "flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                  : "text-muted-foreground hover:bg-sidebar-accent/50 hover:text-foreground",
              )}
            >
              <Icon className="h-4 w-4" />
              {category.name}
            </button>
          )
        })}
      </nav>

      <div className="border-t border-border p-4">
        <div className="rounded-lg border border-dashed border-border bg-muted/30 p-4 text-center">
          <p className="text-xs text-muted-foreground">已生成数据</p>
          <p className="mt-1 text-2xl font-bold text-foreground">12,847</p>
          <p className="text-xs text-muted-foreground">本月</p>
        </div>
      </div>
    </aside>
  )
}
