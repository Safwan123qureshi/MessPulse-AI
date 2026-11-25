import { Outlet } from 'react-router-dom'

const AuthLayout = ({ children }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-navy-900">MessPulse AI</h1>
          <p className="text-gray-600 text-sm">Smart Meals. Less Waste. Better Budgets.</p>
        </div>
        <Outlet />
      </div>
    </div>
  )
}

export default AuthLayout