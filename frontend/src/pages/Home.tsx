import { useEffect, useState } from 'react'
import { searchApi } from '../api/search'
import { vacancyApi } from '../api/vacancy'

export default function Home() {
  const [health, setHealth] = useState({ search: '?', vacancy: '?' })

  useEffect(() => {
    Promise.allSettled([
      searchApi.getProfiles('00000000-0000-0000-0000-000000000000').then(() => {}),
      vacancyApi.getSources(1, 1).then(() => {}),
    ]).then(([s, v]) => {
      setHealth({
        search: s.status === 'fulfilled' ? 'OK' : 'Error',
        vacancy: v.status === 'fulfilled' ? 'OK' : 'Error',
      })
    })
  }, [])

  return (
    <div>
      <div className="page-header"><h2>Dashboard</h2></div>
      <div style={{ display: 'flex', gap: 16 }}>
        <div className="card" style={{ flex: 1 }}>
          <h3>Search Service</h3>
          <p style={{ marginTop: 8 }}>
            Status: <span className={`badge ${health.search === 'OK' ? 'badge-success' : 'badge-danger'}`}>{health.search}</span>
          </p>
        </div>
        <div className="card" style={{ flex: 1 }}>
          <h3>Vacancy Service</h3>
          <p style={{ marginTop: 8 }}>
            Status: <span className={`badge ${health.vacancy === 'OK' ? 'badge-success' : 'badge-danger'}`}>{health.vacancy}</span>
          </p>
        </div>
      </div>
      <div className="card" style={{ marginTop: 16 }}>
        <h3>Quick Links</h3>
        <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
          <a href="/profiles" className="btn btn-primary">Search Profiles</a>
          <a href="/sources" className="btn btn-outline">Sources</a>
          <a href="/vacancies" className="btn btn-outline">Vacancies</a>
        </div>
      </div>
    </div>
  )
}
