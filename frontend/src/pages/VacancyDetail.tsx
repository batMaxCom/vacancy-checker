import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { vacancyApi } from '../api/vacancy'
import type { Vacancy } from '../api/types'

export default function VacancyDetail() {
  const { id } = useParams()
  const [vacancy, setVacancy] = useState<Vacancy | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return
    setLoading(true)
    vacancyApi.getVacancy(id)
      .then(v => {
        setVacancy(v)
        if (v.status === 'ACTIVE') {
          vacancyApi.updateVacancy(id, { status: 'VIEWED' })
            .then(() => setVacancy(prev => prev ? { ...prev, status: 'VIEWED' } : prev))
            .catch(() => {})
        }
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error-msg">{error}</div>
  if (!vacancy) return <div className="empty">Vacancy not found</div>

  return (
    <div>
      <div className="page-header">
        <h2>{vacancy.title}</h2>
        <Link to={`/vacancies/${vacancy.id}/edit`} className="btn btn-outline">Edit</Link>
      </div>

      <div className="card">
        <table>
          <tbody>
            <tr><td style={{ fontWeight: 600, width: 180 }}>ID</td><td>{vacancy.id}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Source ID</td><td>{vacancy.source_id}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Company</td><td>{vacancy.company_name || '-'}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Employment</td><td>{vacancy.employment_type}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Work Format</td><td>{vacancy.work_format}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Location</td><td>{vacancy.location || '-'}</td></tr>
            <tr><td style={{ fontWeight: 600 }}>Salary</td><td>
              {vacancy.salary
                ? `${vacancy.salary.min_amount ?? ''} - ${vacancy.salary.max_amount ?? ''}`.replace(/^ - /, 'up to ').replace(/ - $/, '+')
                : '-'}
            </td></tr>
            <tr><td style={{ fontWeight: 600 }}>URL</td><td>
              {vacancy.url ? <a href={vacancy.url} target="_blank" rel="noreferrer">{vacancy.url}</a> : '-'}
            </td></tr>
            <tr><td style={{ fontWeight: 600 }}>Status</td><td>
              <span className={`badge ${
                vacancy.status === 'ACTIVE' ? 'badge-success' :
                vacancy.status === 'ARCHIVED' ? 'badge-warning' : 'badge-danger'
              }`}>{vacancy.status}</span>
            </td></tr>
            <tr><td style={{ fontWeight: 600 }}>Published</td><td>{new Date(vacancy.published_at).toLocaleString()}</td></tr>
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: 8 }}>Description</h3>
        <pre>{vacancy.description || 'No description'}</pre>
      </div>
    </div>
  )
}
