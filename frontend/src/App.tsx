import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import ChatAnalyzer from './pages/ChatAnalyzer'
import KnowledgeBase from './pages/KnowledgeBase'
import StudyPlanner from './pages/StudyPlanner'
import ActivityTracker from './pages/ActivityTracker'
import Sources from './pages/Sources'
import Settings from './pages/Settings'
import Navbar from './components/Navbar'

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <div className="flex flex-col h-screen">
        <Navbar />
        <div className="flex-1 overflow-hidden flex">
          <Outlet />
        </div>
      </div>
    ),
    children: [
      { index: true, element: <Dashboard /> },
      { path: 'chat-analyzer', element: <ChatAnalyzer /> },
      { path: 'knowledge-base', element: <KnowledgeBase /> },
      { path: 'study-planner', element: <StudyPlanner /> },
      { path: 'activity-tracker', element: <ActivityTracker /> },
      { path: 'sources', element: <Sources /> },
      { path: 'settings', element: <Settings /> },
    ],
  },
])

export default function App() {
  return <RouterProvider router={router} />
}
