import { useState } from 'react'
import { Calendar } from 'lucide-react'

export default function StudyPlanner() {
  const [goal, setGoal] = useState('')
  const [topics, setTopics] = useState('')
  const [hours, setHours] = useState('')
  const [days, setDays] = useState('')

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault()
    alert('Plan generation will call the AI planner API')
  }

  return (
    <div className="p-6 max-w-2xl">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Study Planner</h1>
        <p className="text-gray-500">Generate AI-powered study plans based on your goals and availability.</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">What do you want to achieve?</label>
            <input
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., Learn C++ OOP from basics to advanced"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Topics you want to learn</label>
            <input
              className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              placeholder="e.g., Classes, Objects, Inheritance, Polymorphism"
              value={topics}
              onChange={(e) => setTopics(e.target.value)}
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Daily available hours</label>
              <input type="number" className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" value={hours} onChange={(e) => setHours(e.target.value)} />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Complete within (days)</label>
              <input type="number" className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none" value={days} onChange={(e) => setDays(e.target.value)} />
            </div>
          </div>
          <button type="submit" className="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 flex items-center justify-center gap-2">
            <Calendar className="w-5 h-5" /> Generate My Plan
          </button>
        </form>
      </div>
    </div>
  )
}
