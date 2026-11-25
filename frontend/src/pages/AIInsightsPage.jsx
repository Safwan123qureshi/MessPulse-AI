import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search, Bot } from 'lucide-react'

const AIInsightsPage = () => {
  const { user } = useAuth()
  const [insights, setInsights] = useState({ predictions: [], recommendations: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchInsights(hostelId)
  }, [])

  const fetchInsights = async (hostelId) => {
    try {
      const res = await api.get(`/ai/insights/${hostelId}`)
      setInsights(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const generateRecommendations = async () => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (!hostelId) return
    try {
      await api.post(`/ai/generate-recommendations/${hostelId}`)
      fetchInsights(hostelId)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">AI Insights</h1>
          <p className="text-gray-600">Predictions and recommendations based on your hostel's data.</p>
        </div>
        <button
          onClick={generateRecommendations}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Bot size={18} /> Generate Recommendations
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-bold mb-4">Demand Predictions</h3>
          {insights.predictions.length === 0 ? (
            <p className="text-gray-500 text-sm">No predictions available. Add attendance data to generate predictions.</p>
          ) : (
            <div className="space-y-3">
              {insights.predictions.map((p) => (
                <div key={p.id} className="p-3 border rounded-lg bg-gray-50">
                  <div className="flex justify-between">
                    <span className="text-sm capitalize">{p.meal_type}</span>
                    <span className="text-sm font-medium">{p.predicted_quantity}</span>
                  </div>
                  <p className="text-xs text-gray-500">{p.method} • {p.data_points_used} data points</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-bold mb-4">Recommendations</h3>
          {insights.recommendations.length === 0 ? (
            <p className="text-gray-500 text-sm">No recommendations yet. Click generate to create AI insights.</p>
          ) : (
            <div className="space-y-3">
              {insights.recommendations.map((r) => (
                <div key={r.id} className="p-3 border rounded-lg bg-blue-50">
                  <h4 className="text-sm font-bold">{r.title}</h4>
                  <p className="text-xs text-gray-600 mt-1">{r.recommendation_text}</p>
                  <p className="text-xs text-gray-500 mt-1">{r.suggested_action}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default AIInsightsPage