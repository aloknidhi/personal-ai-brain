import { useState } from 'react'
import { Play, X } from 'lucide-react'

export default function ActivityTracker() {
  const [activity, setActivity] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [elapsed, setElapsed] = useState(0)
  const [activities, setActivities] = useState<any[]>([])

  const startTimer = () => {
    if (!activity) return
    setIsRunning(true)
  }

  const stopTimer = () => {
    setIsRunning(false)
    setActivities([...activities, { title: activity, duration: elapsed }])
    setActivity('')
    setElapsed(0)
  }

  return (
    <div className="p-6 max-w-lg">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Activity Tracker</h1>
        <p className="text-gray-500">Track your actual work and learning sessions.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div className="text-center mb-6">
          <div className="text-6xl font-mono font-bold text-indigo-600">
            {Math.floor(elapsed / 60).toString().padStart(2, '0')}:{Math.floor(elapsed % 60).toString().padStart(2, '0')}
          </div>
          <p className="text-gray-500 text-sm mt-2">{activity || 'No active session'}</p>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">Activity name</label>
          <input
            className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="e.g., C++ Inheritance Study"
            value={activity}
            onChange={(e) => setActivity(e.target.value)}
          />
        </div>

        <div className="flex gap-3">
          {isRunning ? (
            <div>
              <button onClick={stopTimer} className="flex-1 bg-red-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-red-700 flex items-center justify-center gap-2">
                <X className="w-5 h-5" /> Stop
              </button>
            </div>
          ) : (
            <div>
              <button onClick={startTimer} disabled={!activity} className="flex-1 bg-green-600 disabled:opacity-50 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-700 flex items-center justify-center gap-2">
                <Play className="w-5 h-5" /> Start
              </button>
            </div>
          )}
        </div>
      </div>

      {activities.length > 0 && (
        <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold p-6 border-b border-gray-100">Recent Sessions</h3>
          <div className="divide-y divide-gray-100">
            {activities.map((a, i) => (
              <div key={i} className="p-4 flex justify-between items-center">
                <span className="text-gray-700">{a.title}</span>
                <span className="text-sm text-gray-500">{Math.floor(a.duration / 60)}m {a.duration % 60}s</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
