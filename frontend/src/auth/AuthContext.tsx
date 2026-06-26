import { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from 'react'
import { authApi, type TokenResult } from '../api/auth'
import { setTokenStore } from '../api/http'

function decodePayload(token: string): { sub: string; role: string } | null {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch {
    return null
  }
}

interface AuthState {
  user: { id: string; role: string } | null
  isAuthenticated: boolean
  isLoading: boolean
}

interface AuthContextValue extends AuthState {
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, first_name: string, last_name: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>(() => {
    const accessToken = localStorage.getItem('access_token')
    if (accessToken) {
      const payload = decodePayload(accessToken)
      if (payload) {
        return { user: { id: payload.sub, role: payload.role }, isAuthenticated: true, isLoading: false }
      }
    }
    return { user: null, isAuthenticated: false, isLoading: true }
  })

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token')
    if (accessToken) {
      const payload = decodePayload(accessToken)
      if (payload) {
        setState({ user: { id: payload.sub, role: payload.role }, isAuthenticated: true, isLoading: false })
      } else {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        setState({ user: null, isAuthenticated: false, isLoading: false })
      }
    } else {
      setState(s => ({ ...s, isLoading: false }))
    }
  }, [])

  useEffect(() => {
    setTokenStore({
      getAccessToken: () => localStorage.getItem('access_token'),
      getRefreshToken: () => localStorage.getItem('refresh_token'),
      setTokens: (access: string, refresh: string) => {
        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        const payload = decodePayload(access)
        if (payload) {
          localStorage.setItem('user_id', payload.sub)
          setState({ user: { id: payload.sub, role: payload.role }, isAuthenticated: true, isLoading: false })
        }
      },
      clearTokens: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_id')
        setState({ user: null, isAuthenticated: false, isLoading: false })
      },
    })
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const result: TokenResult = await authApi.login({ email, password })
    localStorage.setItem('access_token', result.access_token)
    localStorage.setItem('refresh_token', result.refresh_token)
    const payload = decodePayload(result.access_token)
    if (payload) {
      localStorage.setItem('user_id', payload.sub)
      setState({ user: { id: payload.sub, role: payload.role }, isAuthenticated: true, isLoading: false })
    }
  }, [])

  const register = useCallback(async (email: string, password: string, first_name: string, last_name: string) => {
    await authApi.register({ email, password, first_name, last_name })
  }, [])

  const logout = useCallback(async () => {
    const userId = localStorage.getItem('user_id')
    const refreshToken = localStorage.getItem('refresh_token')
    if (userId && refreshToken) {
      try {
        await authApi.logout(userId, refreshToken)
      } catch {
      }
    }
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_id')
    setState({ user: null, isAuthenticated: false, isLoading: false })
  }, [])

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
