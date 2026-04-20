# Images API Backend

FastAPI backend для сервиса рисунков. Проект построен по слоистой архитектуре и пока не использует базу данных: пользователи и метаданные рисунков хранятся в памяти процесса, а PNG-файлы сохраняются на диск.

## Что умеет

- регистрация пользователя
- логин и выдача JWT access token
- получение профиля текущего пользователя
- создание рисунка через multipart/form-data
- просмотр, обновление и удаление своих рисунков
- получение PNG-файла по отдельному URL
- публичная галерея всех рисунков с именем автора

## Архитектура

Проект разбит на следующие слои:

- `app/api` — маршруты и зависимости FastAPI
- `app/services` — бизнес-логика
- `app/repositories` — in-memory репозитории
- `app/models` — доменные сущности
- `app/storage` — файловое хранилище для PNG
- `app/core` — настройки, безопасность, общие ошибки
- `app/schemas` — схемы запросов и ответов

Репозитории специально сделаны без БД. Это удобно для демонстрации архитектуры и быстрой разработки, но данные теряются после перезапуска приложения.

## Технологии

- FastAPI
- Uvicorn
- Pydantic v2
- python-jose для JWT
- passlib для хеширования паролей
- python-multipart для загрузки файлов

## Установка

Из корня репозитория:

```bash
cd backend
python -m venv ../venv
source ../venv/bin/activate
pip install -r requirements.txt
```

Если виртуальное окружение уже создано в корне репозитория, достаточно активировать его и поставить зависимости из `backend/requirements.txt`.

## Переменные окружения

Скопируй `.env.example` в `.env` и при необходимости измени значения:

- `APP_NAME` — название приложения
- `JWT_SECRET_KEY` — секрет для подписи JWT
- `JWT_ALGORITHM` — алгоритм JWT, по умолчанию `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES` — время жизни access token
- `STORAGE_DIR` — папка для PNG-файлов
- `CORS_ORIGINS` — разрешённые origin-ы фронтенда

## Запуск

Запуск из каталога `backend`:

```bash
PYTHONPATH=/Users/d.lobanev/Desktop/vsh/backend /Users/d.lobanev/Desktop/vsh/venv/bin/python -m app.main
```

Если удобнее через Uvicorn:

```bash
PYTHONPATH=/Users/d.lobanev/Desktop/vsh/backend uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

После старта:

- API: `http://localhost:8080/api`
- Swagger: `http://localhost:8080/docs`
- OpenAPI schema: `http://localhost:8080/openapi.json`

## Авторизация

JWT передаётся в заголовке:

```http
Authorization: Bearer <access_token>
```

Сессии и refresh token не используются, только access token, как и было задумано для этой версии проекта.

## API

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`

Пример регистрации:

```bash
curl -X POST http://localhost:8080/api/auth/register \
	-H 'Content-Type: application/json' \
	-d '{"username":"demo","password":"demo_password"}'
```

Пример логина:

```bash
curl -X POST http://localhost:8080/api/auth/login \
	-H 'Content-Type: application/json' \
	-d '{"username":"demo","password":"demo_password"}'
```

### Пользователь

- `GET /api/me`

Возвращает текущего пользователя по JWT.

### Рисунки

- `GET /api/images` — список своих рисунков
- `POST /api/images` — создание рисунка
- `GET /api/images/{id}` — просмотр своего рисунка
- `GET /api/images/{id}/file` — PNG-файл
- `PATCH /api/images/{id}` — обновление рисунка
- `DELETE /api/images/{id}` — удаление рисунка

Формат создания и обновления:

- `title` — поле формы
- `file` — PNG-файл

Пример создания:

```bash
curl -X POST http://localhost:8080/api/images \
	-H "Authorization: Bearer <token>" \
	-F "title=My drawing" \
	-F "file=@./image.png;type=image/png"
```

### Галерея

- `GET /api/gallery`

Возвращает все рисунки всех пользователей с именем автора.

## Поведение без базы данных

- пользователи и рисунки хранятся в памяти процесса
- после перезапуска сервера всё, что не лежит в PNG-файлах, сбрасывается
- PNG сохраняются в `STORAGE_DIR`

## Структура проекта

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── storage/
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Проверка

Для быстрого smoke-теста можно пройти сценарий:

1. зарегистрировать пользователя
2. получить JWT через login
3. создать рисунок
4. проверить список своих рисунков
5. открыть файл через `/file`
6. обновить рисунок
7. удалить рисунок
8. проверить галерею

Если нужен следующий шаг, я могу добавить сюда раздел с примерами ответов API или сразу подготовить `pytest`-тесты.
