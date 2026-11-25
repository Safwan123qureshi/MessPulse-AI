import { useState } from 'react'
import { Outlet, Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import {
  Menu, Home, Users, Utensils, Calendar, ShoppingCart, DollarSign, Activity,
  BarChart3, FileText, Settings, LogOut, Shield, Plus, LayoutDashboard, MessageSquare
} from 'lucide-react'

const MainLayout = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const navItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
    { name: 'Hostels', icon: Shield, path: '/hostels' },
    { name: 'Students', icon: Users, path: '/students' },
    { name: 'Meals', icon: Utensils, path: '/meals' },
    { name: 'Bookings', icon: Calendar, path: '/bookings' },
    { name: 'Inventory', icon: ShoppingCart, path: '/inventory' },
    { name: 'Purchases', icon: Plus, path: '/purchases' },
    { name: 'Expenses', icon: DollarSign, path: '/expenses' },
    { name: 'Budgets', icon: BarChart3, path: '/budgets' },
    { name: 'Attendance', icon: Activity, path: '/attendance' },
    { name: 'Food Waste', icon: FileText, path: '/food-waste' },
    { name: 'Feedback', icon: MessageSquare, path: '/feedback' },
    { name: 'AI Insights', icon: BarChart3, path: '/ai-insights' },
    { name: 'Reports', icon: FileText, path: '/reports' },
    { name: 'Bills', icon: FileText, path: '/bills' },
    { name: 'Settings', icon: Settings, path: '/settings' },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-navy-900 text-white transition-transform duration-300 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex items-center justify-between h-16 px-4 border-b border-navy-800">
          <span className="text-xl font-bold flex items-center gap-2">
            <span className="text-blue-500">M</span>Pulse AI
          </span>
          <button
            onClick={() => setSidebarOpen(false)}
            className="text-navy-300 hover:text-white"
          >
            <Menu size={24} />
          </button>
        </div>
        <nav className="mt-4 px-3 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className="flex items-center gap-3 px-3 py-2 text-sm rounded-lg transition-colors hover:bg-navy-800 hover:text-blue-400"
            >
              <item.icon size={18} />
              {item.name}
            </Link>
          ))}
        </nav>
        <div className="absolute bottom-0 w-full p-4 border-t border-navy-800">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2 text-sm rounded-lg bg-red-900/20 text-red-300 hover:bg-red-900/40 transition-colors"
          >
            <LogOut size={18} />
            Logout
          </button>
          <p className="text-xs text-navy-400 mt-2 px-3">
            {user?.role.replace('_', ' ').toUpperCase()}
          </p>
        </div>
      </aside>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main content */}
      <div className={`flex-1 ${sidebarOpen ? 'ml-64' : ''}`}>
        <header className="h-16 border-b border-gray-200 bg-white flex items-center justify-between px-6">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden text-gray-600"
          >
            <Menu size={24} />
          </button>
          <div className="flex items-center gap-4 ml-4">
            <span className="text-sm text-gray-600">
              {user?.email}
            </span>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default MainLayout