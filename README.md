# YLab task 1

## Запуск через docker
```bat
docker-compose up -d
```

## Запуск через docker (тестирование)
```bat
docker-compose up -d
docker-compose run app pytest -v
```
Тестирование прод базы только на get запросы.<br/>
Тестовая база:<br/>
&emsp;имя базы: `{POSTGRES_DB}`_test;<br/>
&emsp;создается, если отсутствует;<br/>
&emsp;после тестирования база удаляется вне зависимости от ее существования на начало тестов.<br/>
Postman работает с прод базой, поэтому основную базу не выносил на отдельный volume
(для postman тестов она должна быть чистой перед каждым запуском). 

## Запуск через ком строку
```bat
uvicorn app.main:app --reload
```

### Переменные среды (.env)
- `POSTGRES_HOST` - имя хоста
- `POSTGRES_PORT` - порт
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь
- `POSTGRES_PASSWORD` - пароль
