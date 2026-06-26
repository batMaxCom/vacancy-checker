import { USER_API } from './config'
import type { UserProfile } from './types'
import { createHttpClient } from './http'

const request = createHttpClient(USER_API)

export const userApi = {
  getMe: () =>
    request<UserProfile>('/profile'),

  updateProfile: (data: { first_name: string; last_name: string }) =>
    request<null>('/profile', {
      method: 'PATCH',
      body: JSON.stringify(data),
    }),

  deleteUser: () =>
    request<null>('/profile', { method: 'DELETE' }),
}
