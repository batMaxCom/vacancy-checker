import { Routes, Route } from 'react-router-dom'
import Layout from './pages/Layout'
import Home from './pages/Home'
import ProfilesList from './pages/ProfilesList'
import ProfileDetail from './pages/ProfileDetail'
import ProfileForm from './pages/ProfileForm'
import SourcesList from './pages/SourcesList'
import SourceForm from './pages/SourceForm'
import VacanciesList from './pages/VacanciesList'
import VacancyDetail from './pages/VacancyDetail'
import VacancyForm from './pages/VacancyForm'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/profiles" element={<ProfilesList />} />
        <Route path="/profiles/new" element={<ProfileForm />} />
        <Route path="/profiles/:id" element={<ProfileDetail />} />
        <Route path="/profiles/:id/edit" element={<ProfileForm />} />
        <Route path="/sources" element={<SourcesList />} />
        <Route path="/sources/new" element={<SourceForm />} />
        <Route path="/sources/:id/edit" element={<SourceForm />} />
        <Route path="/vacancies" element={<VacanciesList />} />
        <Route path="/vacancies/new" element={<VacancyForm />} />
        <Route path="/vacancies/:id" element={<VacancyDetail />} />
        <Route path="/vacancies/:id/edit" element={<VacancyForm />} />
      </Routes>
    </Layout>
  )
}
