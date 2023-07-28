FROM python:3.10-slim

#
LABEL maintainer="mkhaikin@yandex.ru"

#
WORKDIR /app

#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

#
COPY . .

#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#
CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8000"]
