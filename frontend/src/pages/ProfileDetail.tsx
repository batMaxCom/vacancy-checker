import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { searchApi } from '../api/search'
import type { SearchProfile, SearchJob } from '../api/types'

export default function ProfileDetail() {
  const { id } = useParams()
  const [profile, setProfile] = useState<SearchProfile | null>(null)
  const [jobs, setJobs] = useState<SearchJob[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [running, setRunning] = useState(false)

  const load = () => {
    if (!id) return
    setLoading(true)
    setError('')
    Promise.all([
      searchApi.getProfile(id),
      searchApi.getJobs(id),
    ])
      .then(([p, j]) => { setProfile(p); setJobs(j) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [id])

  const toggleActive = async () => {
    if (!profile) return
    try {
      if (profile.is_active) {
        await searchApi.deactivateProfile(profile.id)
      } else {
        await searchApi.activateProfile(profile.id)
      }
      load()
    } catch (e: any) { alert(e.message) }
  }

  const handleRunSearch = async () => {
    if (!profile) return
    setRunning(true)
    try {
      await searchApi.runSearch(profile.id)
      load()
    } catch (e: any) { alert(e.message) }
    finally { setRunning(false) }
  }

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error-msg">{error}</div>
  if (!profile) return <div className="empty">Profile not found</div>

  return (
    <div>
      <div className="page-header">
        <h2>{profile.name}</h2>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className={`btn ${profile.is_active ? 'btn-outline' : 'btn-primary'}`} onClick={toggleActive}>
            {profile.is_active ? 'Deactivate' : 'Activate'}
          </button>
          <button className="btn btn-primary" onClick={handleRunSearch} disabled={running}>
            {running ? 'Running...' : 'Run Search'}
          </button>
          <Link to={`/profiles/${profile.id}/edit`} className="btn btn-outline">Edit</Link>
        </div>
      </div>

      <div className="card">
        <table>
          <tbody>
            <tr><td style={{ fontWeight: 600, width: 200 }}>ID</td><td>{profile.id}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>User ID</td><td>{profile.user_id}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Keywords</td><td>
              <div className="keywords">
                {profile.keywords.map((k, i) => <span key={i} className="keyword-tag">{String((k as any).value ?? k)}</span>)}
              </div>
            </td></tr>
            <tr><td style={{ fontWeight: 600 }}>Interval</td><td>{profile.search_interval_minutes} min</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Status</td><td>
              <span className={`badge ${profile.is_active ? 'badge-success' : 'badge-warning'}`}>
                {profile.is_active ? 'Active' : 'Inactive'}
              </span>
            </td></tr>
            <tr><td style={{ fontWeight: 600 }}>Created</td><td>{new Date(profile.created_at).toLocaleString()}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Updated</td><td>{new Date(profile.updated_at).toLocaleString()}</td></tr>
          </tbody>
        </table>
      </div>

      <h3 style={{ marginBottom: 12, marginTop: 24 }}>Search Jobs</h3>
      {jobs.length === 0 ? (
        <div className="empty"><p>No search jobs yet</p></div>
      ) : (
        <div className="card" style={{ padding: 0 }}>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Started</th>
                <th>Finished</th>
                <th>Status</th>
                <th>Found</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map(j => (
                <tr key={j.id}>
                  <td style={{ fontFamily: 'monospace', fontSize: 12 }}>{j.id.slice(0, 8)}...</td>
                  <td>{new Date(j.started_at).toLocaleString()}</td>
                  <td>{j.finished_at ? new Date(j.finished_at).toLocaleString() : '-'}</td>
                  <td>
                    <span className={`badge ${
                      j.status === 'success' ? 'badge-success' :
                      j.status === 'failed' ? 'badge-danger' :
                      j.status === 'running' ? 'badge-info' : 'badge-warning'
                    }`}>{j.status}</span>
                  </td>
                  <td>{j.vacancies_found}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
