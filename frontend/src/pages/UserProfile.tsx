import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { userApi } from '../api/user'
import type { UserProfile } from '../api/types'

export default function UserProfilePage() {
  const { user: authUser, logout } = useAuth()
  const navigate = useNavigate()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [editing, setEditing] = useState(false)
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState('')

  const load = () => {
    setLoading(true)
    setError('')
    userApi.getMe()
      .then(p => { setProfile(p); setFirstName(p.first_name); setLastName(p.last_name) })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!authUser) return
    setSaveError('')
    setSaving(true)
    try {
      await userApi.updateProfile({ first_name: firstName, last_name: lastName })
      setEditing(false)
      load()
    } catch (err: any) {
      setSaveError(err.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!authUser) return
    if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) return
    try {
      await userApi.deleteUser()
      await logout()
      navigate('/login')
    } catch (err: any) {
      alert(err.message)
    }
  }

  if (loading) return <div className="loading">Loading...</div>
  if (error) return <div className="error-msg">{error}</div>
  if (!profile) return <div className="empty"><p>Profile not found</p></div>

  return (
    <div>
      <div className="page-header">
        <h2>My Profile</h2>
        {!editing && (
          <button className="btn btn-primary" onClick={() => { setFirstName(profile.first_name); setLastName(profile.last_name); setEditing(true) }}>
            Edit Profile
          </button>
        )}
      </div>

      {editing ? (
        <form onSubmit={handleSave} className="card">
          {saveError && <div className="error-msg">{saveError}</div>}
          <div className="form-row">
            <div className="form-group">
              <label>First Name</label>
              <input value={firstName} onChange={e => setFirstName(e.target.value)} required autoFocus />
            </div>
            <div className="form-group">
              <label>Last Name</label>
              <input value={lastName} onChange={e => setLastName(e.target.value)} required />
            </div>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Saving...' : 'Save'}
            </button>
            <button type="button" className="btn btn-outline" onClick={() => setEditing(false)}>Cancel</button>
          </div>
        </form>
      ) : (
        <div className="card">
          <table>
            <tbody>
              <tr><td style={{ fontWeight: 600, width: 140 }}>ID</td><td style={{ fontFamily: 'monospace', fontSize: 13 }}>{profile.id}</td></tr>
              <tr><td style={{ fontWeight: 600 }}>Email</td><td>{profile.email}</td></tr>
              <tr><td style={{ fontWeight: 600 }}>First Name</td><td>{profile.first_name}</td></tr>
              <tr><td style={{ fontWeight: 600 }}>Last Name</td><td>{profile.last_name}</td></tr>
              <tr><td style={{ fontWeight: 600 }}>Role</td><td><span className="badge badge-info">{profile.role}</span></td></tr>
              <tr><td style={{ fontWeight: 600 }}>Status</td><td>
                <span className={`badge ${profile.status === 'ACTIVE' ? 'badge-success' : profile.status === 'SUSPENDED' ? 'badge-warning' : 'badge-danger'}`}>
                  {profile.status}
                </span>
              </td></tr>
            </tbody>
          </table>
        </div>
      )}

      <div className="card" style={{ border: '1px solid var(--color-danger)', marginTop: 24 }}>
        <h3 style={{ color: 'var(--color-danger)', marginBottom: 8 }}>Danger Zone</h3>
        <p style={{ fontSize: 14, color: 'var(--color-text-secondary)', marginBottom: 12 }}>
          Once you delete your account, there is no going back. Please be certain.
        </p>
        <button className="btn btn-danger" onClick={handleDelete}>Delete Account</button>
      </div>
    </div>
  )
}
