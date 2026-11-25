import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search, FileImage, AlertTriangle } from 'lucide-react'

const BillsPage = () => {
  const { user } = useAuth()
  const [bills, setBills] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchBills(hostelId)
  }, [])

  const fetchBills = async (hostelId) => {
    try {
      const res = await api.get(`/bills/?hostel_id=${hostelId}`)
      setBills(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Bill Scanner</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> Upload Bill
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Supplier</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Invoice #</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Date</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Amount</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {bills.map((b) => (
              <tr key={b.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4">{b.supplier_name || 'Unknown'}</td>
                <td className="px-6 py-4 text-sm">{b.invoice_number || '-'}</td>
                <td className="px-6 py-4 text-sm">{b.purchase_date ? new Date(b.purchase_date).toLocaleDateString() : '-'}</td>
                <td className="px-6 py-4 text-sm font-medium">PKR {b.final_amount}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    b.verification_status === 'verified'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {b.verification_status}
                  </span>
                  {b.is_duplicate && (
                    <span className="ml-2 text-xs text-red-600" title={b.duplicate_warning}>
                      ⚠ Duplicate
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default BillsPage