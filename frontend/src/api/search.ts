import { SEARCH_API } from './config'
import type { SearchProfile, SearchJob, SelectItem } from './types'
import { createHttpClient } from './http'

const request = createHttpClient(SEARCH_API)

export const searchApi = {
  getProfiles: () =>
    request<SearchProfile[]>('/search-profiles'),

  getProfile: (id: string) =>
    request<SearchProfile>(`/search-profiles/${id}`),

  createProfile: (data: {
    name: string
    keywords: string[]
    search_interval_minutes: number
  }) =>
    request<string>('/search-profiles', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  updateProfile: (id: string, data: {
    name: string
    keywords: string[]
    search_interval_minutes: number
  }) =>
    request<null>(`/search-profiles/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  deleteProfile: (id: string) =>
    request<null>(`/search-profiles/${id}`, { method: 'DELETE' }),

  activateProfile: (id: string) =>
    request<null>(`/search-profiles/${id}/activate`, { method: 'POST' }),

  deactivateProfile: (id: string) =>
    request<null>(`/search-profiles/${id}/deactivate`, { method: 'POST' }),

  runSearch: (id: string) =>
    request<string>(`/search-profiles/${id}/search`, { method: 'POST' }),

  getProfileSelectList: () =>
    request<SelectItem[]>('/search-profiles/select'),

  getJobs: (profileId: string) =>
    request<SearchJob[]>(`/search-profiles/${profileId}/jobs`),

  getJob: (jobId: string) =>
    request<SearchJob>(`/search-jobs/${jobId}`),

  deleteJobsByProfile: (profileId: string) =>
    request<null>(`/search-jobs/profile/${profileId}`, { method: 'DELETE' }),
}
