import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { searchApi } from '../api/search'
export default function ProfileForm() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)
  const [name, setName] = useState('')
  const [keywords, setKeywords] = useState('')
  const [searchInterval, setSearchInterval] = useState(60)
  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return
    searchApi.getProfile(id)
      .then(p => {
        setName(p.name)
        setKeywords(p.keywords.map((k: any) => String((k as any).value ?? k)).join(', '))
        setSearchInterval(p.search_interval_minutes)
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [id])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    const kwList = keywords.split(',').map(s => s.trim()).filter(Boolean)
    try {
      if (isEdit && id) {
        await searchApi.updateProfile(id, { name, keywords: kwList, search_interval_minutes: searchInterval })
        navigate(`/profiles/${id}`)
      } else {
        const userId = localStorage.getItem('userId')
        if (!userId) { alert('Enter a User ID on the profiles page first'); return }
        const newId = await searchApi.createProfile({
          user_id: userId,
          name,
          keywords: kwList,
          search_interval_minutes: searchInterval,
        })
        navigate(`/profiles/${newId}`)
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
      <div className="page-header"><h2>{isEdit ? 'Edit Profile' : 'New Profile'}</h2></div>
      {error && <div className="error-msg">{error}</div>}
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input value={name} onChange={e => setName(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Keywords (comma-separated)</label>
            <input value={keywords} onChange={e => setKeywords(e.target.value)} placeholder="python, golang, remote" />
          </div>
          <div className="form-group">
            <label>Search Interval (minutes)</label>
            <input type="number" value={searchInterval} onChange={e => setSearchInterval(Number(e.target.value))} min={1} />
          </div>
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
