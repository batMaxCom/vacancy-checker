import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import Layout from './pages/Layout'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import ProfilesList from './pages/ProfilesList'
import ProfileDetail from './pages/ProfileDetail'
import ProfileForm from './pages/ProfileForm'
import SourcesList from './pages/SourcesList'
import SourceForm from './pages/SourceForm'
import UserProfilePage from './pages/UserProfile'
import VacanciesList from './pages/VacanciesList'
import VacancyDetail from './pages/VacancyDetail'
import VacancyForm from './pages/VacancyForm'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()
  if (isLoading) return <div className="loading">Loading...</div>
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <>{children}</>
}

function AppRoutes() {
  const { isLoading } = useAuth()

  if (isLoading) return <div className="loading">Loading...</div>

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/" element={<Layout><ProtectedRoute><Home /></ProtectedRoute></Layout>} />
      <Route path="/profiles" element={<Layout><ProtectedRoute><ProfilesList /></ProtectedRoute></Layout>} />
      <Route path="/profiles/new" element={<Layout><ProtectedRoute><ProfileForm /></ProtectedRoute></Layout>} />
      <Route path="/profiles/:id" element={<Layout><ProtectedRoute><ProfileDetail /></ProtectedRoute></Layout>} />
      <Route path="/profiles/:id/edit" element={<Layout><ProtectedRoute><ProfileForm /></ProtectedRoute></Layout>} />
      <Route path="/profile" element={<Layout><ProtectedRoute><UserProfilePage /></ProtectedRoute></Layout>} />
      <Route path="/sources" element={<Layout><ProtectedRoute><SourcesList /></ProtectedRoute></Layout>} />
      <Route path="/sources/new" element={<Layout><ProtectedRoute><SourceForm /></ProtectedRoute></Layout>} />
      <Route path="/sources/:id/edit" element={<Layout><ProtectedRoute><SourceForm /></ProtectedRoute></Layout>} />
      <Route path="/vacancies" element={<Layout><ProtectedRoute><VacanciesList /></ProtectedRoute></Layout>} />
      <Route path="/vacancies/new" element={<Layout><ProtectedRoute><VacancyForm /></ProtectedRoute></Layout>} />
      <Route path="/vacancies/:id" element={<Layout><ProtectedRoute><VacancyDetail /></ProtectedRoute></Layout>} />
      <Route path="/vacancies/:id/edit" element={<Layout><ProtectedRoute><VacancyForm /></ProtectedRoute></Layout>} />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}
