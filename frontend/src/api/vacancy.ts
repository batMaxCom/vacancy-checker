import { VACANCY_API } from './config'
import type { ApiResponse, PaginationResult, SelectItem, Source, Vacancy } from './types'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${VACANCY_API}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  const body: ApiResponse<T> = await res.json()
  if (!res.ok) throw new Error((body as any).error ?? `HTTP ${res.status}`)
  return body.result as T
}

export const vacancyApi = {
  getSources: (page = 1, pageSize = 20) =>
    request<PaginationResult<Source>>(`/source/list/paginated?page_number=${page}&page_size=${pageSize}`),

  getSourceSelectList: () =>
    request<SelectItem[]>('/source/list/select'),

  getSource: (id: string) =>
    request<Source>(`/source/${id}`),

  createSource: (data: { name: string; base_url?: string }) =>
    request<null>('/source', { method: 'POST', body: JSON.stringify({ body: data }) }),

  updateSource: (id: string, data: {
    name?: string
    base_url?: string
    is_active?: boolean
  }) =>
    request<null>(`/source/${id}`, { method: 'PUT', body: JSON.stringify({ body: data }) }),

  getVacancies: (page = 1, pageSize = 20) =>
    request<PaginationResult<Vacancy>>(`/vacancy/list/paginated?page_number=${page}&page_size=${pageSize}`),

  getVacancy: (id: string) =>
    request<Vacancy>(`/vacancy/${id}`),

  createVacancy: (data: {
    vacancy_id: string
    source_id: string
    external_id: string | null
    title: string
    description: string
    company_name: string | null
    employment_type: string
    work_format: string
    salary_min_amount: number | null
    salary_max_amount: number | null
    location: string | null
    url: string
    published_at: string
  }) =>
    request<null>('/vacancy', { method: 'POST', body: JSON.stringify({ body: data }) }),

  updateVacancy: (id: string, data: Record<string, unknown>) =>
    request<null>(`/vacancy/${id}`, { method: 'PUT', body: JSON.stringify({ body: data }) }),
}
