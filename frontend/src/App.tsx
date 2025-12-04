import { useState, useEffect } from 'react'
import { Header } from './components/Header'
import { Sidebar } from './components/Sidebar'
import { GeneratorPanel } from './components/GeneratorPanel'
import { PreviewPanel } from './components/PreviewPanel'
import { fetchDataTypes, fetchTemplates, generateData, type DataField, type DataType, type Template } from './lib/api'

function App() {
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
    fetchDataTypes().then(setDataTypes)
    fetchTemplates().then(setTemplates)
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
            onGenerate={handleGenerate}
            isGenerating={isGenerating}
            dataTypes={filteredDataTypes}
            templates={templates}
            setTemplates={setTemplates}
          />
          <PreviewPanel data={generatedData} fields={fields} />
        </main>
      </div>
    </div>
  )
}

export default App
