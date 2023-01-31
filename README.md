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

## SQlite3 и CSV
### Для работы с sqlite3 и CSV используем следующие расширения:
"SQLite Viewer" и "Edit csv"
"SQLite Viewer" - расширение для просмотра файлов типа .sqlite
"Edit csv" - расширение для редактирования таблиц типа .csv
### Команды(для наполнения data base из CSV):
-sqlite3 - запускаем терминал для работы с sqlite3
-.open db.sqlite3 - открываем нашу базу
-.mode csv - запускаем интерпретатор файлов CSV
-.import s:/dev/api_yamdb/api_yamdb/static/data/users.csv users_user - импортируем пользователей из users.csv в db.sqlite3(users_user)
-.import s:/dev/api_yamdb/api_yamdb/static/data/genre.csv reviews_genre - импортируем жанры из genre.csv в db.sqlite3(reviews_genre)
-.import s:/dev/api_yamdb/api_yamdb/static/data/category.csv reviews_category - импортируем категории из category.csv в db.sqlite3(reviews_category)
-.import s:/dev/api_yamdb/api_yamdb/static/data/titles.csv reviews_title - импортируем произведения из title.csv в db.sqlite3(reviews_title)
-.import s:/dev/api_yamdb/api_yamdb/static/data/genre_title.csv reviews_genretitle - импортируем связи произведений с жанрами из genre_title.csv в db.sqlite3(reviews_genretitle)
-.import s:/dev/api_yamdb/api_yamdb/static/data/review.csv reviews_review - импортируем отзывы из review.csv в db.sqlite3(reviews_review)
-.import s:/dev/api_yamdb/api_yamdb/static/data/comments.csv reviews_comment - импортируем комментарии из comments.csv в db.sqlite3(reviews_comment)
-.schema - проверяем наличие таблиц и их наименование полей

## Некоторые примеры запросов к API:
### 1.1. Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/
### 1.2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
### 1.3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит token (JWT-токен).
### 2. GET, POST к произведениям /api/v1/titles/
### 3. GET, POST к жанрам\ категориям /api/v1/genres/ \ /api/v1/categories/
### 4. GET, POST к отзывам /api/v1/titles/1/reviews/
### 5. GET, POST к комментариям /api/v1/titles/1/reviews/1/comments
### 6. Документация по api доступна по ссылке http://127.0.0.1:8000/redoc/
