# YLab task 1

## Запуск через docker
```bat
docker-compose up -d
```

## Запуск через docker (тестирование)
```bat
 docker-compose run app pytest .
```

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
