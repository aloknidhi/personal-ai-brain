// Dashboard page
import { useState, useEffect } from 'react'
import { Clock, CheckCircle, Brain, Activity } from 'lucide-react'

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    // Fetch dashboard stats
    setStats({
      todayStudyTime: '4h 20m',
      dailyGoalCompletion: 75,
      currentTopic: 'C++ OOP',
      streak: 5,
    })
  }, [])

  const statCards = [
    { label: "Today's Study Time", value: stats?.todayStudyTime || '0h 0m', icon: Clock, color: 'bg-indigo-100 text-indigo-600' },
    { label: 'Daily Goal Completion', value: `${stats?.dailyGoalCompletion || 0}%`, icon: CheckCircle, color: 'bg-green-100 text-green-600' },
    { label: 'Current Topic', value: stats?.currentTopic || '—', icon: Brain, color: 'bg-purple-100 text-purple-600' },
    { label: 'Learning Streak', value: `${stats?.streak || 0} Days`, icon: Activity, color: 'bg-blue-100 text-blue-600' },
  ]

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500">Your personal productivity overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {statCards.map((card) => (
          <div key={card.label} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-500">{card.label}</p>
                <h3 className="text-2xl font-bold">{card.value}</h3>
              </div>
              <div className="w-10 h-10 rounded-lg {card.color} flex items-center justify-center">
                <card.icon className="w-5 h-5" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-bold mb-4">Today's AI-Generated Plan</h3>
        <div className="space-y-3">
          {[
            { time: '7:00 – 8:00 PM', subject: 'C++ Inheritance', status: 'Completed', color: 'text-green-600' },
            { time: '8:00 – 8:45 PM', subject: 'Polymorphism', status: 'In Progress', color: 'text-indigo-600' },
            { time: '8:45 – 9:15 PM', subject: 'Practice', status: 'Upcoming', color: 'text-gray-500' },
            { time: '9:15 – 10:00 PM', subject: 'Java JDBC', status: 'Upcoming', color: 'text-gray-500' },
          ].map((item, i) => (
            <div key={i} className="flex items-center justify-between p-3 border-b border-gray-50 last:border-0">
              <div className="flex items-center gap-4">
                <span className="text-sm font-medium text-gray-700">{item.time}</span>
                <span className="text-sm font-semibold">{item.subject}</span>
              </div>
              <span className={`text-xs font-medium px-2 py-1 rounded-full ${item.color}`}>
                {item.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
