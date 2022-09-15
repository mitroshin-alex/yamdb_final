# Docker yamdb_final
![example workflow](https://github.com/mitroshin-alex/yamdb_final/actions/workflows/main.yml/badge.svg)
### Описание
Блог, где Вы можете оценить фильмы, музыку, 
книги и многое другое. 
У нас Вы сможете подобрать произведения определенного жанра. 
Узнать, как его оценило сообщество. Оставить свою собственную рецензию, 
а также комментировать чужие отзывы. Теперь в api и Docker!
### Технологии
- Python 3.7
- Django 2.2.16
- Djangorestframework 3.12.4
- Djangorestframework-simplejwt 4.7.2
- Docker
- Google
### Пример заполнения .env
Файл .env должен располагаться в директории infra
```
SECRET_KEY=xxxxxxxxxxxxxxxx
ALLOWED_HOSTS=localhost;web
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123aaaBBBccc!
DB_HOST=db
DB_PORT=5432
``` 
- SECRET_KEY - секретный ключ проекта
- ALLOWED_HOSTS - список разрешенных хостов разделенных ;
- DB_ENGINE - движок базы данных
- DB_NAME - имя базы данных
- POSTGRES_USER - пользователь базы данных
- POSTGRES_PASSWORD - пароль POSTGRES_USER
- DB_HOST - имя сервера базы данных
- DB_PORT - порт DB_HOST
### Запуск проекта
- Перейти в директорию infra:
```
cd infra
``` 
- Запустить docker-compose:
```
docker-compose -p api_yamdb up -d
``` 
- Применить миграции к базе данных:
```
docker-compose -p api_yamdb exec web python manage.py migrate
```
- Создание суперпользователя:
```
docker-compose -p api_yamdb exec web python manage.py createsuperuser
```
- Сбор статики:
```
docker-compose -p api_yamdb exec web python manage.py collectstatic --no-input 
```
### Загрузка тестовых данных в BD
- В файле конфигурации проекта задать путь к папке с данными
```
По умолчанию
DATA_DIR = os.path.join(BASE_DIR, 'static/data/')
```
- В папке с файлом manage.py выполните команду:
```
docker-compose -p api_yamdb exec web python manage.py loadcsv
```
### Примеры запросов
- POST /api/v1/auth/token/
```json
{
  "username": "string",
  "confirmation_code": "string"
}
```
> <font color="blue">200</font>
```json
{
  "token": "string"
}
```
- GET api/v1/titles/
> <font color="green">200</font>
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
- POST api/v1/titles/{title_id}/reviews/
```json
{
  "text": "string",
  "score": 1
}
```
> <font color="blue">201</font>
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
### Автор
Митрошин Алексей