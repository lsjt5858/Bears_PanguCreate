"use client"

import { useState } from "react"
import { Sidebar } from "./sidebar"
import { GeneratorPanel } from "./generator-panel"
import { PreviewPanel } from "./preview-panel"
import { Header } from "./header"
import type { Template } from "./template-manager"

export type DataField = {
  id: string
  name: string
  type: string
  options?: Record<string, unknown>
}

export type GeneratedData = Record<string, unknown>[]

const defaultTemplates: Template[] = [
  {
    id: "default-1",
    name: "用户注册数据",
    description: "包含用户注册所需的基本信息字段",
    category: "user",
    fields: [
      { id: "d1-1", name: "user_id", type: "uuid" },
      { id: "d1-2", name: "username", type: "chineseName" },
      { id: "d1-3", name: "email", type: "email" },
      { id: "d1-4", name: "phone", type: "chinesePhone" },
      { id: "d1-5", name: "password", type: "string" },
      { id: "d1-6", name: "created_at", type: "datetime" },
    ],
    createdAt: "2024-01-01T00:00:00.000Z",
    updatedAt: "2024-01-01T00:00:00.000Z",
  },
  {
    id: "default-2",
    name: "电商订单数据",
    description: "电商平台订单测试数据模板",
    category: "order",
    fields: [
      { id: "d2-1", name: "order_id", type: "uuid" },
      { id: "d2-2", name: "customer_name", type: "chineseName" },
      { id: "d2-3", name: "total_amount", type: "amount" },
      { id: "d2-4", name: "shipping_address", type: "chineseAddress" },
      { id: "d2-5", name: "order_date", type: "datetime" },
      { id: "d2-6", name: "phone", type: "chinesePhone" },
    ],
    createdAt: "2024-01-01T00:00:00.000Z",
    updatedAt: "2024-01-01T00:00:00.000Z",
  },
  {
    id: "default-3",
    name: "商品信息数据",
    description: "商品基础信息测试数据",
    category: "product",
    fields: [
      { id: "d3-1", name: "product_id", type: "uuid" },
      { id: "d3-2", name: "product_name", type: "word" },
      { id: "d3-3", name: "price", type: "amount" },
      { id: "d3-4", name: "description", type: "sentence" },
      { id: "d3-5", name: "created_at", type: "datetime" },
    ],
    createdAt: "2024-01-01T00:00:00.000Z",
    updatedAt: "2024-01-01T00:00:00.000Z",
  },
  {
    id: "default-4",
    name: "财务流水数据",
    description: "财务交易流水测试数据",
    category: "finance",
    fields: [
      { id: "d4-1", name: "transaction_id", type: "uuid" },
      { id: "d4-2", name: "account_name", type: "chineseName" },
      { id: "d4-3", name: "bank_card", type: "bankCard" },
      { id: "d4-4", name: "amount", type: "amount" },
      { id: "d4-5", name: "transaction_time", type: "datetime" },
    ],
    createdAt: "2024-01-01T00:00:00.000Z",
    updatedAt: "2024-01-01T00:00:00.000Z",
  },
]

export function DataGeneratorPlatform() {
  const [fields, setFields] = useState<DataField[]>([
    { id: "1", name: "id", type: "uuid" },
    { id: "2", name: "name", type: "chineseName" },
    { id: "3", name: "email", type: "email" },
    { id: "4", name: "phone", type: "chinesePhone" },
  ])
  const [generatedData, setGeneratedData] = useState<GeneratedData>([])
  const [recordCount, setRecordCount] = useState(10)
  const [activeCategory, setActiveCategory] = useState("all")
  const [templates, setTemplates] = useState<Template[]>(defaultTemplates)

  return (
    <div className="flex h-screen flex-col bg-background">
      <Header />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
        <main className="flex flex-1 overflow-hidden">
          <GeneratorPanel
            fields={fields}
            setFields={setFields}
            recordCount={recordCount}
            setRecordCount={setRecordCount}
            setGeneratedData={setGeneratedData}
            activeCategory={activeCategory}
            templates={templates}
            setTemplates={setTemplates}
          />
          <PreviewPanel data={generatedData} fields={fields} />
        </main>
      </div>
    </div>
  )
}
