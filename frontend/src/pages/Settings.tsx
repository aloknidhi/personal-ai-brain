import { useState } from 'react'
import { Shield, User, Mail, Lock, GitBranch } from 'lucide-react'

export default function Settings() {
  const [apiKey, setApiKey] = useState('')

  return (
    <div className="p-6 max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500">Manage your application preferences and account.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-bold mb-4">AI Configuration</h3>
        <p className="text-gray-500 text-sm mb-4">Configure your OpenAI API key for AI-powered features.</p>
        <div className="space-y-4">
          <label className="block text-sm font-medium text-gray-700">OpenAI API Key</label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="sk-..."
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
          />
          <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-indigo-700">
            Save API Key
          </button>
        </div>
      </div>

      <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-bold mb-4">Privacy &amp; Data</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border border-gray-100 rounded-lg">
            <div>
              <Shield className="w-5 h-5 text-indigo-600" />
              <p className="text-sm font-medium text-gray-900 ml-3 inline">Data Encryption</p>
            </div>
            <span className="text-green-600 text-sm">Enabled</span>
          </div>
          <div className="flex items-center justify-between p-4 border border-gray-100 rounded-lg">
            <div>
              <User className="w-5 h-5 text-indigo-600" />
              <p className="text-sm font-medium text-gray-900 ml-3 inline">Anonymous Analytics</p>
            </div>
            <span className="text-gray-500 text-sm">Disabled</span>
          </div>
          <div className="flex items-center justify-between p-4 border border-gray-100 rounded-lg">
            <div>
              <Lock className="w-5 h-5 text-indigo-600" />
              <p className="text-sm font-medium text-gray-900 ml-3 inline">Local-First Storage</p>
            </div>
            <span className="text-green-600 text-sm">Enabled</span>
          </div>
        </div>
      </div>

      <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-bold mb-4">Account</h3>
        <div className="space-y-4">
          <button className="w-full py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 flex items-center justify-center gap-2">
            <Mail className="w-4 h-4" /> Change Email
          </button>
          <button className="w-full py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 flex items-center justify-center gap-2">
            <Lock className="w-4 h-4" /> Change Password
          </button>
          <button className="w-full py-3 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 flex items-center justify-center gap-2">
            <GitBranch className="w-4 h-4" /> Delete Account
          </button>
        </div>
      </div>
    </div>
  )
}
