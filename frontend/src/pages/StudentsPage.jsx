import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const StudentsPage = () => {
  const { user } = useAuth()
  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchStudents(hostelId)
  }, [])

  const fetchStudents = async (hostelId) => {
    try {
      const res = await api.get(`/students/?hostel_id=${hostelId}`)
      setStudents(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Student Management</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> Add Student
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Student ID</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Name</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Room</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4 font-medium">{s.student_id}</td>
                <td className="px-6 py-4">{s.full_name}</td>
                <td className="px-6 py-4 text-sm">{s.room_number}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">
                    Active
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

export default StudentsPage