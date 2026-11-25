import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const ExpensesPage = () => {
  const { user } = useAuth()
  const [expenses, setExpenses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchExpenses(hostelId)
  }, [])

  const fetchExpenses = async (hostelId) => {
    try {
      const res = await api.get(`/expenses/?hostel_id=${hostelId}`)
      setExpenses(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Expenses</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> New Expense
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Category</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Description</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Amount</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Date</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((e) => (
              <tr key={e.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4">{e.category}</td>
                <td className="px-6 py-4 text-sm">{e.description}</td>
                <td className="px-6 py-4 text-sm font-medium">PKR {e.amount}</td>
                <td className="px-6 py-4 text-sm">{new Date(e.expense_date).toLocaleDateString()}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-medium">
                    {e.payment_status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default ExpensesPage