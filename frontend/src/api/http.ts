import { AUTH_API } from './config'
import type { ApiResponse } from './types'

export interface TokenStore {
  getAccessToken: () => string | null
  getRefreshToken: () => string | null
  setTokens: (access: string, refresh: string) => void
  clearTokens: () => void
}

let tokenStore: TokenStore = {
  getAccessToken: () => localStorage.getItem('access_token'),
  getRefreshToken: () => localStorage.getItem('refresh_token'),
  setTokens: (access: string, refresh: string) => {
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  },
  clearTokens: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_id')
  },
}

export function setTokenStore(store: TokenStore) {
  tokenStore = store
}

export function createHttpClient(baseUrl: string) {
  return async function request<T>(path: string, init?: RequestInit): Promise<T> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(init?.headers as Record<string, string>),
    }

    const accessToken = tokenStore.getAccessToken()
    if (accessToken) {
      headers['X-Access-Token'] = accessToken
    }

    const res = await fetch(`${baseUrl}${path}`, { ...init, headers })

    if (res.status === 401 && tokenStore.getRefreshToken()) {
      const refreshToken = tokenStore.getRefreshToken()
      try {
        const refreshRes = await fetch(`${AUTH_API}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refreshToken }),
        })
        if (refreshRes.ok) {
          const data: ApiResponse<{ access_token: string; refresh_token: string }> = await refreshRes.json()
          const tokens = data.result!
          tokenStore.setTokens(tokens.access_token, tokens.refresh_token)
          headers['X-Access-Token'] = tokens.access_token
          const retryRes = await fetch(`${baseUrl}${path}`, { ...init, headers })
          const retryBody: ApiResponse<T> = await retryRes.json()
          if (!retryRes.ok) throw new Error((retryBody as any).error ?? `HTTP ${retryRes.status}`)
          return retryBody.result as T
        }
      } catch {
      }
      tokenStore.clearTokens()
      window.location.href = '/login'
      throw new Error('Session expired')
    }

    const body: ApiResponse<T> = await res.json()
    if (!res.ok) throw new Error((body as any).error ?? `HTTP ${res.status}`)
    return body.result as T
  }
}
