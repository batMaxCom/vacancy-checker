import { SEARCH_API } from './config'
import type { ApiResponse, SearchProfile, SearchJob, SelectItem } from './types'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${SEARCH_API}${path}`, {
    ...init,
    headers: { 'Content-Type': 'application/json', ...init?.headers },
  })
  const body: ApiResponse<T> = await res.json()
  if (!res.ok) throw new Error((body as any).error ?? `HTTP ${res.status}`)
  return body.result as T
}

export const searchApi = {
  getProfiles: (userId: string) =>
    request<SearchProfile[]>(`/api/v1/search-profiles?user_id=${userId}`),

  getProfile: (id: string) =>
    request<SearchProfile>(`/api/v1/search-profiles/${id}`),

  createProfile: (data: {
    user_id: string
    name: string
    keywords: string[]
    search_interval_minutes: number
  }) =>
    request<string>('/api/v1/search-profiles', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateProfile: (id: string, data: {
    name: string
    keywords: string[]
    search_interval_minutes: number
  }) =>
    request<null>(`/api/v1/search-profiles/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  deleteProfile: (id: string) =>
    request<null>(`/api/v1/search-profiles/${id}`, { method: 'DELETE' }),

  activateProfile: (id: string) =>
    request<null>(`/api/v1/search-profiles/${id}/activate`, { method: 'POST' }),

  deactivateProfile: (id: string) =>
    request<null>(`/api/v1/search-profiles/${id}/deactivate`, { method: 'POST' }),

  runSearch: (id: string) =>
    request<string>(`/api/v1/search-profiles/${id}/search`, { method: 'POST' }),

  getProfileSelectList: (userId: string) =>
    request<SelectItem[]>(`/api/v1/search-profiles/select/${userId}`),

  getJobs: (profileId: string) =>
    request<SearchJob[]>(`/api/v1/search-profiles/${profileId}/jobs`),

  getJob: (jobId: string) =>
    request<SearchJob>(`/api/v1/search-jobs/${jobId}`),

  deleteJobsByProfile: (profileId: string) =>
    request<null>(`/api/v1/search-jobs/profile/${profileId}`, { method: 'DELETE' }),
}
