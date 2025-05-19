## Currency Exchange with FastAPI

---
Проект представляет собой API для получения курсов и конвертации валют, разработанный на FastAPI. 
### Основные возможности:

- Регистрация пользователей
- Аутентификация пользователей через JWT (JSON Web Tokens)

  Для авторизованных пользователей:
- Получение доступных валют
- Получение актуальных курсов валют
- Конвертация валют

## Стек

---
- FastAPI — основной web-фреймворк
- Pydantic — валидация данных
- PostgreSQL — база данных
- asyncpg — асинхронный клиент для PostgreSQL
- pytest — основной фреймворк для тестов
- pytest-mock — удобная работа с моками
- pytest-asyncio — поддержка асинхронного тестирования
- uvicorn — ASGI-сервер для запуска FastAPI-приложения
- PyJWT — работа с JWT-токенами

## API Endpoints

### Регистрация пользователя
- **Endpoint:** `/auth/register/`
- **Method:** `POST`
- **Content-Type:** `json`
- **Request Body:** 
    ```json
    {
    "email": "user@example.com",
    "username": "string",
    "password": "string"
    }
  
- **Response:**
    ```json
    {
    "message": "Пользователь успешно создан",
    "username": "string"
    }
  
### Авторизация пользователя
- **Endpoint:** `/login`
- **Method:** `POST`
- **Content-Type:** `x-www-form-urlencoded`
- **Request Body:** 
    ```
    grant_type=password&username=string&password=Qwerty123!&scope=&client_id=string&client_secret=string
- **Response:**
    ```json
    {
    "access_token": "JWT_token",
    "token_type": "bearer"
    }
  
### Получение списка доступных валют
- **Endpoint:** `/currency/list`
- **Method:** `GET`
- **Authorization:** `Bearer <JWT_token>`
- **Response:**
    ```json
    {
    "AED": "UAE Dirham",
    "AFN": "Afghan Afghani",
    ...
    }
  
### Получение курсов конвертации базовой валюты
- **Endpoint:** `/currency/rates?base_currency=RUB`
- **Method:** `GET`
- **Authorization:** `Bearer <JWT_token>`
- **Response:**
    ```json
    {
    "RUB": 1,
    "AED": 0.04537,
    "AFN": 0.867,
    "ALL": 1.0865,
    ...
    }
  
### Конвертация пары валют
- **Endpoint:** `/currency/exchange`
- **Method:** `POST`
- **Authorization:** `Bearer <JWT_token>`
- **Content-Type:** `json`
- **Request Body:** 
    ```json
    {
    "base_currency": "RUB",
    "target_currency": "USD",
    "amount": 1000
    }
  
- **Response:**
    ```json
    {
    "base_currency": "RUB",
    "target_currency": "USD",
    "amount": 1000,
    "conversion_result": 12.36
    }
  
## Интеграция с внешними API

Проект интегрируется с внешним API обмена валют для получения курсов обмена и информации о валютах 
в реальном времени.

Использовался следующий внешний API:
- **ExchangeRate-API**
- **URL:** https://www.exchangerate-api.com/

