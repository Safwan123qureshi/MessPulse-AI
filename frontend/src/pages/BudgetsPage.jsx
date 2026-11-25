import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const BudgetsPage = () => {
  const { user } = useAuth()
  const [budgets, setBudgets] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchBudgets(hostelId)
  }, [])

  const fetchBudgets = async (hostelId) => {
    try {
      const res = await api.get(`/budgets/?hostel_id=${hostelId}`)
      setBudgets(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Monthly Budget</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> Set Budget
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Month</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Allocated</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Expenses</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Remaining</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Utilization</th>
            </tr>
          </thead>
          <tbody>
            {budgets.map((b) => {
              const util = b.allocated_amount > 0
                ? ((b.total_expenses / b.allocated_amount) * 100).toFixed(1)
                : 0
              return (
                <tr key={b.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium">{b.month}</td>
                  <td className="px-6 py-4 text-sm">PKR {b.allocated_amount}</td>
                  <td className="px-6 py-4 text-sm">PKR {b.total_expenses}</td>
                  <td className="px-6 py-4 text-sm font-medium">PKR {b.remaining_amount}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 rounded-full text-xs font-medium">
                      {util}%
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default BudgetsPage