import { Link } from 'react-router-dom'
import type { ReactNode } from 'react'
import { useAuth } from '../auth/AuthContext'

export default function Layout({ children }: { children: ReactNode }) {
  const { user, logout } = useAuth()

  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>CCheck</h1>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/profiles">Search Profiles</Link>
          <Link to="/sources">Sources</Link>
          <Link to="/vacancies">Vacancies</Link>
        </nav>
        <div className="sidebar-footer">
          <Link to="/profile" className="sidebar-user">{user?.id?.slice(0, 8)}...</Link>
          <button className="btn btn-outline btn-sm" onClick={logout}>Logout</button>
        </div>
      </aside>
      <main className="content">{children}</main>
    </div>
  )
}
