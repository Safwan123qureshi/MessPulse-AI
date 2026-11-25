import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search, Edit, Trash2 } from 'lucide-react'

const HostelsPage = () => {
  const { user } = useAuth()
  const [hostels, setHostels] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchHostels()
  }, [])

  const fetchHostels = async () => {
    try {
      const res = await api.get('/hostels/')
      setHostels(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Hostel Directory</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> Add Hostel
        </button>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-sm font-medium text-gray-600">Name</th>
                <th className="px-6 py-3 text-sm font-medium text-gray-600">Slug</th>
                <th className="px-6 py-3 text-sm font-medium text-gray-600">Status</th>
                <th className="px-6 py-3 text-sm font-medium text-gray-600">Capacity</th>
                <th className="px-6 py-3 text-sm font-medium text-gray-600">Actions</th>
              </tr>
            </thead>
            <tbody>
              {hostels.map((h) => (
                <tr key={h.id} className="border-b hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium">{h.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{h.slug}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      h.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}>
                      {h.is_active ? 'Active' : 'Suspended'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">{h.student_capacity}</td>
                  <td className="px-6 py-4 flex gap-2">
                    <button className="text-blue-600 hover:underline text-sm">View</button>
                    <button className="text-gray-600 hover:underline text-sm">Edit</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default HostelsPage