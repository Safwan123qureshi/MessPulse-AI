import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { Building, User, Mail, Phone, AlertCircle } from 'lucide-react'

const RegisterHostelPage = () => {
  const [form, setForm] = useState({
    name: '', slug: '', address: '', contact_phone: '', contact_email: '',
    owner_name: '', owner_email: '', owner_phone: '', student_capacity: '',
    email: '', password: '', full_name: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      // Register hostel (super admin only endpoint, but we'll use a simplified flow)
      const res = await api.post('/hostels/', {
        name: form.name,
        slug: form.slug,
        address: form.address,
        contact_phone: form.contact_phone,
        contact_email: form.contact_email,
        owner_name: form.owner_name,
        owner_email: form.owner_email,
        owner_phone: form.owner_phone,
        student_capacity: parseInt(form.student_capacity) || 0,
      })
      navigate('/login')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm flex items-center gap-2">
          <AlertCircle size={18} /> {error}
        </div>
      )}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Hostel Name</label>
          <input
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            leftIcon={<Building size={18} className="text-gray-400" />}
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Slug (unique ID)</label>
          <input
            value={form.slug}
            onChange={(e) => setForm({ ...form, slug: e.target.value })}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>
      </div>
      <div className="space-y-2">
        <label className="block text-sm font-medium text-gray-700">Address</label>
        <input
          value={form.address}
          onChange={(e) => setForm({ ...form, address: e.target.value })}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
        />
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Contact Phone</label>
          <input
            value={form.contact_phone}
            onChange={(e) => setForm({ ...form, contact_phone: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            leftIcon={<Phone size={18} className="text-gray-400" />}
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Contact Email</label>
          <input
            type="email"
            value={form.contact_email}
            onChange={(e) => setForm({ ...form, contact_email: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            leftIcon={<Mail size={18} className="text-gray-400" />}
          />
        </div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Owner Name</label>
          <input
            value={form.owner_name}
            onChange={(e) => setForm({ ...form, owner_name: e.target.value })}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            leftIcon={<User size={18} className="text-gray-400" />}
          />
        </div>
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Owner Email</label>
          <input
            type="email"
            value={form.owner_email}
            onChange={(e) => setForm({ ...form, owner_email: e.target.value })}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
          />
        </div>
      </div>
      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-3 rounded-lg font-medium transition-colors"
      >
        {loading ? 'Creating...' : 'Register Hostel'}
      </button>
      <p className="text-center text-sm text-gray-600">
        Already have an account?{' '}
        <Link to="/login" className="text-blue-600 hover:underline">Sign in</Link>
      </p>
    </form>
  )
}

export default RegisterHostelPage