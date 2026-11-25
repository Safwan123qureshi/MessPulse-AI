import { Link } from 'react-router-dom'
import { Shield, Utensils, BarChart3, DollarSign, Activity, Users } from 'lucide-react'

const LandingPage = () => {
  const features = [
    { icon: Shield, title: 'Multi-Tenant Isolation', desc: 'Each hostel has its own isolated workspace with private data.' },
    { icon: Utensils, title: 'Meal Management', desc: 'Plan weekly menus, take bookings, and track attendance.' },
    { icon: BarChart3, title: 'AI Demand Prediction', desc: 'Predict meal demand using historical data and trends.' },
    { icon: DollarSign, title: 'Budget Balancer', desc: 'Track expenses, manage budgets, and reduce waste.' },
    { icon: Activity, title: 'Food Waste Tracking', desc: 'Monitor and reduce food waste with detailed reports.' },
    { icon: Users, title: 'Role-Based Access', desc: 'Super admin, owner, manager, and student roles.' },
  ]

  return (
    <div className="min-h-screen bg-navy-900 text-white">
      {/* Navigation */}
      <nav className="border-b border-navy-800 bg-white/5 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-blue-400 text-xl font-bold">M</span>
            <span className="font-bold text-xl">Pulse AI</span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <Link to="/" className="hover:text-blue-400 transition-colors">Home</Link>
            <Link to="#features" className="hover:text-blue-400 transition-colors">Features</Link>
            <Link to="#about" className="hover:text-blue-400 transition-colors">About</Link>
            <Link to="/login" className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors">Login</Link>
            <button className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg transition-colors">
              Register Hostel
            </button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="py-20 px-4 text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
          Smart Meals. Less Waste. Better Budgets.
        </h1>
        <p className="text-navy-300 text-lg md:text-xl mb-8 max-w-2xl mx-auto">
          MessPulse AI is a multi-tenant SaaS platform that helps hostels manage their mess operations,
          reduce food waste, and balance budgets with AI-powered insights.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/register-hostel" className="bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-lg text-lg font-medium transition-colors">
            Register Your Hostel
          </Link>
          <Link to="/login" className="border border-navy-600 hover:border-blue-500 px-8 py-4 rounded-lg text-lg font-medium transition-colors">
            Sign In
          </Link>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold mb-12 text-center">Powerful Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((f) => (
              <div key={f.title} className="bg-navy-800/50 p-6 rounded-xl border border-navy-700 hover:border-blue-500 transition-colors">
                <div className="w-12 h-12 bg-blue-600/20 rounded-lg flex items-center justify-center mb-4">
                  <f.icon size={24} className="text-blue-400" />
                </div>
                <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                <p className="text-navy-300">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-navy-800 bg-navy-800 py-8 px-4 text-center">
        <p className="text-navy-400 text-sm">&copy; 2026 MessPulse AI. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default LandingPage