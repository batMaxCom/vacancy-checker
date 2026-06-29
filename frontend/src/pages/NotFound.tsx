import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="auth-page">
      <div className="auth-card" style={{ textAlign: 'center' }}>
        <h1>CCheck</h1>
        <h2>404 — Page Not Found</h2>
        <p style={{ color: 'var(--color-text-secondary)', fontSize: 14, marginBottom: 24 }}>
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link to="/" className="btn btn-primary auth-btn" style={{ textDecoration: 'none' }}>
          Go Home
        </Link>
      </div>
    </div>
  )
}
