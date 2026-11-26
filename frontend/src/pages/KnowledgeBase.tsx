export default function KnowledgeBase() {
  const subjects = [
    { name: 'C++ Programming', topics: 6, progress: 65 },
    { name: 'Java', topics: 3, progress: 40 },
    { name: 'Japanese Language', topics: 2, progress: 20 },
  ]

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Knowledge Base</h1>
        <p className="text-gray-500">Your personal knowledge graph and learning profile</p>
      </div>

      <div className="space-y-4">
        {subjects.map((s, i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-bold">{s.name}</h3>
                <p className="text-gray-500 text-sm">{s.topics} topics tracked</p>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold">{s.progress}%</div>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-indigo-600 h-2 rounded-full" style={{ width: `${s.progress}%` }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
