import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { vacancyApi } from '../api/vacancy'
import type { Vacancy } from '../api/types'

const statusBadge: Record<string, string> = {
  ACTIVE: 'badge-success',
  ARCHIVED: 'badge-warning',
  DELETED: 'badge-danger',
}

export default function VacanciesList() {
  const [vacancies, setVacancies] = useState<Vacancy[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  const load = (p: number) => {
    setLoading(true)
    setError('')
    vacancyApi.getVacancies(p)
      .then(r => { setVacancies(r.items); setTotalPages(r.total_pages); setPage(r.page) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load(page) }, [])

  return (
    <div>
      <div className="page-header">
        <h2>Vacancies</h2>
        <Link to="/vacancies/new" className="btn btn-primary">+ New Vacancy</Link>
      </div>

      {error && <div className="error-msg">{error}</div>}

      {loading ? <div className="loading">Loading...</div> : vacancies.length === 0 ? (
        <div className="empty"><p>No vacancies found</p></div>
      ) : (
        <>
          <div className="card" style={{ padding: 0 }}>
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Company</th>
                  <th>Employment</th>
                  <th>Format</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {vacancies.map(v => (
                  <tr key={v.id}>
                    <td><Link to={`/vacancies/${v.id}`}>{v.title}</Link></td>
                    <td>{v.company_name || '-'}</td>
                    <td>{v.employment_type}</td>
                    <td>{v.work_format}</td>
                    <td>{v.location || '-'}</td>
                    <td>
                      <span className={`badge ${statusBadge[v.status] || 'badge-info'}`}>{v.status}</span>
                    </td>
                    <td>
                      <Link to={`/vacancies/${v.id}`} className="btn btn-outline btn-sm">View</Link>
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
