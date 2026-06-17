# CCheck Frontend

React SPA для управления поисковыми профилями, источниками и вакансиями.

## Требования

- Node.js >= 20

## Установка и запуск

```bash
npm install

# Настройка API (опционально, если сервисы не на localhost:8000/8001)
cp .env.example .env
# VITE_SEARCH_API=http://localhost:8000
# VITE_VACANCY_API=http://localhost:8001

npm run dev        # http://localhost:3000
npm run build      # production сборка в dist/
```

## Страницы

| Путь | Описание |
|------|----------|
| `/` | Dashboard со статусами сервисов |
| `/profiles` | Список поисковых профилей (по User ID) |
| `/profiles/new` | Создать профиль |
| `/profiles/:id` | Детали профиля, управление (activate/deactivate/run), история поисков |
| `/profiles/:id/edit` | Редактировать профиль |
| `/sources` | Список источников вакансий |
| `/sources/new` | Создать источник |
| `/sources/:id/edit` | Редактировать источник |
| `/vacancies` | Список вакансий |
| `/vacancies/new` | Создать вакансию |
| `/vacancies/:id` | Детали вакансии |
| `/vacancies/:id/edit` | Редактировать вакансию |
