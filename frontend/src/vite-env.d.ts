/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_SEARCH_API: string
  readonly VITE_VACANCY_API: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
