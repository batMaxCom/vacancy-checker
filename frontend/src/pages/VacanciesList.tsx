import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { vacancyApi } from '../api/vacancy'
import { searchApi } from '../api/search'
import type { Vacancy, SelectItem } from '../api/types'

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
  const [profiles, setProfiles] = useState<SelectItem[]>([])
  const [selectedProfile, setSelectedProfile] = useState('')

  const load = (p: number, profileId?: string) => {
    setLoading(true)
    setError('')
    vacancyApi.getVacancies(p, 20, profileId)
      .then(r => { setVacancies(r.items); setTotalPages(r.total_pages); setPage(r.page) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  const handleProfileChange = (value: string) => {
    setSelectedProfile(value)
    load(1, value || undefined)
  }

  useEffect(() => {
    searchApi.getProfileSelectList()
      .then(items => {
        const mapped: SelectItem[] = items.map((i: any) => ({ value: i.id ?? i.value, label: i.name ?? i.label }))
        const sorted = [...mapped].sort((a, b) => a.label.localeCompare(b.label))
        setProfiles(sorted)
      })
      .catch(() => {})
    load(1)
  }, [])

  return (
    <div>
      <div className="page-header">
        <h2>Vacancies</h2>
        <Link to="/vacancies/new" className="btn btn-primary">+ New Vacancy</Link>
      </div>

      <div className="card" style={{ display: 'flex', gap: 8, alignItems: 'flex-end', padding: 16, marginBottom: 16 }}>
        <div className="form-group" style={{ margin: 0, flex: 1 }}>
          <label>Profile</label>
          <select value={selectedProfile} onChange={e => handleProfileChange(e.target.value)}>
            <option value="">All</option>
            {profiles.map(p => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>
        </div>
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
              <button className="btn btn-outline btn-sm" disabled={page <= 1} onClick={() => load(page - 1, selectedProfile || undefined)}>Prev</button>
              <span style={{ padding: '4px 8px', fontSize: 14 }}>{page} / {totalPages}</span>
              <button className="btn btn-outline btn-sm" disabled={page >= totalPages} onClick={() => load(page + 1, selectedProfile || undefined)}>Next</button>
            </div>
          )}
        </>
      )}
    </div>
  )
}
