import { Link } from 'react-router-dom'
import type { ReactNode } from 'react'

export default function Layout({ children }: { children: ReactNode }) {
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
      </aside>
      <main className="content">{children}</main>
    </div>
  )
}
