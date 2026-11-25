import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const FeedbackPage = () => {
  const { user } = useAuth()
  const [feedbacks, setFeedbacks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchFeedback(hostelId)
  }, [])

  const fetchFeedback = async (hostelId) => {
    try {
      const res = await api.get(`/feedback/?hostel_id=${hostelId}`)
      setFeedbacks(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Student Feedback</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> New Feedback
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Student</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Rating</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Type</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Date</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Resolved</th>
            </tr>
          </thead>
          <tbody>
            {feedbacks.map((f) => (
              <tr key={f.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4">{f.student_id}</td>
                <td className="px-6 py-4 text-sm">{f.rating} / 5</td>
                <td className="px-6 py-4 text-sm">{f.feedback_type}</td>
                <td className="px-6 py-4 text-sm">{new Date(f.created_at).toLocaleDateString()}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    f.is_resolved ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {f.is_resolved ? 'Resolved' : 'Open'}
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

export default FeedbackPage