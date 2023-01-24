# api_yamdb
В данном проекте реализованы api запросы GET, POST, PUT, PATCH, DELETE
Авторизация реализована через simplejwt Token (с подтверждением через email).
Обьекты: произведения (title), категории (category), жанры (genre), комментарии (comment), отзывы (review).

## Как развернуть проект на локальной машине:
### 1. Клонировать репозиторий и перейти в него в командной строке:
-git clone git@github.com:SkyRedis/api_yamdb.git
-cd api_yamdb
### 2. Cоздать и активировать виртуальное окружение:
-python -m venv env
-. venv/Scripts/activate
### 3. Установить зависимости из файла requirements.txt:
-python -m pip install --upgrade pip
-pip install -r requirements.txt
### 4. Выполнить миграции:
-cd yatube_api (перейти в приложение с файлом manage.py)
-python manage.py migrate

## Некоторые примеры запросов к API:
### 1.1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/
### 1.2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
### 1.3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
### 2. GET, POST к произведениям /api/v1/titles/
### 3. GET, POST к жанрам\ категориям /api/v1/genres/ \ /api/v1/categories/
### 4. GET, POST к отзывам /api/v1/titles/1/reviews/
### 5. GET, POST к комментариям /api/v1/titles/1/reviews/1/comments
### 6. Документация по api доступна по ссылке http://127.0.0.1:8000/redoc/