import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { vacancyApi } from '../api/vacancy'
import type { Source } from '../api/types'

export default function VacancyForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [sources, setSources] = useState<Source[]>([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [employmentType, setEmploymentType] = useState('FULL_TIME')
  const [workFormat, setWorkFormat] = useState('REMOTE')
  const [salaryMin, setSalaryMin] = useState('')
  const [salaryMax, setSalaryMax] = useState('')
  const [location, setLocation] = useState('')
  const [url, setUrl] = useState('')
  const [sourceId, setSourceId] = useState('')
  const [externalId, setExternalId] = useState('')
  const [publishedAt, setPublishedAt] = useState(() => new Date().toISOString().slice(0, 16))
  const [status, setStatus] = useState('ACTIVE')

  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    vacancyApi.getSources(1, 100).then(r => setSources(r.items)).catch(() => {})
    if (!id) return
    vacancyApi.getVacancy(id)
      .then(v => {
        setTitle(v.title)
        setDescription(v.description)
        setCompanyName(v.company_name ?? '')
        setEmploymentType(v.employment_type)
        setWorkFormat(v.work_format)
        setSalaryMin(v.salary?.min_amount?.toString() ?? '')
        setSalaryMax(v.salary?.max_amount?.toString() ?? '')
        setLocation(v.location ?? '')
        setUrl(v.url)
        setSourceId(v.source_id)
        setExternalId(v.external_id ?? '')
        setPublishedAt(v.published_at.slice(0, 16))
        setStatus(v.status)
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      const data: any = {
        title,
        description,
        company_name: companyName || null,
        employment_type: employmentType,
        work_format: workFormat,
        salary_min_amount: salaryMin ? Number(salaryMin) : null,
        salary_max_amount: salaryMax ? Number(salaryMax) : null,
        location: location || null,
        url,
        published_at: new Date(publishedAt).toISOString(),
      }
      if (isEdit && id) {
        data.status = status
        await vacancyApi.updateVacancy(id, data)
        navigate(`/vacancies/${id}`)
      } else {
        data.vacancy_id = crypto.randomUUID()
        data.source_id = sourceId
        data.external_id = externalId || null
        await vacancyApi.createVacancy(data)
        navigate('/vacancies')
      }
    } catch (e: any) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div>
      <div className="page-header"><h2>{isEdit ? 'Edit Vacancy' : 'New Vacancy'}</h2></div>
      {error && <div className="error-msg">{error}</div>}
      <div className="card">
        <form onSubmit={handleSubmit}>
          {!isEdit && (
            <div className="form-group">
              <label>Source</label>
              <select value={sourceId} onChange={e => setSourceId(e.target.value)} required>
                <option value="">Select source...</option>
                {sources.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
              </select>
            </div>
          )}
          <div className="form-group">
            <label>Title</label>
            <input value={title} onChange={e => setTitle(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Company</label>
            <input value={companyName} onChange={e => setCompanyName(e.target.value)} />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Employment Type</label>
              <select value={employmentType} onChange={e => setEmploymentType(e.target.value)}>
                <option value="FULL_TIME">Full Time</option>
                <option value="PART_TIME">Part Time</option>
                <option value="CONTRACT">Contract</option>
                <option value="INTERNSHIP">Internship</option>
              </select>
            </div>
            <div className="form-group">
              <label>Work Format</label>
              <select value={workFormat} onChange={e => setWorkFormat(e.target.value)}>
                <option value="REMOTE">Remote</option>
                <option value="HYBRID">Hybrid</option>
                <option value="OFFICE">Office</option>
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Salary Min</label>
              <input type="number" value={salaryMin} onChange={e => setSalaryMin(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Salary Max</label>
              <input type="number" value={salaryMax} onChange={e => setSalaryMax(e.target.value)} />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Location</label>
              <input value={location} onChange={e => setLocation(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Published At</label>
              <input type="datetime-local" value={publishedAt} onChange={e => setPublishedAt(e.target.value)} required />
            </div>
          </div>
          <div className="form-group">
            <label>URL</label>
            <input value={url} onChange={e => setUrl(e.target.value)} placeholder="https://..." />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea rows={5} value={description} onChange={e => setDescription(e.target.value)} required />
          </div>
          {!isEdit && (
            <div className="form-group">
              <label>External ID</label>
              <input value={externalId} onChange={e => setExternalId(e.target.value)} />
            </div>
          )}
          {isEdit && (
            <div className="form-group">
              <label>Status</label>
              <select value={status} onChange={e => setStatus(e.target.value)}>
                <option value="ACTIVE">Active</option>
                <option value="ARCHIVED">Archived</option>
                <option value="DELETED">Deleted</option>
              </select>
            </div>
          )}
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : isEdit ? 'Update' : 'Create'}
            </button>
            <button type="button" className="btn btn-outline" onClick={() => navigate(-1)}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  )
}
