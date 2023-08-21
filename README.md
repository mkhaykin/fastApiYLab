# YLab 4.2
Учебный проект: REST API по работе с меню ресторана.\
Техническое задание: [specification.md](./specification.md).\
Технологии: FastAPI, Postgres, Redis, Celery + RabbitMQ, Google Sheets.\
Описание решения и задачи<sup>*</sup> в файле [solution.md](./solution.md).

## Переменные среды
Для запуска и тестирования проекта, требуется создать файл `.env` с переменными окружения.\
Для обмена с Google sheet так же необходим id и файл токена.\
Пример файла: `.env.example`

### Параметры postgres
- `POSTGRES_HOST` - имя хоста
- `POSTGRES_PORT` - порт
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь
- `POSTGRES_PASSWORD` - пароль

### Параметра redis
- `REDIS_SERVER` - имя хоста
- `REDIS_PORT` - порт
- `CACHE_LIFETIME` - время жизни кэша

### Параметры rabbit
- `RABBITMQ_SERVER` - имя хоста
- `RABBITMQ_PORT` - порт
- `RABBITMQ_DEFAULT_USER` - пользователь
- `RABBITMQ_DEFAULT_PASS` - пароль
- `RABBITMQ_DEFAULT_VHOST` - vhost

### Синхронизация с внешними данными
- `EXCHANGE_SCHEDULE` - период запуска обмена (в секундах)
- `EXCHANGE_TYPE` - тип запускаемого обмена SHEET или FILE
- `EXCHANGE_SHEET_ID` - google sheets id
- `EXCHANGE_SHEET_TOKEN` - путь к файлу токена
- `EXCHANGE_FILE` - путь до файла с меню

Имена хостов используются только для локального запуска и в контейнере для запуска тестов,
в docker-compose установлены фиксированные значения.\
Пример файла: https://docs.google.com/spreadsheets/d/1B6QgEBkGXSkFh7B1g_vFPonNVl8e2VZGsxYEuKzM9iI \
В случае проблем или для получения id | ключа, обратитесь https://t.me/mikhail_khaykin
## Запуск через docker
```sh
docker-compose up -d
```
Перед выполнением создайте файл переменных окружения (`.env`).\
Пример файла см. [Переменные среды](#пример-файла).

## Запуск через ком строку
```sh
uvicorn app.main:app --reload
```
Перед запуском создайте файл переменных окружения (`.env`).\
Пример файла см. [Переменные среды](#пример-файла).

## Тестирование: docker
```sh
docker build -f Dockerfile.test -t fastapiylab-test:latest .
docker create --name fastapiylab-test --network=host --env-file=.env -t fastapiylab-test:latest
docker start -i fastapiylab-test
```
### Примечание
Перед началом тестирование создайте файл переменных окружения (`.env`).\
Пример файла см. [Переменные среды](#пример-файла).
### Особенности
Тестирование прод базы только на get запросы.\
CRUD тесты проводятся на тестовой базе.
### Тестовая база:
&emsp;**имя базы**: `{POSTGRES_DB}`_test; \
&emsp;**создание**: если отсутствует; \
&emsp;**удаление**: после тестирования база удаляется.

Удаление производится вне зависимости от ее наличия на начало тестов.\
Postman работает с прод базой, поэтому основную базу не выносил на отдельный volume
(для postman тестов она должна быть чистой перед каждым запуском). При наличии
menu.xlsx могут быть проблемы с postman. Удалите или переименуйте файл.

## Тестирование: cmd
```sh
pytest -v -s
```
Пользователю СУБД требуются права на создание тестовой базы данных.
