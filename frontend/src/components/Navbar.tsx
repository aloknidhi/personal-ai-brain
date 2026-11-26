import { Link } from 'react-router-dom'
import { LayoutDashboard, Bot, Brain, Calendar, Timer, Settings, Share2 } from 'lucide-react'

const menuItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/chat-analyzer', label: 'Chat Analyzer', icon: Bot },
  { to: '/knowledge-base', label: 'Knowledge Base', icon: Brain },
  { to: '/study-planner', label: 'Study Planner', icon: Calendar },
  { to: '/activity-tracker', label: 'Activity Tracker', icon: Timer },
  { to: '/sources', label: 'Data Sources', icon: Share2 },
]

export default function Navbar() {
  return (
    <nav className="bg-indigo-900 text-white px-6 py-4 flex justify-between items-center shadow-md">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 bg-indigo-400 rounded flex items-center justify-center">
          <Brain className="w-5 h-5" />
        </div>
        <Link to="/" className="text-xl font-bold tracking-tight">
          Personal AI Brain
        </Link>
      </div>
      <div className="flex items-center gap-6">
        {menuItems.map((item) => (
          <Link key={item.to} to={item.to} className="text-sm font-medium hover:text-indigo-200 transition flex items-center gap-2">
            <item.icon className="w-4 h-4" />
            {item.label}
          </Link>
        ))}
        <Link to="/settings" className="text-sm font-medium hover:text-indigo-200 flex items-center gap-2">
          <Settings className="w-4 h-4" /> Settings
        </Link>
      </div>
    </nav>
  )
}
