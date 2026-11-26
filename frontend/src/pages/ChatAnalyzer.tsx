import { useState, useEffect } from 'react'
import api from '../services/api'
import { analyzeSelected } from '../services/imports'
import { Upload, Bot, FileText, CheckCircle, RefreshCw } from 'lucide-react'

export default function ChatAnalyzer() {
  const [file, setFile] = useState<File | null>(null)
  const [conversations, setConversations] = useState<any[]>([])
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set())
  const [analyses, setAnalyses] = useState<any[]>([])
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState<any>(null)

  useEffect(() => {
    loadConversations()
    loadAnalyses()
  }, [])

  const loadConversations = async () => {
    try {
      const res = await api.get('/conversations/')
      setConversations(res.data)
    } catch (err) {
      console.error('Failed to load conversations', err)
    }
  }

  const loadAnalyses = async () => {
    try {
      const res = await api.get('/analysis/')
      setAnalyses(res.data)
    } catch (err) {
      console.error('Failed to load analyses', err)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setFile(e.target.files[0])
  }

  const handleImport = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    try {
      // First create a source
      const sourceRes = await api.post('/sources/', { source_type: 'chatgpt' })
      const res = await api.post('/imports/import/chatgpt', formData, {
        params: { source_id: sourceRes.data.id },
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setConversations(res.data.conversations || [])
      setFile(null)
    } catch (err) {
      alert('Import failed')
    }
  }

  const toggleSelection = (id: string) => {
    const newSet = new Set(selectedIds)
    if (newSet.has(id)) newSet.delete(id)
    else newSet.add(id)
    setSelectedIds(newSet)
  }

  const handleAnalyze = async () => {
    if (selectedIds.size === 0) return
    setAnalyzing(true)
    try {
      const res = await analyzeSelected(Array.from(selectedIds))
      setAnalysisResult(res.data.result)
      setAnalyzing(false)
      loadAnalyses()
    } catch (err) {
      alert('Analysis failed')
      setAnalyzing(false)
    }
  }

  const isSelected = (id: string) => selectedIds.has(id)

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Chat Analyzer</h1>
        <p className="text-gray-500">Import your ChatGPT conversation history and let AI extract learning insights.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-bold mb-4">Import ChatGPT Export</h3>
            <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center hover:border-indigo-300 hover:bg-indigo-50 transition cursor-pointer" onClick={() => document.getElementById('file-input')?.click()}>
              <input type="file" id="file-input" accept=".zip,.json" className="hidden" onChange={handleFileChange} />
              <Upload className="w-12 h-12 text-indigo-400 mb-3" />
              <p className="text-sm text-gray-600">{file ? file.name : 'Click to upload ChatGPT export ZIP'}</p>
            </div>
            <button
              onClick={handleImport}
              disabled={!file}
              className="mt-4 bg-indigo-600 disabled:opacity-50 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700"
            >
              Import Conversations
            </button>
          </div>

          {conversations.length > 0 && (
            <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-bold mb-4">Detected Conversations ({conversations.length})</h3>
              <div className="max-h-96 overflow-y-auto space-y-2">
                {conversations.map((c) => (
                  <div key={c.id} className="flex items-center gap-3 p-3 border border-gray-100 rounded-lg hover:bg-indigo-50 cursor-pointer group" onClick={() => toggleSelection(c.id)}>
                    <input
                      type="checkbox"
                      checked={isSelected(c.id)}
                      onChange={() => toggleSelection(c.id)}
                      className="w-4 h-4 text-indigo-600 rounded border-gray-300"
                    />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">{c.title || 'Untitled'}</p>
                      <p className="text-xs text-gray-500">{c.external_id || 'No ID'}</p>
                    </div>
                    {isSelected(c.id) && <CheckCircle className="w-4 h-4 text-indigo-600" />}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-bold mb-4">AI Actions</h3>
            <p className="text-sm text-gray-500 mb-4">{selectedIds.size} conversation(s) selected</p>
            <button
              onClick={handleAnalyze}
              disabled={selectedIds.size === 0 || analyzing}
              className="w-full py-3 bg-indigo-600 disabled:opacity-50 text-white rounded-lg font-medium hover:bg-indigo-700 flex items-center justify-center gap-2"
            >
              {analyzing ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Bot className="w-4 h-4" />
                  <span>Analyze Selected</span>
                </>
              )}
            </button>

            <div className="mt-4 space-y-2">
              <button className="w-full py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 text-sm flex items-center justify-center gap-2">
                <FileText className="w-4 h-4" /> Create Study Roadmap
              </button>
              <button className="w-full py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 text-sm flex items-center justify-center gap-2">
                <CheckCircle className="w-4 h-4" /> Identify Weak Concepts
              </button>
            </div>
          </div>

          {analysisResult && (
            <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="text-lg font-bold mb-4">Analysis Results</h3>
              <pre className="bg-gray-50 p-4 rounded text-sm overflow-x-auto">{JSON.stringify(analysisResult, null, 2)}</pre>
            </div>
          )}
        </div>
      </div>

      {analyses.length > 0 && (
        <div className="mt-8 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-lg font-bold mb-4">Analysis History</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="p-4 font-medium text-gray-600">Type</th>
                  <th className="p-4 font-medium text-gray-600">Created</th>
                </tr>
              </thead>
              <tbody>
                {analyses.map((a, i) => (
                  <tr key={i} className="border-b border-gray-50">
                    <td className="p-4">{a.analysis_type}</td>
                    <td className="p-4">{a.created_at || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
