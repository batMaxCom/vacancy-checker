import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { vacancyApi } from '../api/vacancy'

export default function SourceForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)
  const [name, setName] = useState('')
  const [baseUrl, setBaseUrl] = useState('')
  const [isActive, setIsActive] = useState(true)
  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return
    vacancyApi.getSource(id)
      .then(s => { setName(s.name); setBaseUrl(s.base_url); setIsActive(s.is_active) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    try {
      if (isEdit && id) {
        await vacancyApi.updateSource(id, { name, base_url: baseUrl, is_active: isActive })
      } else {
        await vacancyApi.createSource({ name, base_url: baseUrl })
      }
      navigate('/sources')
    } catch (e: any) {
      setError(e.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="loading">Loading...</div>

  return (
    <div>
      <div className="page-header"><h2>{isEdit ? 'Edit Source' : 'New Source'}</h2></div>
      {error && <div className="error-msg">{error}</div>}
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input value={name} onChange={e => setName(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Base URL</label>
            <input value={baseUrl} onChange={e => setBaseUrl(e.target.value)} placeholder="https://api.example.com" />
          </div>
          {isEdit && (
            <div className="form-group">
              <label>
                <input type="checkbox" checked={isActive} onChange={e => setIsActive(e.target.checked)} style={{ width: 'auto', marginRight: 8 }} />
                Active
              </label>
            </div>
          )}
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : isEdit ? 'Update' : 'Create'}
            </button>
            <button type="button" className="btn btn-outline" onClick={() => navigate('/sources')}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  )
}
