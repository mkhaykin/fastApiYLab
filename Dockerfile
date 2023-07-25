FROM tiangolo/uvicorn-gunicorn:python3.8

#
WORKDIR /app

#
RUN pip install --no-cache-dir -U pip

#
COPY requirements.txt /tmp/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

#
RUN pip install psycopg2
#
COPY ./app /app

#
# EXPOSE 8000

#
CMD ["uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8002"]
