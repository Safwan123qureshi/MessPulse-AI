import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { FileText, Download } from 'lucide-react'

const ReportsPage = () => {
  const { user } = useAuth()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)

  const hostelId = user?.memberships?.[0]?.hostel_id

  const fetchReport = async (type) => {
    if (!hostelId) return
    setLoading(true)
    try {
      let url = `/reports/${type}/${hostelId}`
      if (type === 'food-waste') url += `?start_date=2026-01-01&end_date=2026-12-31`
      if (type === 'budget') url += `?month=2026-11`
      const res = await api.get(url)
      setReport(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const exportCSV = async (type) => {
    if (!hostelId) return
    try {
      const res = await api.get(`/reports/export/csv/${hostelId}/${type}`, {
        responseType: 'blob',
      })
      const url = window.URL.createObjectURL(new Blob([res.data]))
      const link = document.createElement('a')
      link.href = url
      link.download = `${type}_${hostelId}.csv`
      link.click()
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-navy-900">Reports</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          { name: 'Daily Meal', type: 'daily-meal', icon: FileText },
          { name: 'Weekly Consumption', type: 'weekly-consumption', icon: FileText },
          { name: 'Monthly Expenses', type: 'monthly-expenses', icon: FileText },
          { name: 'Budget Report', type: 'budget', icon: FileText },
          { name: 'Food Waste', type: 'food-waste', icon: FileText },
          { name: 'Feedback', type: 'feedback', icon: FileText },
          { name: 'AI Forecast', type: 'ai-forecast', icon: FileText },
        ].map((r) => (
          <div key={r.name} className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-bold mb-2">{r.name}</h3>
            <div className="flex gap-2">
              <button
                onClick={() => fetchReport(r.type)}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded text-sm"
              >
                View
              </button>
              <button
                onClick={() => exportCSV(r.type)}
                className="px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 py-2 rounded text-sm"
              >
                <Download size={16} /> CSV
              </button>
            </div>
            {report && (
              <div className="mt-4 p-3 bg-gray-50 rounded text-sm">
                {JSON.stringify(report)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ReportsPage