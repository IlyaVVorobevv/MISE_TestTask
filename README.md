# MISE Bookings API

REST API для онлайн-бронирования столика в ресторане.
Backend Trainee тестовое задание · Python 3.11 · FastAPI · Pydantic v2 · SQLAlchemy 2.0 (async).

## Стек

- **FastAPI** — роутинг, DI, документация из коробки
- **Pydantic v2** — валидация запросов/ответов
- **SQLAlchemy 2.0 (async) + SQLite** через `aiosqlite`
- **pytest + httpx.AsyncClient** — тесты эндпоинтов
- **Docker / docker-compose** — запуск в одну команду

## Запуск локально

```bash
python -m venv .venv
source .venv/bin/activate        
pip install -r requirements.txt

uvicorn app.main:app --reload
```

API будет доступно на `http://localhost:8000`, Swagger UI — на `/docs`, ReDoc — на `/redoc`.
База данных (SQLite-файл `bookings.db`) создаётся автоматически при старте приложения.

## Запуск через Docker

```bash
docker compose up --build
```

## Тесты

```bash
pytest -v
```

Тесты используют отдельную in-memory SQLite базу (через override зависимости `get_db`),
поэтому не трогают файл `bookings.db` и полностью изолированы друг от друга.

## Структура проекта

```
app/
  main.py                 # точка входа
  db.py                    # async engine, session factory, Base
  api/
    bookings.py            # роуты — тонкий слой, без бизнес-логики
  schemas/
    booking.py             # Pydantic-схемы + пофилдовая валидация
  services/
    booking_service.py     # бизнес-логика: создание, отмена, проверка слотов
  models/
    booking.py              # SQLAlchemy ORM-модель
  core/
    config.py               # настройки (pydantic-settings)
tests/
  conftest.py               # фикстуры: изолированная тестовая БД + клиент
  test_bookings.py           # тесты эндпоинтов и edge cases
```

## Эндпоинты

| Метод  | Путь              | Описание                                      |
|--------|-------------------|------------------------------------------------|
| POST   | `/bookings`       | Создать бронь → 201                            |
| GET    | `/bookings`       | Список броней, опционально `?date=2026-08-20`  |
| GET    | `/bookings/{id}`  | Получить бронь по id → 404 если не найдена     |
| DELETE | `/bookings/{id}`  | Отменить бронь (status → cancelled) → 200      |

## Какие решения я принял и почему

1. **Разделение на слои (роуты / схемы / сервис / модели)** — роуты не содержат
   бизнес-логики, только парсинг запроса и вызов сервиса. Это позволяет
   переиспользовать `BookingService` вне HTTP-контекста (например, в консольной
   команде или воркере) и тестировать бизнес-правила отдельно от FastAPI.
2. **Слот занят только активными бронями** — отменённая бронь (`status=cancelled`)
   освобождает слот, что соответствует реальному поведению ресторана: гость
   отменил столик — время снова свободно для брони.
3. **In-memory SQLite для тестов через override `get_db`** — тесты не трогают
   файл на диске, полностью изолированы друг от друга и выполняются быстро.

## Если бы было ещё время
1. **Добавил бы пагинацию**

- 

