import { useState, useEffect } from 'react'
import api from '../services/api'
import { importChatGPT, syncSource } from '../services/imports'
import { Plus, RefreshCw, Upload, Trash2 } from 'lucide-react'

export default function Sources() {
  const [sources, setSources] = useState<any[]>([])
  const [file, setFile] = useState<File | null>(null)
  const [newSourceType, setNewSourceType] = useState('chatgpt')

  useEffect(() => {
    loadSources()
  }, [])

  const loadSources = async () => {
    const res = await api.get('/sources/')
    setSources(res.data)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setFile(e.target.files[0])
  }

  const handleConnectSource = async () => {
    const res = await api.post('/sources/', { source_type: newSourceType })
    setSources([...sources, res.data])
    setNewSourceType('chatgpt')
  }

  const handleImport = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    // Use a source_id - for now create one first
    await api.post('/sources/', { source_type: 'chatgpt' })
    await importChatGPT(formData)
    setFile(null)
    loadSources()
  }

  const handleSync = async (id: string) => {
    await syncSource(id)
    loadSources()
  }

  const handleDelete = async (id: string) => {
    await api.delete(`/sources/${id}`)
    loadSources()
  }

  const sourceTypeLabels: Record<string, string> = {
    chatgpt: 'ChatGPT Export',
    github: 'GitHub',
    local: 'Local Files',
    google_drive: 'Google Drive',
    browser: 'Browser Activity',
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Data Sources</h1>
        <p className="text-gray-500">Connect and manage your data sources.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-bold mb-4">Connect New Source</h3>
            <div className="space-y-3">
              <select
                value={newSourceType}
                onChange={(e) => setNewSourceType(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
              >
                <option value="chatgpt">ChatGPT Export</option>
                <option value="github">GitHub</option>
                <option value="local">Local Files</option>
                <option value="google_drive">Google Drive</option>
              </select>
              <button
                onClick={handleConnectSource}
                className="w-full bg-indigo-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-indigo-700 flex items-center justify-center gap-2"
              >
                <Plus className="w-4 h-4" /> Connect Source
              </button>
            </div>
          </div>

          <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-bold mb-4">Import ChatGPT Export</h3>
            <div className="border-2 border-dashed border-gray-200 rounded-lg p-8 text-center hover:border-indigo-300 hover:bg-indigo-50 transition cursor-pointer" onClick={() => document.getElementById('file-input')?.click()}>
              <input type="file" id="file-input" accept=".zip,.json" className="hidden" onChange={handleFileChange} />
              <Upload className="w-12 h-12 text-indigo-400 mb-3" />
              <p className="text-sm text-gray-600">{file ? file.name : 'Click to upload ChatGPT export ZIP'}</p>
            </div>
            <button
              onClick={handleImport}
              disabled={!file}
              className="mt-4 w-full bg-indigo-600 disabled:opacity-50 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700"
            >
              Import Conversations
            </button>
          </div>
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-lg font-bold mb-4">Connected Sources</h3>
            <div className="space-y-3">
              {sources.length === 0 && (
                <p className="text-sm text-gray-500 text-center">No sources connected yet.</p>
              )}
              {sources.map((source) => (
                <div key={source.id} className="p-3 border border-gray-100 rounded-lg flex justify-between items-center">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{sourceTypeLabels[source.source_type] || source.source_type}</p>
                    <p className="text-xs text-gray-500">{source.imported_count || 0} items imported</p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleSync(source.id)}
                      className="p-2 bg-indigo-50 text-indigo-600 rounded hover:bg-indigo-100"
                    >
                      <RefreshCw className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleDelete(source.id)}
                      className="p-2 bg-red-50 text-red-600 rounded hover:bg-red-100"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
