import { useState, useEffect } from 'react'
import { Header, MobileNav } from './components/layout'
import { Sidebar } from './components/Sidebar'
import { GeneratorPanel } from './components/GeneratorPanel'
import { PreviewPanel } from './components/PreviewPanel'
import {
  DashboardPage,
  HistoryPage,
  TemplateMarketPage,
  DataSourcePage,
  ApiPage,
  RelationPage
} from './pages'
import {
  fetchDataTypes,
  fetchTemplates,
  generateData,
  type DataField,
  type DataType,
  type Template
} from './lib/api'

function App() {
  // 页面状态
  const [activePage, setActivePage] = useState('generator')

  // 数据生成相关状态
  const [fields, setFields] = useState<DataField[]>([
    { id: '1', name: 'id', type: 'uuid' },
    { id: '2', name: 'name', type: 'chineseName' },
    { id: '3', name: 'email', type: 'email' },
    { id: '4', name: 'phone', type: 'chinesePhone' },
  ])
  const [generatedData, setGeneratedData] = useState<Record<string, unknown>[]>([])
  const [recordCount, setRecordCount] = useState(10)
  const [activeCategory, setActiveCategory] = useState('all')
  const [dataTypes, setDataTypes] = useState<DataType[]>([])
  const [templates, setTemplates] = useState<Template[]>([])
  const [isGenerating, setIsGenerating] = useState(false)

  useEffect(() => {
    fetchDataTypes().then(setDataTypes).catch(console.error)
    fetchTemplates().then(setTemplates).catch(console.error)
  }, [])

  const handleGenerate = async () => {
    setIsGenerating(true)
    try {
      const data = await generateData(fields, recordCount)
      setGeneratedData(data)
    } catch (error) {
      console.error('生成失败:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  const filteredDataTypes = activeCategory === 'all'
    ? dataTypes
    : dataTypes.filter(dt => dt.category === activeCategory)

  // 渲染当前页面
  const renderPage = () => {
    switch (activePage) {
      case 'dashboard':
        return <DashboardPage />

      case 'generator':
        return (
          <div className="flex flex-1 overflow-hidden">
            <Sidebar activeCategory={activeCategory} setActiveCategory={setActiveCategory} />
            <main className="flex flex-1 overflow-hidden">
              <GeneratorPanel
                fields={fields}
                setFields={setFields}
                recordCount={recordCount}
                setRecordCount={setRecordCount}
                onGenerate={handleGenerate}
                isGenerating={isGenerating}
                dataTypes={filteredDataTypes}
                templates={templates}
                setTemplates={setTemplates}
              />
              <PreviewPanel data={generatedData} fields={fields} />
            </main>
          </div>
        )

      case 'templates':
        return <TemplateMarketPage onUseTemplate={(template) => {
          // 应用模板
          if (template.fields && template.fields.length > 0) {
            setFields(template.fields)
            setActivePage('generator')
          }
        }} />

      case 'history':
        return <HistoryPage onReuse={(record) => {
          // 复用历史配置
          setFields(record.fields)
          setRecordCount(record.count)
          setActivePage('generator')
        }} />

      case 'datasource':
        return <DataSourcePage />

      case 'api':
        return <ApiPage />

      case 'relation':
        return <RelationPage />

      default:
        return <DashboardPage />
    }
  }

  return (
    <div className="flex h-screen flex-col bg-background">
      <Header activePage={activePage} onPageChange={setActivePage} />
      <div className="flex flex-1 overflow-hidden pb-16 lg:pb-0">
        {renderPage()}
      </div>
      <MobileNav activePage={activePage} onPageChange={setActivePage} />
    </div>
  )
}

export default App
