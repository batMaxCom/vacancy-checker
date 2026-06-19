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

const STATUS_MAP = ['ACTIVE', 'ARCHIVED', 'DELETED']

function mapVacancy(r: any): Vacancy {
  return {
    id: r.vacancy_id,
    source_id: r.source_id,
    external_id: r.external_id ?? null,
    title: r.title,
    description: r.description,
    company_name: r.company_name || null,
    employment_type: r.employment_type ?? '',
    work_format: r.work_format ?? '',
    salary: r.salary ?? null,
    location: r.location || null,
    url: r.url,
    status: STATUS_MAP[r.status - 1] ?? 'ACTIVE',
    published_at: r.published_at,
    created_at: r.created_at,
    updated_at: r.updated_at,
  }
}

export const vacancyApi = {
  getSources: async (page = 1, pageSize = 20) => {
    const result = await request<any>(`/source/list/paginated?page_number=${page}&page_size=${pageSize}`)
    return {
      items: (result.records || []).map((r: any) => ({
        id: r.source_id,
        name: r.name,
        base_url: r.base_url,
        is_active: r.is_active,
        created_at: r.created_at ?? '',
        updated_at: r.updated_at ?? '',
      })),
      total: result.count_records,
      page: result.page,
      page_size: pageSize,
      total_pages: result.max_page_count,
    } as PaginationResult<Source>
  },

  getSourceSelectList: () =>
    request<SelectItem[]>('/source/list/select'),

  getSource: async (id: string) => {
    const result = await request<any>(`/source/${id}`)
    return {
      id: result.source_id,
      name: result.name,
      base_url: result.base_url,
      is_active: result.is_active,
      created_at: result.created_at ?? '',
      updated_at: result.updated_at ?? '',
    } as Source
  },

  createSource: (data: { name: string; base_url?: string }) =>
    request<null>('/source', { method: 'POST', body: JSON.stringify({ body: data }) }),

  updateSource: (id: string, data: {
    name?: string
    base_url?: string
    is_active?: boolean
  }) =>
    request<null>(`/source/${id}`, { method: 'PUT', body: JSON.stringify({ body: data }) }),

  getVacancies: async (page = 1, pageSize = 20, profileId?: string) => {
    const params = new URLSearchParams({ page_number: String(page), page_size: String(pageSize) })
    if (profileId) params.set('profile_id', profileId)
    const result = await request<any>(`/vacancy/list/paginated?${params}`)
    return {
      items: (result.records || []).map(mapVacancy),
      total: result.count_records,
      page: result.page,
      page_size: pageSize,
      total_pages: result.max_page_count,
    } as PaginationResult<Vacancy>
  },

  getVacancy: async (id: string) => {
    const result = await request<any>(`/vacancy/${id}`)
    return mapVacancy(result)
  },

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
