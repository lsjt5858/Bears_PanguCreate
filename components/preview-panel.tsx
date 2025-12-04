"use client"

import { useState } from "react"
import { Copy, FileJson, FileSpreadsheet, FileCode, Check, Table, Code } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { DataField, GeneratedData } from "./data-generator-platform"
import { cn } from "@/lib/utils"

interface PreviewPanelProps {
  data: GeneratedData
  fields: DataField[]
}

export function PreviewPanel({ data, fields }: PreviewPanelProps) {
  const [copied, setCopied] = useState(false)
  const [viewMode, setViewMode] = useState<"table" | "json">("table")

  const copyToClipboard = async (format: "json" | "csv" | "sql") => {
    let content = ""

    if (format === "json") {
      content = JSON.stringify(data, null, 2)
    } else if (format === "csv") {
      const headers = fields.map((f) => f.name).join(",")
      const rows = data.map((row) => fields.map((f) => `"${row[f.name]}"`).join(","))
      content = [headers, ...rows].join("\n")
    } else if (format === "sql") {
      const tableName = "test_data"
      const columns = fields.map((f) => f.name).join(", ")
      const values = data
        .map((row) => {
          const vals = fields.map((f) => `'${row[f.name]}'`).join(", ")
          return `(${vals})`
        })
        .join(",\n")
      content = `INSERT INTO ${tableName} (${columns}) VALUES\n${values};`
    }

    await navigator.clipboard.writeText(content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadData = (format: "json" | "csv" | "sql") => {
    let content = ""
    let mimeType = ""
    let extension = ""

    if (format === "json") {
      content = JSON.stringify(data, null, 2)
      mimeType = "application/json"
      extension = "json"
    } else if (format === "csv") {
      const headers = fields.map((f) => f.name).join(",")
      const rows = data.map((row) => fields.map((f) => `"${row[f.name]}"`).join(","))
      content = [headers, ...rows].join("\n")
      mimeType = "text/csv"
      extension = "csv"
    } else if (format === "sql") {
      const tableName = "test_data"
      const columns = fields.map((f) => f.name).join(", ")
      const values = data
        .map((row) => {
          const vals = fields.map((f) => `'${row[f.name]}'`).join(", ")
          return `(${vals})`
        })
        .join(",\n")
      content = `INSERT INTO ${tableName} (${columns}) VALUES\n${values};`
      mimeType = "text/plain"
      extension = "sql"
    }

    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `generated_data.${extension}`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="hidden flex-1 flex-col overflow-hidden bg-background lg:flex">
      <div className="border-b border-border bg-card p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">数据预览</h2>
            <p className="text-sm text-muted-foreground">
              {data.length > 0 ? `已生成 ${data.length} 条数据` : "配置字段后点击生成"}
            </p>
          </div>
          {data.length > 0 && (
            <div className="flex items-center gap-2">
              <div className="flex rounded-lg border border-border p-1">
                <button
                  onClick={() => setViewMode("table")}
                  className={cn(
                    "flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs transition-colors",
                    viewMode === "table"
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  <Table className="h-3.5 w-3.5" />
                  表格
                </button>
                <button
                  onClick={() => setViewMode("json")}
                  className={cn(
                    "flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs transition-colors",
                    viewMode === "json"
                      ? "bg-primary text-primary-foreground"
                      : "text-muted-foreground hover:text-foreground",
                  )}
                >
                  <Code className="h-3.5 w-3.5" />
                  JSON
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {data.length === 0 ? (
        <div className="flex flex-1 items-center justify-center">
          <div className="text-center">
            <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-muted">
              <FileJson className="h-8 w-8 text-muted-foreground" />
            </div>
            <h3 className="text-lg font-medium text-foreground">暂无数据</h3>
            <p className="mt-1 text-sm text-muted-foreground">在左侧配置字段,然后点击"生成数据"</p>
          </div>
        </div>
      ) : (
        <div className="flex flex-1 flex-col overflow-hidden">
          <div className="flex-1 overflow-auto p-4">
            {viewMode === "table" ? (
              <div className="rounded-lg border border-border overflow-hidden">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border bg-muted/50">
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">#</th>
                      {fields.map((field) => (
                        <th key={field.id} className="px-4 py-3 text-left font-medium text-muted-foreground">
                          {field.name}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.slice(0, 100).map((row, index) => (
                      <tr
                        key={index}
                        className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors"
                      >
                        <td className="px-4 py-3 text-muted-foreground">{index + 1}</td>
                        {fields.map((field) => (
                          <td key={field.id} className="px-4 py-3 text-foreground font-mono text-xs">
                            {String(row[field.name]).slice(0, 30)}
                            {String(row[field.name]).length > 30 && "..."}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
                {data.length > 100 && (
                  <div className="border-t border-border bg-muted/30 px-4 py-2 text-center text-xs text-muted-foreground">
                    仅显示前 100 条,共 {data.length} 条数据
                  </div>
                )}
              </div>
            ) : (
              <pre className="rounded-lg border border-border bg-muted/30 p-4 text-xs text-foreground overflow-auto font-mono">
                {JSON.stringify(data.slice(0, 20), null, 2)}
                {data.length > 20 && "\n\n// ... 更多数据"}
              </pre>
            )}
          </div>

          <div className="border-t border-border bg-card p-4">
            <div className="flex items-center justify-between">
              <p className="text-xs text-muted-foreground">选择导出格式</p>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm" onClick={() => copyToClipboard("json")} className="text-xs">
                  {copied ? <Check className="mr-1.5 h-3.5 w-3.5" /> : <Copy className="mr-1.5 h-3.5 w-3.5" />}
                  复制
                </Button>
                <Button variant="outline" size="sm" onClick={() => downloadData("json")} className="text-xs">
                  <FileJson className="mr-1.5 h-3.5 w-3.5" />
                  JSON
                </Button>
                <Button variant="outline" size="sm" onClick={() => downloadData("csv")} className="text-xs">
                  <FileSpreadsheet className="mr-1.5 h-3.5 w-3.5" />
                  CSV
                </Button>
                <Button variant="outline" size="sm" onClick={() => downloadData("sql")} className="text-xs">
                  <FileCode className="mr-1.5 h-3.5 w-3.5" />
                  SQL
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
