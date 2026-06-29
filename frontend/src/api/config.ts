const runtimeEnv = typeof window !== 'undefined' ? window.__ENV__ ?? {} : {}
const env = (key: string, fallback: string) =>
  runtimeEnv[key] ?? import.meta.env[key] ?? fallback

const API_HOST = env('VITE_API_HOST', 'http://localhost:8080')

export const SEARCH_API  = env('VITE_SEARCH_API',  API_HOST)
export const VACANCY_API = env('VITE_VACANCY_API', API_HOST)
export const AUTH_API    = env('VITE_AUTH_API',    API_HOST)
export const USER_API    = env('VITE_USER_API',    API_HOST)
