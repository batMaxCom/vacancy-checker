export interface ApiResponse<T> {
  status_code: number
  result: T | null
}

export interface PaginationResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface SelectItem<T = string> {
  value: T
  label: string
}

export interface SearchProfile {
  id: string
  user_id: string
  name: string
  keywords: { value: string }[]
  search_interval_minutes: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface SearchJob {
  id: string
  profile_id: string
  started_at: string
  finished_at: string | null
  status: 'pending' | 'running' | 'success' | 'failed'
  vacancies_found: number
}

export interface Source {
  id: string
  name: string
  base_url: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Salary {
  min_amount: number | null
  max_amount: number | null
}

export interface Vacancy {
  id: string
  source_id: string
  external_id: string | null
  title: string
  description: string
  company_name: string | null
  employment_type: string
  work_format: string
  salary: Salary | null
  location: string | null
  url: string
  status: string
  published_at: string
  created_at: string
  updated_at: string
}
