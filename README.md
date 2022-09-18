# Docker yamdb_final
![workflow status](https://github.com/mitroshin-alex/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg) \
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
- Docker compose
- Google
### Автоматическое тестирование и развертывание проекта на сервер
 - Скопировать файл yamdb_workflow.yml из корня проекта в директорию .github/workflows/
```shell
cp yamdb_workflow.yml .github/workflows/yamdb_workflow.yml
```
 - Заполнить секреты в GitHub
```Settings -> Secrets```\
Пример заполнения:
```
DEPLOY_HOST = 1.1.1.1
DEPLOY_KEY = -----BEGIN OPENSSH PRIVATE KEY-----
             dbvivvsfv98934ur09fnveuvBYU*(UGC^&U
             -----END OPENSSH PRIVATE KEY-----
DEPLOY_KEY_PASS = 123qwe
DEPLOY_USER = user
DOCKER_USERNAME = user
DOCKER_PASSWORD = 1234qwer
TELEGRAM_TO = 12345
TELEGRAM_TOKEN = 1111111111:dfvbjev7VVGVJHB8384-95JH
```
Плюс настройки для .env представленные ниже
 - На сервере: \
Остановите службу nginx и отключить ее \
```sudo systemctl stop nginx``` \
```sudo systemctl disable nginx``` \
Установите docker \
```sudo apt install docker.io``` \
Установите docker compose \
[официальная документация](https://docs.docker.com/compose/install/) \
Скопировать \
```docker-compose.yaml``` в домашнюю директорию на сервер \
```default.conf``` в каталог nginx домашней директории на сервере \
 - Push commit проекта на GitHab
### Ручное развертывание проекта на сервере
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
docker compose -p api_yamdb up -d
``` 
- Применить миграции к базе данных:
```
docker compose -p api_yamdb exec web python manage.py migrate
```
- Создание суперпользователя:
```
docker compose -p api_yamdb exec web python manage.py createsuperuser
```
- Сбор статики:
```
docker compose -p api_yamdb exec web python manage.py collectstatic --no-input 
```
### Загрузка тестовых данных в BD
- В файле конфигурации проекта задать путь к папке с данными
```
По умолчанию
DATA_DIR = os.path.join(BASE_DIR, 'static/data/')
```
- В папке с файлом manage.py выполните команду:
```
docker compose -p api_yamdb exec web python manage.py loadcsv
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