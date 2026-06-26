export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
}

export interface TokenResult {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface ApiAuthResponse<T> {
  status_code: number
  result: T
}

async function authRequest<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data: ApiAuthResponse<T> = await res.json()
  if (!res.ok) throw new Error((data as any).error ?? `HTTP ${res.status}`)
  return data.result
}

import { AUTH_API } from './config'

export const authApi = {
  login: (data: LoginRequest) =>
    authRequest<TokenResult>(`${AUTH_API}/auth/login`, data),

  register: (data: RegisterRequest) =>
    authRequest<null>(`${AUTH_API}/auth/register`, data),

  refresh: (refreshToken: string) =>
    authRequest<TokenResult>(`${AUTH_API}/auth/refresh`, { refresh_token: refreshToken }),

  logout: (userId: string, refreshToken: string) =>
    authRequest<null>(`${AUTH_API}/auth/logout?user_id=${encodeURIComponent(userId)}`, { refresh_token: refreshToken }),
}
