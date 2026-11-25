import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import {
  Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle
} from '../components/ui/card'
import { Users, Clock, CreditCard, TrendingDown, Percent, ChartLine } from 'lucide-react'

const Dashboard = () => {
  const { user } = useAuth()
  const { hostelId } = useParams()
  const [stats, setStats] = useState({
    total_students: 0,
    meals_booked_today: 0,
    monthly_budget: 0,
    monthly_expenses: 0,
    remaining_budget: 0,
    food_waste_today: 0,
    average_rating: 0,
  })
  const [loading, setLoading] = useState(true)

  const hostelIdToUse = hostelId || (user?.memberships?.[0]?.hostel_id)

  useEffect(() => {
    if (hostelIdToUse) {
      fetchStats(hostelIdToUse)
    }
  }, [hostelIdToUse])

  const fetchStats = async (id) => {
    try {
      const res = await api.get(`/ai/dashboard-stats/${id}`)
      setStats(res.data)
    } catch (err) {
      console.error('Failed to fetch stats', err)
    } finally {
      setLoading(false)
    }
  }

  const utilization = stats.monthly_budget > 0
    ? ((stats.monthly_expenses / stats.monthly_budget) * 100).toFixed(1)
    : 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">Hostel Dashboard</h1>
          <p className="text-gray-600">Welcome back, {user?.full_name}</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-navy-600 bg-navy-100 px-2 py-1 rounded">
            Real-time data
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Total Students"
          value={stats.total_students}
          icon={<Users className="w-6 h-6" />}
          color="bg-blue-500"
        />
        <DashboardCard
          title="Meals Booked Today"
          value={stats.meals_booked_today}
          icon={<Clock className="w-6 h-6" />}
          color="bg-green-500"
        />
        <DashboardCard
          title="Monthly Budget"
          value={`PKR ${stats.monthly_budget.toLocaleString()}`}
          icon={<CreditCard className="w-6 h-6" />}
          color="bg-purple-500"
        />
        <DashboardCard
          title="Monthly Expenses"
          value={`PKR ${stats.monthly_expenses.toLocaleString()}`}
          icon={<TrendingDown className="w-6 h-6" />}
          color="bg-red-500"
        />
        <DashboardCard
          title="Remaining Budget"
          value={`PKR ${stats.remaining_budget.toLocaleString()}`}
          icon={<Percent className="w-6 h-6" />}
          color="bg-green-500"
        />
        <DashboardCard
          title="Budget Utilization"
          value={`${utilization}%`}
          icon={<ChartLine className="w-6 h-6" />}
          color="bg-orange-500"
        />
        <DashboardCard
          title="Food Waste Today"
          value={`${stats.food_waste_today} kg`}
          icon={<TrendingDown className="w-6 h-6" />}
          color="bg-red-500"
        />
        <DashboardCard
          title="Avg Meal Rating"
          value={stats.average_rating.toFixed(1)}
          icon={<ChartLine className="w-6 h-6" />}
          color="bg-yellow-500"
        />
      </div>

      {/* Placeholder for charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-bold mb-4">Daily Meal Consumption</h3>
          <div className="h-64 flex items-center justify-center text-gray-400">
            Chart data loading from database...
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-bold mb-4">Monthly Expenses</h3>
          <div className="h-64 flex items-center justify-center text-gray-400">
            Chart data loading from database...
          </div>
        </div>
      </div>

      {!loading && !hostelIdToUse && (
        <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-yellow-800 text-sm">
            No hostel selected. Please select a hostel to view dashboard data.
          </p>
        </div>
      )}
    </div>
  )
}

const DashboardCard = ({ title, value, icon, color }) => (
  <Card className="bg-white border border-gray-200 rounded-lg">
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium text-gray-500">{title}</CardTitle>
      <div className={`w-8 h-8 rounded-lg ${color} flex items-center justify-center`}>
        {icon}
      </div>
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold text-navy-900">{value}</div>
    </CardContent>
  </Card>
)

export default Dashboard