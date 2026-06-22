import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { searchApi } from '../api/search'
import { vacancyApi } from '../api/vacancy'
import type { SearchProfile } from '../api/types'

export default function ProfilesList() {
  const [profiles, setProfiles] = useState<SearchProfile[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [userId, setUserId] = useState(() => localStorage.getItem('userId') ?? '')

  const load = (uid: string) => {
    if (!uid) { setProfiles([]); setLoading(false); return }
    setLoading(true)
    setError('')
    searchApi.getProfiles(uid)
      .then(setProfiles)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load(userId) }, [])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    localStorage.setItem('userId', userId)
    load(userId)
  }

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this profile?')) return
    try {
      await vacancyApi.deleteVacanciesByProfile(id)
      await searchApi.deleteProfile(id)
      setProfiles(p => p.filter(x => x.id !== id))
    } catch (e: any) {
      alert(e.message)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h2>Search Profiles</h2>
        <Link to="/profiles/new" className="btn btn-primary">+ New Profile</Link>
      </div>

      <form onSubmit={handleSubmit} className="card" style={{ display: 'flex', gap: 8, alignItems: 'flex-end', padding: 16 }}>
        <div className="form-group" style={{ margin: 0, flex: 1 }}>
          <label>User ID</label>
          <input value={userId} onChange={e => setUserId(e.target.value)} placeholder="Enter user UUID" />
        </div>
        <button type="submit" className="btn btn-primary">Load</button>
      </form>

      {error && <div className="error-msg">{error}</div>}

      {loading ? <div className="loading">Loading...</div> : profiles.length === 0 ? (
        <div className="empty">
          <p>No profiles found{userId ? ' for this user' : ''}</p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0 }}>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Keywords</th>
                <th>Interval</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {profiles.map(p => (
                <tr key={p.id}>
                  <td><Link to={`/profiles/${p.id}`}>{p.name}</Link></td>
                  <td>
                    <div className="keywords">
                      {p.keywords.map((k, i) => <span key={i} className="keyword-tag">{String((k as any).value ?? k)}</span>)}
                    </div>
                  </td>
                  <td>{p.search_interval_minutes} min</td>
                  <td>
                    <span className={`badge ${p.is_active ? 'badge-success' : 'badge-warning'}`}>
                      {p.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td>
                    <Link to={`/profiles/${p.id}/edit`} className="btn btn-outline btn-sm">Edit</Link>
                    {' '}
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(p.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
