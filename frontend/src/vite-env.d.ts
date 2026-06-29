/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_HOST: string
  readonly VITE_SEARCH_API?: string
  readonly VITE_VACANCY_API?: string
  readonly VITE_AUTH_API?: string
  readonly VITE_USER_API?: string
}

interface Window {
  __ENV__?: Partial<ImportMetaEnv>
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
