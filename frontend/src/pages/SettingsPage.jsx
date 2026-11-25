import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Save, Mail, Phone, Building } from 'lucide-react'

const SettingsPage = () => {
  const { user } = useAuth()
  const [hostel, setHostel] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchHostel(hostelId)
  }, [])

  const fetchHostel = async (hostelId) => {
    try {
      const res = await api.get(`/hostels/${hostelId}`)
      setHostel(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-navy-900">Hostel Settings</h1>
      {loading ? (
        <p>Loading...</p>
      ) : hostel ? (
        <div className="bg-white rounded-lg border border-gray-200 p-6 max-w-2xl">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Hostel Name</label>
              <input
                defaultValue={hostel.name}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
              <input
                defaultValue={hostel.address}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Contact Phone</label>
                <input
                  defaultValue={hostel.contact_phone}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Contact Email</label>
                <input
                  type="email"
                  defaultValue={hostel.contact_email}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Student Capacity</label>
              <input
                type="number"
                defaultValue={hostel.student_capacity}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Currency</label>
              <select className="w-full px-4 py-2 border border-gray-300 rounded-lg">
                <option>PKR</option>
                <option>USD</option>
                <option>EUR</option>
              </select>
            </div>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg">
            <Save size={18} /> Save Changes
          </button>
        </div>
      ) : (
        <p>No hostel data available.</p>
      )}
    </div>
  )
}

export default SettingsPage