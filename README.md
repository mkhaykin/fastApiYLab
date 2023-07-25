# YLab task 1

## Запуск через docker
```bat
docker-compose up
```

## Запуск через ком строку
```bat
uvicorn app.main:app --reload
```

### Переменные среды (.env)
- `POSTGRES_HOST` - имя хоста
- `DATABASE_PORT` - порт
- `POSTGRES_DB` - имя базы данных
- `POSTGRES_USER` - пользователь
- `POSTGRES_PASSWORD` - пароль
