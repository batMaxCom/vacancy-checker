import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { vacancyApi } from '../api/vacancy'
import type { Source } from '../api/types'

export default function SourcesList() {
  const [sources, setSources] = useState<Source[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  const load = (p: number) => {
    setLoading(true)
    setError('')
    vacancyApi.getSources(p)
      .then(r => { setSources(r.items); setTotalPages(r.total_pages); setPage(r.page) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load(page) }, [])

  return (
    <div>
      <div className="page-header">
        <h2>Sources</h2>
        <Link to="/sources/new" className="btn btn-primary">+ New Source</Link>
      </div>

      {error && <div className="error-msg">{error}</div>}

      {loading ? <div className="loading">Loading...</div> : sources.length === 0 ? (
        <div className="empty"><p>No sources found</p></div>
      ) : (
        <>
          <div className="card" style={{ padding: 0 }}>
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Base URL</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sources.map(s => (
                  <tr key={s.id}>
                    <td>{s.name}</td>
                    <td style={{ fontFamily: 'monospace', fontSize: 13 }}>{s.base_url || '-'}</td>
                    <td>
                      <span className={`badge ${s.is_active ? 'badge-success' : 'badge-warning'}`}>
                        {s.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <Link to={`/sources/${s.id}/edit`} className="btn btn-outline btn-sm">Edit</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {totalPages > 1 && (
            <div style={{ display: 'flex', gap: 8, justifyContent: 'center', marginTop: 16 }}>
              <button className="btn btn-outline btn-sm" disabled={page <= 1} onClick={() => load(page - 1)}>Prev</button>
              <span style={{ padding: '4px 8px', fontSize: 14 }}>{page} / {totalPages}</span>
              <button className="btn btn-outline btn-sm" disabled={page >= totalPages} onClick={() => load(page + 1)}>Next</button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
