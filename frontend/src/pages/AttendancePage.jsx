import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const AttendancePage = () => {
  const { user } = useAuth()
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchAttendance(hostelId)
  }, [])

  const fetchAttendance = async (hostelId) => {
    try {
      const res = await api.get(`/attendance/?hostel_id=${hostelId}`)
      setRecords(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Attendance</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> Record Attendance
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Meal Type</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Date</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Expected</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Served</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Waste</th>
            </tr>
          </thead>
          <tbody>
            {records.map((a) => (
              <tr key={a.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4">{a.meal_type}</td>
                <td className="px-6 py-4 text-sm">{new Date(a.attendance_date).toLocaleDateString()}</td>
                <td className="px-6 py-4 text-sm">{a.expected_meals}</td>
                <td className="px-6 py-4 text-sm">{a.actual_meals_served}</td>
                <td className="px-6 py-4 text-sm">{a.discarded_quantity} {a.unit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default AttendancePage