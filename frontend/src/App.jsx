import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import MainLayout from './layouts/MainLayout'
import AuthLayout from './layouts/AuthLayout'
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterHostelPage from './pages/RegisterHostelPage'
import Dashboard from './pages/Dashboard'
import HostelsPage from './pages/HostelsPage'
import StudentsPage from './pages/StudentsPage'
import MealsPage from './pages/MealsPage'
import BookingsPage from './pages/BookingsPage'
import InventoryPage from './pages/InventoryPage'
import PurchasesPage from './pages/PurchasesPage'
import ExpensesPage from './pages/ExpensesPage'
import BudgetsPage from './pages/BudgetsPage'
import AttendancePage from './pages/AttendancePage'
import FoodWastePage from './pages/FoodWastePage'
import FeedbackPage from './pages/FeedbackPage'
import AIInsightsPage from './pages/AIInsightsPage'
import ReportsPage from './pages/ReportsPage'
import BillsPage from './pages/BillsPage'
import SettingsPage from './pages/SettingsPage'

function App() {
  const { user, loading } = useAuth()

  useEffect(() => {
    if (localStorage.getItem('token') && !loading) {
      // Token exists, user will be loaded by context
    }
  }, [loading])

  if (loading) return null

  const isAuth = !!user

  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={isAuth ? <Navigate to="/dashboard" replace /> : <AuthLayout><LoginPage /></AuthLayout>} />
        <Route path="/register-hostel" element={<AuthLayout><RegisterHostelPage /></AuthLayout>} />

        {/* Protected routes */}
        <Route element={isAuth ? <MainLayout /> : <Navigate to="/login" replace />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/hostels" element={<HostelsPage />} />
          <Route path="/students" element={<StudentsPage />} />
          <Route path="/meals" element={<MealsPage />} />
          <Route path="/bookings" element={<BookingsPage />} />
          <Route path="/inventory" element={<InventoryPage />} />
          <Route path="/purchases" element={<PurchasesPage />} />
          <Route path="/expenses" element={<ExpensesPage />} />
          <Route path="/budgets" element={<BudgetsPage />} />
          <Route path="/attendance" element={<AttendancePage />} />
          <Route path="/food-waste" element={<FoodWastePage />} />
          <Route path="/feedback" element={<FeedbackPage />} />
          <Route path="/ai-insights" element={<AIInsightsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/bills" element={<BillsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App