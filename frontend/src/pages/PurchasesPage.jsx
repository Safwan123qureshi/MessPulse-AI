import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const PurchasesPage = () => {
  const { user } = useAuth()
  const [purchases, setPurchases] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchPurchases(hostelId)
  }, [])

  const fetchPurchases = async (hostelId) => {
    try {
      const res = await api.get(`/purchases/?hostel_id=${hostelId}`)
      setPurchases(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Purchases</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> New Purchase
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Supplier</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Date</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Invoice</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Total</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Status</th>
            </tr>
          </thead>
          <tbody>
            {purchases.map((p) => (
              <tr key={p.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4">{p.supplier_id}</td>
                <td className="px-6 py-4 text-sm">{new Date(p.purchase_date).toLocaleDateString()}</td>
                <td className="px-6 py-4 text-sm">{p.invoice_number || '-'}</td>
                <td className="px-6 py-4 text-sm font-medium">PKR {p.total_amount}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-medium">
                    {p.payment_status}
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

export default PurchasesPage