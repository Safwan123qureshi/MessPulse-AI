import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'
import { Plus, Search } from 'lucide-react'

const InventoryPage = () => {
  const { user } = useAuth()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const hostelId = user?.memberships?.[0]?.hostel_id
    if (hostelId) fetchInventory(hostelId)
  }, [])

  const fetchInventory = async (hostelId) => {
    try {
      const res = await api.get(`/inventory/?hostel_id=${hostelId}`)
      setItems(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-navy-900">Inventory Management</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <Plus size={18} /> Add Item
        </button>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Name</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Category</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Quantity</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Unit Price</th>
              <th className="px-6 py-3 text-sm font-medium text-gray-600">Supplier</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-4 font-medium">{item.name}</td>
                <td className="px-6 py-4 text-sm">{item.category}</td>
                <td className="px-6 py-4 text-sm">{item.quantity} {item.unit}</td>
                <td className="px-6 py-4 text-sm">PKR {item.purchase_price}</td>
                <td className="px-6 py-4 text-sm">{item.supplier}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default InventoryPage