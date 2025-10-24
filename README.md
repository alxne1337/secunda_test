# Organizations API

REST API для справочника организаций, зданий и деятельностей. Реализовано на FastAPI с использованием PostgreSQL в качестве базы данных.

## Функциональность

- Управление организациями, зданиями и видами деятельностей
- Поиск организаций по различным критериям:
  - По зданию
  - По виду деятельности (включая дочерние в древовидной структуре)
  - По названию
  - В географическом радиусе или прямоугольной области
- Древовидная структура видов деятельностей с ограничением вложенности (3 уровня)
- Авторизация по статическому API ключу

## Технологический стек

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker & Docker Compose

## Требования

- Docker
- Docker Compose

## Быстрый запуск

1. Клонируйте репозиторий и перейдите в директорию проекта.

2. Создайте файл `.env` в корне проекта (опционально, если нужно переопределить настройки):
   ```env
   DATABASE_URL=postgresql://app_user:password@postgres:5432/organizations_db
   API_KEY=your-static-api-key-here
   ```
3. Запустите проект с помощью Docker Compose:

    ```bash
    docker-compose up -d
    ```

Приложение будет доступно по адресу: http://localhost:8000

Документация API (Swagger UI): http://localhost:8000/docs

## Остановка и очистка
1. Остановить контейнеры:

    ```bash
    docker-compose down
    ```
2. Остановить и удалить volumes (данные БД будут удалены):
    
    ```bash
    docker-compose down -v
    ```

## Использование API
Все запросы к API (кроме корневого и health-check) требуют заголовок с API ключом.
Для этого нажмите authorize в SWAGGER UI и введите API ключ (стандарт: 12fhg79)

## Примеры запросов
1. Получить список всех зданий

    ```
    GET /buildings/
    ```
API-Key: 12fhg79
2. Найти организации в радиусе 2 км от точки

    ```
    POST /buildings/geo-search/organizations

    Content-Type: application/json

    {
    "latitude": 55.755826,
    "longitude": 37.617300,
    "radius_km": 2.0
    }
    ```
3. Получить организации по виду деятельности (включая дочерние)

    ```
    GET /organizations/activity/1
    ```
4. Поиск организаций по названию

    ```
    GET /organizations/search/name?name=ООО
    ```